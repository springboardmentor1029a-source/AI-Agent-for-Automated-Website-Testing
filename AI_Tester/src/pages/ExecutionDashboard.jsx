import React, { useEffect } from 'react';
import { useTheme } from '../context/ThemeContext';
import '../styles/ExecutionDashboard.css';

// Optional icons – adjust paths or replace with your own
import PlayIcon from '../assets/icons/Play.png';
import ClockIcon from '../assets/icons/Clock.png';
import PassIcon from '../assets/icons/Pass.png';
import FailIcon from '../assets/icons/Fail.png';
import EnvIcon from '../assets/icons/Env.png';

const metricCards = [
  {
    id: 1,
    label: 'Total tests in run',
    value: '184',
    subLabel: 'Current execution batch',
  },
  {
    id: 2,
    label: 'Pass rate (last 24h)',
    value: '92%',
    subLabel: 'Stable across 6 runs',
  },
  {
    id: 3,
    label: 'Average duration',
    value: '08:34',
    subLabel: 'Per full regression',
  },
  {
    id: 4,
    label: 'Flaky tests detected',
    value: '7',
    subLabel: 'Auto-retired candidates',
  },
];

const activeRun = {
  id: 'RUN-2025.12.06-004',
  status: 'Running',
  startedAt: '12:41 IST',
  progress: 68,
  passed: 112,
  failed: 9,
  pending: 63,
};

const envSummary = [
  { id: 1, name: 'Chrome · Staging', status: 'Healthy', tests: 96 },
  { id: 2, name: 'Firefox · Staging', status: 'Degraded', tests: 52 },
  { id: 3, name: 'API · Sandbox', status: 'Healthy', tests: 36 },
];

const recentRuns = [
  {
    id: 'RUN-2025.12.05-003',
    env: 'Chrome · Staging',
    started: 'Dec 5 · 22:11',
    duration: '09:21',
    total: 176,
    passed: 162,
    failed: 8,
    status: 'Passed',
  },
  {
    id: 'RUN-2025.12.05-002',
    env: 'Firefox · Staging',
    started: 'Dec 5 · 18:03',
    duration: '07:48',
    total: 152,
    passed: 131,
    failed: 15,
    status: 'Failed',
  },
  {
    id: 'RUN-2025.12.04-001',
    env: 'API · Sandbox',
    started: 'Dec 4 · 16:29',
    duration: '05:12',
    total: 98,
    passed: 95,
    failed: 3,
    status: 'Passed',
  },
];

const ExecutionDashboard = () => {
  const { theme } = useTheme();

  useEffect(() => {
    document.title = 'Execution Dashboard - Youval AutoQA';
  }, []);

  const activeProgressStyle = {
    width: `${activeRun.progress}%`,
  };

  return (
    <main className={`exec-page exec-page--${theme}`}>
      {/* Header */}
      <header className="exec-header">
        <div className="exec-header-left">
          <span className="exec-pill">Step 3 · Execution Dashboard</span>
          <h1>Live test execution overview</h1>
          <p>
            Track real-time progress, environment health, and key quality metrics for your
            automated test runs.
          </p>

          <div className="exec-header-actions">
            <button className="btn btn-primary exec-header-btn">
              <img src={PlayIcon} alt="Run" className="btn-icon" />
              Start new run
            </button>
            <button className="btn btn-outline exec-header-btn">
              <img src={ClockIcon} alt="Schedule" className="btn-icon" />
              Schedule nightly run
            </button>
          </div>
        </div>

        <aside className="exec-header-right">
          <div className="exec-summary-card">
            <div className="exec-summary-header">
              <div className="exec-summary-labels">
                <span className="summary-pill">Active run</span>
                <span className="summary-id">{activeRun.id}</span>
              </div>
              <span className={`summary-status summary-status--${activeRun.status.toLowerCase()}`}>
                {activeRun.status}
              </span>
            </div>

            <div className="exec-summary-main">
              <div className="summary-progress">
                <div className="summary-progress-bar">
                  <div
                    className="summary-progress-fill"
                    style={activeProgressStyle}
                  />
                </div>
                <div className="summary-progress-meta">
                  <span>{activeRun.progress}% complete</span>
                  <span>Started at {activeRun.startedAt}</span>
                </div>
              </div>

              <div className="summary-breakdown">
                <div className="summary-breakdown-item">
                  <img src={PassIcon} alt="Passed" />
                  <div>
                    <span className="breakdown-label">Passed</span>
                    <span className="breakdown-value">{activeRun.passed}</span>
                  </div>
                </div>
                <div className="summary-breakdown-item">
                  <img src={FailIcon} alt="Failed" />
                  <div>
                    <span className="breakdown-label">Failed</span>
                    <span className="breakdown-value breakdown-value--danger">
                      {activeRun.failed}
                    </span>
                  </div>
                </div>
                <div className="summary-breakdown-item">
                  <img src={ClockIcon} alt="Pending" />
                  <div>
                    <span className="breakdown-label">Pending</span>
                    <span className="breakdown-value">{activeRun.pending}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </aside>
      </header>

      {/* Metrics row */}
      <section className="exec-metrics">
        <div className="exec-metrics-grid">
          {metricCards.map((card) => (
            <article key={card.id} className="exec-metric-card">
              <p className="exec-metric-label">{card.label}</p>
              <p className="exec-metric-value">{card.value}</p>
              <p className="exec-metric-sublabel">{card.subLabel}</p>
            </article>
          ))}
        </div>
      </section>

      {/* Main layout */}
      <section className="exec-layout">
        {/* Left: run controls + live log */}
        <section className="exec-panel">
          <header className="exec-panel-header">
            <h2>Run controls & live log</h2>
            <p>Manage the active run and inspect the latest execution events.</p>
          </header>

          <div className="exec-run-actions">
            <button className="btn btn-outline btn-sm">Pause run</button>
            <button className="btn btn-outline btn-sm">Retry failed tests</button>
            <button className="btn btn-outline btn-sm">Stop run</button>
          </div>

          <div className="exec-log">
            <div className="exec-log-header">
              <span>Recent events</span>
              <span className="exec-log-env">Environment · Chrome · Staging</span>
            </div>
            <ul className="exec-log-list">
              <li>
                <span className="log-time">12:44:02</span>
                <span className="log-status log-status--pass">PASS</span>
                <span className="log-message">Checkout · Apply coupon flow</span>
              </li>
              <li>
                <span className="log-time">12:43:51</span>
                <span className="log-status log-status--fail">FAIL</span>
                <span className="log-message">
                  Login · SSO with Google – assertion on redirect URL
                </span>
              </li>
              <li>
                <span className="log-time">12:43:29</span>
                <span className="log-status log-status--pass">PASS</span>
                <span className="log-message">Profile · Update phone number</span>
              </li>
              <li>
                <span className="log-time">12:43:10</span>
                <span className="log-status log-status--pending">PENDING</span>
                <span className="log-message">Reporting · Export last 30 days CSV</span>
              </li>
            </ul>
          </div>
        </section>

        {/* Right: environments + queue */}
        <section className="exec-panel">
          <header className="exec-panel-header">
            <h2>Environments & queue</h2>
            <p>See where tests are running and what is scheduled next.</p>
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
                    <p className="exec-env-tests">{env.tests} tests in batch</p>
                  </div>
                </div>
                <span
                  className={`exec-env-status exec-env-status--${env.status.toLowerCase()}`}
                >
                  {env.status}
                </span>
              </div>
            ))}
          </div>

          <div className="exec-queue">
            <h3>Upcoming runs</h3>
            <ul>
              <li>
                <span className="queue-title">Nightly regression · Staging</span>
                <span className="queue-time">Today · 23:30 IST</span>
              </li>
              <li>
                <span className="queue-title">Smoke tests · Production</span>
                <span className="queue-time">Tomorrow · 07:00 IST</span>
              </li>
            </ul>
          </div>
        </section>
      </section>

      {/* Charts */}
      <section className="exec-charts">
        <div className="exec-charts-grid">
          <article className="exec-chart-card">
            <h3>Pass / fail trend (last 7 runs)</h3>
            <div className="exec-chart-placeholder">
              <span>Embed chart image or component here</span>
            </div>
          </article>

          <article className="exec-chart-card">
            <h3>Duration by environment</h3>
            <div className="exec-chart-placeholder">
              <span>Embed chart image or component here</span>
            </div>
          </article>
        </div>
      </section>

      {/* Results table */}
      <section className="exec-results">
        <div className="exec-results-inner">
          <header className="exec-results-header">
            <h2>Recent runs</h2>
            <p>High-level view of the latest executions across environments.</p>
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
                {recentRuns.map((run) => (
                  <tr key={run.id}>
                    <td>{run.id}</td>
                    <td>{run.env}</td>
                    <td>{run.started}</td>
                    <td>{run.duration}</td>
                    <td>{run.total}</td>
                    <td>{run.passed}</td>
                    <td>{run.failed}</td>
                    <td>
                      <span
                        className={`exec-status-badge exec-status-badge--${run.status.toLowerCase()}`}
                      >
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
