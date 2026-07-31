# ADR-0001: Use a Local-First Product

Status: Accepted

Date: 2026-07-31

## Context

The product processes video that can contain private data.
The user also requires open-source components and no paid AI API.

## Decision

The default product will process data on the user computer.
It will work offline after required models and programs are present.

Remote services can exist only as optional adapters.
They must not become a requirement for the core product.

## Consequences

Users keep control of private media.
Users also supply computing resources and electricity.

Model size and system support become important product limits.
The project must test complete local installation paths.
