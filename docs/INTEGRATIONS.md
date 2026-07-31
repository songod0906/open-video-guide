# Integration Strategy

## 1. Recommendation

Build one Model Context Protocol (MCP) server first.
Use platform adapters around the same application service.

This design gives one integration contract for many AI clients.
It also keeps the local product useful without an AI client.

## 2. Stable tool set

The first MCP server will expose these tools:

| Tool | Purpose |
|---|---|
| `inspect_video` | Return media facts and support information |
| `create_guide` | Start a local guide job |
| `get_job` | Return progress and errors |
| `get_guide` | Return the structured guide |
| `list_review_items` | Return uncertain steps |
| `update_step` | Apply an explicit user correction |
| `export_guide` | Write a selected export format |

Write tools must use idempotency keys.
The server must require confirmation for a consequential file change.

The local alpha implements `inspect_video` and synchronous `create_guide`.
The local transport smoke test passed on 2026-07-31.

The installed Odysseus application passed its integration test on 2026-07-31.
Odysseus called both tools through the standard-input server.
It created `frame-only` and `local-ai` guide artifacts.

## 3. ChatGPT and Codex

OpenAI now describes this integration surface as a plugin.
A plugin can include skills, an MCP server, and an optional user interface.

The server defines tools for ChatGPT and Codex.
Custom user interface output is optional.

Public distribution has additional requirements:

- Use a stable public HTTPS endpoint.
- Support MCP Streamable HTTP.
- Use a stable path such as `/mcp`.
- Apply authentication and authorization on the server.
- Keep operational logs and metrics.
- Complete platform review and domain verification.

These requirements conflict with a fully local public plugin.
The project will therefore use two ChatGPT modes.

### 3.1 Developer and private mode

A user can connect a private endpoint during development.
The media worker can remain on the user computer.

### 3.2 Public plugin mode

A public gateway will expose only approved tools.
An authenticated private worker will do local processing.

The public gateway is a future deployment option.
It is not necessary for the open-source local product.

Official source:
[OpenAI plugin MCP server guide](https://developers.openai.com/plugins/build/mcp-server)

## 4. Claude

Claude products support MCP.
The first Claude path will use a local standard-input and standard-output server.

A later remote path will use the current remote MCP transport.
The adapter must pass the official MCP Inspector tests.

Official sources:

- [Anthropic MCP overview](https://docs.anthropic.com/en/docs/mcp)
- [MCP documentation](https://modelcontextprotocol.io/docs/getting-started/intro)

## 5. Odysseus

The user reference was to **Odysseus**, not Odyssey.
Odysseus is a self-hosted AI workspace associated with PewDiePie.

The active community repository has built-in MCP management.
It currently includes standard-input and standard-output support.
It also includes server-sent event support.

Open Video Guide will provide a standard-input adapter first.
It will also keep a compatibility transport for older MCP clients.

The installed Odysseus application passed the local integration test.
This result does not verify all Odysseus versions.

Odysseus is a strong early integration target for these reasons:

- It has the same local-first product direction.
- It already manages local model and MCP services.
- It can keep private video on local hardware.
- It gives technical users an integration path before public plugin review.

The project will not copy Odysseus code.
It will publish a small installation recipe and an MCP configuration example.

Official source:
[Odysseus community repository](https://github.com/odysseus-dev/odysseus)

## 6. Generic clients

The project will support three access layers:

1. Python application service
2. Local HTTP interface
3. MCP server

The command-line interface will call the same application service.
No client can bypass authorization or file policy.

## 7. Integration phases

### Phase A: Local command line

Prove the core pipeline and contracts.
Do not add remote access.

### Phase B: Local MCP

Add standard-input transport.
Test with the MCP Inspector, Claude, and Odysseus.

### Phase C: Local editor

Add a local web editor for evidence review.
Keep the editor independent from AI clients.

### Phase D: Remote MCP

Add Streamable HTTP, authentication, job isolation, and rate limits.
Complete a security assessment before public use.

### Phase E: Platform packages

Publish installation packages for selected clients.
Complete each platform review before a support claim.

## 8. Compatibility policy

Tool names and required fields must remain stable in one major version.
New optional fields must not break an older client.

Each supported client needs:

- A version matrix
- An installation test
- A direct tool test
- An invalid-input test
- An authorization test
- A release note
