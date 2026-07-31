#!/usr/bin/env python3
"""Validate benchmark records, annotations, and optional local source files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from open_video_guide.benchmark import DEFAULT_MANIFEST_PATH, validation_errors


def build_parser() -> argparse.ArgumentParser:
    """Create the command parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST_PATH,
        help="Path to the benchmark manifest.",
    )
    parser.add_argument(
        "--media-dir",
        type=Path,
        help="Optional directory with local source videos.",
    )
    return parser


def main() -> int:
    """Validate the selected benchmark."""
    args = build_parser().parse_args()
    errors = validation_errors(args.manifest, args.media_dir)

    if errors:
        print("\n".join(errors))
        return 1

    print(f"Benchmark records are valid: {args.manifest}")
    if args.media_dir is not None:
        print(f"Local source digests are valid: {args.media_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
