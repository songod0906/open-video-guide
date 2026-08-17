# Shared Agent Handoff

## Purpose

This workflow lets Codex and Claude continue the same project safely.
It separates stable product meaning from live repository data.

## Records

`docs/PROJECT_STATE.json` is the committed semantic project state.
It records goals, capabilities, evidence, priorities, limits, and rules.

`.project-context/PROJECT_CONTEXT.md` is the generated project context.
It adds the current Git branch, revision, worktree, commits, pull request, and checks.

Git ignores the generated project context.
Each agent can refresh it without changing the worktree.

## First setup

Run this command once in a new checkout:

```bash
make setup
```

This command installs development dependencies.
It also activates the tracked Git hooks.

The hooks refresh the project context after a commit or checkout.

## Start an agent session

1. Open the repository in the agent tool.
2. Tell the agent to read its repository instructions.
3. Tell the agent to refresh the project context.
4. Give the agent the next task.

Use this prompt with Claude:

```text
Read CLAUDE.md and refresh the project context.
Then continue this task: <task>.
```

Use this prompt with Codex:

```text
Read AGENTS.md and refresh the project context.
Then continue this task: <task>.
```

The latest user task has priority over the recorded task queue.

## Finish an agent session

1. Update the project state when semantic status changed.
2. Add evidence for each new verified capability.
3. Run the required quality checks.
4. Generate the verified handoff.
5. Commit the intended files.
6. Push the current branch.

Generate the verified handoff:

```bash
make handoff
```

The command runs the quality commands from the project state.
It exits with an error when a quality command fails.

## Update rules

Update `docs/PROJECT_STATE.json` when one of these items changes:

- Product stage or release state
- Current milestone or objective
- Verified capability or evidence
- Task priority or state
- Known product limit
- Non-negotiable product rule

Do not update the state for a formatting-only change.
Do not copy conversation transcripts into the state.
Do not record private media paths or secrets.

## Truth hierarchy

Use this order when two records disagree:

1. The latest user instruction
2. Current source and Git state
3. Passing tests and dated evidence
4. Accepted architecture decisions
5. The committed project state
6. The generated project context

Refresh the context when the generated record disagrees with Git.

## Automation boundary

The generator can collect repository data automatically.
It cannot decide product meaning or task priority safely.

An agent must update the semantic state after a material decision.
This control prevents a generated summary from inventing product direction.
