# Repository Instructions

These instructions apply to all files in this repository.

## Language

Write technical text in ASD-STE100 Simplified Technical English, Issue 9.
Use the project terms in `docs/TERMINOLOGY.md`.

Use active voice.
Use one term for one meaning.
Use a maximum of 20 words in a procedural sentence.
Use a maximum of 25 words in a descriptive sentence.
Put only one instruction in each procedural sentence.
Do not use a technical abbreviation before you define it.

Do not change legal license text or exact source text.
Do not claim full compliance from an automated language check.

## Product truth

Describe the product as local-first and open source.
Do not describe the product as a free hosted service.
Do not claim that the video pipeline works before tests prove the claim.
Do not claim support for a platform before an integration test passes.

## Scope

Keep the core engine independent from user interfaces and AI clients.
Put platform code in an adapter.
Keep model weights, input videos, screenshots, logs, and generated guides out of Git.

## Quality

Run these checks before a commit:

```bash
python scripts/check_ste.py
python -m pytest
python -m ruff check .
```

Add an architecture decision record for a change to a major technical decision.
Add test evidence for each product capability.
Update the risk register when a change adds a material risk.

## Shared project handoff

Run this command at the start of each work session:

```bash
python scripts/project_context.py
```

Read `.project-context/PROJECT_CONTEXT.md` before you plan work.
Use `docs/PROJECT_STATE.json` as the semantic project record.

Update `docs/PROJECT_STATE.json` when capability, priority, status, or limits change.
Do not store conversation transcripts in the project state.

Run this command before a handoff:

```bash
make handoff
```

Give the next agent the repository path.
The next agent must refresh the project context before work.
