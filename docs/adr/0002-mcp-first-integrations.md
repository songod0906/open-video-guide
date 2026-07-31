# ADR-0002: Use MCP for AI Client Integrations

Status: Accepted

Date: 2026-07-31

## Context

The product can integrate with ChatGPT, Claude, Odysseus, and other AI clients.
Separate native logic for each client would create duplicated behavior.

## Decision

The project will build one Model Context Protocol server.
The server will call the platform-independent application service.

The first transport will use standard input and standard output.
Streamable HTTP will follow after remote security controls exist.

## Consequences

One tool contract can support many clients.
Client-specific metadata remains in small adapters.

Some clients use older transports.
The project must keep a tested compatibility matrix.
