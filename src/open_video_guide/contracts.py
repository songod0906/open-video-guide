"""Functions that validate Open Video Guide interchange files."""

from __future__ import annotations

import json
from importlib import resources
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_FILE = "guide.schema.json"


def repository_root() -> Path:
    """Return the repository root for an editable installation."""
    return Path(__file__).resolve().parents[2]


def load_schema(schema_path: Path | None = None) -> dict[str, Any]:
    """Load the guide schema."""
    if schema_path is not None:
        return json.loads(schema_path.read_text(encoding="utf-8"))

    repository_schema = repository_root() / "schemas" / SCHEMA_FILE
    if repository_schema.exists():
        return json.loads(repository_schema.read_text(encoding="utf-8"))

    packaged_schema = resources.files("open_video_guide").joinpath("schemas", SCHEMA_FILE)
    return json.loads(packaged_schema.read_text(encoding="utf-8"))


def load_guide(guide_path: Path) -> dict[str, Any]:
    """Load a guide JSON file."""
    return json.loads(guide_path.read_text(encoding="utf-8"))


def validation_errors(
    guide: dict[str, Any],
    schema: dict[str, Any] | None = None,
) -> list[str]:
    """Return stable error messages for a guide."""
    validator = Draft202012Validator(
        schema or load_schema(),
        format_checker=FormatChecker(),
    )
    errors = sorted(validator.iter_errors(guide), key=lambda error: list(error.path))
    messages: list[str] = []

    for error in errors:
        location = ".".join(str(part) for part in error.absolute_path) or "$"
        messages.append(f"{location}: {error.message}")

    return messages
