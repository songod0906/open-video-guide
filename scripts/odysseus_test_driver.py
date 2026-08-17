#!/usr/bin/env python3
"""Provide exact Odysseus tool calls for an integration test."""

from __future__ import annotations

import argparse
import json
import re
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

MODEL_NAME = "ovg-odysseus-test-driver"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SERVER_COMMAND = str(PROJECT_ROOT / ".venv" / "bin" / "ovg-mcp")
SERVER_ENV = {
    "OVG_INPUT_ROOT": str(PROJECT_ROOT / "benchmark" / "raw"),
    "OVG_OUTPUT_ROOT": str(PROJECT_ROOT / "outputs"),
    "OVG_MODEL_DIR": str(PROJECT_ROOT / "models"),
}


def response_action(
    messages: list[dict[str, Any]],
    tool_names: list[str] | None = None,
) -> tuple[str | None, str | None, dict[str, Any] | None]:
    """Return the next exact action for the setup test."""
    tool_call_count = sum(
        len(message.get("tool_calls", []))
        for message in messages
        if message.get("role") == "assistant"
    )
    last_user = next(
        (
            str(message.get("content", ""))
            for message in reversed(messages)
            if message.get("role") == "user"
        ),
        "",
    )

    if "OVG_LIST_SERVERS" in last_user:
        if tool_call_count == 0:
            return None, "manage_mcp", {"action": "list"}
        return "The server list is ready.", None, None

    if "OVG_LOCAL_AI_TEST" in last_user:
        if tool_call_count == 0:
            create_tool = next(
                (
                    name
                    for name in (tool_names or [])
                    if name.endswith("__create_guide")
                ),
                None,
            )
            if not create_tool:
                return "The create_guide tool is not available.", None, None
            return (
                None,
                create_tool,
                {
                    "source_path": str(
                        PROJECT_ROOT
                        / "benchmark"
                        / "raw"
                        / "short-form-mobile-screencast.ogv"
                    ),
                    "output_directory": str(
                        PROJECT_ROOT / "outputs" / "odysseus-ai-smoke"
                    ),
                    "model_profile": "local-ai",
                },
            )
        return "The local AI guide test is complete.", None, None

    delete_match = re.search(r"OVG_DELETE_SERVER\s+([A-Za-z0-9_-]+)", last_user)
    if delete_match:
        if tool_call_count == 0:
            return (
                None,
                "manage_mcp",
                {
                    "action": "delete",
                    "server_id": delete_match.group(1),
                },
            )
        return "The duplicate server is deleted.", None, None

    if tool_call_count == 1:
        return None, "manage_mcp", {"action": "list_tools"}
    if tool_call_count >= 2:
        return "The Odysseus setup test is complete.", None, None

    payload = {
        "action": "add",
        "name": "Open Video Guide",
        "command": SERVER_COMMAND,
        "args": [],
        "env": SERVER_ENV,
    }
    return None, "manage_mcp", payload


def completion_payload(
    content: str | None,
    tool_name: str | None,
    tool_arguments: dict[str, Any] | None,
) -> dict[str, Any]:
    """Return one OpenAI-compatible completion."""
    message: dict[str, Any] = {"role": "assistant", "content": content}
    finish_reason = "stop"
    if tool_name is not None and tool_arguments is not None:
        message["tool_calls"] = [
            {
                "id": "call_ovg_setup",
                "type": "function",
                "function": {
                    "name": tool_name,
                    "arguments": json.dumps(tool_arguments, separators=(",", ":")),
                },
            }
        ]
        finish_reason = "tool_calls"
    return {
        "id": "ovg-odysseus-test",
        "object": "chat.completion",
        "model": MODEL_NAME,
        "choices": [
            {
                "index": 0,
                "message": message,
                "finish_reason": finish_reason,
            }
        ],
    }


def stream_payload(
    content: str | None,
    tool_name: str | None,
    tool_arguments: dict[str, Any] | None,
) -> bytes:
    """Return one Server-Sent Events stream."""
    delta: dict[str, Any]
    finish_reason = "stop"
    if tool_name is None or tool_arguments is None:
        delta = {"content": content or ""}
    else:
        delta = {
            "tool_calls": [
                {
                    "index": 0,
                    "id": "call_ovg_setup",
                    "type": "function",
                    "function": {
                        "name": tool_name,
                        "arguments": json.dumps(tool_arguments, separators=(",", ":")),
                    },
                }
            ]
        }
        finish_reason = "tool_calls"
    chunk = {
        "id": "ovg-odysseus-test",
        "object": "chat.completion.chunk",
        "model": MODEL_NAME,
        "choices": [
            {
                "index": 0,
                "delta": delta,
                "finish_reason": None,
            }
        ],
    }
    end = {
        "id": "ovg-odysseus-test",
        "object": "chat.completion.chunk",
        "model": MODEL_NAME,
        "choices": [
            {
                "index": 0,
                "delta": {},
                "finish_reason": finish_reason,
            }
        ],
    }
    return (
        f"data: {json.dumps(chunk)}\n\n"
        f"data: {json.dumps(end)}\n\n"
        "data: [DONE]\n\n"
    ).encode()


class DriverHandler(BaseHTTPRequestHandler):
    """Serve a small OpenAI-compatible application programming interface."""

    server_version = "OVGOdysseusTestDriver/1.0"

    def log_message(self, format_string: str, *args: Any) -> None:
        """Write one access log entry."""
        print(f"{self.address_string()} - {format_string % args}")

    def send_json(self, payload: dict[str, Any]) -> None:
        """Send one JavaScript Object Notation response."""
        data = json.dumps(payload).encode()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:  # noqa: N802
        """Serve the model list and health routes."""
        if self.path == "/v1/models":
            self.send_json(
                {
                    "object": "list",
                    "data": [
                        {
                            "id": MODEL_NAME,
                            "object": "model",
                            "owned_by": "open-video-guide",
                        }
                    ],
                }
            )
            return
        if self.path == "/health":
            self.send_json({"status": "ok"})
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        """Serve one chat completion route."""
        if self.path != "/v1/chat/completions":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        length = int(self.headers.get("Content-Length", "0"))
        request = json.loads(self.rfile.read(length) or b"{}")
        tool_names = [
            str(tool.get("function", {}).get("name", ""))
            for tool in request.get("tools", [])
            if tool.get("function")
        ]
        content, tool_name, tool_arguments = response_action(
            request.get("messages", []),
            tool_names,
        )
        if request.get("stream"):
            data = stream_payload(content, tool_name, tool_arguments)
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        self.send_json(completion_payload(content, tool_name, tool_arguments))


def build_parser() -> argparse.ArgumentParser:
    """Create the command parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=11435, type=int)
    return parser


def main() -> int:
    """Run the integration test driver."""
    args = build_parser().parse_args()
    server = ThreadingHTTPServer((args.host, args.port), DriverHandler)
    print(f"Odysseus test driver listens on http://{args.host}:{args.port}/v1")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
