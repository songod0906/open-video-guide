# Seed Benchmark Dataset Card

## Summary

This benchmark tests early video-to-guide contracts.
It contains four public source records and four provisional annotations.

The source videos stay outside Git.
The manifest records each source digest, license, duration, language, and speech state.

## Categories

| Category | Seed records | Target records |
|---|---:|---:|
| Narrated software | 1 | 5 |
| Silent software | 1 | 5 |
| Physical work | 1 | 5 |
| Short-form motion | 1 | 5 |

The seed has 20 percent of the planned records.
Do not use this seed for final quality claims.

## Source rights

| Record | Author | License | Change |
|---|---|---|---|
| Cite a video | 85jesse | CC0 1.0 | Wikimedia 480p transcode |
| Wikimedia screencast | Toolboxx8 | CC BY-SA 4.0 | Wikimedia 480p transcode and audio removal |
| Rope bowline | Slashme | CC BY-SA 4.0 | Wikimedia 480p transcode |
| Mobile screen capture | LauraHale | CC BY 3.0 | No change |

Each manifest record links to its source page and license.
Users must follow the applicable attribution and share-alike terms.

## Collection method

We selected public tutorial videos from Wikimedia Commons.
We checked each source page before download.
We recorded the local source digest after each permitted transformation.

We removed audio from one source to create a controlled silent case.
The transformed source remains subject to Creative Commons Attribution-ShareAlike 4.0.

## Annotation method

One review pass produced each seed annotation.
Visual review supplied all screenshot times and regions.
Local Whisper transcripts supported narrated-video time bounds.
The review used faster-whisper 1.2.1 with the `tiny.en` model.
The transcripts supported timing only and are not benchmark labels.

The annotation includes ordered steps, time bounds, and one screenshot region per step.
The repository does not contain extracted screenshots.

## Intended use

Use the seed to test schemas, loaders, and early pipeline output.
Use it to find annotation problems before the full collection.

Do not use the seed to compare model quality.
Do not use it to make safety claims.

## Limits

The seed contains only four videos.
The videos use English interfaces or English speech.
The source interfaces include old software versions.
One reviewer can introduce annotation bias.

Two reviewers must check each annotation before benchmark scoring.
An adjudicator must resolve material differences.

## Privacy and safety

The selected sources are public media.
The benchmark does not contain private user video.

Physical knot instructions can cause injury or property damage.
Users must not treat generated guides as safety certification.

## Version status

Version `0.1-seed` is provisional.
Issue 4 tracks collection of the remaining 16 videos.
