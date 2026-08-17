# Claude Project Instructions

Read `AGENTS.md` before you change the repository.
Its language, product truth, scope, and quality rules apply to all work.

## Start each session

Run this command:

```bash
python scripts/project_context.py
```

Read `.project-context/PROJECT_CONTEXT.md`.
Read `docs/PROJECT_STATE.json` when you need the structured record.

Treat Git, tests, evidence, and architecture records as authoritative.
Do not trust an old generated snapshot when Git has changed.

## During work

Keep the core engine independent from clients.
Put Claude-specific code in an adapter.

Update `docs/PROJECT_STATE.json` when product status changes.
Update it when a verified capability changes.
Update it when the next priority changes.
Update it when a known limit changes.

Do not put private media or conversation transcripts in the state file.

## Before handoff

Run this command:

```bash
make handoff
```

Resolve each failed check before handoff.
Tell the user which task is next.
