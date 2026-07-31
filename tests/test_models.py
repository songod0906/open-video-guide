from open_video_guide.models import TranscriptSegment, _json_object, transcript_for_window


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
