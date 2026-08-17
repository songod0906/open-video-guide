# Product Improvement and Growth Plan

## Product loop

Use one evidence loop for each release.

1. Run the current profile on the benchmark.
2. Measure step quality and correction time.
3. Classify the largest failure group.
4. Change one pipeline component.
5. Run the same benchmark again.
6. Keep the change only when evidence improves.

## Improvement order

### 1. Better event boundaries

Replace fixed windows with scene, motion, and interface-change signals.
Keep a fixed-window fallback for unusual videos.

### 2. Better frame selection

Score frames for sharpness, text visibility, and state change.
Select the best evidence frame for each action.

### 3. Better speech and visible text

Add multilingual speech profiles.
Add optical character recognition for interface text.

### 4. Better verification

Compare each instruction with multiple frames.
Reject a proposal when its evidence does not support the action.

### 5. Better correction workflow

Add a local review editor.
Record correction types without collecting private source media.

## Safe growth channels

The project earns trust through useful evidence.
Do not use automated spam or false capability claims.

MCP means Model Context Protocol.

- Publish benchmark reports with reproducible commands.
- Publish short before-and-after guide examples with authorized media.
- Submit the project to open-source directories.
- Write integration guides for Odysseus, Claude, ChatGPT, and Codex.
- Invite tutorial creators to test private local processing.
- Use GitHub Discussions for failure examples and profile requests.

## Automation

GitHub Actions can automate repeatable release work.

- Run tests and the language checker for each pull request.
- Build a release evidence package for each tag.
- Publish checksums and dependency records.
- Create a draft release note from merged changes.
- Update a public benchmark table after an approved benchmark run.

Human approval must control each public announcement.
Platform credentials must stay outside the repository.

## Launch gate

Start public promotion after these conditions pass:

- Five external users complete one guide.
- The MCP integration passes on one supported client.
- The benchmark report includes silent-video results.
- The security review has no open critical defect.
- The documentation states all known limits.
