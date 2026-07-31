"""Command-line interface for Open Video Guide."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from open_video_guide import __version__
from open_video_guide.contracts import load_guide, validation_errors


def build_parser() -> argparse.ArgumentParser:
    """Create the command parser."""
    parser = argparse.ArgumentParser(prog="ovg")
    parser.add_argument("--version", action="version", version=__version__)

    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate", help="Validate a guide JSON file.")
    validate.add_argument("guide", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line interface."""
    args = build_parser().parse_args(argv)

    if args.command == "validate":
        errors = validation_errors(load_guide(args.guide))
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1

        print(f"Valid guide: {args.guide}")
        return 0

    return 2
