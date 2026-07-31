"""Functions that validate benchmark records and annotations."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from open_video_guide.contracts import repository_root

BENCHMARK_ROOT = repository_root() / "benchmark"
MANIFEST_SCHEMA_PATH = BENCHMARK_ROOT / "schemas" / "manifest.schema.json"
ANNOTATION_SCHEMA_PATH = BENCHMARK_ROOT / "schemas" / "annotation.schema.json"
DEFAULT_MANIFEST_PATH = BENCHMARK_ROOT / "v0.1-seed" / "manifest.json"
EXPECTED_CATEGORIES = {
    "narrated_software",
    "silent_software",
    "physical",
    "short_form",
}


def load_json(path: Path) -> dict[str, Any]:
    """Load one JavaScript Object Notation file."""
    return json.loads(path.read_text(encoding="utf-8"))


def schema_errors(document: dict[str, Any], schema_path: Path) -> list[str]:
    """Return stable schema error messages."""
    validator = Draft202012Validator(
        load_json(schema_path),
        format_checker=FormatChecker(),
    )
    errors = sorted(
        validator.iter_errors(document),
        key=lambda error: list(error.absolute_path),
    )
    messages: list[str] = []

    for error in errors:
        location = ".".join(str(part) for part in error.absolute_path) or "$"
        messages.append(f"{location}: {error.message}")

    return messages


def file_sha256(path: Path) -> str:
    """Return the Secure Hash Algorithm 256 digest for one file."""
    digest = hashlib.sha256()

    with path.open("rb") as source_file:
        for chunk in iter(lambda: source_file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def annotation_errors(
    annotation: dict[str, Any],
    record: dict[str, Any],
) -> list[str]:
    """Return semantic annotation errors for one source record."""
    errors: list[str] = []
    record_id = record["id"]
    duration_ms = record["media"]["duration_ms"]

    if annotation["benchmark_id"] != record_id:
        errors.append(f"{record_id}: annotation identifier does not match")

    if annotation["source_sha256"] != record["media"]["sha256"]:
        errors.append(f"{record_id}: annotation source digest does not match")

    review = annotation["review"]
    if review["status"] == "seed_single_review" and review["reviewer_count"] != 1:
        errors.append(f"{record_id}: seed review must have one reviewer")
    if review["status"] != "seed_single_review" and review["reviewer_count"] < 2:
        errors.append(f"{record_id}: reviewed annotation must have two reviewers")

    previous_end_ms = 0
    for index, step in enumerate(annotation["steps"], start=1):
        prefix = f"{record_id}.steps.{index}"
        if step["order"] != index:
            errors.append(f"{prefix}: order must be {index}")
        if step["step_id"] != f"step-{index:02d}":
            errors.append(f"{prefix}: step identifier does not match order")
        if step["start_ms"] < previous_end_ms:
            errors.append(f"{prefix}: step overlaps the prior step")
        if step["start_ms"] >= step["end_ms"]:
            errors.append(f"{prefix}: start time must be before end time")
        if step["end_ms"] > duration_ms:
            errors.append(f"{prefix}: end time exceeds source duration")
        previous_end_ms = step["end_ms"]

        screenshot = step["screenshot"]
        if not step["start_ms"] <= screenshot["time_ms"] <= step["end_ms"]:
            errors.append(f"{prefix}: screenshot time is outside the step")

        region = screenshot["region"]
        if region["x"] + region["width"] > 1:
            errors.append(f"{prefix}: screenshot region exceeds frame width")
        if region["y"] + region["height"] > 1:
            errors.append(f"{prefix}: screenshot region exceeds frame height")

    return errors


def media_errors(record: dict[str, Any], media_dir: Path) -> list[str]:
    """Return local media identity errors for one source record."""
    errors: list[str] = []
    record_id = record["id"]
    media = record["media"]
    media_path = media_dir / media["file_name"]

    if not media_path.is_file():
        return [f"{record_id}: local source file is missing"]

    if media_path.stat().st_size != media["size_bytes"]:
        errors.append(f"{record_id}: local source size does not match")

    if file_sha256(media_path) != media["sha256"]:
        errors.append(f"{record_id}: local source digest does not match")

    return errors


def validation_errors(
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
    media_dir: Path | None = None,
) -> list[str]:
    """Return all benchmark validation errors."""
    errors: list[str] = []
    manifest = load_json(manifest_path)
    manifest_schema_errors = schema_errors(manifest, MANIFEST_SCHEMA_PATH)
    errors.extend(f"manifest: {message}" for message in manifest_schema_errors)

    if manifest_schema_errors:
        return errors

    records = manifest["records"]
    record_ids = [record["id"] for record in records]
    duplicate_ids = sorted(
        record_id for record_id in set(record_ids) if record_ids.count(record_id) > 1
    )
    errors.extend(f"manifest: duplicate record identifier {item}" for item in duplicate_ids)

    present_categories = {record["category"] for record in records}
    for category in sorted(EXPECTED_CATEGORIES - present_categories):
        errors.append(f"manifest: category {category} has no seed record")

    for record in records:
        annotation_path = manifest_path.parent / record["annotation_path"]
        if not annotation_path.is_file():
            errors.append(f"{record['id']}: annotation file is missing")
            continue

        annotation = load_json(annotation_path)
        current_schema_errors = schema_errors(annotation, ANNOTATION_SCHEMA_PATH)
        errors.extend(
            f"{record['id']}: {message}"
            for message in current_schema_errors
        )
        if not current_schema_errors:
            errors.extend(annotation_errors(annotation, record))

        if media_dir is not None:
            errors.extend(media_errors(record, media_dir))

    return errors
