"""Local guide-generation application service."""

from __future__ import annotations

import json
import math
import os
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from open_video_guide.contracts import validation_errors
from open_video_guide.media import MediaInfo, extract_audio, extract_frame, inspect_video
from open_video_guide.models import (
    DEFAULT_SPEECH_MODEL,
    DEFAULT_VISION_MODEL,
    PROMPT_VERSION,
    ModelError,
    TranscriptSegment,
    analyze_frame,
    transcribe_audio,
    transcript_for_window,
)
from open_video_guide.renderers import render_html, render_json, render_markdown

PROFILE_FRAME_ONLY = "frame-only"
PROFILE_LOCAL_AI = "local-ai"
SUPPORTED_PROFILES = (PROFILE_FRAME_ONLY, PROFILE_LOCAL_AI)
OUTPUT_MARKER = ".open-video-guide-output"
MAXIMUM_DURATION_MS = 2 * 60 * 60 * 1000


@dataclass(frozen=True)
class GuideResult:
    """Store paths for one generated guide."""

    job_id: str
    output_directory: Path
    guide_json: Path
    guide_markdown: Path
    guide_html: Path
    manifest: Path

    def as_dict(self) -> dict[str, str]:
        """Return serializable result paths."""
        return {key: str(value) for key, value in asdict(self).items()}


def inspect_result(source_path: Path) -> dict[str, Any]:
    """Return the public inspection result."""
    info = inspect_video(source_path)
    return {
        "contract_version": "0.1",
        "source": info.as_dict(),
        "support": {"supported": True, "problems": []},
    }


def _windows(duration_ms: int, window_seconds: int, maximum_steps: int) -> list[tuple[int, int]]:
    window_ms = window_seconds * 1000
    count = max(1, min(maximum_steps, math.ceil(duration_ms / window_ms)))
    actual_window_ms = math.ceil(duration_ms / count)
    return [
        (index * actual_window_ms, min(duration_ms, (index + 1) * actual_window_ms))
        for index in range(count)
    ]


def _prepare_output_directory(output_directory: Path) -> None:
    if output_directory.exists() and not output_directory.is_dir():
        raise ValueError("The output path is not a directory.")
    output_directory.mkdir(parents=True, exist_ok=True)
    marker = output_directory / OUTPUT_MARKER
    if any(output_directory.iterdir()) and not marker.is_file():
        raise ValueError("The output directory contains files from another application.")
    marker.write_text("Open Video Guide output\n", encoding="utf-8")


def _fallback_proposal(transcript: str, order: int) -> tuple[str, str]:
    if transcript:
        clean_text = " ".join(transcript.split())
        return f"Review action {order}", clean_text[:600]
    return f"Review visual action {order}", "Review the action shown in this frame."


def _transcribe(
    source_path: Path,
    info: MediaInfo,
    work_directory: Path,
    language: str,
    speech_model: str,
) -> list[TranscriptSegment]:
    if not info.audio_present:
        return []
    configured_root = os.environ.get("OVG_MODEL_DIR")
    model_root = (
        Path(configured_root).expanduser().resolve()
        if configured_root
        else Path.home() / ".cache" / "open-video-guide" / "models"
    )
    audio_path = work_directory / "audio" / "speech.wav"
    extract_audio(source_path, audio_path)
    return transcribe_audio(
        audio_path,
        language,
        model_name=speech_model,
        download_root=model_root / "faster-whisper",
    )


def generate_guide(
    source_path: Path,
    output_directory: Path,
    *,
    profile: str = PROFILE_LOCAL_AI,
    language: str = "en",
    window_seconds: int = 30,
    maximum_steps: int = 8,
    speech_model: str = DEFAULT_SPEECH_MODEL,
    vision_model: str = DEFAULT_VISION_MODEL,
) -> GuideResult:
    """Generate one local guide and its exports."""
    if profile not in SUPPORTED_PROFILES:
        raise ValueError(f"Unknown model profile: {profile}")
    if not 10 <= window_seconds <= 120:
        raise ValueError("Window length must be from 10 through 120 seconds.")
    if not 1 <= maximum_steps <= 30:
        raise ValueError("Maximum steps must be from 1 through 30.")

    source_path = source_path.expanduser().resolve()
    output_directory = output_directory.expanduser().resolve()
    _prepare_output_directory(output_directory)
    job_id = str(uuid.uuid4())
    work_directory = output_directory
    info = inspect_video(source_path)
    if info.duration_ms > MAXIMUM_DURATION_MS:
        raise ValueError("The alpha supports videos with a maximum duration of two hours.")

    transcript_segments: list[TranscriptSegment] = []
    model_problems: list[str] = []
    if profile == PROFILE_LOCAL_AI:
        try:
            transcript_segments = _transcribe(
                source_path,
                info,
                work_directory,
                language,
                speech_model,
            )
        except ModelError as error:
            model_problems.append(str(error))

    transcript_path = work_directory / "transcript.json"
    transcript_path.write_text(
        json.dumps([segment.as_dict() for segment in transcript_segments], indent=2) + "\n",
        encoding="utf-8",
    )

    steps: list[dict[str, Any]] = []
    for order, (start_ms, end_ms) in enumerate(
        _windows(info.duration_ms, window_seconds, maximum_steps),
        start=1,
    ):
        timestamp_ms = min(max(start_ms, (start_ms + end_ms) // 2), info.duration_ms - 1)
        relative_frame = Path("screenshots") / f"step-{order:03d}.png"
        frame_path = work_directory / relative_frame
        extract_frame(source_path, timestamp_ms, frame_path)
        transcript = transcript_for_window(transcript_segments, start_ms, end_ms)
        title, instruction = _fallback_proposal(transcript, order)
        used_vision = False
        if profile == PROFILE_LOCAL_AI:
            try:
                proposal = analyze_frame(frame_path, transcript, model_name=vision_model)
                title, instruction = proposal.title, proposal.instruction
                used_vision = True
            except ModelError as error:
                model_problems.append(f"Window {order}: {error}")

        evidence: list[dict[str, Any]] = [
            {
                "kind": "frame",
                "start_ms": timestamp_ms,
                "end_ms": timestamp_ms,
                "asset_path": relative_frame.as_posix(),
            }
        ]
        if transcript:
            evidence.append(
                {
                    "kind": "transcript",
                    "start_ms": start_ms,
                    "end_ms": end_ms,
                    "text": transcript,
                }
            )
        confidence = 0.45 + (0.1 if used_vision else 0.0) + (0.1 if transcript else 0.0)
        steps.append(
            {
                "step_id": str(uuid.uuid4()),
                "order": order,
                "title": title,
                "instruction": instruction,
                "start_ms": start_ms,
                "end_ms": end_ms,
                "screenshot_path": relative_frame.as_posix(),
                "confidence": round(confidence, 2),
                "review_state": "unreviewed",
                "evidence": evidence,
            }
        )

    guide = {
        "schema_version": "1.0",
        "guide_id": str(uuid.uuid4()),
        "title": f"Guide for {source_path.stem}",
        "language": language,
        "source": {
            "file_name": info.file_name,
            "duration_ms": info.duration_ms,
            "sha256": info.sha256,
        },
        "steps": steps,
    }
    errors = validation_errors(guide)
    if errors:
        raise RuntimeError("Generated guide is invalid: " + "; ".join(errors))

    guide_json = work_directory / "guide.json"
    guide_markdown = work_directory / "guide.md"
    guide_html = work_directory / "guide.html"
    manifest = work_directory / "manifest.json"
    render_json(guide, guide_json)
    render_markdown(guide, guide_markdown)
    render_html(guide, guide_html)
    manifest_data = {
        "job_id": job_id,
        "state": "complete",
        "model_profile": profile,
        "speech_model": speech_model if profile == PROFILE_LOCAL_AI else None,
        "vision_model": vision_model if profile == PROFILE_LOCAL_AI else None,
        "prompt_version": PROMPT_VERSION if profile == PROFILE_LOCAL_AI else None,
        "model_problems": model_problems,
        "artifacts": [
            guide_json.name,
            guide_markdown.name,
            guide_html.name,
            transcript_path.name,
        ],
    }
    manifest.write_text(json.dumps(manifest_data, indent=2) + "\n", encoding="utf-8")

    audio_directory = work_directory / "audio"
    audio_path = audio_directory / "speech.wav"
    audio_path.unlink(missing_ok=True)
    if audio_directory.exists() and not any(audio_directory.iterdir()):
        audio_directory.rmdir()
    return GuideResult(
        job_id=job_id,
        output_directory=work_directory,
        guide_json=guide_json,
        guide_markdown=guide_markdown,
        guide_html=guide_html,
        manifest=manifest,
    )
