from __future__ import annotations

import importlib.util
from pathlib import Path


def load_driver():
    path = Path(__file__).parents[1] / "scripts" / "odysseus_test_driver.py"
    spec = importlib.util.spec_from_file_location("odysseus_test_driver", path)
    assert spec
    assert spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_first_response_adds_the_server() -> None:
    driver = load_driver()
    content, tool_name, payload = driver.response_action(
        [{"role": "user", "content": "Start the setup test."}]
    )

    assert content is None
    assert tool_name == "manage_mcp"
    assert payload
    assert payload["action"] == "add"
    assert payload["name"] == "Open Video Guide"


def test_second_response_lists_tools() -> None:
    driver = load_driver()
    messages = [
        {
            "role": "assistant",
            "tool_calls": [{"id": "call_ovg_setup"}],
        }
    ]

    assert driver.response_action(messages) == (
        None,
        "manage_mcp",
        {"action": "list_tools"},
    )


def test_stream_has_done_marker() -> None:
    driver = load_driver()

    result = driver.stream_payload("Test", None, None).decode()

    assert '"content": "Test"' in result
    assert result.endswith("data: [DONE]\n\n")


def test_stream_has_native_tool_call() -> None:
    driver = load_driver()

    result = driver.stream_payload(
        None,
        "manage_mcp",
        {"action": "list"},
    ).decode()

    assert '"name": "manage_mcp"' in result
    assert '\\"action\\":\\"list\\"' in result
    assert '"finish_reason": "tool_calls"' in result


def test_list_mode_stops_after_one_call() -> None:
    driver = load_driver()
    messages = [
        {"role": "user", "content": "OVG_LIST_SERVERS"},
        {
            "role": "assistant",
            "tool_calls": [{"id": "call_ovg_setup"}],
        },
    ]

    assert driver.response_action(messages) == (
        "The server list is ready.",
        None,
        None,
    )


def test_delete_mode_uses_exact_server_id() -> None:
    driver = load_driver()
    messages = [{"role": "user", "content": "OVG_DELETE_SERVER ab12cd34"}]

    assert driver.response_action(messages) == (
        None,
        "manage_mcp",
        {"action": "delete", "server_id": "ab12cd34"},
    )


def test_local_ai_mode_selects_dynamic_create_tool() -> None:
    driver = load_driver()
    messages = [{"role": "user", "content": "OVG_LOCAL_AI_TEST MCP"}]

    content, tool_name, payload = driver.response_action(
        messages,
        ["mcp__abc123__create_guide"],
    )

    assert content is None
    assert tool_name == "mcp__abc123__create_guide"
    assert payload
    assert payload["model_profile"] == "local-ai"
