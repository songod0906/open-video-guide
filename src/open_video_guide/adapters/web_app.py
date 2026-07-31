"""Local review interface adapter."""

import json
import os
import re
import threading
import uuid
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, Any
from urllib.parse import urlsplit

from open_video_guide.contracts import load_guide, repository_root, validation_errors
from open_video_guide.media import extract_frame
from open_video_guide.pipeline import SUPPORTED_PROFILES, generate_guide
from open_video_guide.renderers import render_html, render_json, render_markdown

ALLOWED_VIDEO_SUFFIXES = {".avi", ".mkv", ".mov", ".mp4", ".ogv", ".webm"}
DEFAULT_MAXIMUM_UPLOAD_BYTES = 4 * 1024 * 1024 * 1024
JOB_ID_PATTERN = re.compile(r"^[0-9a-f-]{36}$")
REVIEW_STATES = {"accepted", "changed", "rejected", "unreviewed"}


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _safe_file_name(file_name: str) -> str:
    name = Path(file_name).name
    if not name or name in {".", ".."}:
        raise ValueError("The source file name is invalid.")
    if Path(name).suffix.lower() not in ALLOWED_VIDEO_SUFFIXES:
        raise ValueError("The source file type is not supported.")
    return name


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    temporary_path = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    temporary_path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temporary_path.replace(path)


class JobStore:
    """Store local review jobs and their artifacts."""

    def __init__(self, root: Path, maximum_upload_bytes: int) -> None:
        self.root = root.expanduser().resolve()
        self.jobs_root = self.root / "jobs"
        self.maximum_upload_bytes = maximum_upload_bytes
        self._lock = threading.RLock()
        self.jobs_root.mkdir(parents=True, exist_ok=True)

    def job_directory(self, job_id: str) -> Path:
        """Return one validated job directory."""
        try:
            canonical_id = str(uuid.UUID(job_id))
        except ValueError as error:
            raise KeyError("The job identifier is invalid.") from error
        if canonical_id != job_id or not JOB_ID_PATTERN.fullmatch(job_id):
            raise KeyError("The job identifier is invalid.")
        path = (self.jobs_root / canonical_id).resolve()
        if not path.is_relative_to(self.jobs_root):
            raise KeyError("The job identifier is invalid.")
        return path

    def read_job(self, job_id: str) -> dict[str, Any]:
        """Read one job record."""
        path = self.job_directory(job_id) / "job.json"
        if not path.is_file() or path.is_symlink():
            raise KeyError("The job does not exist.")
        return json.loads(path.read_text(encoding="utf-8"))

    def write_job(self, job: dict[str, Any]) -> None:
        """Write one job record."""
        with self._lock:
            job["updated_at"] = _now()
            path = self.job_directory(job["job_id"]) / "job.json"
            _atomic_json(path, job)

    def public_job(self, job: dict[str, Any]) -> dict[str, Any]:
        """Return a job without internal paths."""
        return {
            key: value
            for key, value in job.items()
            if key not in {"stored_file_name"}
        }

    def list_jobs(self) -> list[dict[str, Any]]:
        """Return recent jobs."""
        jobs: list[dict[str, Any]] = []
        for job_path in self.jobs_root.glob("*/job.json"):
            if job_path.is_symlink():
                continue
            try:
                job = json.loads(job_path.read_text(encoding="utf-8"))
                self.job_directory(job["job_id"])
            except (KeyError, ValueError, json.JSONDecodeError):
                continue
            jobs.append(self.public_job(job))
        return sorted(jobs, key=lambda item: item["created_at"], reverse=True)[:25]

    async def create_job(
        self,
        upload: Any,
        *,
        model_profile: str,
        language: str,
        window_seconds: int,
        maximum_steps: int,
    ) -> dict[str, Any]:
        """Store one source video and create its job."""
        file_name = _safe_file_name(upload.filename or "")
        if model_profile not in SUPPORTED_PROFILES:
            raise ValueError("The model profile is not supported.")
        if not 10 <= window_seconds <= 120:
            raise ValueError("The window length must be from 10 through 120 seconds.")
        if not 1 <= maximum_steps <= 30:
            raise ValueError("The maximum step count must be from 1 through 30.")
        if not 2 <= len(language) <= 12:
            raise ValueError("The language code is invalid.")

        job_id = str(uuid.uuid4())
        job_directory = self.job_directory(job_id)
        source_directory = job_directory / "source"
        source_directory.mkdir(parents=True)
        source_path = source_directory / file_name
        byte_count = 0
        try:
            with source_path.open("xb") as target:
                while chunk := await upload.read(1024 * 1024):
                    byte_count += len(chunk)
                    if byte_count > self.maximum_upload_bytes:
                        raise ValueError("The source video exceeds the upload limit.")
                    target.write(chunk)
        except Exception:
            source_path.unlink(missing_ok=True)
            source_directory.rmdir()
            job_directory.rmdir()
            raise
        finally:
            await upload.close()

        timestamp = _now()
        job = {
            "job_id": job_id,
            "state": "queued",
            "source_file_name": file_name,
            "stored_file_name": file_name,
            "source_size_bytes": byte_count,
            "model_profile": model_profile,
            "language": language,
            "window_seconds": window_seconds,
            "maximum_steps": maximum_steps,
            "revision": 0,
            "created_at": timestamp,
            "updated_at": timestamp,
            "error": None,
        }
        _atomic_json(job_directory / "job.json", job)
        return job

    def run_job(self, job_id: str) -> None:
        """Run one queued job."""
        job = self.read_job(job_id)
        job["state"] = "analyzing"
        job["error"] = None
        self.write_job(job)
        job_directory = self.job_directory(job_id)
        source_path = self.source_path(job_id)
        output_directory = job_directory / "output"
        try:
            generate_guide(
                source_path,
                output_directory,
                profile=job["model_profile"],
                language=job["language"],
                window_seconds=job["window_seconds"],
                maximum_steps=job["maximum_steps"],
            )
        except Exception as error:
            job["state"] = "failed"
            job["error"] = str(error)[:1000]
        else:
            job["state"] = "ready_for_review"
        self.write_job(job)

    def guide_path(self, job_id: str) -> Path:
        """Return the guide path for a completed job."""
        job = self.read_job(job_id)
        if job["state"] != "ready_for_review":
            raise RuntimeError("The guide is not ready for review.")
        path = self.job_directory(job_id) / "output" / "guide.json"
        if not path.is_file() or path.is_symlink():
            raise FileNotFoundError("The guide file does not exist.")
        return path

    def source_path(self, job_id: str) -> Path:
        """Return the source path for one job."""
        job = self.read_job(job_id)
        source_directory = (self.job_directory(job_id) / "source").resolve()
        path = (source_directory / job["stored_file_name"]).resolve()
        if not path.is_relative_to(source_directory):
            raise FileNotFoundError("The source path is invalid.")
        if not path.is_file() or path.is_symlink():
            raise FileNotFoundError("The source video does not exist.")
        return path

    def output_file(self, job_id: str, relative_path: str) -> Path:
        """Return one contained output file."""
        output_directory = (self.job_directory(job_id) / "output").resolve()
        path = (output_directory / relative_path).resolve()
        if not path.is_relative_to(output_directory):
            raise FileNotFoundError("The artifact path is invalid.")
        if not path.is_file() or path.is_symlink():
            raise FileNotFoundError("The artifact does not exist.")
        return path

    def update_guide(self, job_id: str, review: dict[str, Any]) -> dict[str, Any]:
        """Apply one complete guide review."""
        with self._lock:
            path = self.guide_path(job_id)
            guide = load_guide(path)
            title = str(review.get("title", "")).strip()
            if not title:
                raise ValueError("The guide title is required.")
            submitted_steps = review.get("steps")
            if not isinstance(submitted_steps, list):
                raise ValueError("The review steps are required.")

            original_by_id = {step["step_id"]: step for step in guide["steps"]}
            if not all(isinstance(step, dict) for step in submitted_steps):
                raise ValueError("Each review step must be an object.")
            submitted_ids = [str(step.get("step_id", "")) for step in submitted_steps]
            if len(submitted_ids) != len(set(submitted_ids)):
                raise ValueError("Each step must occur one time.")
            if set(submitted_ids) != set(original_by_id):
                raise ValueError("The review must contain every original step.")

            updated_steps: list[dict[str, Any]] = []
            for order, submitted in enumerate(submitted_steps, start=1):
                original = deepcopy(original_by_id[submitted["step_id"]])
                step_title = str(submitted.get("title", "")).strip()
                instruction = str(submitted.get("instruction", "")).strip()
                review_state = str(submitted.get("review_state", ""))
                if not step_title or not instruction:
                    raise ValueError("Each step needs a title and an instruction.")
                if review_state not in REVIEW_STATES:
                    raise ValueError("A step has an invalid review state.")
                original.update(
                    {
                        "order": order,
                        "title": step_title,
                        "instruction": instruction,
                        "review_state": review_state,
                    }
                )
                updated_steps.append(original)

            guide["title"] = title
            guide["steps"] = updated_steps
            errors = validation_errors(guide)
            if errors:
                raise ValueError("The reviewed guide is invalid: " + "; ".join(errors))
            self._write_exports(job_id, guide)
            job = self.read_job(job_id)
            job["revision"] += 1
            self.write_job(job)
            return guide

    def replace_step_frame(
        self,
        job_id: str,
        step_id: str,
        timestamp_ms: int,
    ) -> dict[str, Any]:
        """Replace one screenshot with another source frame."""
        with self._lock:
            path = self.guide_path(job_id)
            guide = load_guide(path)
            if not 0 <= timestamp_ms < guide["source"]["duration_ms"]:
                raise ValueError("The frame time is outside the source video.")
            step = next((item for item in guide["steps"] if item["step_id"] == step_id), None)
            if step is None:
                raise KeyError("The step does not exist.")
            relative_path = Path("screenshots") / f"review-{step_id}.png"
            target_path = self.job_directory(job_id) / "output" / relative_path
            extract_frame(self.source_path(job_id), timestamp_ms, target_path)
            step["screenshot_path"] = relative_path.as_posix()
            frame_evidence = next(
                (item for item in step["evidence"] if item["kind"] == "frame"),
                None,
            )
            if frame_evidence is None:
                step["evidence"].insert(
                    0,
                    {
                        "kind": "frame",
                        "start_ms": timestamp_ms,
                        "end_ms": timestamp_ms,
                        "asset_path": relative_path.as_posix(),
                    },
                )
            else:
                frame_evidence.update(
                    {
                        "start_ms": timestamp_ms,
                        "end_ms": timestamp_ms,
                        "asset_path": relative_path.as_posix(),
                    }
                )
            if step["review_state"] == "unreviewed":
                step["review_state"] = "changed"
            self._write_exports(job_id, guide)
            job = self.read_job(job_id)
            job["revision"] += 1
            self.write_job(job)
            return guide

    def _write_exports(self, job_id: str, guide: dict[str, Any]) -> None:
        output_directory = self.job_directory(job_id) / "output"
        render_json(guide, output_directory / "guide.json")
        render_markdown(guide, output_directory / "guide.md")
        render_html(guide, output_directory / "guide.html")


def create_app(
    data_root: Path | None = None,
    *,
    maximum_upload_bytes: int = DEFAULT_MAXIMUM_UPLOAD_BYTES,
) -> Any:
    """Create the local review application."""
    try:
        from fastapi import (
            BackgroundTasks,
            FastAPI,
            File,
            Form,
            HTTPException,
            Request,
            UploadFile,
        )
        from fastapi.responses import FileResponse, JSONResponse
        from starlette.middleware.trustedhost import TrustedHostMiddleware
    except ImportError as error:
        raise RuntimeError('Install the web extra with: pip install -e ".[web]"') from error

    configured_root = os.environ.get("OVG_WEB_DATA_ROOT")
    resolved_root = data_root or (
        Path(configured_root) if configured_root else repository_root() / ".ovg-data"
    )
    store = JobStore(resolved_root, maximum_upload_bytes)
    web_directory = Path(__file__).resolve().parents[1] / "web"
    app = FastAPI(title="Open Video Guide", docs_url=None, redoc_url=None)
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["127.0.0.1", "localhost", "testserver"],
    )
    app.state.job_store = store

    @app.middleware("http")
    async def restrict_write_origins(request: Request, call_next: Any) -> Any:
        if request.method in {"DELETE", "PATCH", "POST", "PUT"}:
            origin = request.headers.get("origin")
            if origin:
                parsed_origin = urlsplit(origin)
                origin_port = parsed_origin.port or 80
                request_port = request.url.port or 80
                permitted = (
                    parsed_origin.scheme == "http"
                    and parsed_origin.hostname == request.url.hostname
                    and origin_port == request_port
                )
                if not permitted:
                    return JSONResponse(
                        status_code=403,
                        content={"detail": "The request origin is not permitted."},
                    )
        return await call_next(request)

    def job_or_404(job_id: str) -> dict[str, Any]:
        try:
            return store.read_job(job_id)
        except KeyError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error

    @app.get("/")
    def index() -> Any:
        return FileResponse(web_directory / "index.html", media_type="text/html")

    @app.get("/assets/{file_name}")
    def interface_asset(file_name: str) -> Any:
        if file_name not in {"app.js", "styles.css"}:
            raise HTTPException(status_code=404, detail="The interface asset does not exist.")
        media_type = "text/javascript" if file_name.endswith(".js") else "text/css"
        return FileResponse(web_directory / file_name, media_type=media_type)

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"state": "ready"}

    @app.get("/api/jobs")
    def list_jobs() -> dict[str, list[dict[str, Any]]]:
        return {"jobs": store.list_jobs()}

    @app.post("/api/jobs", status_code=202)
    async def create_job(
        background_tasks: BackgroundTasks,
        source: Annotated[UploadFile, File()],
        model_profile: Annotated[str, Form()] = "frame-only",
        language: Annotated[str, Form()] = "en",
        window_seconds: Annotated[int, Form()] = 30,
        maximum_steps: Annotated[int, Form()] = 8,
    ) -> dict[str, Any]:
        try:
            job = await store.create_job(
                source,
                model_profile=model_profile,
                language=language,
                window_seconds=window_seconds,
                maximum_steps=maximum_steps,
            )
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error
        background_tasks.add_task(store.run_job, job["job_id"])
        return store.public_job(job)

    @app.get("/api/jobs/{job_id}")
    def get_job(job_id: str) -> dict[str, Any]:
        return store.public_job(job_or_404(job_id))

    @app.get("/api/jobs/{job_id}/guide")
    def get_guide(job_id: str) -> dict[str, Any]:
        job_or_404(job_id)
        try:
            return load_guide(store.guide_path(job_id))
        except RuntimeError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error
        except FileNotFoundError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error

    @app.patch("/api/jobs/{job_id}/guide")
    def update_guide(job_id: str, review: dict[str, Any]) -> dict[str, Any]:
        job_or_404(job_id)
        try:
            return store.update_guide(job_id, review)
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error
        except RuntimeError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @app.post("/api/jobs/{job_id}/steps/{step_id}/frame")
    def replace_frame(job_id: str, step_id: str, selection: dict[str, Any]) -> dict[str, Any]:
        job_or_404(job_id)
        try:
            timestamp_ms = int(selection.get("timestamp_ms", -1))
            return store.replace_step_frame(job_id, step_id, timestamp_ms)
        except (TypeError, ValueError) as error:
            raise HTTPException(status_code=400, detail=str(error)) from error
        except KeyError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        except RuntimeError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @app.get("/api/jobs/{job_id}/source")
    def source_video(job_id: str) -> Any:
        job_or_404(job_id)
        try:
            return FileResponse(store.source_path(job_id), filename=None)
        except FileNotFoundError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error

    @app.get("/api/jobs/{job_id}/artifacts/{relative_path:path}")
    def artifact(job_id: str, relative_path: str) -> Any:
        job_or_404(job_id)
        try:
            return FileResponse(store.output_file(job_id, relative_path))
        except FileNotFoundError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error

    @app.get("/api/jobs/{job_id}/exports/{export_format}")
    def export(job_id: str, export_format: str) -> Any:
        job_or_404(job_id)
        formats = {
            "html": ("guide.html", "text/html"),
            "json": ("guide.json", "application/json"),
            "markdown": ("guide.md", "text/markdown"),
        }
        if export_format not in formats:
            raise HTTPException(status_code=404, detail="The export format is not supported.")
        file_name, media_type = formats[export_format]
        try:
            path = store.output_file(job_id, file_name)
        except FileNotFoundError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        return FileResponse(path, media_type=media_type, filename=file_name)

    return app


def main() -> None:
    """Run the local review application."""
    try:
        import uvicorn
    except ImportError as error:
        raise RuntimeError('Install the web extra with: pip install -e ".[web]"') from error

    port = int(os.environ.get("OVG_WEB_PORT", "8765"))
    uvicorn.run(create_app(), host="127.0.0.1", port=port)
