import React, { useEffect, useState } from 'react';
import { useTheme } from '../context/ThemeContext';
import '../styles/AnalysisReview.css';

// Optional icons reusing your existing assets
import RequirementsIcon from '../assets/icons/Requirements.png';
import RiskIcon from '../assets/icons/Risk.png';
import ChecklistIcon from '../assets/icons/Checklist.png';
import CodeIcon from '../assets/icons/Code.png';
import GoalIcon from '../assets/icons/Goal.png';

const aiFindings = [
  {
    id: 1,
    type: 'Missing Scenario',
    category: 'gaps',
    title: 'No coverage for password reset flow',
    impact: 'High',
    area: 'Authentication',
    summary:
      'Requirements mention password reset but no test scenarios were generated for email link expiry or invalid token handling.',
    tags: ['Gap', 'Auth', 'Regression'],
  },
  {
    id: 2,
    type: 'Ambiguous Requirement',
    category: 'ambiguities',
    title: 'Unclear behavior on partial payment failure',
    impact: 'Medium',
    area: 'Billing',
    summary:
      'Spec does not define expected behavior when card is approved but wallet fails, leading to inconsistent states.',
    tags: ['Clarification', 'Billing'],
  },
  {
    id: 3,
    type: 'Edge Case',
    category: 'edge',
    title: 'Boundary not defined for date filters',
    impact: 'Low',
    area: 'Reporting',
    summary:
      'Start and end date inclusivity is not explicitly stated, which may cause off-by-one day errors.',
    tags: ['Edge case', 'Reporting'],
  },
];

const coverageBreakdown = [
  { id: 1, label: 'Happy paths', value: 32, total: 40 },
  { id: 2, label: 'Negative paths', value: 18, total: 32 },
  { id: 3, label: 'Edge cases', value: 7, total: 24 },
  { id: 4, label: 'Non-functional', value: 5, total: 18 },
];

const riskHotspots = [
  {
    id: 1,
    area: 'Checkout',
    risk: 'High',
    reason: 'Multiple steps changed in latest release, limited regression coverage.',
    owners: 'Frontend & API',
  },
  {
    id: 2,
    area: 'Login & Sessions',
    risk: 'Medium',
    reason: 'New SSO provider added with partial test coverage.',
    owners: 'Platform',
  },
  {
    id: 3,
    area: 'Reporting',
    risk: 'Low',
    reason: 'Read-only features, minimal change footprint.',
    owners: 'Analytics',
  },
];

const AnalysisReview = () => {
  const { theme } = useTheme();
  const [activeFilter, setActiveFilter] = useState('all');

  useEffect(() => {
    document.title = 'Analysis & Review - Youval AutoQA';
  }, []);

  const filteredFindings =
    activeFilter === 'all'
      ? aiFindings
      : aiFindings.filter((item) => item.category === activeFilter);

  return (
    <main className={`analysis-page analysis-page--${theme}`}>
      {/* Header */}
      <header className="analysis-header">
        <div className="analysis-header-left">
          <span className="analysis-pill">Step 2 · Analysis & Review</span>
          <h1>AI-powered requirement analysis</h1>
          <p>
            Review gaps, risks, and coverage recommendations before committing scenarios
            into your automated suites.
          </p>
          <div className="analysis-header-meta">
            <div className="meta-item">
              <img src={RequirementsIcon} alt="Requirements" />
              <div>
                <span className="meta-label">Requirements parsed</span>
                <span className="meta-value">26 documents</span>
              </div>
            </div>
            <div className="meta-item">
              <img src={ChecklistIcon} alt="Scenarios" />
              <div>
                <span className="meta-label">Scenarios generated</span>
                <span className="meta-value">148 test cases</span>
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
              <span className="summary-score">82%</span>
              <span className="summary-chip summary-chip--good">Stable for release</span>
            </div>
            <ul className="summary-list">
              <li>
                <span>Requirement coverage</span>
                <span>78%</span>
              </li>
              <li>
                <span>High-risk areas covered</span>
                <span>6 / 8</span>
              </li>
              <li>
                <span>Open clarifications</span>
                <span>3</span>
              </li>
            </ul>
          </div>
        </aside>
      </header>

      {/* Metrics row */}
      <section className="analysis-metrics">
        <div className="analysis-metrics-grid">
          <div className="analysis-metric-card">
            <div className="metric-icon metric-icon--risk">
              <img src={RiskIcon} alt="Risk" />
            </div>
            <div>
              <p className="metric-label">Overall risk level</p>
              <p className="metric-value metric-value--high">High</p>
            </div>
            <span className="metric-pill metric-pill--critical">5 critical gaps</span>
          </div>

          <div className="analysis-metric-card">
            <div className="metric-icon">
              <img src={CodeIcon} alt="Change" />
            </div>
            <div>
              <p className="metric-label">Files impacted</p>
              <p className="metric-value">43</p>
            </div>
            <span className="metric-pill">Mapped to 19 modules</span>
          </div>

          <div className="analysis-metric-card">
            <div className="metric-icon">
              <img src={ChecklistIcon} alt="Coverage" />
            </div>
            <div>
              <p className="metric-label">Scenario readiness</p>
              <p className="metric-value">124 / 148</p>
            </div>
            <span className="metric-pill metric-pill--good">24 need review</span>
          </div>
        </div>
      </section>

      {/* Main layout */}
      <section className="analysis-layout">
        {/* Left column: AI findings */}
        <section className="analysis-panel">
          <header className="analysis-panel-header">
            <h2>AI findings</h2>
            <p>Prioritized list of gaps, ambiguities, and edge cases detected by the engine.</p>
          </header>

          <div className="analysis-filter-chips">
            <button
              type="button"
              className={`chip ${activeFilter === 'all' ? 'chip--active' : ''}`}
              onClick={() => setActiveFilter('all')}
            >
              All
            </button>
            <button
              type="button"
              className={`chip ${activeFilter === 'gaps' ? 'chip--active' : ''}`}
              onClick={() => setActiveFilter('gaps')}
            >
              Gaps
            </button>
            <button
              type="button"
              className={`chip ${activeFilter === 'ambiguities' ? 'chip--active' : ''}`}
              onClick={() => setActiveFilter('ambiguities')}
            >
              Ambiguities
            </button>
            <button
              type="button"
              className={`chip ${activeFilter === 'edge' ? 'chip--active' : ''}`}
              onClick={() => setActiveFilter('edge')}
            >
              Edge cases
            </button>
          </div>

          <div className="analysis-finding-list">
            {filteredFindings.map((item) => (
              <article key={item.id} className="finding-card">
                <div className="finding-badge-row">
                  <span className="finding-type">{item.type}</span>
                  <span
                    className={`finding-impact finding-impact--${item.impact.toLowerCase()}`}
                  >
                    {item.impact} impact
                  </span>
                </div>
                <h3>{item.title}</h3>
                <p className="finding-summary">{item.summary}</p>
                <div className="finding-footer">
                  <span className="finding-area">{item.area}</span>
                  <div className="finding-tags">
                    {item.tags.map((tag) => (
                      <span key={tag} className="finding-tag">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              </article>
            ))}
          </div>
        </section>

        {/* Right column: coverage + risks */}
        <section className="analysis-panel">
          <header className="analysis-panel-header">
            <h2>Coverage & risk map</h2>
            <p>Understand how well requirements map to tests and where risk is concentrated.</p>
          </header>

          <div className="analysis-coverage">
            <h3>Requirement coverage by category</h3>
            <div className="coverage-list">
              {coverageBreakdown.map((row) => {
                const percent = Math.round((row.value / row.total) * 100);
                return (
                  <div key={row.id} className="coverage-row">
                    <div className="coverage-label">
                      <span>{row.label}</span>
                      <span className="coverage-count">
                        {row.value} / {row.total}
                      </span>
                    </div>
                    <div className="coverage-bar">
                      <div
                        className="coverage-bar-fill"
                        style={{ width: `${percent}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="analysis-risks">
            <h3>Risk hotspots</h3>
            <div className="risk-list">
              {riskHotspots.map((risk) => (
                <div key={risk.id} className="risk-card">
                  <div className="risk-header">
                    <span className="risk-area">{risk.area}</span>
                    <span
                      className={`risk-level risk-level--${risk.risk.toLowerCase()}`}
                    >
                      {risk.risk}
                    </span>
                  </div>
                  <p className="risk-reason">{risk.reason}</p>
                  <p className="risk-owners">Owners: {risk.owners}</p>
                </div>
              ))}
            </div>
          </div>
        </section>
      </section>

      {/* CTA */}
      <section className="analysis-cta">
        <div className="analysis-cta-inner">
          <div>
            <h2>Ready to generate executable tests?</h2>
            <p>
              Send the reviewed scenarios directly into the Test Console and Execution
              Dashboard with one click.
            </p>
          </div>
          <div className="analysis-cta-actions">
            <button className="btn btn-primary">Send to Test Console</button>
            <button className="btn btn-outline">Export analysis report</button>
          </div>
        </div>
      </section>
    </main>
  );
};

export default AnalysisReview;
