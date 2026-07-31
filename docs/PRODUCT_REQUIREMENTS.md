# Product Requirements

## 1. Purpose

Open Video Guide converts a tutorial video into an editable illustrated guide.
The guide helps a user scan, search, verify, and reuse tutorial instructions.

## 2. Product principles

The product has these principles:

1. Local processing is the default.
2. No paid AI API is necessary.
3. Every generated step has source evidence.
4. The user controls the final guide.
5. Platform adapters do not control the core engine.
6. The product reports uncertainty.
7. The project uses components with compatible licenses.

## 3. Primary users

### 3.1 Tutorial learner

This user has a long tutorial video.
The user wants a guide that is easy to scan.

### 3.2 Tutorial creator

This user owns the source video.
The user wants an accessible guide for the audience.

### 3.3 Support and training team

This team records software procedures.
The team wants a reviewable standard operating procedure.

### 3.4 AI workspace user

This user works in ChatGPT, Claude, or Odysseus.
The user wants an agent to create or query a guide.

## 4. Version 0.1 scope

Version 0.1 will:

- Accept local MP4, MOV, and WebM files.
- Process narrated screen recordings.
- Process silent screen recordings.
- Extract ordered steps with timestamps.
- Select one screenshot for each step.
- Keep transcript, frame, optical character recognition, or motion evidence.
- Mark low-confidence steps.
- Let the user change or reject a step.
- Export JSON, Markdown, and self-contained HTML.
- Work offline after required files are present.

## 5. Version 0.1 exclusions

Version 0.1 will not:

- Download a video from YouTube or another platform.
- Process protected or encrypted media.
- Run as a free public hosting service.
- Require an account or a remote database.
- Create a tutorial video from text.
- Promise correct results without user review.
- Support physical tutorials as a release requirement.

Physical tutorials remain an evaluation category.
They can become a later product capability.

## 6. Functional requirements

### FR-001: Media inspection

The engine must inspect the input before inference.
It must report format, duration, streams, size, and decode errors.

### FR-002: Source identity

The engine must calculate a SHA-256 source digest.
The guide must keep the source file name and duration.

### FR-003: Speech extraction

The engine must extract timestamped speech when speech exists.
The engine must continue when speech does not exist.

### FR-004: Visual candidates

The engine must select candidate frames from scene, motion, and interface changes.
It must not use a fixed interval as the only selection method.

### FR-005: Visible text

The engine must extract useful visible text from candidate frames.
It must keep text time bounds.

### FR-006: Step analysis

The engine must analyze bounded video windows.
Each proposed step must cite one or more evidence records.

### FR-007: Verification

The engine must test each step against source evidence.
It must mark a step when the evidence is weak or inconsistent.

### FR-008: Editing

The user must be able to change titles, instructions, screenshots, and order.
The user must be able to reject a step.

### FR-009: Export

Each export must keep step timestamps.
The JSON export must obey the versioned public schema.

### FR-010: Resume

The engine must keep completed intermediate results.
The user must be able to resume an interrupted job.

## 7. Nonfunctional requirements

### NFR-001: Privacy

The default path must not upload the source or result.
Telemetry must be off by default.

### NFR-002: Resource control

The user must be able to select a model profile.
The profile must show expected memory and disk requirements.

### NFR-003: Reproducibility

Each job must record component versions, model identifiers, settings, and prompts.

### NFR-004: Portability

The first supported system is Apple Silicon with 32 GB memory.
Linux with a compatible graphics processor is the second supported system.

### NFR-005: Reliability

One failed video segment must not discard completed segments.
The system must give an actionable error message.

### NFR-006: Accessibility

The editor must support keyboard use.
Exported HTML must use semantic headings and alternative text.

### NFR-007: Security

The system must treat media, model output, and MCP input as untrusted data.
It must validate paths and structured data.

## 8. Product acceptance

Version 0.1 can ship when all release gates in `QUALITY_PLAN.md` pass.
The product owner must accept the final evaluation report.
