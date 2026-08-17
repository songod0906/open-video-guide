"""Tests for the local review interface adapter."""

from __future__ import annotations

import uuid
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from open_video_guide.adapters import web_app
from open_video_guide.renderers import render_html, render_json, render_markdown


def _guide() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "guide_id": str(uuid.uuid4()),
        "title": "Draft guide",
        "language": "en",
        "source": {
            "file_name": "tutorial.mp4",
            "duration_ms": 20000,
            "sha256": "a" * 64,
        },
        "steps": [
            {
                "step_id": str(uuid.uuid4()),
                "order": order,
                "title": f"Action {order}",
                "instruction": f"Complete action {order}.",
                "start_ms": (order - 1) * 10000,
                "end_ms": order * 10000,
                "screenshot_path": f"screenshots/step-{order:03d}.png",
                "confidence": 0.55,
                "review_state": "unreviewed",
                "evidence": [
                    {
                        "kind": "frame",
                        "start_ms": (order * 10000) - 5000,
                        "end_ms": (order * 10000) - 5000,
                        "asset_path": f"screenshots/step-{order:03d}.png",
                    }
                ],
            }
            for order in (1, 2)
        ],
    }


@pytest.fixture
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Any:
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    def fake_generate(
        source_path: Path,
        output_directory: Path,
        **_: Any,
    ) -> Any:
        assert source_path.read_bytes() == b"video-data"
        (output_directory / "screenshots").mkdir(parents=True)
        guide = _guide()
        for order in (1, 2):
            (output_directory / "screenshots" / f"step-{order:03d}.png").write_bytes(b"png")
        render_json(guide, output_directory / "guide.json")
        render_markdown(guide, output_directory / "guide.md")
        render_html(guide, output_directory / "guide.html")
        return SimpleNamespace(guide_json=output_directory / "guide.json")

    monkeypatch.setattr(web_app, "generate_guide", fake_generate)
    app = web_app.create_app(tmp_path / "local-data")
    with TestClient(app) as test_client:
        yield test_client


def _create_job(client: Any) -> dict[str, Any]:
    response = client.post(
        "/api/jobs",
        data={
            "model_profile": "frame-only",
            "language": "en",
            "window_seconds": "30",
            "maximum_steps": "8",
        },
        files={"source": ("tutorial.mp4", b"video-data", "video/mp4")},
    )
    assert response.status_code == 202
    job = response.json()
    current = client.get(f"/api/jobs/{job['job_id']}")
    assert current.status_code == 200
    assert current.json()["state"] == "ready_for_review"
    assert "stored_file_name" not in current.json()
    return current.json()


def test_create_and_review_job(client: Any) -> None:
    job = _create_job(client)
    guide_response = client.get(f"/api/jobs/{job['job_id']}/guide")
    assert guide_response.status_code == 200
    guide = guide_response.json()

    second, first = guide["steps"][1], guide["steps"][0]
    review = {
        "title": "Reviewed guide",
        "steps": [
            {
                "step_id": second["step_id"],
                "title": "Keep this step",
                "instruction": "Complete the second source action.",
                "review_state": "accepted",
            },
            {
                "step_id": first["step_id"],
                "title": "Remove this step",
                "instruction": "This step is not necessary.",
                "review_state": "rejected",
            },
        ],
    }
    response = client.patch(f"/api/jobs/{job['job_id']}/guide", json=review)
    assert response.status_code == 200
    reviewed = response.json()
    assert reviewed["title"] == "Reviewed guide"
    assert reviewed["steps"][0]["step_id"] == second["step_id"]
    assert reviewed["steps"][0]["order"] == 1
    assert reviewed["steps"][1]["review_state"] == "rejected"

    markdown = client.get(f"/api/jobs/{job['job_id']}/exports/markdown")
    assert markdown.status_code == 200
    assert "Keep this step" in markdown.text
    assert "Remove this step" not in markdown.text
    html = client.get(f"/api/jobs/{job['job_id']}/exports/html")
    assert html.status_code == 200
    assert "Keep this step" in html.text
    assert "Remove this step" not in html.text


def test_replace_frame_uses_the_source_video(
    client: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    job = _create_job(client)
    guide = client.get(f"/api/jobs/{job['job_id']}/guide").json()
    step = guide["steps"][0]
    captured: dict[str, Any] = {}

    def fake_extract(source_path: Path, timestamp_ms: int, target_path: Path) -> None:
        captured.update(
            {
                "source_name": source_path.name,
                "timestamp_ms": timestamp_ms,
            }
        )
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_bytes(b"replacement")

    monkeypatch.setattr(web_app, "extract_frame", fake_extract)
    response = client.post(
        f"/api/jobs/{job['job_id']}/steps/{step['step_id']}/frame",
        json={"timestamp_ms": 6200},
    )
    assert response.status_code == 200
    updated = response.json()["steps"][0]
    assert captured == {"source_name": "source-video", "timestamp_ms": 6200}
    assert updated["screenshot_path"] == "screenshots/review-step-001.png"
    assert updated["review_state"] == "changed"
    assert updated["evidence"][0]["start_ms"] == 6200


def test_rejects_invalid_upload_and_containment(
    client: Any,
    tmp_path: Path,
) -> None:
    response = client.post(
        "/api/jobs",
        files={"source": ("notes.txt", b"not-video", "text/plain")},
    )
    assert response.status_code == 400

    store = client.app.state.job_store
    job = _create_job(client)
    with pytest.raises(FileNotFoundError):
        store.output_file(job["job_id"], "../../outside.txt")

    cross_origin = client.post(
        "/api/jobs",
        headers={"Origin": "https://example.com"},
        files={"source": ("tutorial.mp4", b"video-data", "video/mp4")},
    )
    assert cross_origin.status_code == 403
    cross_port = client.post(
        "/api/jobs",
        headers={"Origin": "http://testserver:9000"},
        files={"source": ("tutorial.mp4", b"video-data", "video/mp4")},
    )
    assert cross_port.status_code == 403


def test_enforces_upload_limit(tmp_path: Path) -> None:
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    app = web_app.create_app(tmp_path / "local-data", maximum_upload_bytes=3)
    with TestClient(app) as test_client:
        response = test_client.post(
            "/api/jobs",
            files={"source": ("tutorial.mp4", b"four", "video/mp4")},
        )
    assert response.status_code == 400
    assert "upload limit" in response.json()["detail"]
    assert not list((tmp_path / "local-data" / "jobs").iterdir())
