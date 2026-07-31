# Contributing

Thank you for your interest in Open Video Guide.
Use a focused change that is easy to review.

## Before work starts

1. Search existing issues.
2. Open an issue for a material change.
3. Define the outcome and acceptance criteria.
4. Record a new technical term when it is necessary.
5. Record the license data for a new component.

## Local setup

Use Python 3.11 or a later compatible version.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Change process

1. Create a short branch.
2. Add tests before or with the change.
3. Keep platform logic in an adapter.
4. Update related technical documents.
5. Run the complete local check.

```bash
make check
```

## Pull request

The pull request must explain:

- The user or system outcome
- The reason for the change
- The important implementation decision
- The test evidence
- The security and privacy effect
- The license effect
- The technical writing review

Do not include private video, model files, logs, or generated user data.

## Writing

Use the rules in `docs/STE_STYLE_GUIDE.md`.
Use the terms in `docs/TERMINOLOGY.md`.

The automated check does not prove full compliance.
Complete a manual review before you request review.

## Commit

Use a short command phrase for the commit subject.
For example, use `Add guide schema validation`.

## Contributor agreement

By submitting a change, you license it under Apache License 2.0.
You also confirm that you have the right to submit it.
