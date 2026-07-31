# Open Video Guide

Open Video Guide converts a tutorial video into an illustrated guide.

The project is local-first and open source. It does not require a paid AI API.
Users supply the computer, storage, network bandwidth, and electricity.

> [!IMPORTANT]
> The repository contains an experimental local alpha.
> Review each generated step before use.

## Product goal

The product must make each generated step easy to verify.
Each step must include a timestamp, visual evidence, confidence data, and a review state.

The alpha processes user-owned video files.
It exports Markdown, Hypertext Markup Language (HTML), and structured JavaScript Object Notation (JSON).

Narrated-video smoke tests pass.
Silent-video quality does not yet meet a release gate.

## Product difference

Most products extract a transcript and make a summary.
Open Video Guide will connect each instruction to evidence from the source video.

The product will:

- Keep all processing on the local computer after model download.
- Mark uncertain instructions for review.
- Keep source timestamps with each step.
- Select useful screenshots for each instruction.
- Let the user correct the result before export.
- Use replaceable model and platform adapters.

## Local alpha pipeline

```text
Video file
  |
  +-- FFmpeg: media inspection and extraction
  +-- faster-whisper: narrated speech and timestamps
  +-- Fixed windows: candidate frame selection
  +-- Qwen3-VL through MLX-VLM: visual step proposals
  |
Evidence merge and verification
  |
Editable guide
  |
Markdown, HTML, JSON, and screenshots
```

The architecture also permits other runtimes.
For example, Linux systems can use faster-whisper and a CUDA model server.

## Integration plan

One Model Context Protocol (MCP) server will expose the product functions.
Transport adapters will support these clients:

- ChatGPT and Codex plugins
- Claude and other MCP clients
- Odysseus local workspaces
- Command-line and local web clients

Odysseus is the correct name of the PewDiePie project.
It is a self-hosted AI workspace that can connect to MCP servers.

See [docs/INTEGRATIONS.md](docs/INTEGRATIONS.md) for the verified plan.

## Repository map

| Path | Purpose |
|---|---|
| `src/open_video_guide` | Stable Python contracts and future engine code |
| `schemas` | Versioned interchange contracts |
| `examples` | Synthetic contract examples |
| `benchmark` | Public benchmark records and provisional annotations |
| `docs` | Product and engineering records |
| `.github` | Review, issue, dependency, and continuous integration controls |

## Current commands

Use Python 3.11 or a later compatible version.

```bash
python -m pip install -e ".[dev]"
ovg validate examples/example-guide.json
python scripts/validate_benchmark.py
pytest
python scripts/check_ste.py
```

The `validate` command checks a guide against the public JSON schema.
The `inspect` command returns local video facts.
The `generate` command creates a local illustrated guide.

Run a fast file test without model inference:

```bash
ovg generate /path/to/tutorial.mp4 \
  --output outputs/my-first-guide \
  --profile frame-only
```

Install the local model dependencies:

```bash
python -m pip install -e ".[dev,local-ai,mcp]"
```

Run the local Artificial Intelligence (AI) profile:

```bash
ovg generate /path/to/tutorial.mp4 \
  --output outputs/my-ai-guide \
  --profile local-ai
```

See [the local alpha test](docs/LOCAL_TEST.md) for complete instructions.

The benchmark validator checks public records without the source videos.
Use its media option to check local source digests.

## Development status

The project has a testable alpha pipeline.
The complete benchmark and silent-video release gates remain open.

The local Model Context Protocol adapter exposes two tested tools.
Odysseus setup is prepared, but its authenticated integration test remains open.

See these documents:

- [Product requirements](docs/PRODUCT_REQUIREMENTS.md)
- [System architecture](docs/ARCHITECTURE.md)
- [AI system plan](docs/AI_SYSTEM.md)
- [MCP tool contract](docs/MCP_TOOL_CONTRACT.md)
- [Development workflow](docs/DEVELOPMENT_WORKFLOW.md)
- [Quality plan](docs/QUALITY_PLAN.md)
- [Roadmap](docs/ROADMAP.md)

## Writing standard

Project technical text must obey ASD-STE100 Simplified Technical English, Issue 9.
The project uses an approved terminology list for software terms.

The automated checker finds only some rule violations.
A trained reviewer must do the final language review.

Legal text and exact source text are not changed.
See [docs/STE_STYLE_GUIDE.md](docs/STE_STYLE_GUIDE.md).

## License

The project source uses the Apache License 2.0.
Model files and third-party programs keep their own licenses.

See [LICENSE](LICENSE) and [docs/MODEL_LICENSE_POLICY.md](docs/MODEL_LICENSE_POLICY.md).
