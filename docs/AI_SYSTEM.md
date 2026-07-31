# AI System Plan

## 1. AI objective

The AI system must make an evidence-grounded guide.
It must not make a general video summary.

## 2. Model tasks

The pipeline divides inference into small tasks:

1. Detect speech and make timestamped text.
2. Detect scene and interface changes.
3. Extract visible text from candidate frames.
4. Propose actions from bounded evidence windows.
5. Merge duplicate actions.
6. Verify each action against source evidence.
7. Write clear guide text.

## 3. Initial model profiles

### 3.1 Apple Silicon profile

Use these initial components:

- `whisper.cpp` with a suitable Whisper model
- PySceneDetect and OpenCV
- PaddleOCR
- Qwen3-VL-4B through MLX-VLM

The project can test SmolVLM2 as a low-resource alternative.

### 3.2 Linux graphics processor profile

Use these initial components:

- faster-whisper
- PySceneDetect and OpenCV
- PaddleOCR
- Qwen3-VL through a compatible inference server

## 4. Chunk policy

Do not send a complete long video in one model request.
Split the timeline into bounded analysis windows.

The first experiment will test windows from 30 to 90 seconds.
Each window will include selected frames, nearby text, and motion information.

Window overlap must prevent a lost action at a boundary.
The assembler must remove duplicate boundary steps.

## 5. Silent-video policy

The system must not depend on speech.
Silent-video analysis will use these signals:

- Cursor movement
- Click indicators
- Interface state changes
- Scene differences
- Visible text changes
- Object movement
- Dense frame samples near activity

The evaluation set must contain silent videos.
The release gate will report silent-video results separately.

## 6. Evidence model

Each step needs one or more evidence records.
An evidence record includes a type and time bounds.

The system can use these evidence types:

- Frame
- Transcript
- Optical character recognition result
- Motion event

The system must not accept a step without evidence.

## 7. Confidence model

The first confidence score will combine explicit features.
It will not use model self-confidence as the only input.

Candidate features include:

- Agreement between speech and visible action
- Agreement between multiple frames
- Optical character recognition match
- Temporal localization quality
- Verifier pass result
- Duplicate proposal agreement
- Missing evidence penalty

The quality report must calibrate the score.
A low score must set `review_state` to `unreviewed`.

## 8. Prompt controls

Prompts must:

- Request structured data.
- Define permitted evidence references.
- Forbid unsupported actions.
- Require an uncertainty reason.
- Keep observed facts separate from inference.
- Use the project terminology.

Prompts must have versions.
An inference manifest must record the prompt version.

## 9. Failure controls

The system must detect these failures:

- Media decode failure
- No useful frames
- Unsupported language
- Invalid model response
- Missing evidence reference
- Time bounds outside the source
- Duplicate step identifier
- Resource exhaustion

The system must keep intermediate work after a recoverable failure.

## 10. Evaluation data

The benchmark will start with 20 authorized videos.
It will have five videos in each category:

- Narrated software tutorial
- Silent software tutorial
- Physical or do-it-yourself tutorial
- Fast short-form tutorial

The dataset record must contain source rights and expected steps.
It must also contain expected time ranges and screenshot regions.

## 11. Model change gate

A model change requires:

1. A license check.
2. A resource check.
3. A benchmark run.
4. A regression comparison.
5. A model card update.
6. A recorded decision.

The change must not reduce a release metric without an accepted exception.
