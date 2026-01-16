const BACKEND_URL = "http://127.0.0.1:5000";
let lastInstruction = "";

/* =======================
   ✅ STATE PERSISTENCE
======================= */
function saveLastResult(data) {
  localStorage.setItem("lastTestResult", JSON.stringify(data));
}

function loadLastResult() {
  const saved = localStorage.getItem("lastTestResult");
  if (!saved) return null;
  return JSON.parse(saved);
}

/* =======================
   RUN TEST
======================= */
function runTest(instructionOverride = null) {
  const instruction =
    instructionOverride ||
    document.getElementById("instruction").value.trim();

  if (!instruction) return;

  lastInstruction = instruction;
  updateWizard(0);

  fetch(`${BACKEND_URL}/test`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ instruction })
  })
    .then(r => r.json())
    .then(d => {

      // ✅ SAVE RESULT
      saveLastResult(d);

      renderResult(d);
    })
    .catch(() => {
      const box = document.getElementById("result");
      box.innerText = "Backend not reachable";
      box.className = "result-box error";
    });
}

/* =======================
   RENDER RESULT (NEW)
======================= */
function renderResult(d) {
  updateWizard(1);

  const box = document.getElementById("result");

  let extraInfo = "";
  if (d.execution_time !== undefined) {
    extraInfo += `\nExecution Time: ${d.execution_time}s`;
  }
  if (d.failure_reason) {
    extraInfo += `\nFailure Reason: ${d.failure_reason}`;
  }

  box.innerText =
    (d.status === "PASSED"
      ? "Test executed successfully"
      : "Test failed") + extraInfo;

  box.className =
    "result-box " + (d.status === "PASSED" ? "success" : "error");

  /* ---------- STATS ---------- */
  document.getElementById("total").innerText = d.stats.total;
  document.getElementById("passed").innerText = d.stats.passed;
  document.getElementById("failed").innerText = d.stats.failed;

  updateWizard(2);

  /* ---------- SCREENSHOT ---------- */
  const img = document.getElementById("screenshot");
  const dl = document.getElementById("downloadShot");

  if (d.screenshot) {
    const src = `${BACKEND_URL}/screenshots/${d.screenshot}?t=${Date.now()}`;
    img.src = src;
    dl.href = src;
    dl.download=d.screenshot;
    dl.style.display = "inline-block";
  } else {
    img.src = "";
    dl.style.display = "none";
  }

  /* ---------- VIDEO ---------- */
  const video = document.getElementById("video");
  const dlVideo = document.getElementById("downloadVideo");

  if (d.video) {
    const videoSrc = `${BACKEND_URL}/videos/${d.video}?t=${Date.now()}`;
    video.src = videoSrc;
    video.load();
    video.style.display = "block";
    dlVideo.href = videoSrc;
    dlVideo.style.display = "inline-block";
  } else {
    video.style.display = "none";
    dlVideo.style.display = "none";
  }

  updateWizard(3);
  loadHistory();
}

/* =======================
   RESTORE ON PAGE LOAD
======================= */
window.onload = function () {
  const last = loadLastResult();
  if (last) {
    renderResult(last); // ✅ RESTORE UI AFTER BACK / REFRESH
  }
};

/* ---------- RUN AGAIN ---------- */
function runLast() {
  if (lastInstruction) runTest(lastInstruction);
}

/* ---------- CLEAR ---------- */
function clearAll() {
  localStorage.removeItem("lastTestResult");
  document.getElementById("instruction").value = "";
  document.getElementById("result").innerText = "Cleared.";
  document.getElementById("result").className = "result-box neutral";
  document.getElementById("screenshot").src = "";
  document.getElementById("downloadShot").style.display = "none";
  document.getElementById("video").style.display = "none";
  document.getElementById("downloadVideo").style.display = "none";
  updateWizard(0);
}

/* ---------- EXAMPLES ---------- */
function useExample(el) {
  document.getElementById("instruction").value = el.innerText;
}

/* ---------- WIZARD ---------- */
function updateWizard(step) {
  document.querySelectorAll(".step").forEach((s, i) => {
    s.classList.toggle("active", i <= step);
  });
}

/* ---------- HISTORY ---------- */
function loadHistory() {
  fetch(`${BACKEND_URL}/history`)
    .then(r => r.json())
    .then(list => {
      const h = document.getElementById("history");
      if (!list.length) {
        h.innerText = "No history yet";
        return;
      }
      h.innerHTML = "";
      list.forEach(item => {
        const div = document.createElement("div");
        div.innerHTML = `
          <b>${item.time}</b> – ${item.instruction}
          <span style="float:right;color:${item.status === "PASSED" ? "green" : "red"}">
            ${item.status}
          </span>`;
        div.onclick = () => runTest(item.instruction);
        h.appendChild(div);
      });
    });
}
