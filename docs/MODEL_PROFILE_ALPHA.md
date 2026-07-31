# Alpha Model Profile

## Profile record

| Item | Selected value |
|---|---|
| Profile | `local-ai` |
| Speech runtime | faster-whisper 1.2.1 |
| Speech model | `tiny.en` |
| Vision runtime | MLX-VLM 0.6.8 |
| Vision model | `mlx-community/Qwen3-VL-2B-Instruct-3bit` |
| Vision model license | Apache License 2.0 |
| Vision model size | Approximately 1.57 GB |
| Computer | Apple M1 Pro with 32 GB memory |
| Decision date | 2026-07-31 |

## Installed dependency record

MCP means Model Context Protocol.

| Component | Version | License record | Decision |
|---|---:|---|---|
| faster-whisper | 1.2.1 | MIT | Accept for alpha |
| MLX-VLM | 0.6.8 | MIT | Accept for alpha |
| MLX | 0.32.0 | MIT | Accept for alpha |
| MCP Python SDK | 1.29.0 | MIT | Accept for alpha |
| PyTorch | 2.13.0 | BSD-style | Accept for alpha |
| Torchvision | 0.28.0 | BSD | Accept for alpha |

The project does not distribute these packages or model weights.
The installation command downloads them from their package sources.

The system FFmpeg license depends on its build configuration.
Complete the FFmpeg review before a binary release.

## Purpose

This profile gives a practical first download for alpha testing.
It does not define the final quality profile.

The model reads one frame and nearby speech for each analysis window.
The model must return one structured step proposal.

## Known limits

- The English speech model does not support all languages.
- One frame can miss a short action.
- Fixed windows can combine multiple actions.
- The small vision model can return weak or invalid text.
- All steps need user review.

## Planned comparison

Compare this profile with Qwen3-VL-4B.
Use the complete 20-video benchmark.

Report accuracy, speed, peak memory, and correction time.
Do not change the default profile without benchmark evidence.
