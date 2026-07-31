# Shared Agent Handoff Test Evidence

Date: 2026-07-31

## Tested capabilities

| Capability | Result | Evidence |
|---|---|---|
| Load the semantic project state | Pass | The generator loaded the version 1.0 record |
| Reject duplicate task identifiers | Pass | The validator returned a controlled error |
| Read the current Git state | Pass | The context kept branch, revision, status columns, and commits |
| Read the active pull request | Pass | The context recorded pull request 14 |
| Read pull request checks | Pass | The context recorded four passing checks |
| Run local quality commands | Pass | The verified handoff ran all three required commands |
| Record a failed quality command | Pass | The unit test kept the failed state and summary |
| Write an ignored context file | Pass | The generator wrote `.project-context/PROJECT_CONTEXT.md` |
| Activate repository Git hooks | Pass | The local Git configuration uses `.githooks` |
| Give Claude startup instructions | Pass | `CLAUDE.md` requires a context refresh |
| Give Codex startup instructions | Pass | `AGENTS.md` requires a context refresh |

## Verification result

The complete test suite passed 39 tests.
Ruff found no Python lint problems.
The limited language check found no problems.

A trained reviewer must complete the language review.

## Current pull request result

Python 3.11 passed.
Python 3.12 passed.
CodeQL passed.
The CodeQL analysis workflow passed.

## Known limits

- The generator cannot select product priorities safely.
- An agent must update semantic state after a material decision.
- GitHub data needs network access and authentication.
- Git hooks need activation in each new checkout.
- Startup instructions provide a second refresh control.
