from pathlib import Path

import pytest

from open_video_guide.adapters.mcp_server import _approved_path


def test_approved_path_accepts_a_child(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = tmp_path / "input" / "video.webm"
    source.parent.mkdir()
    source.write_bytes(b"video")
    monkeypatch.setenv("OVG_INPUT_ROOT", str(source.parent))

    assert _approved_path(str(source), "OVG_INPUT_ROOT", must_exist=True) == source


def test_approved_path_rejects_a_sibling(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    approved = tmp_path / "approved"
    approved.mkdir()
    source = tmp_path / "private.webm"
    source.write_bytes(b"video")
    monkeypatch.setenv("OVG_INPUT_ROOT", str(approved))

    with pytest.raises(ValueError, match="outside"):
        _approved_path(str(source), "OVG_INPUT_ROOT", must_exist=True)
