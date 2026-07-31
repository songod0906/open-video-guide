# ADR 0006: Local Review Editor

Status: Accepted

Date: 2026-07-31

## Context

The alpha creates guide files, but users need a controlled correction workflow.
The workflow must keep private media on the local computer.

The core engine must not depend on a user interface framework.
Completed jobs must remain available after an editor restart.

## Decision

Add a local Hypertext Transfer Protocol adapter with a browser interface.
Use FastAPI for the adapter and Uvicorn for the local server.

Bind the server to `127.0.0.1`.
Reject untrusted host headers and write-request origins.

Store each job in one local file directory.
Store job metadata in an atomic JavaScript Object Notation file.

Keep the core engine independent from the editor.
Call the existing application service from a background task.

Let users change titles, instructions, order, review states, and source frames.
Create replacement screenshots only from the uploaded source video.

Keep rejected steps in the structured guide.
Omit rejected steps from reader exports.

## Consequences

Users can create, review, and export a guide in one local interface.
Completed job records remain available after a server restart.

The first adapter uses coarse progress states.
A running pipeline job does not resume after a process interruption.

The browser interface adds local storage and request-origin risks.
Upload limits, path containment, and origin checks control these risks.

The editor does not add authentication.
Local network and remote profiles need separate authenticated adapters.
