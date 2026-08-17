# Prompt Repetition Fix Evidence

Date: 2026-08-01

Computer: Apple M1 Pro with 32 GB memory

JSON means JavaScript Object Notation.

This record closes defect D-01 in
`docs/evidence/2026-07-31-silent-review-workflow.md`.

## Problem

The vision model returned the last part of the prompt as the instruction.
The prompt gave the model a complete sentence to copy.

The prompt also ended with the speech line.
A model continues from the last line.

On a silent video the model returned one identical instruction for each frame.

## Change

The change is in `src/open_video_guide/models.py`.

1. The prompt gives no complete fallback sentence.
2. The prompt puts the speech context above the task instructions.
3. The prompt ends with the answer format, not with source data.
4. The prompt asks the model to name the application, window, or control.
5. A guard rejects model text that repeats the prompt.
6. The prompt version changed from `guide-window-1` to `guide-window-2`.

The guard compares lowercase text without punctuation.
It ignores a value with fewer than 12 comparable characters.

A rejected proposal raises a model error.
The pipeline then uses its fallback text and records the problem.
This behavior keeps prompt text out of a guide.

## Measured result

Source: `silent-software-wikimedia-screencast.webm`
Duration: 87.125 seconds
Profile: `local-ai`
Window length: 20 seconds
Maximum steps: 6

| Measurement | Before | After |
|---|---:|---:|
| Unique instructions | 1 of 5 | 5 of 5 |
| Instructions that repeat the prompt | 5 | 0 |
| Recorded model problems | 0 | 0 |
| Generation time in seconds | 18.9 | 15.8 |
| Real-time factor | 0.22 | 0.18 |

### Instructions before the change

Each of the five steps returned this text:

```text
Review the visible action when evidence is insufficient. Nearby speech: No speech is available.
```

### Instructions after the change

```text
1  Create a new task in the project
2  Click on the 'Edit' button in the top right corner, then click on the title to edit it
3  Edit Task
4  Save Task
5  Edit the task
```

The instructions now name a control and an action.
They follow the recorded task order in the benchmark annotation.

## Tests

The suite has 49 tests. All tests pass.

New tests cover these rules:

| Test | Rule |
|---|---|
| Prompt does not end with the speech line | Acceptance 2 |
| Prompt keeps the speech for the model | Speech stays available |
| Silent prompt gives no fallback sentence | Acceptance 1 |
| Guard finds a copied instruction | Acceptance 4 |
| Guard finds a copied speech line | Acceptance 4 |
| Guard keeps a real instruction | No false rejection |
| Guard ignores a short value | No false rejection |
| Frame analysis rejects a repeated prompt | Acceptance 4 |
| Frame analysis keeps a grounded instruction | No false rejection |

Ruff reported no problems.
The limited language check reported no problems.

## Remaining limits

The instructions are short and some are not imperative sentences.
Steps 3 and 4 give a control name without a complete action.

Five step titles still repeat visible text from the recorded form.
The title quality needs separate work.

The confidence value stays at 0.55 for each step.
The value still does not change with frame content.

This test used one silent video.
The complete benchmark must measure silent-video recall.

## Reproduction

```bash
.venv/bin/ovg generate \
  benchmark/raw/silent-software-wikimedia-screencast.webm \
  --output outputs/silent-after-fix \
  --profile local-ai \
  --window-seconds 20 \
  --maximum-steps 6

.venv/bin/python -m pytest tests/test_models.py
```
