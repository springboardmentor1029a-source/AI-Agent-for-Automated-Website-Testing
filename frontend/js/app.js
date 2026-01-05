const BACKEND_URL = "http://127.0.0.1:5000";
let lastInstruction = "";

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
      updateWizard(1);

      /* ---------- RESULT ---------- */
      const box = document.getElementById("result");
      box.innerText =
        d.status === "PASSED"
          ? "Test executed successfully"
          : "Test failed";

      box.className =
        "result-box " + (d.status === "PASSED" ? "success" : "error");

      /* ---------- ✅ EXECUTION DETAILS (FIXED) ---------- */
      const extra = document.getElementById("extraInfo");
      const reportLink = document.getElementById("reportLink");

      extra.innerHTML = `
        <b>Execution Time:</b> ${d.execution_time ?? "-"} seconds<br>
        <b>Failure Reason:</b> ${d.failure_reason || "N/A"}<br>
      `;

      if (d.report) {
        reportLink.href = `${BACKEND_URL}/reports/${d.report}`;
        reportLink.style.display = "inline-block";
      } else {
        reportLink.style.display = "none";
      }

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
        video.load(); // ensures full playback
        video.style.display = "block";
        dlVideo.href = videoSrc;
        dlVideo.style.display = "inline-block";
      } else {
        video.style.display = "none";
        dlVideo.style.display = "none";
      }

      updateWizard(3);
      loadHistory();
    })
    .catch(() => {
      const box = document.getElementById("result");
      box.innerText = "Backend not reachable";
      box.className = "result-box error";
    });
}

/* ---------- RUN AGAIN ---------- */
function runLast() {
  if (lastInstruction) runTest(lastInstruction);
}

/* ---------- CLEAR ---------- */
function clearAll() {
  document.getElementById("instruction").value = "";
  document.getElementById("result").innerText = "Cleared.";
  document.getElementById("result").className = "result-box neutral";

  document.getElementById("extraInfo").innerHTML = `
    <b>Execution Time:</b> - seconds<br>
    <b>Failure Reason:</b> N/A<br>
  `;
  document.getElementById("reportLink").style.display = "none";

  document.getElementById("screenshot").src = "";
  document.getElementById("downloadShot").style.display = "none";
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
