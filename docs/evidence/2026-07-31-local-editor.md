# Local Review Editor Test Evidence

Date: 2026-07-31

Computer: Apple M1 Pro with 32 GB memory

Browser viewport tests used 1200 by 953 pixels and 390 by 844 pixels.
The source was `short-form-mobile-screencast.ogv`.
Its duration was 58.77 seconds.

## Automated tests

| Capability | Result | Evidence |
|---|---|---|
| Create a local job | Pass | The adapter stored an uploaded test video |
| Reject an unsupported file | Pass | The adapter returned status 400 |
| Enforce the upload limit | Pass | The adapter rejected a four-byte file with a three-byte limit |
| Keep artifact paths contained | Pass | The store rejected a parent-directory path |
| Reject an untrusted origin | Pass | The adapter returned status 403 |
| Save guide corrections | Pass | The adapter stored titles, instructions, states, and order |
| Replace a source frame | Pass | The adapter extracted the selected source timestamp |
| Omit rejected reader steps | Pass | Hypertext Markup Language and Markdown exports omitted the rejected step |

The complete test suite passed 32 tests.
Ruff found no Python lint problems.
The limited language check found no problems.
A trained reviewer must complete the language review.

## Browser workflow

| Action | Result |
|---|---|
| Load the start page | Pass |
| Upload a real local video | Pass |
| Create a two-step fast draft | Pass |
| Open the review workspace | Pass |
| Change the guide title | Pass |
| Change a step title and instruction | Pass |
| Replace a screenshot from the source | Pass |
| Preserve unsaved text during frame replacement | Pass |
| Reject one step | Pass |
| Save the reviewed guide | Pass |
| Download the Hypertext Markup Language export | Pass |
| Use the editor at the narrow viewport | Pass |
| Complete the final flow without console errors | Pass |

The browser test used job `85ece836-c878-41c0-9e62-496be50c13c1`.
The saved guide title was `Reviewed globe demo`.

The structured guide kept two steps.
The reader export kept one visible step.

## Defect found during the test

The first frame-replacement flow discarded unsaved step text.
The editor replaced the complete client guide with the server response.

The fix now merges only the new frame evidence.
The repeated browser flow preserved the title and instruction.

## Current limits

- A running job does not resume after a process interruption.
- Job progress uses coarse states.
- The browser interface does not delete a job.
- The test did not measure guide accuracy.
- Silent-video quality remains below the release gate.
