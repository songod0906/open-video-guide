#!/usr/bin/env python3
"""Find some ASD-STE100 rule violations in Markdown files."""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterable
from pathlib import Path

WORD_PATTERN = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*")
LINK_TARGET_PATTERN = re.compile(r"\]\([^)]*\)")
INLINE_CODE_PATTERN = re.compile(r"`[^`]*`")
SENTENCE_END_PATTERN = re.compile(r"(?<=[.!?])\s+")

NOT_APPROVED = {
    "commence": "start",
    "commences": "starts",
    "commenced": "started",
    "prior to": "before",
    "shall": "must",
    "should": "must, can, or a factual statement",
    "utilize": "use",
    "utilizes": "uses",
    "utilized": "used",
}

SKIP_PARTS = {
    ".git",
    ".venv",
    "venv",
    "dist",
    "build",
    "site-packages",
}


def markdown_files(paths: Iterable[Path]) -> list[Path]:
    """Return Markdown files below the selected paths."""
    files: set[Path] = set()

    for path in paths:
        if path.is_file() and path.suffix.lower() == ".md":
            files.add(path)
            continue

        if path.is_dir():
            for candidate in path.rglob("*.md"):
                if not SKIP_PARTS.intersection(candidate.parts):
                    files.add(candidate)

    return sorted(files)


def prose_lines(text: str) -> list[tuple[int, str]]:
    """Return Markdown prose lines that are outside code blocks and tables."""
    results: list[tuple[int, str]] = []
    in_fence = False

    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()

        if stripped.startswith("```"):
            in_fence = not in_fence
            continue

        if in_fence or not stripped:
            continue

        if stripped.startswith(("#", "|", "<!--")):
            continue

        cleaned = re.sub(r"^(?:[-*+]|\d+\.)\s+", "", stripped)
        cleaned = re.sub(r"^>\s*(?:\[![A-Z]+\]\s*)?", "", cleaned)
        cleaned = LINK_TARGET_PATTERN.sub("]", cleaned)
        cleaned = INLINE_CODE_PATTERN.sub("identifier", cleaned)
        results.append((line_number, cleaned))

    return results


def check_file(path: Path, maximum_words: int = 25) -> list[str]:
    """Return measurable writing problems in one Markdown file."""
    problems: list[str] = []
    text = path.read_text(encoding="utf-8")

    for line_number, line in prose_lines(text):
        lower_line = line.lower()

        for word, replacement in NOT_APPROVED.items():
            if re.search(rf"\b{re.escape(word)}\b", lower_line):
                problems.append(
                    f"{path}:{line_number}: replace '{word}' with {replacement}"
                )

        for sentence in SENTENCE_END_PATTERN.split(line):
            word_count = len(WORD_PATTERN.findall(sentence))
            if word_count > maximum_words:
                problems.append(
                    f"{path}:{line_number}: sentence has {word_count} words; "
                    f"maximum is {maximum_words}"
                )

    return problems


def build_parser() -> argparse.ArgumentParser:
    """Create the command parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path, default=[Path(".")])
    parser.add_argument("--maximum-words", type=int, default=25)
    return parser


def main() -> int:
    """Run the limited writing check."""
    args = build_parser().parse_args()
    problems: list[str] = []

    for path in markdown_files(args.paths):
        problems.extend(check_file(path, args.maximum_words))

    if problems:
        print("\n".join(problems))
        print(f"\nFound {len(problems)} possible ASD-STE100 problems.")
        return 1

    print("The limited ASD-STE100 check found no problems.")
    print("A trained reviewer must complete the language review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
