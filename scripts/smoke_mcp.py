"""Run a local Model Context Protocol smoke test."""

from __future__ import annotations

import argparse
import asyncio
import os
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run(source_path: Path) -> None:
    """Connect to the server and inspect one source video."""
    repository = Path(__file__).resolve().parents[1]
    output_root = repository / "outputs"
    output_root.mkdir(exist_ok=True)
    parameters = StdioServerParameters(
        command=str(repository / ".venv" / "bin" / "ovg-mcp"),
        env={
            **os.environ,
            "OVG_INPUT_ROOT": str(source_path.parent),
            "OVG_OUTPUT_ROOT": str(output_root),
        },
    )
    async with stdio_client(parameters) as streams, ClientSession(*streams) as session:
        await session.initialize()
        tools = await session.list_tools()
        names = {tool.name for tool in tools.tools}
        required = {"inspect_video", "create_guide"}
        if not required.issubset(names):
            raise RuntimeError("The server does not expose all required tools.")
        result = await session.call_tool(
            "inspect_video",
            arguments={"source_path": str(source_path)},
        )
        if result.isError:
            raise RuntimeError("The inspect_video smoke test failed.")
        guide_result = await session.call_tool(
            "create_guide",
            arguments={
                "source_path": str(source_path),
                    "output_directory": str(output_root / "mcp-smoke-current"),
                "model_profile": "frame-only",
                "language": "en",
            },
        )
        if guide_result.isError:
            raise RuntimeError("The create_guide smoke test failed.")
        print("MCP tools: " + ", ".join(sorted(names)))
        print("The inspect_video smoke test passed.")
        print("The create_guide smoke test passed.")


def main() -> None:
    """Parse arguments and run the smoke test."""
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    args = parser.parse_args()
    asyncio.run(run(args.video.expanduser().resolve()))


if __name__ == "__main__":
    main()
