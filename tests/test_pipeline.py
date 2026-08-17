from pathlib import Path

import pytest

from open_video_guide.pipeline import OUTPUT_MARKER, _prepare_output_directory, _windows


def test_windows_cover_the_complete_video() -> None:
    windows = _windows(duration_ms=58767, window_seconds=30, maximum_steps=8)

    assert windows == [(0, 29384), (29384, 58767)]


def test_windows_obey_the_step_limit() -> None:
    windows = _windows(duration_ms=600000, window_seconds=30, maximum_steps=3)

    assert windows == [(0, 200000), (200000, 400000), (400000, 600000)]


def test_prepare_output_directory_adds_a_marker(tmp_path: Path) -> None:
    output = tmp_path / "guide"

    _prepare_output_directory(output)

    assert (output / OUTPUT_MARKER).is_file()


def test_prepare_output_directory_rejects_unrecognized_files(tmp_path: Path) -> None:
    output = tmp_path / "guide"
    output.mkdir()
    (output / "private.txt").write_text("keep", encoding="utf-8")

    with pytest.raises(ValueError, match="another application"):
        _prepare_output_directory(output)
    assert (output / "private.txt").read_text(encoding="utf-8") == "keep"
