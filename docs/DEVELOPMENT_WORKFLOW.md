# Professional Product Development Workflow

## 1. Purpose

This workflow moves the project from an idea to a supported release.
It uses evidence at each decision gate.

## 2. Work roles

One person can have more than one role.
Each decision must still name the responsible role.

| Role | Main responsibility |
|---|---|
| Product owner | Scope, user value, and release acceptance |
| Technical lead | Architecture and technical decisions |
| AI engineer | Models, prompts, datasets, and evaluation |
| Software engineer | Core services, adapters, and tests |
| Security reviewer | Threats, privacy, and release controls |
| Technical writer | ASD-STE100 text and user instructions |
| Release manager | Version, evidence, package, and release record |

## 3. Stage 0: Product discovery

### Inputs

- User problem
- Market evidence
- Open-source requirement
- Hardware limits

### Work

1. Define the user and the job.
2. Compare direct and adjacent products.
3. Define the product difference.
4. Record legal and platform limits.
5. Define the smallest useful release.

### Outputs

- Product requirements
- Scope exclusions
- Initial risk register
- Initial architecture decisions

### Gate 0

The product owner confirms the problem and version 0.1 scope.
The technical lead confirms that the scope is technically possible.

## 4. Stage 1: Feasibility and benchmark

### Work

1. Build the authorized 20-video benchmark.
2. Make a deterministic media extraction baseline.
3. Test speech, scene, text, and vision components.
4. Measure quality, speed, memory, and disk use.
5. Compare at least two visual model profiles.
6. Test narrated and silent videos separately.

### Outputs

- Dataset card
- Baseline report
- Model comparison report
- Updated license register
- Go or stop decision

### Gate 1

The selected stack must process all benchmark files.
It must not have an unresolved license conflict.

The median manual correction time must improve from the transcript-only baseline.
The product owner must accept the measured product advantage.

## 5. Stage 2: Technical prototype

### Work

1. Implement resumable job state.
2. Implement evidence extraction.
3. Implement chunked step analysis.
4. Implement verification and confidence features.
5. Implement JSON, Markdown, and HTML output.
6. Add deterministic unit and integration tests.

### Outputs

- Command-line prototype
- Versioned guide schema
- Reproducible inference manifest
- Prototype benchmark report

### Gate 2

All guide steps must have valid evidence references.
The schema and resume tests must pass.

No benchmark step can cite a time outside the source.
The prototype must report all known failures.

## 6. Stage 3: Alpha product

### Work

1. Add the local review editor.
2. Add corrections and guide history.
3. Add installation and model setup.
4. Add local MCP transport.
5. Complete threat modeling.
6. Test on clean supported computers.

### Outputs

- Signed alpha package
- Installation guide
- Security review
- Usability report
- Claude and Odysseus integration reports

### Gate 3

A new user must complete the primary task without developer help.
The package must keep user media out of Git and telemetry.

All high security risks must have controls.
The quality gates must meet the alpha targets.

## 7. Stage 4: Beta product

### Work

1. Run external tests with authorized users.
2. Measure correction time and task success.
3. Improve accessibility and error recovery.
4. Freeze the version 1 guide contract.
5. Add remote MCP only after security approval.
6. Prepare platform packages.

### Outputs

- Beta evaluation report
- Compatibility matrix
- Support policy
- Migration tests
- Release candidate

### Gate 4

No open critical defect can remain.
All public claims must have test evidence.

The release manager must reproduce the package from a clean checkout.
The product owner must accept the known limits.

## 8. Stage 5: General release

### Work

1. Freeze source and dependency versions.
2. Run the complete benchmark and security checks.
3. Create the software bill of materials.
4. Sign packages and provenance data.
5. Publish the release notes and migration guide.
6. Publish the release.

### Outputs

- Tagged source
- Signed packages
- Checksums
- Software bill of materials
- Model and dataset cards
- Release evidence

### Gate 5

Continuous integration must pass on the release commit.
The release evidence must match the published files.

The security reviewer and product owner must approve the release.

## 9. Stage 6: Operation and improvement

### Work

1. Triage defects and security reports.
2. Monitor supported dependency changes.
3. Run benchmark tests for model changes.
4. Review product metrics without collecting private media.
5. Publish fixes with the release process.
6. Remove support only with a migration period.

## 10. Git workflow

Use `main` as the protected release branch.
Use a short branch for each change.

Branch names use these prefixes:

- `feat/`
- `fix/`
- `docs/`
- `test/`
- `chore/`
- `security/`

Each pull request must:

- Have one clear purpose.
- Link to an issue.
- State the user effect.
- Include test evidence.
- Include a license check for a new component.
- Include an ASD-STE100 review for technical text.
- Update an architecture record for a major decision.

Use squash merge for normal changes.
Use a signed tag for a release.

## 11. Issue workflow

Issues use these states:

1. `triage`
2. `ready`
3. `in progress`
4. `in review`
5. `blocked`
6. `done`

An issue is ready when it has:

- A user or system outcome
- Acceptance criteria
- Required test evidence
- Known dependencies
- A risk and license note

## 12. Definition of done

A change is done when:

- The acceptance criteria pass.
- New logic has tests.
- Existing tests pass.
- The documentation is correct.
- The language review passes.
- The change records security and privacy effects.
- License data is current.
- The user-facing behavior has evidence.

## 13. Decision process

Use an architecture decision record for a hard-to-reverse decision.
Record the context, decision, consequences, and status.

Do not hide an important decision in a pull request comment.
Replace a decision only with a new decision record.
