# Odysseus Test

Status: Passed on 2026-07-31

The installed Odysseus application connected to the local Model Context Protocol (MCP) adapter.
Odysseus found `inspect_video` and `create_guide`.

## Verified results

| Test | Result |
|---|---|
| Connect the standard-input server | Pass |
| List configured servers | Pass |
| Inspect the benchmark video | Pass |
| Create a `frame-only` guide | Pass |
| Create a `local-ai` guide | Pass |

The inspection returned a 58,767-millisecond Theora video.
The inspection returned the correct source digest.
The inspection reported no support problems.

The `frame-only` job created two steps.
The `local-ai` job created two steps.
Both jobs created JSON, Markdown, HTML, and manifest artifacts.
Both manifests recorded no problems.

## Test driver

The local test driver gives Odysseus exact administration calls.
It does not replace the product model.
It binds to the local computer only.

Start the driver:

```bash
.venv/bin/python scripts/odysseus_test_driver.py
```

Add `http://127.0.0.1:11435/v1` as a local model endpoint.
Select `ovg-odysseus-test-driver`.
Enable Agent mode.
Send `Start the OVG setup and MCP registration test.`

The driver registers this command:

```text
/Users/sonhoangnguyen/Documents/guiding video app/.venv/bin/ovg-mcp
```

The driver sets these environment variables:

```text
OVG_INPUT_ROOT=/Users/sonhoangnguyen/Documents/guiding video app/benchmark/raw
OVG_OUTPUT_ROOT=/Users/sonhoangnguyen/Documents/guiding video app/outputs
OVG_MODEL_DIR=/Users/sonhoangnguyen/Documents/guiding video app/models
```

## Product tool test

Select `qwen3.5:4b`.
Start a new chat.
Enable Agent mode.
Ask the agent to use the Open Video Guide MCP tools.

Use this source:

```text
/Users/sonhoangnguyen/Documents/guiding video app/benchmark/raw/short-form-mobile-screencast.ogv
```

Use a new directory below `OVG_OUTPUT_ROOT` for each job.
Open the generated `guide.html`.
Review each screenshot and timestamp.

The test driver is test support code.
Do not use it as a general model endpoint.
