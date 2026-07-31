"""Model Context Protocol adapter."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from open_video_guide.pipeline import generate_guide, inspect_result

CONTRACT_VERSION = "0.1"


def _approved_path(raw_path: str, root_variable: str, *, must_exist: bool) -> Path:
    root_text = os.environ.get(root_variable)
    if not root_text:
        raise ValueError(f"{root_variable} is not set.")
    root = Path(root_text).expanduser().resolve()
    path = Path(raw_path).expanduser().resolve()
    if not path.is_relative_to(root):
        raise ValueError(f"The path is outside the approved directory: {root}")
    if must_exist and not path.is_file():
        raise ValueError(f"The source video does not exist: {path}")
    return path


def create_server() -> Any:
    """Create the local MCP server."""
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as error:
        raise RuntimeError('Install the MCP extra with: pip install -e ".[mcp]"') from error

    server = FastMCP("Open Video Guide")

    @server.tool()
    def inspect_video(source_path: str) -> dict[str, Any]:
        """Inspect one video in the approved input directory."""
        source = _approved_path(source_path, "OVG_INPUT_ROOT", must_exist=True)
        return inspect_result(source)

    @server.tool()
    def create_guide(
        source_path: str,
        output_directory: str,
        model_profile: str = "local-ai",
        language: str = "en",
    ) -> dict[str, str]:
        """Create one guide in the approved output directory."""
        source = _approved_path(source_path, "OVG_INPUT_ROOT", must_exist=True)
        output = _approved_path(output_directory, "OVG_OUTPUT_ROOT", must_exist=False)
        result = generate_guide(source, output, profile=model_profile, language=language)
        return {"contract_version": CONTRACT_VERSION, **result.as_dict()}

    return server


def main() -> None:
    """Run the local MCP server through standard input and output."""
    create_server().run(transport="stdio")
