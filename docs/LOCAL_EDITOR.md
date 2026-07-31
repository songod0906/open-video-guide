# Local Review Editor

## Purpose

The local review editor turns pipeline output into a controlled review workflow.
It keeps source videos and guide data on the local computer.

The editor does not make a generated instruction correct.
Review each step against the source video.

## Requirements

Install Python 3.11 or a later compatible version.
Install FFmpeg with FFprobe.

Install the editor:

```bash
python -m pip install -e ".[web]"
```

Install the local models only when you need them:

```bash
python -m pip install -e ".[web,local-ai]"
```

## Start

Start the local server:

```bash
ovg-web
```

Open this address:

```text
http://127.0.0.1:8765
```

The server accepts connections only from the local computer.
The editor does not require an account.

## Create a guide

1. Select one supported tutorial video.
2. Select the fast draft or the local model draft.
3. Change the draft settings when necessary.
4. Select **Create draft guide**.
5. Wait for the review workspace.

The fast draft extracts frames without model inference.
The local model draft uses the installed speech and vision models.

## Review a guide

1. Compare each instruction with its source frame.
2. Select a frame to move the source video.
3. Change incorrect titles and instructions.
4. Move each step to the correct position.
5. Select another source frame when necessary.
6. Accept, change, or reject each step.
7. Save the guide.

Rejected steps remain in the JavaScript Object Notation export.
Markdown and Hypertext Markup Language exports omit rejected steps.

## Export

Select **Export guide**.
Select Hypertext Markup Language, Markdown, or JavaScript Object Notation.

The editor saves changes before export only when you select **Save changes**.

## Local data

The default data directory is `.ovg-data`.
This directory contains source videos, screenshots, job records, and guides.

Git ignores this directory.
The application does not automatically delete completed jobs.

Set a different directory when necessary:

```bash
OVG_WEB_DATA_ROOT=/approved/private/path ovg-web
```

Set a different local port when necessary:

```bash
OVG_WEB_PORT=8877 ovg-web
```

## Current limits

- A running job does not resume after a process interruption.
- The job state uses coarse progress stages.
- The alpha does not delete jobs through the editor.
- The alpha accepts videos with a maximum size of 4 GB.
- The pipeline accepts videos with a maximum duration of two hours.
- Silent-video quality does not meet a release gate.
