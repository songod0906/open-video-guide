# MCP Tool Contract

Status: Draft

Contract version: `0.1`

## 1. Contract rules

All tools call the same application service.
The server must validate all input before it starts work.

Local tools can accept an approved local path.
Remote tools must accept an upload identifier instead of an arbitrary path.

Each write tool needs an idempotency key.
Each result includes the contract version.

## 2. Common error result

```json
{
  "contract_version": "0.1",
  "error": {
    "code": "invalid_input",
    "message": "The source file is outside the approved input directory.",
    "retryable": false
  }
}
```

Error codes use a stable machine value.
Messages use clear technical text.

## 3. `inspect_video`

Purpose: Inspect one video without model inference.

Side effect: Read only

Input:

```json
{
  "source_path": "/approved/input/tutorial.mp4"
}
```

Result:

```json
{
  "contract_version": "0.1",
  "source": {
    "file_name": "tutorial.mp4",
    "duration_ms": 42000,
    "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "video_codec": "h264",
    "audio_present": true
  },
  "support": {
    "supported": true,
    "problems": []
  }
}
```

## 4. `create_guide`

Purpose: Start one guide-generation job.

Side effect: Creates local job artifacts

Input:

```json
{
  "source_path": "/approved/input/tutorial.mp4",
  "model_profile": "apple-silicon-balanced",
  "language": "en",
  "idempotency_key": "user-generated-stable-key"
}
```

Result:

```json
{
  "contract_version": "0.1",
  "job_id": "7dbc1c10-337c-4ab8-a3dc-d0bc4127668e",
  "state": "queued"
}
```

The tool must return the existing job for a repeated idempotency key.

## 5. `get_job`

Purpose: Return current job state.

Side effect: Read only

Input:

```json
{
  "job_id": "7dbc1c10-337c-4ab8-a3dc-d0bc4127668e"
}
```

Result:

```json
{
  "contract_version": "0.1",
  "job_id": "7dbc1c10-337c-4ab8-a3dc-d0bc4127668e",
  "state": "analyzing",
  "progress": 0.62,
  "current_stage": "Analyze evidence windows",
  "retryable_error": null
}
```

## 6. `get_guide`

Purpose: Return the current structured guide.

Side effect: Read only

Input:

```json
{
  "job_id": "7dbc1c10-337c-4ab8-a3dc-d0bc4127668e"
}
```

The result contains a guide that obeys `schemas/guide.schema.json`.
It also contains a monotonically increasing guide revision.

## 7. `list_review_items`

Purpose: Return steps that need user review.

Side effect: Read only

Input:

```json
{
  "guide_id": "90c65d27-a3e1-4e6e-9d94-2370690459be",
  "maximum_confidence": 0.75
}
```

The result includes step identifiers, confidence features, and evidence references.

## 8. `update_step`

Purpose: Apply one explicit user correction.

Side effect: Changes a guide revision

Input:

```json
{
  "guide_id": "90c65d27-a3e1-4e6e-9d94-2370690459be",
  "step_id": "13020ea5-eae4-44ad-858f-c60c5e09c589",
  "expected_revision": 3,
  "patch": {
    "instruction": "Select File. Then, select New Project.",
    "review_state": "changed"
  },
  "idempotency_key": "user-generated-stable-key"
}
```

The server must reject a stale expected revision.
The server must keep the old revision.

## 9. `export_guide`

Purpose: Write one export from an accepted guide revision.

Side effect: Creates export files

Input:

```json
{
  "guide_id": "90c65d27-a3e1-4e6e-9d94-2370690459be",
  "revision": 4,
  "format": "html",
  "target_directory": "/approved/output",
  "idempotency_key": "user-generated-stable-key"
}
```

Permitted formats are `json`, `markdown`, and `html`.
The server must resolve the target below an approved output directory.

## 10. Tool annotations

Mark read tools as read-only.
Mark write tools as non-read-only.

Mark `update_step` and `export_guide` as idempotent.
Do not mark `create_guide` as destructive.

## 11. Compatibility

Add optional fields without changing existing field meanings.
Use a new major contract version for a breaking change.

Keep contract fixtures for each supported client.
Run the MCP Inspector before each integration release.
