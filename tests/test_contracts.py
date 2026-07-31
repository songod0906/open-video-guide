from pathlib import Path

from open_video_guide.contracts import load_guide, validation_errors

ROOT = Path(__file__).resolve().parents[1]


def test_example_guide_is_valid() -> None:
    guide = load_guide(ROOT / "examples" / "example-guide.json")
    assert validation_errors(guide) == []


def test_missing_steps_is_invalid() -> None:
    guide = load_guide(ROOT / "examples" / "example-guide.json")
    del guide["steps"]
    errors = validation_errors(guide)
    assert any("'steps' is a required property" in error for error in errors)


def test_invalid_identifier_is_invalid() -> None:
    guide = load_guide(ROOT / "examples" / "example-guide.json")
    guide["guide_id"] = "not-a-uuid"
    errors = validation_errors(guide)
    assert any("is not a 'uuid'" in error for error in errors)
