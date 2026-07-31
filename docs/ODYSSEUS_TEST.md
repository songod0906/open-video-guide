# Odysseus Test

Status: Setup prepared

The product has a local Model Context Protocol (MCP) adapter.
An Odysseus integration test still needs an active local Odysseus session.

## Add the server

Open Odysseus.
Open **Settings**.
Open **MCP Registry**.
Select **Add server**.

Use these values:

| Field | Value |
|---|---|
| Name | `Open Video Guide` |
| Transport | `stdio` |
| Command | `/Users/sonhoangnguyen/Documents/guiding video app/.venv/bin/ovg-mcp` |
| Argument | Leave empty |
| `OVG_INPUT_ROOT` | The absolute source video directory |
| `OVG_OUTPUT_ROOT` | `/Users/sonhoangnguyen/Documents/guiding video app/outputs` |

Save the server.
Inspect its tools.

Odysseus must show these tools:

- `inspect_video`
- `create_guide`

## Test the tools

Ask an Odysseus agent to inspect one file in `OVG_INPUT_ROOT`.
Check the returned duration and source digest.

Ask the agent to create a `frame-only` guide.
Use a new directory below `OVG_OUTPUT_ROOT`.

Open the generated `guide.html`.
Review its screenshots and timestamps.

Run the `local-ai` profile after the first test passes.

## Current access requirement

Codex also needs an Odysseus integration token for an automated in-app test.
Create this token in **Settings > Integrations > Add Integration > Codex Agent**.

Expose `ODYSSEUS_URL` and `ODYSSEUS_API_TOKEN` to the Codex environment.
Do not put the token in this repository.
