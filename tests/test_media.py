import hashlib
import json
from pathlib import Path
from subprocess import CompletedProcess

import pytest

from open_video_guide.media import MediaError, inspect_video


def test_inspect_video_returns_source_data(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = tmp_path / "tutorial.webm"
    source.write_bytes(b"test video")
    probe = {
        "format": {"duration": "12.500"},
        "streams": [
            {"codec_type": "video", "codec_name": "vp9"},
            {"codec_type": "audio", "codec_name": "opus"},
        ],
    }
    monkeypatch.setattr(
        "open_video_guide.media.subprocess.run",
        lambda *args, **kwargs: CompletedProcess(args[0], 0, json.dumps(probe), ""),
    )
    monkeypatch.setattr("open_video_guide.media.executable", lambda name: name)

    info = inspect_video(source)

    assert info.duration_ms == 12500
    assert info.video_codec == "vp9"
    assert info.audio_present is True
    assert info.sha256 == hashlib.sha256(b"test video").hexdigest()


def test_inspect_video_rejects_a_missing_source(tmp_path: Path) -> None:
    with pytest.raises(MediaError, match="does not exist"):
        inspect_video(tmp_path / "missing.webm")
