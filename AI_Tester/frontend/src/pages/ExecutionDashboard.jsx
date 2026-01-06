import React, { useEffect, useMemo, useState } from "react";
import { useTheme } from "../context/ThemeContext";
import "../styles/ExecutionDashboard.css";

import PlayIcon from "../assets/icons/Play.png";
import ClockIcon from "../assets/icons/Clock.png";
import PassIcon from "../assets/icons/Pass.png";
import FailIcon from "../assets/icons/Fail.png";
import EnvIcon from "../assets/icons/Env.png";

const API_BASE = import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8000";

async function safeJson(res) {
  const text = await res.text();
  try {
    return JSON.parse(text);
  } catch {
    return { error: "Non-JSON response", raw: text };
  }
}

function fmtIso(iso) {
  if (!iso) return "-";
  try {
    return new Date(iso).toLocaleString();
  } catch {
    return iso;
  }
}

function durationFromIso(startedAt, finishedAt) {
  if (!startedAt || !finishedAt) return "-";
  try {
    const s = new Date(startedAt).getTime();
    const f = new Date(finishedAt).getTime();
    const ms = Math.max(0, f - s);
    const sec = Math.round(ms / 1000);
    const m = String(Math.floor(sec / 60)).padStart(2, "0");
    const r = String(sec % 60).padStart(2, "0");
    return `${m}:${r}`;
  } catch {
    return "-";
  }
}

const ExecutionDashboard = () => {
  const theme = useTheme();

  const [loading, setLoading] = useState(true);
  const [runsMap, setRunsMap] = useState({});
  const [error, setError] = useState("");

  const [startingRun, setStartingRun] = useState(false);
  const [startMessage, setStartMessage] = useState("");

  useEffect(() => {
    document.title = "Execution Dashboard - Youval AutoQA";
  }, []);

  const loadRuns = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_BASE}/api/runs`);
      const data = await safeJson(res);
      if (!res.ok) throw new Error(data?.detail || `Failed to load runs (${res.status})`);
      setRunsMap(data && typeof data === "object" ? data : {});
    } catch (e) {
      setRunsMap({});
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRuns();
  }, []);

  const runs = useMemo(() => {
    const arr = Object.values(runsMap || {}).filter(Boolean);
    // newest first
    arr.sort((a, b) => String(b.startedAt || "").localeCompare(String(a.startedAt || "")));
    return arr;
  }, [runsMap]);

  const latestRun = runs[0] || null;

  const metrics = useMemo(() => {
    const totalRuns = runs.length;
    const passRuns = runs.filter((r) => r.status === "PASS").length;
    const failRuns = runs.filter((r) => r.status === "FAIL").length;
    const passRate = totalRuns ? Math.round((passRuns / totalRuns) * 100) : 0;

    return [
      { id: 1, label: "Total runs", value: totalRuns, subLabel: "Runs stored in backend" },
      { id: 2, label: "Pass rate", value: `${passRate}%`, subLabel: `${passRuns} PASS / ${failRuns} FAIL` },
      { id: 3, label: "Latest run status", value: latestRun?.status || "-", subLabel: latestRun?.scenario?.title || "-" },
      { id: 4, label: "Latest duration", value: latestRun ? durationFromIso(latestRun.startedAt, latestRun.finishedAt) : "-", subLabel: "From timestamps" },
    ];
  }, [runs, latestRun]);

  const envSummary = useMemo(() => {
    const total = runs.length;
    const pass = runs.filter((r) => r.status === "PASS").length;
    const fail = runs.filter((r) => r.status === "FAIL").length;

    return [
      { id: 1, name: "Backend runner", status: error ? "Degraded" : "Healthy", tests: total },
      { id: 2, name: "PASS runs", status: "Healthy", tests: pass },
      { id: 3, name: "FAIL runs", status: fail ? "Degraded" : "Healthy", tests: fail },
    ];
  }, [runs, error]);

  const recentRunsTable = useMemo(() => {
    return runs.slice(0, 10).map((r) => ({
      id: r.runId,
      env: r.environment || "-",
      started: fmtIso(r.startedAt),
      duration: durationFromIso(r.startedAt, r.finishedAt),
      total: (r.passCount || 0) + (r.failCount || 0) + (r.pendingCount || 0) || "-",
      passed: r.passCount ?? (r.status === "PASS" ? 1 : 0),
      failed: r.failCount ?? (r.status === "FAIL" ? 1 : 0),
      status: r.status === "PASS" ? "Passed" : r.status === "FAIL" ? "Failed" : "Unknown",
      runId: r.runId,
    }));
  }, [runs]);

  const startNewRun = async () => {
    setStartingRun(true);
    setStartMessage("Starting run...");
    try {
      // This runs the approved scenario in backend
      const res = await fetch(`${API_BASE}/api/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ headless: true, keepBrowserOpen: false }),
      });

      const data = await safeJson(res);
      if (!res.ok || data.status !== "ok") {
        throw new Error(data?.message || data?.detail || `Run failed (${res.status})`);
      }

      setStartMessage(`Run started & finished: ${data.run.runId} (${data.run.status})`);
      await loadRuns();
    } catch (e) {
      setStartMessage(`Error: ${e.message}`);
    } finally {
      setStartingRun(false);
    }
  };

  return (
    <main className={`exec-page exec-page--${theme}`}>
      <header className="exec-header">
        <div className="exec-header-left">
          <span className="exec-pill">Step 3 • Execution Dashboard</span>
          <h1>Live test execution overview</h1>
          <p>Track run history, statuses, and open reports generated by the backend runner.</p>

          <div className="exec-header-actions">
            <button className="btn btn-primary exec-header-btn" onClick={startNewRun} disabled={startingRun}>
              <img src={PlayIcon} alt="Run" className="btn-icon" />
              {startingRun ? "Starting..." : "Start new run"}
            </button>

            <button className="btn btn-outline exec-header-btn" onClick={loadRuns} disabled={loading}>
              <img src={ClockIcon} alt="Refresh" className="btn-icon" />
              Refresh
            </button>
          </div>

          {startMessage && <div style={{ marginTop: 10 }}>{startMessage}</div>}
          {error && <div style={{ marginTop: 10 }}>Backend error: {error}</div>}
        </div>

        <aside className="exec-header-right">
          <div className="exec-summary-card">
            <div className="exec-summary-header">
              <div className="exec-summary-labels">
                <span className="summary-pill">Latest run</span>
                <span className="summary-id">{latestRun?.runId || "-"}</span>
              </div>
              <span className={`summary-status summary-status--${(latestRun?.status || "idle").toLowerCase()}`}>
                {latestRun?.status || "Idle"}
              </span>
            </div>

            <div className="exec-summary-main">
              <div className="summary-progress">
                <div className="summary-progress-bar">
                  <div className="summary-progress-fill" style={{ width: latestRun ? "100%" : "0%" }} />
                </div>
                <div className="summary-progress-meta">
                  <span>{latestRun ? "100% complete" : "No run yet"}</span>
                  <span>Started: {fmtIso(latestRun?.startedAt)}</span>
                </div>
              </div>

              <div className="summary-breakdown">
                <div className="summary-breakdown-item">
                  <img src={PassIcon} alt="Passed" />
                  <span className="breakdown-label">Passed</span>
                  <span className="breakdown-value">{latestRun?.passCount ?? (latestRun?.status === "PASS" ? 1 : 0)}</span>
                </div>
                <div className="summary-breakdown-item">
                  <img src={FailIcon} alt="Failed" />
                  <span className="breakdown-label">Failed</span>
                  <span className="breakdown-value breakdown-value--danger">
                    {latestRun?.failCount ?? (latestRun?.status === "FAIL" ? 1 : 0)}
                  </span>
                </div>
                <div className="summary-breakdown-item">
                  <img src={ClockIcon} alt="Pending" />
                  <span className="breakdown-label">Pending</span>
                  <span className="breakdown-value">{latestRun?.pendingCount ?? 0}</span>
                </div>
              </div>
            </div>
          </div>
        </aside>
      </header>

      <section className="exec-metrics">
        <div className="exec-metrics-grid">
          {metrics.map((card) => (
            <article key={card.id} className="exec-metric-card">
              <p className="exec-metric-label">{card.label}</p>
              <p className="exec-metric-value">{loading ? "…" : card.value}</p>
              <p className="exec-metric-sublabel">{card.subLabel}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="exec-layout">
        <section className="exec-panel">
          <header className="exec-panel-header">
            <h2>Run controls & logs</h2>
            <p>For now, runs execute instantly per click (approved scenario).</p>
          </header>

          <div className="exec-run-actions">
            <button className="btn btn-outline btn-sm" onClick={startNewRun} disabled={startingRun}>
              Run approved scenario
            </button>
            <button className="btn btn-outline btn-sm" onClick={() => window.open(`${API_BASE}/api/scenario/approved`, "_blank")}>
              View approved scenario
            </button>
            <button className="btn btn-outline btn-sm" onClick={() => window.open(`${API_BASE}/api/runs`, "_blank")}>
              View runs JSON
            </button>
          </div>

          <div className="exec-log">
            <div className="exec-log-header">
              <span>Recent events</span>
              <span className="exec-log-env">Environment: {latestRun?.environment || "-"}</span>
            </div>

            <ul className="exec-log-list">
              {!latestRun && <li>No runs available.</li>}
              {latestRun && (
                <>
                  <li>
                    <span className="log-time">{fmtIso(latestRun.startedAt)}</span>
                    <span className={`log-status log-status--${latestRun.status === "PASS" ? "pass" : "fail"}`}>
                      {latestRun.status}
                    </span>
                    <span className="log-message">{latestRun.scenario?.title || "Approved scenario run"}</span>
                  </li>
                  {(latestRun.actionResults || []).slice(0, 5).map((a) => (
                    <li key={`${latestRun.runId}-${a.idx}`}>
                      <span className="log-time">Step {a.idx}</span>
                      <span className={`log-status log-status--${a.status === "PASS" ? "pass" : "fail"}`}>
                        {a.status}
                      </span>
                      <span className="log-message">
                        {a.actionType}
                        {a.error ? ` — ${a.error}` : ""}
                      </span>
                    </li>
                  ))}
                </>
              )}
            </ul>
          </div>
        </section>

        <section className="exec-panel">
          <header className="exec-panel-header">
            <h2>Environments queue</h2>
            <p>Aggregated view based on stored run results.</p>
          </header>

          <div className="exec-env-list">
            {envSummary.map((env) => (
              <div key={env.id} className="exec-env-card">
                <div className="exec-env-main">
                  <div className="exec-env-icon">
                    <img src={EnvIcon} alt={env.name} />
                  </div>
                  <div>
                    <p className="exec-env-name">{env.name}</p>
                    <p className="exec-env-tests">{env.tests} items</p>
                  </div>
                </div>
                <span className={`exec-env-status exec-env-status--${env.status.toLowerCase()}`}>{env.status}</span>
              </div>
            ))}
          </div>

          <div className="exec-queue">
            <h3>Useful links</h3>
            <ul>
              <li>
                <a href={`${API_BASE}/api/reports`} target="_blank" rel="noreferrer">
                  Open reports index (JSON)
                </a>
              </li>
              <li>
                <a href={`${API_BASE}/api/analysis/latest`} target="_blank" rel="noreferrer">
                  Open latest analysis (JSON)
                </a>
              </li>
            </ul>
          </div>
        </section>
      </section>

      <section className="exec-results">
        <div className="exec-results-inner">
          <header className="exec-results-header">
            <h2>Recent runs</h2>
            <p>High-level view of stored run results.</p>
          </header>

          <div className="exec-results-table">
            <table>
              <thead>
                <tr>
                  <th>Run ID</th>
                  <th>Environment</th>
                  <th>Started</th>
                  <th>Duration</th>
                  <th>Total</th>
                  <th>Passed</th>
                  <th>Failed</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {recentRunsTable.length === 0 && (
                  <tr>
                    <td colSpan="8">{loading ? "Loading..." : "No runs yet. Approve scenario and start a run."}</td>
                  </tr>
                )}

                {recentRunsTable.map((run) => (
                  <tr key={run.id}>
                    <td>
                      <button
                        type="button"
                        className="btn btn-outline btn-sm"
                        onClick={() => window.open(`${API_BASE}/files/reports/${run.runId}.json`, "_blank")}
                      >
                        {run.id}
                      </button>
                    </td>
                    <td>{run.env}</td>
                    <td>{run.started}</td>
                    <td>{run.duration}</td>
                    <td>{run.total}</td>
                    <td>{run.passed}</td>
                    <td>{run.failed}</td>
                    <td>
                      <span className={`exec-status-badge exec-status-badge--${run.status.toLowerCase()}`}>
                        {run.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </main>
  );
};

export default ExecutionDashboard;
