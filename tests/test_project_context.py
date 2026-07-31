"""Tests for the shared project handoff generator."""

from __future__ import annotations

import importlib.util
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest


def _load_module() -> ModuleType:
    path = Path(__file__).parents[1] / "scripts" / "project_context.py"
    spec = importlib.util.spec_from_file_location("project_context", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


project_context = _load_module()


def _state() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "product": {
            "name": "Open Video Guide",
            "mission": "Create a guide.",
            "position": "Local-first and open source.",
            "release_state": "Alpha",
            "current_stage": "Stage 3",
        },
        "current_milestone": {
            "name": "Review workflow",
            "status": "in_progress",
            "objective": "Test the workflow.",
            "last_verified_implementation_commit": "abc1234",
        },
        "verified_capabilities": [
            {
                "id": "CAP-001",
                "name": "Pipeline",
                "state": "verified",
                "evidence": "docs/evidence/test.md",
            }
        ],
        "task_queue": [
            {
                "id": "P0-001",
                "priority": "P0",
                "state": "ready",
                "title": "Run the test.",
                "acceptance": ["The test passes."],
            }
        ],
        "known_limits": ["One limit remains."],
        "non_negotiable_rules": ["Keep the product local."],
        "important_paths": ["AGENTS.md"],
        "quality_commands": ["python -m pytest"],
        "handoff_rules": ["Read the latest request."],
    }


def test_loads_the_repository_project_state() -> None:
    state = project_context.load_state()
    assert state["product"]["name"] == "Open Video Guide"
    assert state["task_queue"][0]["id"] == "P0-001"


def test_rejects_duplicate_task_identifiers(tmp_path: Path) -> None:
    state = _state()
    state["task_queue"].append(dict(state["task_queue"][0]))
    state_path = tmp_path / "state.json"
    state_path.write_text(json.dumps(state), encoding="utf-8")

    with pytest.raises(ValueError, match="unique identifier"):
        project_context.load_state(state_path)


def test_collects_git_data_without_losing_status_columns(tmp_path: Path) -> None:
    responses = {
        ("git", "branch", "--show-current"): project_context.CommandResult(
            0, "feat/work", ""
        ),
        ("git", "rev-parse", "HEAD"): project_context.CommandResult(0, "a" * 40, ""),
        ("git", "status", "--short"): project_context.CommandResult(
            0, " M tracked.py\n?? new.py", ""
        ),
        (
            "git",
            "log",
            "-5",
            "--format=%h%x09%s",
        ): project_context.CommandResult(0, "abc1234\tAdd feature", ""),
    }

    def fake_runner(arguments: Any, _cwd: Path, _timeout: int) -> Any:
        return responses[tuple(arguments)]

    snapshot = project_context.collect_git_snapshot(tmp_path, fake_runner)
    assert snapshot["branch"] == "feat/work"
    assert snapshot["worktree"] == "changed"
    assert snapshot["changed_paths"] == [" M tracked.py", "?? new.py"]
    assert snapshot["recent_commits"][0]["subject"] == "Add feature"


def test_renders_project_and_repository_context() -> None:
    git = {
        "branch": "feat/work",
        "revision": "a" * 40,
        "short_revision": "aaaaaaa",
        "worktree": "clean",
        "changed_paths": [],
        "recent_commits": [{"revision": "abc1234", "subject": "Add feature"}],
    }
    github = {
        "available": True,
        "pull_request": {
            "number": 14,
            "url": "https://example.test/pr/14",
            "title": "Add feature",
            "state": "OPEN",
            "isDraft": True,
            "baseRefName": "main",
            "headRefName": "feat/work",
        },
        "checks": [{"name": "test", "state": "SUCCESS", "bucket": "pass"}],
    }
    quality = [
        {"command": "python -m pytest", "state": "pass", "summary": "10 passed"}
    ]
    generated_at = datetime(2026, 7, 31, 10, 0, tzinfo=UTC)

    result = project_context.render_context(_state(), git, github, quality, generated_at)

    assert "P0-001: Run the test." in result
    assert "Branch: `feat/work`" in result
    assert "[14](https://example.test/pr/14)" in result
    assert "10 passed" in result


def test_writes_the_generated_context(tmp_path: Path) -> None:
    target = tmp_path / "context" / "PROJECT_CONTEXT.md"
    project_context.write_context("# Context\n", target)
    assert target.read_text(encoding="utf-8") == "# Context\n"


def test_collects_pull_request_and_check_data(tmp_path: Path) -> None:
    responses = {
        (
            "gh",
            "pr",
            "view",
            "--json",
            "number,url,title,state,isDraft,baseRefName,headRefName",
        ): project_context.CommandResult(
            0,
            json.dumps(
                {
                    "number": 14,
                    "url": "https://example.test/pr/14",
                    "title": "Add feature",
                    "state": "OPEN",
                    "isDraft": True,
                    "baseRefName": "main",
                    "headRefName": "feat/work",
                }
            ),
            "",
        ),
        (
            "gh",
            "pr",
            "checks",
            "--json",
            "name,state,bucket,link",
        ): project_context.CommandResult(
            0,
            json.dumps(
                [
                    {
                        "name": "test",
                        "state": "SUCCESS",
                        "bucket": "pass",
                        "link": "https://example.test/check",
                    }
                ]
            ),
            "",
        ),
    }

    def fake_runner(arguments: Any, _cwd: Path, _timeout: int) -> Any:
        return responses[tuple(arguments)]

    result = project_context.collect_github_snapshot(tmp_path, fake_runner)
    assert result["available"] is True
    assert result["pull_request"]["number"] == 14
    assert result["checks"][0]["bucket"] == "pass"


def test_records_a_failed_quality_command(tmp_path: Path) -> None:
    def fake_runner(arguments: Any, _cwd: Path, _timeout: int) -> Any:
        assert list(arguments) == ["python", "-m", "pytest"]
        return project_context.CommandResult(1, "one failed", "")

    result = project_context.run_quality_commands(
        ["python -m pytest"],
        tmp_path,
        fake_runner,
    )
    assert result == [
        {"command": "python -m pytest", "state": "fail", "summary": "one failed"}
    ]
