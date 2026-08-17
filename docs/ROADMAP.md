# Product Roadmap

Dates are target ranges.
Evidence gates control the actual release date.

## Phase 0: Engineering foundation

Target: July 2026

- Define the product scope.
- Define the architecture and contracts.
- Define the development and release workflow.
- Add repository controls and continuous integration.
- Create the public project repository.

Exit: The initial repository passes all checks.

## Phase 1: Feasibility benchmark

Target: August 2026

- Build the authorized 20-video benchmark.
- Implement deterministic media extraction.
- Compare speech, text, scene, and vision components.
- Select the Apple Silicon model profile.
- Publish the baseline report.

Exit: Gate 1 in `DEVELOPMENT_WORKFLOW.md` passes.

## Phase 2: Command-line prototype

Target: September to October 2026

- Add job state and resumable artifacts.
- Add narrated and silent analysis.
- Add evidence merge and step verification.
- Add JSON, Markdown, and HTML export.
- Add benchmark regression tests.

Exit: Gate 2 passes.

## Phase 3: Local alpha

Target: November to December 2026

- Add the local review editor.
- Add install and model management.
- Add local MCP tools.
- Test with Claude and Odysseus.
- Complete the first security review.

Exit: Gate 3 passes.

Current evidence: The local editor and Odysseus adapter have testable alpha implementations.
Phase 3 remains open because its security and quality gates are incomplete.

## Phase 4: Public beta

Target: First quarter of 2027

- Run external user tests.
- Freeze the version 1 guide schema.
- Publish packages for supported systems.
- Prepare an optional remote MCP gateway.
- Start the ChatGPT plugin review path.

Exit: Gate 4 passes.

## Phase 5: Version 1.0

Target: After beta evidence

- Meet all quality targets.
- Publish signed and reproducible packages.
- Publish model, dataset, security, and evaluation records.
- Publish the support and migration policy.

Exit: Gate 5 passes.

## Future work

Future work can include:

- Physical tutorial support
- Mobile review
- Team guide libraries
- More languages
- Text-to-tutorial-video generation
- Creator publishing tools

Future work does not change version 0.1 scope.
