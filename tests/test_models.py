import json
from pathlib import Path

import pytest

from open_video_guide import models
from open_video_guide.models import (
    ModelError,
    TranscriptSegment,
    _json_object,
    _proposal_prompt,
    _repeats_prompt,
    transcript_for_window,
)


def test_transcript_for_window_selects_overlapping_segments() -> None:
    segments = [
        TranscriptSegment(0, 900, "Open the menu."),
        TranscriptSegment(1100, 1900, "Select Export."),
        TranscriptSegment(3000, 3900, "Save the file."),
    ]

    text = transcript_for_window(segments, 1000, 2000)

    assert text == "Select Export."


def test_json_object_reads_a_fenced_result() -> None:
    value = _json_object('```json\n{"title":"Open menu","instruction":"Select File."}\n```')

    assert value["title"] == "Open menu"


def test_json_object_repairs_unquoted_field_names() -> None:
    value = _json_object('{title: "Open menu", instruction: "Select File."}')

    assert value["instruction"] == "Select File."


def test_json_object_repairs_unquoted_string_values() -> None:
    value = _json_object("{title: Review, instruction: Review the visible action}")

    assert value == {
        "title": "Review",
        "instruction": "Review the visible action",
    }


def test_prompt_does_not_end_with_the_speech_line() -> None:
    speech = "Select the export button now."
    prompt = _proposal_prompt(speech)

    assert speech.rstrip(".") not in prompt.splitlines()[-1]
    assert prompt.splitlines()[-1].startswith("Use only the title")


def test_prompt_keeps_the_speech_for_the_model() -> None:
    prompt = _proposal_prompt("Select the export button now.")

    assert "Select the export button now." in prompt


def test_silent_prompt_gives_no_fallback_sentence_to_copy() -> None:
    prompt = _proposal_prompt("")

    assert "no speech" in prompt.lower()
    assert "Review the visible action" not in prompt


def test_repeats_prompt_finds_a_copied_instruction() -> None:
    prompt = _proposal_prompt("")
    copied = "Do not invent a control, a value, or an action."

    assert _repeats_prompt(copied, prompt)


def test_repeats_prompt_finds_a_copied_speech_line() -> None:
    prompt = _proposal_prompt("")

    assert _repeats_prompt("This part of the video has no speech.", prompt)


def test_repeats_prompt_keeps_a_real_instruction() -> None:
    prompt = _proposal_prompt("")

    assert not _repeats_prompt("Select Edit Task to open the edit form.", prompt)
    assert not _repeats_prompt("Type the task title in the Title field.", prompt)


def test_repeats_prompt_ignores_a_short_value() -> None:
    prompt = _proposal_prompt("")

    assert not _repeats_prompt("Save it", prompt)


def _vision_stub(instruction: str):
    """Return a vision model stub that always answers with one instruction."""

    def generate(*args: object, **kwargs: object) -> str:
        return json.dumps({"title": "Open the task", "instruction": instruction})

    def apply_chat_template(processor: object, config: object, prompt: str, **kwargs: object):
        return prompt

    def load(model_name: str):
        return (object(), object(), (object(), generate, apply_chat_template))

    return load


def test_analyze_frame_rejects_a_repeated_prompt(monkeypatch, tmp_path: Path) -> None:
    copied = "Do not invent a control, a value, or an action."
    monkeypatch.setattr(models, "_load_vision_model", _vision_stub(copied))

    with pytest.raises(ModelError, match="repeated the prompt"):
        models.analyze_frame(tmp_path / "frame.png", "")


def test_analyze_frame_keeps_a_grounded_instruction(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(models, "_load_vision_model", _vision_stub("Select Edit Task."))

    proposal = models.analyze_frame(tmp_path / "frame.png", "")

    assert proposal.instruction == "Select Edit Task."
