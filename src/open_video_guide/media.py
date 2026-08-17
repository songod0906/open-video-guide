"""Local media inspection and extraction."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


class MediaError(RuntimeError):
    """Report a local media processing failure."""


@dataclass(frozen=True)
class MediaInfo:
    """Store inspected source video data."""

    file_name: str
    duration_ms: int
    sha256: str
    video_codec: str
    audio_present: bool

    def as_dict(self) -> dict[str, Any]:
        """Return a serializable media record."""
        return asdict(self)


def executable(name: str) -> str:
    """Return an executable path."""
    found = shutil.which(name)
    if not found:
        raise MediaError(f"Required program is not available: {name}")
    return found


def source_digest(source_path: Path) -> str:
    """Calculate the source digest."""
    digest = hashlib.sha256()
    with source_path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inspect_video(source_path: Path) -> MediaInfo:
    """Inspect one local video."""
    source_path = source_path.expanduser().resolve()
    if not source_path.is_file():
        raise MediaError(f"Source video does not exist: {source_path}")

    command = [
        executable("ffprobe"),
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-show_entries",
        "stream=codec_type,codec_name",
        "-of",
        "json",
        str(source_path),
    ]
    result = subprocess.run(command, capture_output=True, check=False, text=True)
    if result.returncode:
        message = result.stderr.strip() or "FFprobe could not inspect the video."
        raise MediaError(message)

    try:
        probe = json.loads(result.stdout)
        duration_ms = round(float(probe["format"]["duration"]) * 1000)
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        raise MediaError("FFprobe returned invalid source metadata.") from error

    streams = probe.get("streams", [])
    video_streams = [stream for stream in streams if stream.get("codec_type") == "video"]
    if not video_streams or duration_ms < 1:
        raise MediaError("The source does not contain a usable video stream.")

    return MediaInfo(
        file_name=source_path.name,
        duration_ms=duration_ms,
        sha256=source_digest(source_path),
        video_codec=str(video_streams[0].get("codec_name", "unknown")),
        audio_present=any(stream.get("codec_type") == "audio" for stream in streams),
    )


def extract_frame(source_path: Path, timestamp_ms: int, target_path: Path) -> None:
    """Extract one candidate frame."""
    target_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        executable("ffmpeg"),
        "-hide_banner",
        "-loglevel",
        "error",
        "-ss",
        f"{timestamp_ms / 1000:.3f}",
        "-i",
        str(source_path),
        "-frames:v",
        "1",
        "-vf",
        "scale='min(1440,iw)':-2",
        "-y",
        str(target_path),
    ]
    result = subprocess.run(command, capture_output=True, check=False, text=True)
    if result.returncode or not target_path.is_file():
        message = result.stderr.strip() or "FFmpeg could not extract a frame."
        raise MediaError(message)


def extract_audio(source_path: Path, target_path: Path) -> None:
    """Extract speech audio for transcription."""
    target_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        executable("ffmpeg"),
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(source_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "pcm_s16le",
        "-y",
        str(target_path),
    ]
    result = subprocess.run(command, capture_output=True, check=False, text=True)
    if result.returncode or not target_path.is_file():
        message = result.stderr.strip() or "FFmpeg could not extract audio."
        raise MediaError(message)
