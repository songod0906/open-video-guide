# Quality and Evaluation Plan

## 1. Quality objective

The product must create a useful guide without hiding uncertainty.
Quality includes accuracy, evidence, speed, resource use, and correction effort.

## 2. Test levels

### 2.1 Unit tests

Unit tests cover:

- Time and path validation
- Guide schema validation
- Step merge rules
- Confidence feature calculations
- Export rendering
- State transitions

### 2.2 Component tests

Component tests cover each media and model adapter.
Recorded fixtures must make deterministic tests possible.

### 2.3 Pipeline tests

Pipeline tests use short authorized videos.
They test restart, cancellation, corruption, and resource limits.

### 2.4 Product tests

Product tests use the benchmark set.
They compare the generated guide with the reviewed reference guide.

### 2.5 Integration tests

Integration tests cover the command line, local HTTP, and MCP transports.
Each platform test must include invalid input and denied access.

## 3. Main metrics

| Metric | Meaning |
|---|---|
| Step precision | Correct generated steps divided by generated steps |
| Step recall | Expected steps found by the system |
| Temporal intersection | Overlap between predicted and expected time ranges |
| Screenshot usefulness | Reviewer score for the selected image |
| Unsupported-step rate | Steps without sufficient source evidence |
| Correction time | Time that a user needs to accept the guide |
| Silent-video recall | Step recall on silent videos |
| Real-time factor | Processing time divided by video duration |
| Peak memory | Maximum memory during one job |
| Resume success | Interrupted jobs that complete after restart |

## 4. Baselines

The project will compare against:

1. Transcript only
2. Transcript with fixed interval screenshots
3. Full evidence pipeline

The full pipeline must reduce correction time.
It must also reduce unsupported steps.

## 5. Version 0.1 release targets

The feasibility stage will confirm final numeric targets.
The first proposed targets are:

| Metric | Proposed target |
|---|---|
| Step precision | At least 0.90 |
| Step recall | At least 0.80 |
| Silent-video recall | At least 0.70 |
| Unsupported-step rate | At most 0.02 |
| Useful screenshot score | At least 4 of 5 |
| Resume success | 100 percent on test cases |
| Schema validity | 100 percent |

The report must include a confidence interval where it is useful.
The report must show each video category separately.

## 6. Human review protocol

Two reviewers will label the first benchmark subset.
They will resolve differences before the final reference guide.

A reviewer will not see the model profile during a blind comparison.
The reviewer will record correction time with the same editor.

## 7. Regression policy

Each model, prompt, or merge change must run the benchmark.
Continuous integration can use a small deterministic subset.

A full benchmark runs before a release.
The report must compare the result with the current release.

## 8. Defect levels

### Critical

A critical defect causes data loss, unauthorized access, or unsafe output.
No release can have an open critical defect.

### High

A high defect causes a wrong guide without an uncertainty mark.
An alpha release needs an accepted control for each open high defect.

### Medium

A medium defect causes a recoverable workflow failure.
The release note must list each accepted medium defect.

### Low

A low defect has a small usability or presentation effect.
The product owner can accept it for a release.

## 9. Evidence package

Each release must contain:

- Test summary
- Benchmark summary
- Supported system matrix
- Dependency and model licenses
- Known defects
- Security scan result
- Reproduction commands
- Build and package checksums
