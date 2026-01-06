import React, { useEffect, useMemo, useState } from "react";
import { useTheme } from "../context/ThemeContext";
import "../styles/AnalysisReview.css";

import RequirementsIcon from "../assets/icons/Requirements.png";
import RiskIcon from "../assets/icons/Risk.png";
import ChecklistIcon from "../assets/icons/Checklist.png";
import CodeIcon from "../assets/icons/Code.png";
import GoalIcon from "../assets/icons/Goal.png";

const API_BASE = import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8000";

async function safeJson(res) {
  const text = await res.text();
  try {
    return JSON.parse(text);
  } catch {
    return { error: "Non-JSON response", raw: text };
  }
}

const AnalysisReview = () => {
  const theme = useTheme();
  const [activeFilter, setActiveFilter] = useState("all");

  const [loading, setLoading] = useState(true);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState("");

  const [approveStatus, setApproveStatus] = useState("idle");
  const [approveMessage, setApproveMessage] = useState("");

  useEffect(() => {
    document.title = "Analysis Review - Youval AutoQA";
  }, []);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError("");
      try {
        const res = await fetch(`${API_BASE}/api/analysis/latest`);
        const data = await safeJson(res);
        if (!res.ok) throw new Error(data?.detail || `Failed to load latest analysis (${res.status})`);
        setAnalysis(data);
      } catch (e) {
        setError(e.message);
        setAnalysis(null);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const findings = Array.isArray(analysis?.findings) ? analysis.findings : [];
  const filteredFindings =
    activeFilter === "all"
      ? findings
      : findings.filter((item) => {
          const cat = (item.category || "").toLowerCase();
          if (activeFilter === "gaps") return cat === "gap";
          if (activeFilter === "ambiguities") return cat === "ambiguity";
          if (activeFilter === "edge") return cat === "edge";
          return true;
        });

  const quality = analysis?.quality || {};
  const coverage = analysis?.coverage || {};
  const riskHotspots = Array.isArray(analysis?.riskHotspots) ? analysis.riskHotspots : [];
  const scenario = analysis?.scenario || null;

  const readinessScore = Number(quality.readinessScore ?? 0);
  const requirementCoveragePct = Number(quality.requirementCoveragePct ?? 0);
  const filesImpacted = Number(quality.filesImpacted ?? 0);
  const openClarifications = Number(quality.openClarifications ?? 0);

  const coverageBreakdown = useMemo(() => {
    const toRow = (label, value, total) => ({ id: label, label, value, total });
    return [
      toRow("Happy paths", Number(coverage.happy ?? 0), 100),
      toRow("Negative paths", Number(coverage.negative ?? 0), 100),
      toRow("Edge cases", Number(coverage.edge ?? 0), 100),
      toRow("Non-functional", Number(coverage.nonFunctional ?? 0), 100),
    ];
  }, [coverage]);

  const approveScenario = async () => {
    if (!scenario || typeof scenario !== "object") {
      setApproveStatus("error");
      setApproveMessage("No scenario found in latest analysis. Run Data Input analyze first.");
      return;
    }

    setApproveStatus("processing");
    setApproveMessage("Approving scenario for Test Console...");

    try {
      const res = await fetch(`${API_BASE}/api/approve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scenario }),
      });
      const data = await safeJson(res);
      if (!res.ok) throw new Error(data?.detail || data?.message || `Approve failed (${res.status})`);

      setApproveStatus("complete");
      setApproveMessage("Scenario approved. Open Test Console and run it.");
    } catch (e) {
      setApproveStatus("error");
      setApproveMessage(e.message);
    }
  };

  return (
    <main className={`analysis-page analysis-page--${theme}`}>
      <header className="analysis-header">
        <div className="analysis-header-left">
          <span className="analysis-pill">Step 2 • Analysis Review</span>
          <h1>AI-powered requirement analysis</h1>
          <p>Review gaps, risks, and coverage recommendations before committing scenarios into your automated suites.</p>

          <div className="analysis-header-meta">
            <div className="meta-item">
              <img src={RequirementsIcon} alt="Requirements" />
              <div>
                <span className="meta-label">Project</span>
                <span className="meta-value">{analysis?.projectId || "-"}</span>
              </div>
            </div>

            <div className="meta-item">
              <img src={ChecklistIcon} alt="Scenarios" />
              <div>
                <span className="meta-label">Scenario</span>
                <span className="meta-value">{scenario?.title || "-"}</span>
              </div>
            </div>
          </div>
        </div>

        <aside className="analysis-header-right">
          <div className="summary-card">
            <div className="summary-card-top">
              <img src={GoalIcon} alt="Quality score" />
              <span className="summary-label">Quality score</span>
            </div>

            <div className="summary-main">
              <span className="summary-score">{loading ? "…" : readinessScore}</span>
              <span className="summary-chip summary-chip--good">
                {quality.scenarioReadiness || "Needs review"}
              </span>
            </div>

            <ul className="summary-list">
              <li>
                <span>Requirement coverage</span>
                <span>{loading ? "…" : `${requirementCoveragePct}%`}</span>
              </li>
              <li>
                <span>Files impacted</span>
                <span>{loading ? "…" : filesImpacted}</span>
              </li>
              <li>
                <span>Open clarifications</span>
                <span>{loading ? "…" : openClarifications}</span>
              </li>
            </ul>
          </div>
        </aside>
      </header>

      <section className="analysis-metrics">
        <div className="analysis-metrics-grid">
          <div className="analysis-metric-card">
            <div className="metric-icon metric-icon--risk">
              <img src={RiskIcon} alt="Risk" />
            </div>
            <div>
              <p className="metric-label">Overall risk level</p>
              <p className="metric-value metric-value--high">{riskHotspots.length ? "Review hotspots" : "Low"}</p>
              <span className="metric-pill metric-pill--critical">{findings.length} findings</span>
            </div>
          </div>

          <div className="analysis-metric-card">
            <div className="metric-icon">
              <img src={CodeIcon} alt="Change" />
            </div>
            <div>
              <p className="metric-label">Files impacted</p>
              <p className="metric-value">{filesImpacted}</p>
              <span className="metric-pill">From AI analysis</span>
            </div>
          </div>

          <div className="analysis-metric-card">
            <div className="metric-icon">
              <img src={ChecklistIcon} alt="Coverage" />
            </div>
            <div>
              <p className="metric-label">Scenario readiness</p>
              <p className="metric-value">{quality.scenarioReadiness || "Needs review"}</p>
              <span className="metric-pill metric-pill--good">Approve to run</span>
            </div>
          </div>
        </div>
      </section>

      <section className="analysis-layout">
        <section className="analysis-panel">
          <header className="analysis-panel-header">
            <h2>AI findings</h2>
            <p>Prioritized list of gaps, ambiguities, and edge cases detected by the engine.</p>
          </header>

          <div className="analysis-filter-chips">
            <button type="button" className={`chip ${activeFilter === "all" ? "chip--active" : ""}`} onClick={() => setActiveFilter("all")}>
              All
            </button>
            <button type="button" className={`chip ${activeFilter === "gaps" ? "chip--active" : ""}`} onClick={() => setActiveFilter("gaps")}>
              Gaps
            </button>
            <button type="button" className={`chip ${activeFilter === "ambiguities" ? "chip--active" : ""}`} onClick={() => setActiveFilter("ambiguities")}>
              Ambiguities
            </button>
            <button type="button" className={`chip ${activeFilter === "edge" ? "chip--active" : ""}`} onClick={() => setActiveFilter("edge")}>
              Edge cases
            </button>
          </div>

          {loading && <div className="analysis-empty">Loading latest analysis...</div>}
          {!loading && error && <div className="analysis-empty">{error}</div>}
          {!loading && !error && filteredFindings.length === 0 && <div className="analysis-empty">No findings available.</div>}

          <div className="analysis-finding-list">
            {filteredFindings.map((item, idx) => {
              const sev = (item.severity || "Low").toLowerCase();
              return (
                <article key={`${item.title}-${idx}`} className="finding-card">
                  <div className="finding-badge-row">
                    <span className="finding-type">{item.category || "Finding"}</span>
                    <span className={`finding-impact finding-impact--${sev}`}>{item.severity || "Low"} impact</span>
                  </div>
                  <h3>{item.title}</h3>
                  <p className="finding-summary">{item.detail}</p>
                </article>
              );
            })}
          </div>
        </section>

        <section className="analysis-panel">
          <header className="analysis-panel-header">
            <h2>Coverage & risk map</h2>
            <p>Understand how well requirements map to tests and where risk is concentrated.</p>
          </header>

          <div className="analysis-coverage">
            <h3>Requirement coverage by category</h3>
            <div className="coverage-list">
              {coverageBreakdown.map((row) => {
                const percent = Math.max(0, Math.min(100, Math.round((row.value / row.total) * 100)));
                return (
                  <div key={row.id} className="coverage-row">
                    <div className="coverage-label">
                      <span>{row.label}</span>
                      <span className="coverage-count">{percent}%</span>
                    </div>
                    <div className="coverage-bar">
                      <div className="coverage-bar-fill" style={{ width: `${percent}%` }} />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="analysis-risks">
            <h3>Risk hotspots</h3>
            <div className="risk-list">
              {riskHotspots.length === 0 && <div className="analysis-empty">No hotspots available.</div>}
              {riskHotspots.map((risk, idx) => (
                <div key={`${risk.module}-${idx}`} className="risk-card">
                  <div className="risk-header">
                    <span className="risk-area">{risk.module}</span>
                    <span className={`risk-level risk-level--${(risk.risk || "low").toLowerCase()}`}>
                      {risk.risk}
                    </span>
                  </div>
                  <p className="risk-reason">{risk.reason}</p>
                  <p className="risk-owners">Owner: {risk.owner}</p>
                </div>
              ))}
            </div>
          </div>
        </section>
      </section>

      <section className="analysis-cta">
        <div className="analysis-cta-inner">
          <div>
            <h2>Ready to generate executable tests?</h2>
            <p>Approve the scenario so it becomes available in Test Console and Execution Dashboard.</p>
            {approveMessage && <p style={{ marginTop: 8 }}>{approveMessage}</p>}
          </div>

          <div className="analysis-cta-actions">
            <button className="btn btn-primary" onClick={approveScenario} disabled={approveStatus === "processing"}>
              {approveStatus === "processing" ? "Approving..." : "Send to Test Console"}
            </button>
            <button className="btn btn-outline" onClick={() => window.open(`${API_BASE}/api/analysis/latest`, "_blank")}>
              Export analysis (JSON)
            </button>
          </div>
        </div>
      </section>
    </main>
  );
};

export default AnalysisReview;
