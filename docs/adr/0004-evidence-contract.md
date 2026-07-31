# ADR-0004: Require Evidence for Every Step

Status: Accepted

Date: 2026-07-31

## Context

A video model can make a plausible instruction that the source does not show.
A transcript-only system also misses silent actions.

## Decision

Each guide step must have one or more timestamped evidence records.
A step without evidence is invalid.

The system will keep confidence and review state as separate fields.

## Consequences

Users can inspect the source for each instruction.
The engine needs more storage and verification work.

The schema can reject an unsupported step.
The quality plan can measure the unsupported-step rate.
