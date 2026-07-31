# Seed Benchmark Dataset Card

## Summary

This benchmark tests early video-to-guide contracts.
It contains 20 public source records and 20 provisional annotations.

The source videos stay outside Git.
The manifest records each source digest, license, duration, language, and speech state.

## Categories

| Category | Seed records | Target records |
|---|---:|---:|
| Narrated software | 5 | 5 |
| Silent software | 5 | 5 |
| Physical work | 5 | 5 |
| Short-form motion | 5 | 5 |

The collection meets the planned source count.
The annotations still require independent review.

## Source rights

| Record | Author | License | Change |
|---|---|---|---|
| Cite a video | 85jesse | CC0 1.0 | Wikimedia 480p transcode |
| Inkscape biohazard | Adam Coster | CC BY 3.0 | Wikimedia 480p transcode |
| npm dependencies | Ganesh H | CC BY 3.0 | Wikimedia 480p transcode |
| Cat-a-lot | Pete Forsyth | CC BY 4.0 | Wikimedia 480p transcode |
| Create wiki links | Psypherium | CC BY 3.0 | Wikimedia 480p transcode |
| Wikimedia screencast | Toolboxx8 | CC BY-SA 4.0 | Wikimedia 480p transcode and audio removal |
| Interlanguage links | -chanakyakdas | CC BY-SA 4.0 | Wikimedia 480p transcode and audio removal |
| Wikiversity editing | JWSchmidt and Daveydweeb | CC BY-SA 3.0 | Wikimedia 480p transcode and audio removal |
| Ogg conversion | Jihei | CC BY-SA 3.0 | Wikimedia 480p transcode and audio removal |
| Wikipedia source links | Frank Schulenburg | CC BY-SA 3.0 | Wikimedia 480p transcode and audio removal |
| Rope bowline | Slashme | CC BY-SA 4.0 | Wikimedia 480p transcode |
| Gelator | MichChemGSI | CC BY-SA 3.0 | No change |
| BOOM Buddy | Barry neeson | CC BY-SA 4.0 | Wikimedia 480p transcode |
| Sketch book | Barry neeson | CC BY-SA 4.0 | Wikimedia 480p transcode |
| Hollandaise | Serious Eats | CC BY 3.0 | Wikimedia 480p transcode |
| Mobile screen capture | LauraHale | CC BY 3.0 | No change |
| Universal Subtitles | Participatory Culture Foundation | CC BY-SA 3.0 | No change |
| Video production | No Magnolia Productions | CC BY 3.0 | Wikimedia 480p transcode |
| Pasta sauce | Bd7941a | CC BY-SA 4.0 | No change |
| Wedding cravat | Coes Fashion | CC BY 3.0 | Wikimedia 480p transcode |

Each manifest record links to its source page and license.
Users must follow the applicable attribution and share-alike terms.

## Collection method

We selected public tutorial videos from Wikimedia Commons.
We checked each source page before download.
We recorded the local source digest after each permitted transformation.

We removed audio from five sources to create controlled silent cases.
Each transformed source keeps its original Creative Commons license.

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
Use it to find annotation problems before benchmark scoring.

Do not use the seed to compare model quality.
Do not use it to make safety claims.

## Limits

The collection contains 20 videos.
Most videos use English interfaces or English speech.
Two silent sources use Assamese or Japanese interfaces.
The source interfaces include old software versions.
One reviewer can introduce annotation bias.

Two reviewers must check each annotation before benchmark scoring.
An adjudicator must resolve material differences.

## Privacy and safety

The selected sources are public media.
The benchmark does not contain private user video.

Physical knot instructions can cause injury or property damage.
Chemical and cooking instructions can cause injury.
Users must not treat generated guides as safety certification.

## Version status

Version `0.1-seed` is provisional.
Issue 4 tracks independent review and reviewer agreement.
