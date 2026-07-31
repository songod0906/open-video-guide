"""Guide output renderers."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


def timestamp(timestamp_ms: int) -> str:
    """Format a video timestamp."""
    total_seconds = timestamp_ms // 1000
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"


def render_json(guide: dict[str, Any], target_path: Path) -> None:
    """Write the structured guide."""
    target_path.write_text(json.dumps(guide, indent=2) + "\n", encoding="utf-8")


def render_markdown(guide: dict[str, Any], target_path: Path) -> None:
    """Write the Markdown guide."""
    lines = [
        f"# {guide['title']}",
        "",
        f"Source: `{guide['source']['file_name']}`",
        "",
        "> Review every step before you use this guide.",
        "",
    ]
    for step in guide["steps"]:
        lines.extend(
            [
                f"## {step['order']}. {step['title']}",
                "",
                f"![Step {step['order']}]({step['screenshot_path']})",
                "",
                step["instruction"],
                "",
                f"Source time: {timestamp(step['start_ms'])}–{timestamp(step['end_ms'])}",
                "",
                f"Confidence: {step['confidence']:.2f}. Review state: {step['review_state']}.",
                "",
            ]
        )
    target_path.write_text("\n".join(lines), encoding="utf-8")


def render_html(guide: dict[str, Any], target_path: Path) -> None:
    """Write the standalone HTML guide."""
    cards = []
    for step in guide["steps"]:
        cards.append(
            "\n".join(
                [
                    '<article class="step">',
                    f"<h2>{step['order']}. {html.escape(step['title'])}</h2>",
                    (
                        f'<img src="{html.escape(step["screenshot_path"])}" '
                        f'alt="Evidence for step {step["order"]}">'
                    ),
                    f"<p>{html.escape(step['instruction'])}</p>",
                    (
                        f"<small>Source time: {timestamp(step['start_ms'])}–"
                        f"{timestamp(step['end_ms'])}. "
                        f"Confidence: {step['confidence']:.2f}.</small>"
                    ),
                    "</article>",
                ]
            )
        )
    document = f"""<!doctype html>
<html lang="{html.escape(guide.get("language", "en"))}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(guide["title"])}</title>
  <style>
    body {{ font: 17px/1.55 system-ui, sans-serif; margin: 0 auto; }}
    body {{ max-width: 900px; padding: 2rem; }}
    .notice {{ background: #fff4cc; border-left: 5px solid #e3aa00; padding: 1rem; }}
    .step {{ border-top: 1px solid #ddd; margin-top: 2rem; padding-top: 1rem; }}
    img {{ border: 1px solid #ddd; border-radius: 8px; height: auto; max-width: 100%; }}
    small {{ color: #555; }}
  </style>
</head>
<body>
  <h1>{html.escape(guide["title"])}</h1>
  <p class="notice">Review every step before you use this guide.</p>
  {"".join(cards)}
</body>
</html>
"""
    target_path.write_text(document, encoding="utf-8")
