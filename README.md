# Open Video Guide

[![Continuous integration](https://github.com/songod0906/open-video-guide/actions/workflows/ci.yml/badge.svg)](https://github.com/songod0906/open-video-guide/actions/workflows/ci.yml)
[![CodeQL](https://github.com/songod0906/open-video-guide/actions/workflows/codeql.yml/badge.svg)](https://github.com/songod0906/open-video-guide/actions/workflows/codeql.yml)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](pyproject.toml)

Open Video Guide turns a tutorial video into an illustrated guide.
Every step keeps a timestamp, a source screenshot, and a confidence value.
You review and correct each step before you trust it.

The project is local-first and open source.
Processing stays on your computer. No paid AI API is necessary.

> [!IMPORTANT]
> The repository contains an experimental local alpha.
> Review each generated step before use.

## Why this project exists

Most tools extract a transcript and summarize it.
A summary is fast, but a reader cannot verify it against the source.

Open Video Guide connects each instruction to evidence instead.
An instruction without a timestamp, a frame, or a transcript segment is invalid by contract.
The public schema in [`schemas/guide.schema.json`](schemas/guide.schema.json) rejects a step without evidence.

The product will:

- Keep all processing on your computer after model download.
- Mark uncertain instructions for review instead of hiding them.
- Keep source timestamps with each step.
- Select a useful screenshot for each instruction.
- Let you correct the result before export.
- Use replaceable model and platform adapters.

## How it works

```text
Video file
  |
  +-- FFmpeg: media inspection and extraction
  +-- Speech adapter: narrated speech and timestamps
  +-- Fixed windows: candidate frame selection
  +-- Vision adapter: visual step proposals from each frame
  |
Evidence merge
  |
Editable guide
  |
Markdown, HTML, JSON, and screenshots
```

The alpha profile uses faster-whisper for speech and Qwen3-VL through MLX-VLM for vision on Apple Silicon.
See [the architecture record](docs/ARCHITECTURE.md) for the full component list and the planned Linux profile.

## A harness, not a locked-in model

The core engine calls small model adapters.
It does not call one fixed vendor.

`src/open_video_guide/models.py` defines the adapter functions.
Each adapter takes a model name and returns a plain structured result.
The alpha ships one tested speech model and one tested vision model, recorded with their license and size in [`docs/MODEL_PROFILE_ALPHA.md`](docs/MODEL_PROFILE_ALPHA.md).

You can already call the Python interface with another local model name:

```python
from pathlib import Path

from open_video_guide.pipeline import generate_guide

generate_guide(
    Path("tutorial.mp4"),
    Path("outputs/my-guide"),
    speech_model="tiny.en",                        # any faster-whisper model
    vision_model="mlx-community/<your-vlm-here>",  # any compatible MLX-VLM model
)
```

Command-line and local editor options to pick a model without editing code are on the roadmap.
See [`docs/ROADMAP.md`](docs/ROADMAP.md) for the current phase and [`docs/AI_SYSTEM.md`](docs/AI_SYSTEM.md) for the model change process.
A model change still needs a license check and a benchmark run before it becomes a default.

## Repository map

| Path | Purpose |
|---|---|
| `src/open_video_guide` | Core engine, model adapters, and client adapters |
| `schemas` | Versioned interchange contracts |
| `examples` | Synthetic contract examples |
| `benchmark` | Public benchmark records and provisional annotations |
| `docs` | Product and engineering records, including test evidence |
| `.github` | Review, issue, dependency, and continuous integration controls |

## Quick start

Use Python 3.11 or a later compatible version.

```bash
python -m pip install -e ".[dev]"
ovg validate examples/example-guide.json
pytest
```

Create a fast draft without model inference:

```bash
ovg generate /path/to/tutorial.mp4 \
  --output outputs/my-first-guide \
  --profile frame-only
```

Install the local model dependencies and create an AI-assisted draft:

```bash
python -m pip install -e ".[dev,local-ai,mcp]"
ovg generate /path/to/tutorial.mp4 \
  --output outputs/my-ai-guide \
  --profile local-ai
```

See [the local alpha test](docs/LOCAL_TEST.md) for complete instructions.

## Local review editor

```bash
python -m pip install -e ".[web]"
ovg-web
```

Open `http://127.0.0.1:8765` in a browser.
Upload a video, review each step next to its source frame, correct it, and export Markdown, HTML, or JSON.

The editor stores private job data in `.ovg-data`.
Git ignores this directory. Nothing leaves your computer.

See [the local editor guide](docs/LOCAL_EDITOR.md) for the complete workflow.

## Connect an AI client

One Model Context Protocol (MCP) server exposes `inspect_video` and `create_guide` over standard input and output.
It works today with Claude and with Odysseus, a self-hosted AI workspace.

```bash
python -m pip install -e ".[mcp]"
ovg-mcp
```

See [the integration strategy](docs/INTEGRATIONS.md) for the tested clients and the planned tool set.

## Where the project actually stands

The project uses dated, reproducible evidence instead of marketing claims.
Every entry below links to a test record you can rerun yourself.

**Verified today:**

- The local file-to-guide pipeline, with JSON, Markdown, and HTML export ([evidence](docs/evidence/2026-07-31-local-alpha.md))
- The local review editor: upload, correct, replace a frame, save, export ([evidence](docs/evidence/2026-07-31-local-editor.md))
- The complete review workflow on a silent video, plus a fixed prompt defect ([evidence](docs/evidence/2026-07-31-silent-review-workflow.md), [fix](docs/evidence/2026-08-01-prompt-echo-fix.md))
- The Model Context Protocol server with Claude and Odysseus ([evidence](docs/evidence/2026-07-31-local-alpha.md))

**Known limits, honestly:**

- Fixed windows can combine actions or miss a short action.
- Silent-video instruction quality does not yet meet the release gate.
- Confidence values are not calibrated against held-out data.
- A running web job does not resume after an interruption.
- The local editor does not reflow at a 375-pixel width.

The complete list lives in [`docs/PROJECT_STATE.json`](docs/PROJECT_STATE.json), refreshed at every work session.
See [`docs/ROADMAP.md`](docs/ROADMAP.md) for what closes each limit and when.

## Contributing

Issues and pull requests are welcome.
Read [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`docs/DEVELOPMENT_WORKFLOW.md`](docs/DEVELOPMENT_WORKFLOW.md) first.

A change needs a test, a passing check suite, and evidence for any new capability claim.
That rule applies to maintainers too. See [`docs/QUALITY_PLAN.md`](docs/QUALITY_PLAN.md).

## Shared Codex and Claude work

The repository keeps one shared project state for AI coding agents.
Each agent reads the same goals, verified capabilities, limits, and task queue.

```bash
python scripts/project_context.py   # refresh the live context
make handoff                        # refresh and run the quality gate
```

See [the shared agent handoff](docs/SHARED_AGENT_HANDOFF.md) for operating instructions.

## Writing standard

Project technical text follows ASD-STE100 Simplified Technical English, Issue 9, with an approved terminology list for product terms.
An automated checker finds some rule violations; a trained reviewer completes the final language review.
See [`docs/STE_STYLE_GUIDE.md`](docs/STE_STYLE_GUIDE.md).

## License

The project source uses the Apache License 2.0.
Model files and third-party programs keep their own licenses.

See [LICENSE](LICENSE) and [`docs/MODEL_LICENSE_POLICY.md`](docs/MODEL_LICENSE_POLICY.md).
