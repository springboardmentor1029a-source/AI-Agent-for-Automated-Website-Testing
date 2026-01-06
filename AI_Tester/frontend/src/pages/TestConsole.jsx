import React, { useEffect, useState } from "react";
import { useTheme } from "../context/ThemeContext";
import "../styles/TestConsolePage.css";
import ConsoleIcon from "../assets/icons/Env.png";

const API_BASE = import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8000";

async function safeJson(res) {
  const text = await res.text();
  try {
    return JSON.parse(text);
  } catch {
    return { error: "Non-JSON response", raw: text };
  }
}

const TestConsolePage = () => {
  const theme = useTheme();

  const [scenarioText, setScenarioText] = useState("");
  const [env, setEnv] = useState("Staging Chrome");
  const [runType, setRunType] = useState("Full execution");

  const [approvedScenario, setApprovedScenario] = useState(null);

  const [running, setRunning] = useState(false);
  const [runResult, setRunResult] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    document.title = "Test Console - Youval AutoQA";
  }, []);

  useEffect(() => {
    const loadApproved = async () => {
      try {
        const res = await fetch(`${API_BASE}/api/scenario/approved`);
        const data = await safeJson(res);
        if (res.ok && data && Object.keys(data).length > 0) {
          setApprovedScenario(data);
          setScenarioText(JSON.stringify(data, null, 2));
        }
      } catch {
        // ignore
      }
    };
    loadApproved();
  }, []);

  const runNow = async () => {
    setRunning(true);
    setError("");
    setRunResult(null);

    try {
      const headless = false;
      const res = await fetch(`${API_BASE}/api/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ headless, keepBrowserOpen: false }),
      });

      const data = await safeJson(res);
      if (!res.ok || data.status !== "ok") {
        throw new Error(data?.message || data?.detail || "Run failed");
      }

      setRunResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setRunning(false);
    }
  };

  const run = runResult?.run;
  const files = runResult?.files;

  return (
    <main className={`test-console-page app-page--${theme}`}>
      <header className="page-header-block page-header-center">
        <span className="page-pill">
          <img src={ConsoleIcon} alt="Console" />
          Test Console
        </span>
        <h1>Experiment, tweak, and run tests</h1>
        <p>Load the approved scenario from Analysis Review and trigger executions from the browser.</p>
      </header>

      <section className="console-layout">
        <section className="console-panel">
          <header className="panel-header">
            <h2>Input configuration</h2>
            <p>Approved scenario is auto-loaded if available.</p>
          </header>

          <div className="console-section">
            <label className="field-label" htmlFor="scenario">
              Test scenario input
            </label>
            <textarea
              id="scenario"
              className="console-textarea"
              placeholder="Approved scenario JSON will appear here..."
              rows={10}
              value={scenarioText}
              onChange={(e) => setScenarioText(e.target.value)}
            />
            <div className="field-hint">This UI input is for preview; execution uses the approved scenario saved in backend.</div>
          </div>

          <div className="console-grid-2">
            <div className="console-section">
              <label className="field-label" htmlFor="env">
                Environment
              </label>
              <select id="env" className="form-select" value={env} onChange={(e) => setEnv(e.target.value)}>
                <option>Staging Chrome</option>
                <option>Staging Firefox</option>
                <option>Production Smoke only</option>
              </select>
            </div>

            <div className="console-section">
              <label className="field-label" htmlFor="runType">
                Run type
              </label>
              <select id="runType" className="form-select" value={runType} onChange={(e) => setRunType(e.target.value)}>
                <option>Dry run (no side effects)</option>
                <option>Full execution</option>
                <option>Debug single step</option>
              </select>
            </div>
          </div>

          <div className="console-actions">
            <button className="btn btn-primary btn-lg" onClick={runNow} disabled={running}>
              {running ? "Running..." : "Run in console"}
            </button>
            <button className="btn btn-outline btn-lg" type="button" onClick={() => window.open(`${API_BASE}/api/scenario/approved`, "_blank")}>
              View approved JSON
            </button>
          </div>

          {error && <div className="console-preview-card" style={{ marginTop: 14 }}>Error: {error}</div>}
        </section>

        <section className="console-panel">
          <header className="panel-header">
            <h2>Preview last run</h2>
            <p>Live output from backend execution.</p>
          </header>

          {!run && (
            <div className="console-preview-card">
              <div className="preview-row">
                <span className="preview-label">Approved scenario</span>
                <span className="preview-value">{approvedScenario?.title || "Not approved yet"}</span>
              </div>
              <div className="preview-row">
                <span className="preview-label">Tip</span>
                <span className="preview-value">Go to Analysis Review → Send to Test Console</span>
              </div>
            </div>
          )}

          {run && (
            <div className="console-preview-card">
              <div className="preview-row">
                <span className="preview-label">Last run ID</span>
                <span className="preview-value">{run.runId}</span>
              </div>
              <div className="preview-row">
                <span className="preview-label">Status</span>
                <span className={`preview-badge ${run.status === "PASS" ? "preview-badge--success" : "preview-badge--danger"}`}>
                  {run.status}
                </span>
              </div>
              <div className="preview-row">
                <span className="preview-label">Started</span>
                <span className="preview-value">{run.startedAt}</span>
              </div>
              <div className="preview-row">
                <span className="preview-label">Finished</span>
                <span className="preview-value">{run.finishedAt}</span>
              </div>

              <div className="preview-log">
                <h3>Artifacts</h3>
                <ul>
                  {files?.reportJsonUrl && (
                    <li>
                      <a href={`${API_BASE}${files.reportJsonUrl}`} target="_blank" rel="noreferrer">
                        Open JSON report
                      </a>
                    </li>
                  )}
                  {files?.reportPdfUrl && (
                    <li>
                      <a href={`${API_BASE}${files.reportPdfUrl}`} target="_blank" rel="noreferrer">
                        Open PDF report
                      </a>
                    </li>
                  )}
                  {files?.screenshotUrl && (
                    <li>
                      <a href={`${API_BASE}${files.screenshotUrl}`} target="_blank" rel="noreferrer">
                        Open screenshot
                      </a>
                    </li>
                  )}
                </ul>
              </div>
            </div>
          )}
        </section>
      </section>
    </main>
  );
};

export default TestConsolePage;
