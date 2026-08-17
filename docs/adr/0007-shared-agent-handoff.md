# ADR 0007: Shared Agent Handoff

Status: Accepted

Date: 2026-07-31

## Context

Codex and Claude will work on the same repository at different times.
Each agent needs current goals, decisions, evidence, limits, and repository status.

Conversation history is not a reliable project record.
A complete transcript can also contain irrelevant or private data.

Git data changes automatically.
Product meaning changes only after a deliberate decision.

## Decision

Use one committed JavaScript Object Notation file for semantic project state.
Use one ignored Markdown file for the generated project context.

Generate live data from Git and the active GitHub pull request.
Run the recorded quality commands during a verified handoff.

Add repository instructions for Codex and Claude.
Require both agents to refresh the context before work.

Use tracked Git hooks to refresh context after commits and checkouts.
Activate the hooks during project setup.

Do not store conversation transcripts in either record.
Do not treat generated context as stronger evidence than tests or source.

## Consequences

Each agent receives the same product direction and task queue.
Live repository facts do not make the tracked worktree dirty.

The generator cannot infer product priorities safely.
An agent must update the semantic state after material decisions.

The context can become stale when hooks are not active.
Agent startup instructions provide a second refresh control.

GitHub data can be unavailable without network access or authentication.
The generator reports this limit and still creates local context.
