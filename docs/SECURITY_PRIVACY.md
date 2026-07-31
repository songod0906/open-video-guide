# Security and Privacy Plan

## 1. Security objective

The product processes private video and powerful model output.
The default system must keep data on the user computer.

## 2. Protected assets

The system must protect:

- Source videos
- Extracted audio and frames
- Generated guides
- User corrections
- Local file paths
- Model files
- Authentication tokens
- Job and error logs

## 3. Trust boundaries

The system has these trust boundaries:

1. Untrusted media enters the media process.
2. Untrusted model output enters the application service.
3. Untrusted MCP input enters a client adapter.
4. Downloaded model files enter the inference runtime.
5. Export files leave the artifact store.

## 4. Main threats and controls

| Threat | Required control |
|---|---|
| Malformed media exploits a decoder | Use current packages and isolate media work |
| A path escapes the job directory | Resolve and validate every path |
| Model output invents a file path | Permit only referenced artifact identifiers |
| Prompt injection appears in video text | Treat video text as data, not instructions |
| An MCP client reads another job | Enforce job ownership in the service |
| A remote request causes high cost | Apply size, time, memory, and job limits |
| A model file has changed | Verify a digest and a trusted source |
| A log contains private text | Redact media text and tokens by default |
| An export executes active content | Escape text and use a strict content policy |
| A dependency is compromised | Pin versions and create a software bill of materials |

## 5. Local mode

Local mode must bind only to loopback by default.
It must not require a user account.

The product must not send telemetry.
It must not check for updates during a job.

## 6. Remote mode

Remote mode requires a separate security review.
It must use transport security and explicit authentication.

The server must:

- Authorize every tool call.
- Isolate jobs by user.
- Limit upload size and duration.
- Expire temporary artifacts.
- Remove sensitive log data.
- Rate-limit expensive tools.
- Require confirmation for destructive actions.

## 7. Media policy

Accept only documented media types.
Inspect the file type from content, not only its name.

Use a restricted work directory.
Do not follow symbolic links from an untrusted job.

## 8. Model supply chain

The model registry must record:

- Source repository
- Exact revision
- File digest
- License
- Required runtime
- Supported task
- Approval date

Do not run a model with an unknown source or license.

## 9. Retention

The user controls retention in local mode.
The default cleanup action must show its exact file scope.

Remote mode must have a documented retention time.
The server must delete expired temporary data.

## 10. Security release gate

A release needs:

- Threat-model review
- Secret scan
- Dependency scan
- Static analysis
- Path and authorization tests
- Software bill of materials
- Private vulnerability reporting instructions

Report a security issue with the process in `SECURITY.md`.
