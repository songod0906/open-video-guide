# ADR 0005: Testable Local Alpha

Status: Accepted

Date: 2026-07-31

## Context

The repository needs a product that a user can test before the complete pipeline exists.
The first test must keep source media on the local computer.

Large vision models create a slow first-run experience.
The first guide also needs visible evidence when model inference fails.

## Decision

Add one synchronous application service for local guide generation.
Keep the command-line and Model Context Protocol adapters outside the core engine.

Use fixed analysis windows in the first alpha.
Extract one candidate frame from each window.

Use faster-whisper for local speech recognition.
Use MLX-VLM for local visual analysis on Apple Silicon.

Use `mlx-community/Qwen3-VL-2B-Instruct-3bit` as the tested default.
The model needs approximately 1.57 GB of storage.

Create an evidence-only guide when the user selects the `frame-only` profile.
Mark every generated step as unreviewed.

## Consequences

The user can test the complete file workflow now.
The alpha can process narrated or silent videos.

Fixed windows can combine different actions.
One frame can miss a short action.

The small model can produce weak instructions.
Benchmark evidence must control future model changes.

The Model Context Protocol call blocks until generation finishes.
A later job service will add progress and restart support.

The alpha pins the Model Context Protocol Python software development kit below version 2.
Version 2 needs a separate adapter migration and compatibility test.
