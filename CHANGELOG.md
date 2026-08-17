# Change Log

This file records important project changes.
The project uses semantic versioning after the first release.

AI means Artificial Intelligence.
MCP means Model Context Protocol.
HTML means Hypertext Markup Language.
JSON means JavaScript Object Notation.

## Unreleased

### Added

- Product requirements and scope
- Local-first system architecture
- AI system and benchmark plan
- MCP-first integration strategy
- Professional stage-gate workflow
- Security, privacy, data, and license policies
- Versioned guide JSON schema
- Guide validation command
- Twenty authorized benchmark records and provisional annotations
- Benchmark schemas and validation command
- Repository quality and contribution controls
- Local video inspection and guide generation commands
- Local speech and vision model adapters
- Markdown, HTML, JSON, and image exports
- Local Model Context Protocol adapter and smoke test
- Odysseus setup instructions
- Local review editor with corrections and exports
- Shared Codex and Claude project handoff
- Guard that rejects model text that repeats the prompt

### Fixed

- The vision model repeated the prompt as a step instruction on silent video.
  The prompt now gives no fallback sentence and ends with the answer format.
  The prompt version changed from `guide-window-1` to `guide-window-2`.
