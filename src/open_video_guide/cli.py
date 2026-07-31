"""Command-line interface for Open Video Guide."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from open_video_guide import __version__
from open_video_guide.contracts import load_guide, validation_errors
from open_video_guide.media import MediaError
from open_video_guide.pipeline import (
    PROFILE_LOCAL_AI,
    SUPPORTED_PROFILES,
    generate_guide,
    inspect_result,
)


def build_parser() -> argparse.ArgumentParser:
    """Create the command parser."""
    parser = argparse.ArgumentParser(prog="ovg")
    parser.add_argument("--version", action="version", version=__version__)

    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate", help="Validate a guide JSON file.")
    validate.add_argument("guide", type=Path)

    inspect = commands.add_parser("inspect", help="Inspect one local video.")
    inspect.add_argument("video", type=Path)

    generate = commands.add_parser("generate", help="Create a local illustrated guide.")
    generate.add_argument("video", type=Path)
    generate.add_argument("--output", type=Path, required=True)
    generate.add_argument("--profile", choices=SUPPORTED_PROFILES, default=PROFILE_LOCAL_AI)
    generate.add_argument("--language", default="en")
    generate.add_argument("--window-seconds", type=int, default=30)
    generate.add_argument("--maximum-steps", type=int, default=8)
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

    if args.command == "inspect":
        import json

        try:
            print(json.dumps(inspect_result(args.video), indent=2))
        except MediaError as error:
            print(f"ERROR: {error}")
            return 1
        return 0

    if args.command == "generate":
        try:
            result = generate_guide(
                args.video,
                args.output,
                profile=args.profile,
                language=args.language,
                window_seconds=args.window_seconds,
                maximum_steps=args.maximum_steps,
            )
        except (MediaError, OSError, RuntimeError, ValueError) as error:
            print(f"ERROR: {error}")
            return 1
        print(f"Guide JSON: {result.guide_json}")
        print(f"Guide Markdown: {result.guide_markdown}")
        print(f"Guide HTML: {result.guide_html}")
        return 0

    return 2
