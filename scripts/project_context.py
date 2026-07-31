#!/usr/bin/env python3
"""Create a shared project handoff from state, Git, and GitHub data."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = REPOSITORY_ROOT / "docs" / "PROJECT_STATE.json"
OUTPUT_PATH = REPOSITORY_ROOT / ".project-context" / "PROJECT_CONTEXT.md"
REQUIRED_STATE_KEYS = {
    "schema_version",
    "product",
    "current_milestone",
    "verified_capabilities",
    "task_queue",
    "known_limits",
    "non_negotiable_rules",
    "important_paths",
    "quality_commands",
    "handoff_rules",
}


@dataclass(frozen=True)
class CommandResult:
    """Store one command result."""

    return_code: int
    stdout: str
    stderr: str


CommandRunner = Callable[[Sequence[str], Path, int], CommandResult]


def run_command(arguments: Sequence[str], cwd: Path, timeout: int = 120) -> CommandResult:
    """Run one command without a shell."""
    try:
        result = subprocess.run(
            list(arguments),
            cwd=cwd,
            capture_output=True,
            check=False,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return CommandResult(1, "", str(error))
    return CommandResult(result.returncode, result.stdout.rstrip(), result.stderr.strip())


def load_state(path: Path = STATE_PATH) -> dict[str, Any]:
    """Load and validate the semantic project state."""
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"The project state is not readable: {error}") from error

    if not isinstance(state, dict):
        raise ValueError("The project state must be an object.")
    missing = sorted(REQUIRED_STATE_KEYS.difference(state))
    if missing:
        raise ValueError("The project state misses these keys: " + ", ".join(missing))
    if state["schema_version"] != "1.0":
        raise ValueError("The project state schema version is not supported.")
    if not isinstance(state["task_queue"], list) or not state["task_queue"]:
        raise ValueError("The project state needs at least one task.")

    task_ids = [task.get("id") for task in state["task_queue"] if isinstance(task, dict)]
    if len(task_ids) != len(state["task_queue"]) or len(task_ids) != len(set(task_ids)):
        raise ValueError("Each project task needs one unique identifier.")
    return state


def collect_git_snapshot(
    root: Path = REPOSITORY_ROOT,
    runner: CommandRunner = run_command,
) -> dict[str, Any]:
    """Collect the current Git state."""
    branch = runner(("git", "branch", "--show-current"), root, 30)
    revision = runner(("git", "rev-parse", "HEAD"), root, 30)
    status = runner(("git", "status", "--short"), root, 30)
    recent = runner(
        ("git", "log", "-5", "--format=%h%x09%s"),
        root,
        30,
    )
    if branch.return_code or revision.return_code or status.return_code:
        raise RuntimeError("Git could not create the project snapshot.")

    recent_commits: list[dict[str, str]] = []
    for line in recent.stdout.splitlines():
        short_hash, separator, subject = line.partition("\t")
        if separator:
            recent_commits.append({"revision": short_hash, "subject": subject})

    changed_paths = [line for line in status.stdout.splitlines() if line]
    return {
        "branch": branch.stdout or "detached",
        "revision": revision.stdout,
        "short_revision": revision.stdout[:7],
        "worktree": "clean" if not changed_paths else "changed",
        "changed_paths": changed_paths,
        "recent_commits": recent_commits,
    }


def collect_github_snapshot(
    root: Path = REPOSITORY_ROOT,
    runner: CommandRunner = run_command,
) -> dict[str, Any]:
    """Collect the pull request and check state when GitHub is available."""
    fields = "number,url,title,state,isDraft,baseRefName,headRefName"
    pull_request = runner(("gh", "pr", "view", "--json", fields), root, 30)
    if pull_request.return_code:
        problem = pull_request.stderr.splitlines()[-1] if pull_request.stderr else "Unavailable"
        return {"available": False, "problem": problem, "checks": []}

    try:
        pull_request_data = json.loads(pull_request.stdout)
    except json.JSONDecodeError:
        return {"available": False, "problem": "GitHub returned invalid data.", "checks": []}

    checks_result = runner(
        ("gh", "pr", "checks", "--json", "name,state,bucket,link"),
        root,
        60,
    )
    checks: list[dict[str, Any]] = []
    if checks_result.stdout:
        try:
            parsed_checks = json.loads(checks_result.stdout)
            if isinstance(parsed_checks, list):
                checks = parsed_checks
        except json.JSONDecodeError:
            checks = []
    return {"available": True, "pull_request": pull_request_data, "checks": checks}


def run_quality_commands(
    commands: list[str],
    root: Path = REPOSITORY_ROOT,
    runner: CommandRunner = run_command,
) -> list[dict[str, Any]]:
    """Run the recorded quality commands."""
    results: list[dict[str, Any]] = []
    for command in commands:
        arguments = shlex.split(command)
        result = runner(arguments, root, 600)
        output_lines = [line for line in (result.stdout or result.stderr).splitlines() if line]
        results.append(
            {
                "command": command,
                "state": "pass" if result.return_code == 0 else "fail",
                "summary": output_lines[-1] if output_lines else "No output",
            }
        )
    return results


def _escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _list_lines(values: list[str]) -> list[str]:
    return [f"- {value}" for value in values]


def render_context(
    state: dict[str, Any],
    git: dict[str, Any],
    github: dict[str, Any],
    quality: list[dict[str, Any]] | None,
    generated_at: datetime | None = None,
) -> str:
    """Render the complete shared handoff."""
    timestamp = (generated_at or datetime.now(UTC)).astimezone(UTC).isoformat()
    product = state["product"]
    milestone = state["current_milestone"]
    ready_tasks = [task for task in state["task_queue"] if task["state"] == "ready"]
    first_task = ready_tasks[0] if ready_tasks else state["task_queue"][0]

    lines = [
        "# Open Video Guide Project Context",
        "",
        "> Generated context. Do not edit this file.",
        "> Update `docs/PROJECT_STATE.json` for semantic project changes.",
        "",
        f"Generated: `{timestamp}`",
        "",
        "## Receiving agent instructions",
        "",
        "1. Read the latest user request.",
        "2. Confirm the branch and worktree below.",
        "3. Read the relevant evidence and architecture records.",
        "4. Use the task queue only when the user gives no newer task.",
        "5. Update the semantic state before the next handoff.",
        "",
        "## Product intent",
        "",
        f"- Product: {product['name']}",
        f"- Mission: {product['mission']}",
        f"- Position: {product['position']}",
        f"- Release state: {product['release_state']}",
        f"- Current stage: {product['current_stage']}",
        "",
        "## Current milestone",
        "",
        f"- Name: {milestone['name']}",
        f"- State: {milestone['status']}",
        f"- Objective: {milestone['objective']}",
        f"- Last verified implementation: `{milestone['last_verified_implementation_commit']}`",
        "",
        "## Next task",
        "",
        f"**{first_task['id']}: {first_task['title']}**",
        "",
        f"Priority: `{first_task['priority']}`. State: `{first_task['state']}`.",
        "",
        "Acceptance:",
        "",
        *_list_lines(first_task["acceptance"]),
        "",
        "## Complete task queue",
        "",
        "| ID | Priority | State | Task |",
        "|---|---|---|---|",
    ]
    lines.extend(
        f"| {_escape(task['id'])} | {_escape(task['priority'])} | "
        f"{_escape(task['state'])} | {_escape(task['title'])} |"
        for task in state["task_queue"]
    )

    lines.extend(
        [
            "",
            "## Verified capabilities",
            "",
            "| ID | Capability | State | Evidence |",
            "|---|---|---|---|",
        ]
    )
    lines.extend(
        f"| {_escape(item['id'])} | {_escape(item['name'])} | "
        f"{_escape(item['state'])} | `{_escape(item['evidence'])}` |"
        for item in state["verified_capabilities"]
    )

    lines.extend(["", "## Known limits", "", *_list_lines(state["known_limits"])])
    lines.extend(
        ["", "## Non-negotiable rules", "", *_list_lines(state["non_negotiable_rules"])]
    )
    lines.extend(
        [
            "",
            "## Live repository snapshot",
            "",
            f"- Branch: `{git['branch']}`",
            f"- Revision: `{git['revision']}`",
            f"- Worktree: `{git['worktree']}`",
        ]
    )
    if git["changed_paths"]:
        lines.extend(["- Changed paths:", *[f"  - `{path}`" for path in git["changed_paths"]]])

    lines.extend(
        [
            "",
            "### Recent commits",
            "",
            "| Revision | Subject |",
            "|---|---|",
        ]
    )
    lines.extend(
        f"| `{item['revision']}` | {_escape(item['subject'])} |"
        for item in git["recent_commits"]
    )

    lines.extend(["", "## Pull request snapshot", ""])
    if github["available"]:
        pull_request = github["pull_request"]
        draft_text = "draft" if pull_request["isDraft"] else "ready"
        lines.extend(
            [
                f"- Pull request: [{pull_request['number']}]({pull_request['url']})",
                f"- Title: {pull_request['title']}",
                f"- State: `{pull_request['state']}` and `{draft_text}`",
                f"- Base: `{pull_request['baseRefName']}`",
                f"- Head: `{pull_request['headRefName']}`",
                "",
                "| Check | State | Group |",
                "|---|---|---|",
            ]
        )
        if github["checks"]:
            lines.extend(
                f"| {_escape(check['name'])} | {_escape(check['state'])} | "
                f"{_escape(check['bucket'])} |"
                for check in github["checks"]
            )
        else:
            lines.append("| No checks found | unknown | unknown |")
    else:
        lines.append(f"GitHub state is unavailable: {github['problem']}")

    lines.extend(["", "## Local quality snapshot", ""])
    if quality is None:
        lines.append("The refresh did not run local quality commands.")
        lines.append("Run `make handoff` before you transfer work.")
    else:
        lines.extend(["| Command | State | Summary |", "|---|---|---|"])
        lines.extend(
            f"| `{_escape(item['command'])}` | {_escape(item['state'])} | "
            f"{_escape(item['summary'])} |"
            for item in quality
        )

    lines.extend(["", "## Important paths", "", *_list_lines(state["important_paths"])])
    lines.extend(["", "## Handoff rules", "", *_list_lines(state["handoff_rules"])])
    lines.extend(
        [
            "",
            "## Refresh commands",
            "",
            "```bash",
            "python scripts/project_context.py",
            "make handoff",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def write_context(text: str, output_path: Path = OUTPUT_PATH) -> None:
    """Write the generated handoff."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    """Create the command parser."""
    parser = argparse.ArgumentParser(description="Refresh the shared project context.")
    parser.add_argument("--verify", action="store_true", help="Run local quality commands.")
    parser.add_argument("--print", action="store_true", dest="print_context")
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    return parser


def main() -> int:
    """Refresh the shared project context."""
    args = build_parser().parse_args()
    try:
        state = load_state()
        git = collect_git_snapshot()
        github = collect_github_snapshot()
        quality = run_quality_commands(state["quality_commands"]) if args.verify else None
        context = render_context(state, git, github, quality)
        write_context(context, args.output)
    except (RuntimeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1

    if args.print_context:
        print(context)
    else:
        print(f"Project context: {args.output}")
    if quality and any(item["state"] == "fail" for item in quality):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
