# Silent-Video Review Workflow Test Evidence

Date: 2026-07-31

Computer: Apple M1 Pro with 32 GB memory

AI means Artificial intelligence.
HTML means Hypertext Markup Language.
JSON means JavaScript Object Notation.

## Test type

An agent controlled the browser and completed the workflow.
A human user did not do this test.

This record gives workflow evidence.
This record does not give usability evidence.

Task P0-001 needs a human user test.
That task stays open.

## Test conditions

| Item | Value |
|---|---|
| Source | `silent-software-wikimedia-screencast.webm` |
| Source duration | 87.125 seconds |
| Source audio | None |
| Model profile | `local-ai` |
| Window length | 15 seconds |
| Maximum steps | 6 |
| Speech model | `tiny.en` |
| Vision model | `mlx-community/Qwen3-VL-2B-Instruct-3bit` |
| Prompt version | `guide-window-1` |
| Interface | Local review editor at `127.0.0.1` |
| Job identifier | `c5283900-acd6-49ed-800b-3893729bea2b` |

The browser test tool cannot open a local file chooser.
The test put the file in the form with a script.
The application then did the upload, the analysis, and the export.

## Workflow result

| Action | Result | Note |
|---|---|---|
| Upload the source video | Pass | The editor accepted the 538,279-byte file |
| Create a local AI draft | Pass | Six steps in about 36 seconds |
| Change the guide title | Pass | The editor marked the guide as unsaved |
| Change a step title and instruction | Pass | Two steps changed |
| Replace a step frame | Pass | The editor extracted the selected source time |
| Keep unsaved text during frame replacement | Pass | The earlier defect stays corrected |
| Accept a step | Pass | One step accepted |
| Reject a step | Pass | One step rejected |
| Reorder a step | Pass | The editor moved one step up |
| Save the review | Pass | The editor reported a local save |
| Export HTML | Pass | Status 200 and 2,277 bytes |
| Export Markdown | Pass | Status 200 and 1,363 bytes |
| Export JSON | Pass | Status 200 and 3,968 bytes |
| Omit the rejected step from reader exports | Pass | Markdown kept five of six steps |
| Show the job in the recent list | Pass | The list showed `ready for review` |
| Open the review workspace at 375 pixels | Fail | See defect D-02 |

The browser reported no console errors.

## Measured time

| Measurement | Value |
|---|---|
| Upload and draft generation | 36.0 seconds |
| Real-time factor for the draft | 0.41 |
| Agent review pass | 293 seconds |

The agent review time includes screenshot and inspection delays.
Do not use this number as a human correction time.

A separate command-line run used 20-second windows.
That run needed 18.9 seconds and gave a real-time factor of 0.22.

## Draft quality result

The draft failed on this silent video.

The vision model returned one identical instruction for five of six steps:

```text
Review the visible action when evidence is insufficient. Nearby speech: No speech is available.
```

Five step titles used the same string `Screencast Test Now`.
That string is visible text inside the recorded application form.

The frames were correct.
The step times were correct.
The instructions carried no task information.

The recorded confidence was 0.55 for five steps.
The value did not change with frame content.

## Defect D-01: The vision model repeats the prompt

Severity: High

The returned instruction is the last part of the prompt.
The prompt in `src/open_video_guide/models.py` ends with these two parts:

```text
Use Review the visible action when evidence is insufficient.
Nearby speech: No speech is available.
```

The model output equals that text without the first word.
A test confirmed this exact match.

Two causes are visible in `_proposal_prompt`:

1. The prompt gives a complete fallback sentence that the model can copy.
2. The prompt puts the speech line last, so the model continues from it.

A separate command-line run reproduced the same output.
The problem is therefore in the prompt, not in one job.

This defect explains the open silent-video quality limit.
The frame selection work in task P0-002 will not correct it.

## Defect D-02: The editor does not reflow at 375 pixels

Severity: Medium

The review workspace is wider than a 375-pixel viewport.
The browser clipped the guide title, the instruction text, and the reorder button.

The reader must pan horizontally to read one step.
The start page showed the same problem.

At this width the agent could not open a job from the recent list.
The same element opened correctly at desktop width.

Requirement NFR-006 asks for accessible review.
This layout does not meet that requirement on a small screen.

## Defect D-03: A reorder marks a step as reviewed

Severity: Medium

The agent moved one step with the up button.
The review counter changed from four to five.

The saved guide recorded that step as `changed`.
The user gave no judgement about that step.

This behavior inflates the review progress signal.
It can mark an unread step as handled.

## Defect D-04: The step list returns to the top

Severity: Low

The workspace scrolled to step one after these actions:

- Use this frame
- Accept
- Reject

The user must scroll again after each action.
A long guide makes this problem worse.

## Defect D-05: An export link has no address before the first click

Severity: Low

The export links carry no address until the user clicks them.
The first click still starts the download.

A right click and a middle click do nothing before a first left click.
The browser also shows no address preview.

## Defect D-06: The recent list shows the file name only

Severity: Low

The recent list shows the source file name.
It does not show the saved guide title.

Two jobs from one source file look the same.

## Observation: two job identifiers

The editor job identifier is `c5283900-acd6-49ed-800b-3893729bea2b`.
The pipeline manifest records `ef41be76-f54f-4c8b-a2f1-84514ba82d9b`.

One job has two identifiers.
This difference can make support work harder.

## Observation: one invalid model response

The manifest recorded one problem for window one:

```text
Window 1: The vision model did not return valid JSON.
```

The pipeline used its fallback text and continued.
This behavior is correct.

## Verified conclusions

- The complete local review workflow operates on a silent video.
- The workflow keeps the source video on the local computer.
- The draft text quality on a silent video is not usable.
- The confidence value does not separate good steps from bad steps.

## Reproduction

```bash
.venv/bin/ovg generate \
  benchmark/raw/silent-software-wikimedia-screencast.webm \
  --output outputs/silent-cli-timing \
  --profile local-ai \
  --window-seconds 20 \
  --maximum-steps 6

.venv/bin/ovg validate outputs/silent-cli-timing/guide.json
```

Start the local editor for the browser workflow:

```bash
OVG_WEB_PORT=8766 .venv/bin/python -c \
  "from open_video_guide.adapters.web_app import main; main()"
```
