import json
from pathlib import Path

from open_video_guide.benchmark import (
    DEFAULT_MANIFEST_PATH,
    EXPECTED_CATEGORIES,
    validation_errors,
)


def test_seed_benchmark_is_valid() -> None:
    assert validation_errors() == []


def test_seed_has_each_required_category() -> None:
    manifest = json.loads(DEFAULT_MANIFEST_PATH.read_text(encoding="utf-8"))
    categories = {record["category"] for record in manifest["records"]}
    assert categories == EXPECTED_CATEGORIES


def test_invalid_step_time_is_reported(tmp_path: Path) -> None:
    manifest = json.loads(DEFAULT_MANIFEST_PATH.read_text(encoding="utf-8"))
    record = manifest["records"][0]
    source_annotation = DEFAULT_MANIFEST_PATH.parent / record["annotation_path"]
    annotation = json.loads(source_annotation.read_text(encoding="utf-8"))
    annotation["steps"][0]["end_ms"] = record["media"]["duration_ms"] + 1

    annotation_dir = tmp_path / "annotations"
    annotation_dir.mkdir()
    annotation_path = annotation_dir / source_annotation.name
    annotation_path.write_text(json.dumps(annotation), encoding="utf-8")
    manifest["records"] = [record]
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    errors = validation_errors(manifest_path)
    assert any("end time exceeds source duration" in error for error in errors)
