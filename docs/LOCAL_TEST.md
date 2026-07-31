# Local Alpha Test

## Purpose

This test creates an illustrated guide on one local computer.
The alpha output needs user review.

Artificial Intelligence (AI) models create the speech and visual proposals.

## Requirements

- Apple Silicon Mac
- Python 3.11 or later
- FFmpeg and FFprobe
- Approximately 1.7 GB for the default vision model and speech model

## Installation

Run these commands from the repository root.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev,local-ai,mcp]"
```

The first AI run downloads model weights from Hugging Face.
Later runs use the local model cache.

## Fast file test

Run this command first.

```bash
.venv/bin/ovg generate /path/to/tutorial.mp4 \
  --output outputs/my-first-guide \
  --profile frame-only
```

Open `outputs/my-first-guide/guide.html`.
Confirm that each image comes from the source video.

## Local AI test

Run this command after the fast file test.

```bash
.venv/bin/ovg generate /path/to/tutorial.mp4 \
  --output outputs/my-ai-guide \
  --profile local-ai
```

Open `outputs/my-ai-guide/guide.html`.
Compare each instruction with its image and timestamp.

Review `manifest.json` for model problems.
Do not accept an unsupported instruction.

## Model Context Protocol test

Set the approved directories.

```bash
export OVG_INPUT_ROOT=/absolute/path/to/video/folder
export OVG_OUTPUT_ROOT=/absolute/path/to/output/folder
.venv/bin/ovg-mcp
```

The server uses standard input and standard output.
An MCP client starts this command and sends tool calls.

Run the included client smoke test.

```bash
.venv/bin/python scripts/smoke_mcp.py /absolute/path/to/tutorial.mp4
```

## Remove local outputs

Delete only an output directory that you created.

```bash
rm -r outputs/my-first-guide
```

Model weights stay in the Hugging Face cache.
