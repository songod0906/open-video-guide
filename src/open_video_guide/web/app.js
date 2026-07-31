const state = {
  currentJob: null,
  guide: null,
  pollTimer: null,
};

const elements = {
  startView: document.querySelector("#start-view"),
  progressView: document.querySelector("#progress-view"),
  reviewView: document.querySelector("#review-view"),
  uploadForm: document.querySelector("#upload-form"),
  sourceInput: document.querySelector("#source-input"),
  dropZone: document.querySelector("#drop-zone"),
  fileChoice: document.querySelector("#file-choice"),
  createButton: document.querySelector("#create-button"),
  uploadError: document.querySelector("#upload-error"),
  recentJobs: document.querySelector("#recent-jobs"),
  progressTitle: document.querySelector("#progress-title"),
  progressMessage: document.querySelector("#progress-message"),
  progressError: document.querySelector("#progress-error"),
  backButton: document.querySelector("#back-button"),
  saveButton: document.querySelector("#save-button"),
  saveStatus: document.querySelector("#save-status"),
  exportButton: document.querySelector("#export-button"),
  exportOptions: document.querySelector("#export-options"),
  guideTitle: document.querySelector("#guide-title"),
  reviewSummary: document.querySelector("#review-summary"),
  sourceVideo: document.querySelector("#source-video"),
  sourceName: document.querySelector("#source-name"),
  sourceDuration: document.querySelector("#source-duration"),
  stepList: document.querySelector("#step-list"),
  reviewError: document.querySelector("#review-error"),
  stepTemplate: document.querySelector("#step-template"),
};

function showView(name) {
  elements.startView.hidden = name !== "start";
  elements.progressView.hidden = name !== "progress";
  elements.reviewView.hidden = name !== "review";
}

function formatTime(milliseconds) {
  const total = Math.max(0, Math.floor(milliseconds / 1000));
  const hours = Math.floor(total / 3600);
  const minutes = Math.floor((total % 3600) / 60);
  const seconds = total % 60;
  const pair = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
  return hours ? `${String(hours).padStart(2, "0")}:${pair}` : pair;
}

function formatState(value) {
  return value.replaceAll("_", " ");
}

async function request(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    let message = `The request failed with status ${response.status}.`;
    try {
      const body = await response.json();
      message = body.detail || message;
    } catch {
      // Keep the status message.
    }
    throw new Error(message);
  }
  return response.json();
}

function setSelectedFile(file) {
  if (!file) {
    elements.fileChoice.hidden = true;
    elements.fileChoice.textContent = "";
    return;
  }
  elements.fileChoice.textContent = `${file.name} · ${(file.size / 1048576).toFixed(1)} MB`;
  elements.fileChoice.hidden = false;
}

function setInputFile(file) {
  const transfer = new DataTransfer();
  transfer.items.add(file);
  elements.sourceInput.files = transfer.files;
  setSelectedFile(file);
}

async function loadRecentJobs() {
  try {
    const result = await request("/api/jobs");
    elements.recentJobs.replaceChildren();
    if (!result.jobs.length) {
      const message = document.createElement("p");
      message.className = "empty-state";
      message.textContent = "No local jobs yet.";
      elements.recentJobs.append(message);
      return;
    }
    result.jobs.forEach((job) => {
      const row = document.createElement("button");
      row.type = "button";
      row.className = "job-row";
      row.innerHTML = `
        <strong></strong>
        <span class="job-state"></span>
        <span></span>
      `;
      row.querySelector("strong").textContent = job.source_file_name;
      row.querySelector(".job-state").textContent = formatState(job.state);
      row.querySelector("span:last-child").textContent =
        new Date(job.updated_at).toLocaleString();
      row.addEventListener("click", () => openJob(job.job_id));
      elements.recentJobs.append(row);
    });
  } catch (error) {
    elements.recentJobs.textContent = error.message;
  }
}

async function openJob(jobId) {
  clearTimeout(state.pollTimer);
  try {
    const job = await request(`/api/jobs/${jobId}`);
    state.currentJob = job;
    if (job.state === "ready_for_review") {
      await openReview(job);
      return;
    }
    showProgress(job);
  } catch (error) {
    showView("start");
    elements.uploadError.textContent = error.message;
  }
}

function showProgress(job) {
  showView("progress");
  elements.progressError.textContent = "";
  elements.progressTitle.textContent =
    job.state === "failed" ? "The draft could not finish" : "Creating your draft guide";
  elements.progressMessage.textContent =
    job.state === "queued" ? "Your job is waiting to start." : "The source video stays here.";
  if (job.state === "failed") {
    elements.progressError.textContent = job.error || "The local pipeline failed.";
    return;
  }
  state.pollTimer = setTimeout(() => openJob(job.job_id), 1100);
}

async function openReview(job) {
  const guide = await request(`/api/jobs/${job.job_id}/guide`);
  state.currentJob = job;
  state.guide = guide;
  elements.guideTitle.value = guide.title;
  elements.sourceName.textContent = guide.source.file_name;
  elements.sourceDuration.textContent = formatTime(guide.source.duration_ms);
  elements.sourceVideo.src = `/api/jobs/${job.job_id}/source`;
  elements.reviewError.textContent = "";
  renderSteps();
  showView("review");
}

function markChanged(step) {
  if (step.review_state === "unreviewed" || step.review_state === "accepted") {
    step.review_state = "changed";
  }
  elements.saveStatus.textContent = "Unsaved changes";
}

function setStepState(step, reviewState) {
  step.review_state = reviewState;
  elements.saveStatus.textContent = "Unsaved changes";
  renderSteps();
}

function seekTo(milliseconds) {
  elements.sourceVideo.currentTime = milliseconds / 1000;
  elements.sourceVideo.play().catch(() => {});
}

function moveStep(index, direction) {
  const target = index + direction;
  if (target < 0 || target >= state.guide.steps.length) {
    return;
  }
  const [step] = state.guide.steps.splice(index, 1);
  state.guide.steps.splice(target, 0, step);
  markChanged(step);
  renderSteps();
}

function reviewCount() {
  return state.guide.steps.filter((step) =>
    ["accepted", "changed", "rejected"].includes(step.review_state)
  ).length;
}

function renderSteps() {
  elements.stepList.replaceChildren();
  state.guide.steps.forEach((step, index) => {
    const fragment = elements.stepTemplate.content.cloneNode(true);
    const card = fragment.querySelector(".step-card");
    const image = fragment.querySelector(".step-image");
    const title = fragment.querySelector(".step-title");
    const instruction = fragment.querySelector(".step-instruction");
    const frameRange = fragment.querySelector(".frame-range");
    const frameTime = fragment.querySelector(".frame-time");
    const currentFrame = step.evidence.find((item) => item.kind === "frame");
    const currentTime = currentFrame ? currentFrame.start_ms : step.start_ms;

    card.dataset.stepId = step.step_id;
    card.classList.toggle("rejected", step.review_state === "rejected");
    fragment.querySelector(".step-number").textContent = `Step ${index + 1}`;
    image.src = `/api/jobs/${state.currentJob.job_id}/artifacts/${step.screenshot_path}?v=${state.currentJob.revision}`;
    image.alt = `Source frame for step ${index + 1}`;
    fragment.querySelector(".time-label").textContent =
      `${formatTime(step.start_ms)}–${formatTime(step.end_ms)}`;
    title.value = step.title;
    instruction.value = step.instruction;
    fragment.querySelector(".confidence").textContent =
      `${Math.round(step.confidence * 100)}% draft confidence`;
    frameRange.min = step.start_ms;
    frameRange.max = Math.max(step.start_ms, step.end_ms - 1);
    frameRange.value = Math.min(Math.max(currentTime, step.start_ms), step.end_ms - 1);
    frameTime.value = formatTime(Number(frameRange.value));

    fragment.querySelector(".move-up").disabled = index === 0;
    fragment.querySelector(".move-down").disabled = index === state.guide.steps.length - 1;
    fragment.querySelector(".move-up").addEventListener("click", () => moveStep(index, -1));
    fragment.querySelector(".move-down").addEventListener("click", () => moveStep(index, 1));
    fragment.querySelector(".frame-button").addEventListener("click", () => {
      document.querySelectorAll(".step-card").forEach((item) => item.classList.remove("selected"));
      card.classList.add("selected");
      seekTo(currentTime);
    });
    title.addEventListener("input", () => {
      step.title = title.value;
      markChanged(step);
      updateStateButtons(card, step);
    });
    instruction.addEventListener("input", () => {
      step.instruction = instruction.value;
      markChanged(step);
      updateStateButtons(card, step);
    });
    frameRange.addEventListener("input", () => {
      frameTime.value = formatTime(Number(frameRange.value));
      elements.sourceVideo.currentTime = Number(frameRange.value) / 1000;
    });
    fragment.querySelector(".capture-button").addEventListener("click", () => {
      replaceFrame(step, Number(frameRange.value));
    });
    fragment.querySelectorAll(".review-state button").forEach((button) => {
      button.addEventListener("click", () => setStepState(step, button.dataset.state));
    });
    updateStateButtons(card, step);
    elements.stepList.append(fragment);
  });
  elements.reviewSummary.textContent =
    `${reviewCount()} of ${state.guide.steps.length} steps reviewed`;
}

function updateStateButtons(card, step) {
  card.classList.toggle("rejected", step.review_state === "rejected");
  card.querySelectorAll(".review-state button").forEach((button) => {
    button.classList.toggle("active", button.dataset.state === step.review_state);
    button.setAttribute("aria-pressed", button.dataset.state === step.review_state);
  });
}

async function replaceFrame(step, timestampMs) {
  elements.reviewError.textContent = "";
  try {
    const updatedGuide = await request(
      `/api/jobs/${state.currentJob.job_id}/steps/${step.step_id}/frame`,
      {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({timestamp_ms: timestampMs}),
      }
    );
    const updatedStep = updatedGuide.steps.find((item) => item.step_id === step.step_id);
    step.screenshot_path = updatedStep.screenshot_path;
    step.evidence = updatedStep.evidence;
    step.review_state = "changed";
    state.currentJob.revision += 1;
    elements.saveStatus.textContent = "Frame saved";
    renderSteps();
  } catch (error) {
    elements.reviewError.textContent = error.message;
  }
}

async function saveGuide() {
  elements.reviewError.textContent = "";
  elements.saveButton.disabled = true;
  const review = {
    title: elements.guideTitle.value,
    steps: state.guide.steps.map((step) => ({
      step_id: step.step_id,
      title: step.title,
      instruction: step.instruction,
      review_state: step.review_state,
    })),
  };
  try {
    state.guide = await request(`/api/jobs/${state.currentJob.job_id}/guide`, {
      method: "PATCH",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(review),
    });
    state.currentJob.revision += 1;
    elements.saveStatus.textContent = "Saved locally";
    renderSteps();
  } catch (error) {
    elements.reviewError.textContent = error.message;
  } finally {
    elements.saveButton.disabled = false;
  }
}

elements.sourceInput.addEventListener("change", () => {
  setSelectedFile(elements.sourceInput.files[0]);
});

["dragenter", "dragover"].forEach((eventName) => {
  elements.dropZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    elements.dropZone.classList.add("dragging");
  });
});

["dragleave", "drop"].forEach((eventName) => {
  elements.dropZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    elements.dropZone.classList.remove("dragging");
  });
});

elements.dropZone.addEventListener("drop", (event) => {
  const file = event.dataTransfer.files[0];
  if (file) {
    setInputFile(file);
  }
});

elements.uploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  elements.uploadError.textContent = "";
  if (!elements.sourceInput.files.length) {
    elements.uploadError.textContent = "Select one source video.";
    return;
  }
  elements.createButton.disabled = true;
  const form = new FormData(elements.uploadForm);
  form.set("language", "en");
  try {
    const job = await request("/api/jobs", {method: "POST", body: form});
    state.currentJob = job;
    showProgress(job);
  } catch (error) {
    elements.uploadError.textContent = error.message;
  } finally {
    elements.createButton.disabled = false;
  }
});

elements.backButton.addEventListener("click", () => {
  state.currentJob = null;
  state.guide = null;
  elements.sourceVideo.pause();
  elements.sourceVideo.removeAttribute("src");
  elements.sourceVideo.load();
  showView("start");
  loadRecentJobs();
});

elements.saveButton.addEventListener("click", saveGuide);
elements.guideTitle.addEventListener("input", () => {
  elements.saveStatus.textContent = "Unsaved changes";
});

elements.exportButton.addEventListener("click", () => {
  const willOpen = elements.exportOptions.hidden;
  elements.exportOptions.hidden = !willOpen;
  elements.exportButton.setAttribute("aria-expanded", willOpen);
});

elements.exportOptions.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    link.href =
      `/api/jobs/${state.currentJob.job_id}/exports/${link.dataset.format}`;
    elements.exportOptions.hidden = true;
    elements.exportButton.setAttribute("aria-expanded", "false");
  });
});

loadRecentJobs();
