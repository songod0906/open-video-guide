# Release Process

## 1. Release types

The project uses these release types:

- Patch for compatible fixes
- Minor for compatible features
- Major for breaking contracts

Pre-release versions can use `alpha`, `beta`, or `rc`.

## 2. Release preparation

1. Create a release issue.
2. Freeze the planned scope.
3. Update the version and change log.
4. Verify all dependency and model licenses.
5. Run the complete test and benchmark set.
6. Run security and secret scans.
7. Build packages from a clean checkout.
8. Create a software bill of materials.
9. Verify package installation on supported systems.
10. Review all technical text.

## 3. Release evidence

Put these records in the release:

- Commit identifier
- Package checksums
- Test summary
- Benchmark summary
- Supported system matrix
- Known defects
- Dependency list
- Model list
- Software bill of materials
- Reproduction commands

## 4. Approval

The technical lead approves the build evidence.
The security reviewer approves the security evidence.
The product owner approves the product limits and claims.

## 5. Publication

1. Create a signed version tag.
2. Push the tag.
3. Create the GitHub release.
4. Attach packages, checksums, and evidence.
5. Verify each public download.
6. Publish the release note.

## 6. After publication

Install the public package on one clean supported system.
Run the smoke test.

Open a defect immediately when the smoke test fails.
Withdraw a package when it can cause data loss or unauthorized access.

## 7. Hotfix

A hotfix uses the same tests that apply to its risk.
It must not bypass the security review.

Document the cause, effect, fix, and regression test.
