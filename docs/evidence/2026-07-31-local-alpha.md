# Local Alpha Test Evidence

Date: 2026-07-31

Computer: Apple M1 Pro with 32 GB memory

MCP means Model Context Protocol.
JSON means JavaScript Object Notation.
HTML means Hypertext Markup Language.

## Tested capabilities

| Capability | Result | Evidence |
|---|---|---|
| Inspect a local video | Pass | FFprobe facts and source digest returned |
| Extract candidate frames | Pass | Two images extracted from a 58.77-second video |
| Export a guide | Pass | JSON, Markdown, HTML, and images created |
| Validate a generated guide | Pass | Public schema returned no errors |
| Transcribe local speech | Pass | faster-whisper created timestamped text |
| Propose visual steps | Pass | Qwen3-VL returned structured proposals |
| Start the MCP server | Pass | Client initialized the standard-input transport |
| List MCP tools | Pass | Client found `inspect_video` and `create_guide` |
| Call both MCP tools | Pass | Both local tool calls completed |
| Start Odysseus | Pass | Native application answered at `127.0.0.1:7860` |
| Connect the MCP server in Odysseus | Pass | One server connected with two product tools |
| Inspect video in Odysseus | Pass | Odysseus returned duration, codec, digest, and support data |
| Create a frame-only guide in Odysseus | Pass | Two steps and four output files created |
| Create a local-AI guide in Odysseus | Pass | Two steps and four output files created |

## Pipeline result

The final test used a 116.49-second narrated software tutorial.
The local pipeline created four illustrated steps in 37.38 seconds.

The real-time factor was 0.32.
The guide and its manifest passed schema validation.

The manifest recorded no model response problems.
Every step kept the `unreviewed` review state.

## Odysseus result

The Odysseus agent called `inspect_video` through the registered MCP server.
The result reported a 58,767-millisecond Theora video.
The result included source digest `7631c751acd8410cd27b125ddba73a5b7326049b38af61ddb8e658d00665a6bc`.

The `frame-only` job used identifier `434653bc-33db-4b92-874c-0ca815d8bc4f`.
The `local-ai` job used identifier `87d1f09a-01ee-46c2-ae08-ca6dbddb056c`.
Each job created two steps.
Each manifest recorded no problems.

## Model result

The selected vision model was `mlx-community/Qwen3-VL-2B-Instruct-3bit`.
Its model page lists the Apache License 2.0.

The component inference reported approximately 1.99 GB peak memory.
The component generated about 67 tokens each second.

These measurements apply only to this computer and input.
They are not release targets.

## Known problems

- Fixed windows can combine actions.
- One frame can miss a short action.
- The model can create awkward titles.
- The confidence value is not calibrated.
- Silent-video quality is not verified.
- The user must review each instruction.

## Reproduction

```bash
.venv/bin/ovg generate \
  benchmark/raw/narrated-npm-dependencies.webm \
  --output outputs/user-test-guide \
  --profile local-ai \
  --window-seconds 30 \
  --maximum-steps 6

.venv/bin/ovg validate outputs/user-test-guide/guide.json

.venv/bin/python scripts/smoke_mcp.py \
  benchmark/raw/short-form-mobile-screencast.ogv

.venv/bin/python scripts/odysseus_test_driver.py
```
