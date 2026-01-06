import React, { useEffect, useMemo, useState } from "react";
import { useTheme } from "../context/ThemeContext";
import "../styles/ReportsPage.css";

import ReportsIcon from "../assets/Rpt.png";

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

function durationFromRun(run) {
  if (!run?.startedAt || !run?.finishedAt) return "-";
  try {
    const s = new Date(run.startedAt).getTime();
    const f = new Date(run.finishedAt).getTime();
    const ms = Math.max(0, f - s);
    const sec = Math.round(ms / 1000);
    const m = String(Math.floor(sec / 60)).padStart(2, "0");
    const r = String(sec % 60).padStart(2, "0");
    return `${m}:${r}`;
  } catch {
    return "-";
  }
}

const ReportsPage = () => {
  const theme = useTheme();

  const [selectedSuite, setSelectedSuite] = useState("All suites");
  const [timeRange, setTimeRange] = useState("Last 7 days");

  const [loading, setLoading] = useState(true);
  const [reportIndex, setReportIndex] = useState({ reports: [] });
  const [error, setError] = useState("");

  const [selectedReportId, setSelectedReportId] = useState(null);
  const [lightboxImg, setLightboxImg] = useState(null);

  useEffect(() => {
    document.title = "Reports - Youval AutoQA";
  }, []);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError("");
      try {
        const res = await fetch(`${API_BASE}/api/reports`);
        const data = await safeJson(res);
        if (!res.ok) throw new Error(data?.detail || `Failed to load reports (${res.status})`);
        setReportIndex(data && typeof data === "object" ? data : { reports: [] });

        const firstId = data?.reports?.[0]?.runId || null;
        setSelectedReportId((prev) => prev || firstId);
      } catch (e) {
        setReportIndex({ reports: [] });
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const reportCards = useMemo(() => {
    const reps = Array.isArray(reportIndex?.reports) ? reportIndex.reports : [];
    // newest first
    const sorted = [...reps].sort((a, b) => String(b.createdAt || "").localeCompare(String(a.createdAt || "")));
    return sorted.map((r) => {
      const runId = r.runId;
      const jsonUrl = r.json ? `${API_BASE}/files/reports/${runId}.json` : null;
      const pdfUrl = r.pdf ? `${API_BASE}/files/reports/${runId}.pdf` : null;
      const screenshotUrl = r.screenshot ? `${API_BASE}/files/screenshots/${runId}.png` : null;

      return {
        id: runId,
        title: `Run ${runId}`,
        type: "Execution summary",
        createdAt: fmtIso(r.createdAt),
        duration: "-", // filled after loading run JSON optionally
        passRate: "-", // not available in current backend model
        status: "Ready",
        links: { jsonUrl, pdfUrl, screenshotUrl },
        screenshots: screenshotUrl
          ? [{ id: `${runId}-s1`, src: screenshotUrl, caption: "Run screenshot evidence" }]
          : [],
      };
    });
  }, [reportIndex]);

  const selectedReport = useMemo(() => {
    return reportCards.find((r) => r.id === selectedReportId) || reportCards[0] || null;
  }, [reportCards, selectedReportId]);

  const screenshots = selectedReport?.screenshots || [];

  return (
    <main className={`reports-page app-page--${theme}`}>
      <aside className="page-filters-sidebar">
        <div className="sidebar-title">Time Range</div>
        <div className="sidebar-filter-group">
          <select className="form-select" value={timeRange} onChange={(e) => setTimeRange(e.target.value)}>
            <option>Last 7 days</option>
            <option>Last 14 days</option>
            <option>Last 30 days</option>
            <option>Last 90 days</option>
            <option>Custom range</option>
          </select>
        </div>

        <div className="sidebar-title" style={{ marginTop: "20px" }}>
          Test Suites
        </div>
        <div className="sidebar-filter-group">
          <label>
            <input type="checkbox" checked={selectedSuite === "All suites"} onChange={() => setSelectedSuite("All suites")} />
            All suites
          </label>
          <label>
            <input type="checkbox" checked={selectedSuite === "Smoke"} onChange={() => setSelectedSuite("Smoke")} />
            Smoke
          </label>
          <label>
            <input type="checkbox" checked={selectedSuite === "Full regression"} onChange={() => setSelectedSuite("Full regression")} />
            Full regression
          </label>
          <label>
            <input type="checkbox" checked={selectedSuite === "API only"} onChange={() => setSelectedSuite("API only")} />
            API only
          </label>
        </div>

        <div className="sidebar-filter-group" style={{ marginTop: "20px" }}>
          <button className="btn btn-primary btn-sm" style={{ width: "100%" }} onClick={() => window.open(`${API_BASE}/api/reports`, "_blank")}>
            Open reports JSON
          </button>
        </div>
      </aside>

      <div className="page-content-area">
        <header className="page-header-block">
          <div className="page-header-left">
            <div className="page-pill">
              <img src={ReportsIcon} alt="Reports" />
              Reports
            </div>
            <div className="page-header-text">
              <h1>Reports analytics</h1>
              <p>Browse execution summaries and export-ready artifacts generated by the backend.</p>
              {error && <p style={{ marginTop: 8 }}>Error: {error}</p>}
            </div>
          </div>

          <div className="page-header-right">
            <button className="btn btn-primary btn-sm" onClick={() => window.open(`${API_BASE}/api/reports`, "_blank")}>
              Refresh source
            </button>
          </div>
        </header>

        <section className="page-metrics">
          <div className="page-metrics-grid">
            <div className="page-metric-card">
              <div className="metric-label-lg">Reports generated</div>
              <div className="metric-value-lg">{loading ? "…" : reportCards.length}</div>
              <div className="metric-note">From backend report index</div>
            </div>
            <div className="page-metric-card">
              <div className="metric-label-lg">Backend URL</div>
              <div className="metric-value-lg" style={{ fontSize: 14 }}>{API_BASE}</div>
              <div className="metric-note">Used for downloads</div>
            </div>
            <div className="page-metric-card">
              <div className="metric-label-lg">Artifacts</div>
              <div className="metric-value-lg">JSON / PDF / PNG</div>
              <div className="metric-note">Depends on backend deps</div>
            </div>
          </div>
        </section>

        <section className="reports-layout">
          <div className="reports-list-panel">
            <div className="panel-header">
              <h2>Recent reports</h2>
              <p>Latest execution summaries in {timeRange.toLowerCase()}.</p>
            </div>

            {loading && <div className="reports-empty">Loading reports...</div>}
            {!loading && reportCards.length === 0 && <div className="reports-empty">No reports yet. Run a test first.</div>}

            <div className="reports-list">
              {reportCards.map((report) => (
                <button
                  key={report.id}
                  type="button"
                  className={`report-card ${report.id === selectedReportId ? "report-card--active" : ""}`}
                  onClick={() => setSelectedReportId(report.id)}
                >
                  <div className="report-card-header">
                    <div className="report-card-info">
                      <p className="report-title">{report.title}</p>
                      <p className="report-type">{report.type}</p>
                    </div>
                    <span className="report-status-chip">{report.status}</span>
                  </div>

                  <div className="report-row">
                    <span className="report-label">Created</span>
                    <span className="report-value">{report.createdAt}</span>
                  </div>

                  <div className="report-row">
                    <span className="report-label">Artifacts</span>
                    <span className="report-value">
                      {report.links.pdfUrl ? "PDF" : "No PDF"} / {report.links.screenshotUrl ? "PNG" : "No PNG"} / JSON
                    </span>
                  </div>
                </button>
              ))}
            </div>
          </div>

          <div className="reports-preview-panel">
            <div className="panel-header">
              <h2>Key highlights</h2>
              <p>Quick export links for the selected report.</p>
            </div>

            {!selectedReport && <div className="reports-empty">Select a report.</div>}

            {selectedReport && (
              <div className="report-preview-card">
                <div className="preview-section">
                  <h3>Exports</h3>
                  <div className="preview-actions">
                    <button
                      className="btn btn-secondary btn-sm"
                      onClick={() => selectedReport.links.pdfUrl && window.open(selectedReport.links.pdfUrl, "_blank")}
                      disabled={!selectedReport.links.pdfUrl}
                    >
                      PDF
                    </button>
                    <button
                      className="btn btn-secondary btn-sm"
                      onClick={() => selectedReport.links.jsonUrl && window.open(selectedReport.links.jsonUrl, "_blank")}
                      disabled={!selectedReport.links.jsonUrl}
                    >
                      JSON
                    </button>
                    <button
                      className="btn btn-secondary btn-sm"
                      onClick={() => selectedReport.links.screenshotUrl && window.open(selectedReport.links.screenshotUrl, "_blank")}
                      disabled={!selectedReport.links.screenshotUrl}
                    >
                      Screenshot
                    </button>
                  </div>
                </div>

                <div className="preview-section">
                  <h3>Notes</h3>
                  <ul>
                    <li>PDF appears only if backend has reportlab installed.</li>
                    <li>Screenshot appears only if Playwright run produced a PNG.</li>
                    <li>JSON report is always generated.</li>
                  </ul>
                </div>
              </div>
            )}
          </div>
        </section>

        <section className="reports-screenshots-section">
          <div className="reports-screenshots-panel">
            <div className="screenshots-header">
              <div className="screenshots-header-left">
                <h2>Screenshots</h2>
                <p>
                  Evidence for: <strong>{selectedReport?.title || "-"}</strong>
                </p>
              </div>
              <div className="screenshots-header-right">
                <span className="screenshots-count">{screenshots.length} items</span>
              </div>
            </div>

            {screenshots.length === 0 ? (
              <div className="screenshots-empty">No screenshots available for this report.</div>
            ) : (
              <div className="screenshots-grid">
                {screenshots.map((shot) => (
                  <button key={shot.id} type="button" className="screenshot-tile" onClick={() => setLightboxImg(shot)}>
                    <img className="screenshot-img" src={shot.src} alt={shot.caption} />
                    <div className="screenshot-caption">{shot.caption}</div>
                  </button>
                ))}
              </div>
            )}
          </div>
        </section>

        {lightboxImg && (
          <div className="screenshots-lightbox" onClick={() => setLightboxImg(null)}>
            <div className="screenshots-lightbox-content" onClick={(e) => e.stopPropagation()}>
              <div className="screenshots-lightbox-header">
                <h3>{lightboxImg.caption}</h3>
                <button className="btn btn-secondary btn-sm" onClick={() => setLightboxImg(null)}>
                  Close
                </button>
              </div>
              <img className="screenshots-lightbox-img" src={lightboxImg.src} alt={lightboxImg.caption} />
            </div>
          </div>
        )}
      </div>
    </main>
  );
};

export default ReportsPage;
