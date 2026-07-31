"""Adapters for local speech and vision models."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

DEFAULT_SPEECH_MODEL = "tiny.en"
DEFAULT_VISION_MODEL = "mlx-community/Qwen3-VL-2B-Instruct-3bit"
PROMPT_VERSION = "guide-window-1"


class ModelError(RuntimeError):
    """Report a local model failure."""


@dataclass(frozen=True)
class TranscriptSegment:
    """Store one timestamped speech segment."""

    start_ms: int
    end_ms: int
    text: str

    def as_dict(self) -> dict[str, Any]:
        """Return a serializable transcript segment."""
        return asdict(self)


@dataclass(frozen=True)
class StepProposal:
    """Store one model step proposal."""

    title: str
    instruction: str


def transcribe_audio(
    audio_path: Path,
    language: str,
    model_name: str = DEFAULT_SPEECH_MODEL,
    download_root: Path | None = None,
) -> list[TranscriptSegment]:
    """Transcribe local audio with faster-whisper."""
    try:
        from faster_whisper import WhisperModel
    except ImportError as error:
        message = 'Install the local model extras with: pip install -e ".[local-ai]"'
        raise ModelError(message) from error

    try:
        model = WhisperModel(
            model_name,
            device="cpu",
            compute_type="int8",
            download_root=str(download_root) if download_root else None,
        )
        selected_language = None if language == "auto" else language
        segments, _ = model.transcribe(
            str(audio_path),
            language=selected_language,
            vad_filter=True,
            beam_size=1,
        )
    except Exception as error:
        raise ModelError(f"Speech inference failed: {error}") from error
    return [
        TranscriptSegment(
            start_ms=max(0, round(segment.start * 1000)),
            end_ms=max(0, round(segment.end * 1000)),
            text=segment.text.strip(),
        )
        for segment in segments
        if segment.text.strip()
    ]


def transcript_for_window(
    segments: list[TranscriptSegment],
    start_ms: int,
    end_ms: int,
) -> str:
    """Return speech that overlaps one analysis window."""
    return " ".join(
        segment.text
        for segment in segments
        if segment.end_ms >= start_ms and segment.start_ms <= end_ms
    ).strip()


def _proposal_prompt(transcript: str) -> str:
    speech = transcript[:1200] if transcript else "No speech is available."
    return (
        "Output one compact JSON object on one line. "
        "Use only title and instruction string fields. "
        "Use a title with no more than five words. "
        "Use an imperative instruction with no more than 15 words. "
        "Do not repeat words. "
        "You create one evidence-grounded tutorial step from this frame. "
        "Use only visible evidence and the supplied speech. "
        "Do not invent a control, value, or action. "
        "Use Review the visible action when evidence is insufficient. "
        f"Nearby speech: {speech}"
    )


def _json_object(text: str) -> dict[str, Any]:
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    candidate = fenced.group(1) if fenced else text[text.find("{") : text.rfind("}") + 1]
    candidate = re.sub(r"([{,])\s*([A-Za-z_][A-Za-z0-9_]*)\s*:", r'\1"\2":', candidate)
    try:
        value = json.loads(candidate)
    except json.JSONDecodeError as error:
        title_match = re.search(r'"title"\s*:\s*["\']?([^,}"\']+)', candidate)
        instruction_match = re.search(
            r'"instruction"\s*:\s*["\']?([^}"\']+)',
            candidate,
        )
        if not title_match or not instruction_match:
            raise ModelError("The vision model did not return valid JSON.") from error
        value = {
            "title": title_match.group(1).strip(),
            "instruction": instruction_match.group(1).strip(),
        }
    if not isinstance(value, dict):
        raise ModelError("The vision model did not return a JSON object.")
    return value


@lru_cache(maxsize=1)
def _load_vision_model(model_name: str) -> tuple[Any, Any, Any]:
    """Load and cache one local vision model."""
    try:
        from mlx_vlm import generate, load
        from mlx_vlm.prompt_utils import apply_chat_template
        from mlx_vlm.utils import load_config
    except ImportError as error:
        message = 'Install the local model extras with: pip install -e ".[local-ai]"'
        raise ModelError(message) from error
    model, processor = load(model_name)
    config = load_config(model_name)
    return model, processor, (config, generate, apply_chat_template)


def analyze_frame(
    frame_path: Path,
    transcript: str,
    model_name: str = DEFAULT_VISION_MODEL,
) -> StepProposal:
    """Propose one step with a local vision-language model."""
    try:
        model, processor, helpers = _load_vision_model(model_name)
        config, generate, apply_chat_template = helpers
        prompt = apply_chat_template(
            processor,
            config,
            _proposal_prompt(transcript),
            num_images=1,
        )
        result = generate(
            model,
            processor,
            prompt,
            [str(frame_path)],
            max_tokens=80,
            temperature=0.0,
            repetition_penalty=1.2,
            verbose=False,
        )
    except ModelError:
        raise
    except Exception as error:
        raise ModelError(f"Vision inference failed: {error}") from error
    result_text = result.text if hasattr(result, "text") else str(result)
    value = _json_object(result_text)
    title = str(value.get("title", "")).strip()
    instruction = str(value.get("instruction", "")).strip()
    if not title or not instruction:
        raise ModelError("The vision model returned an incomplete step.")
    return StepProposal(title=title[:120], instruction=instruction[:600])
