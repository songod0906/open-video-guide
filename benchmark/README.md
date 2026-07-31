# Benchmark

This directory contains public benchmark records and annotations.
It does not contain source videos.

## Layout

| Path | Purpose |
|---|---|
| `schemas` | Machine-readable benchmark contracts |
| `v0.1-seed` | First provisional benchmark version |
| `raw` | Ignored local source videos |

Read the dataset card before benchmark use.
Read the review status before model scoring.

## Validate records

Run the record checks.

```bash
python scripts/validate_benchmark.py
```

Check local source digests when the source videos are available.

```bash
python scripts/validate_benchmark.py --media-dir benchmark/raw
```

The second command does not download source videos.
See the dataset card for source links and license terms.
