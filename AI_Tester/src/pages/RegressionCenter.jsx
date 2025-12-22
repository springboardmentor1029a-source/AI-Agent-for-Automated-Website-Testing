import React, { useEffect, useState } from 'react';
import { useTheme } from '../context/ThemeContext';
import '../styles/RegressionCenter.css';

import RegressionIcon from '../assets/web_spiral.avif';

const regressionSuites = [
  {
    id: 1,
    name: 'Core web checkout',
    size: '184 tests',
    cadence: 'Nightly',
    owner: 'Web platform',
    lastRun: 'Dec 5 · Passed · 92%',
    passRateBefore: 92,
    passRateAfter: 96,
    durationBefore: '48 min',
    durationAfter: '44 min',
    riskBefore: 'High',
    riskAfter: 'Medium',
  },
  {
    id: 2,
    name: 'Mobile critical path',
    size: '72 tests',
    cadence: 'Pre-release',
    owner: 'Mobile squad',
    lastRun: 'Dec 3 · Failed · 81%',
    passRateBefore: 81,
    passRateAfter: 90,
    durationBefore: '30 min',
    durationAfter: '32 min',
    riskBefore: 'Critical',
    riskAfter: 'High',
  },
  {
    id: 3,
    name: 'API contract',
    size: '54 tests',
    cadence: 'Every commit',
    owner: 'API team',
    lastRun: 'Dec 6 · Passed · 95%',
    passRateBefore: 95,
    passRateAfter: 97,
    durationBefore: '18 min',
    durationAfter: '19 min',
    riskBefore: 'Medium',
    riskAfter: 'Low',
  },
];

const failedTestPool = [
  {
    id: 'T-234',
    name: 'Checkout · Apply coupon',
    area: 'Web checkout',
    impact: 'Revenue',
  },
  {
    id: 'T-411',
    name: 'Mobile · Add to cart',
    area: 'Mobile app',
    impact: 'Conversion',
  },
  {
    id: 'T-089',
    name: 'API · Payment status 500',
    area: 'Payments API',
    impact: 'Stability',
  },
  {
    id: 'T-512',
    name: 'Search · Relevance ranking',
    area: 'Search service',
    impact: 'UX',
  },
];

const RegressionCenter = () => {
  const { theme } = useTheme();

  const [selectedSuiteId, setSelectedSuiteId] = useState(regressionSuites[0].id);
  const [availableTests, setAvailableTests] = useState(failedTestPool);
  const [plannedTests, setPlannedTests] = useState([failedTestPool[0], failedTestPool[2]]);
  const [lastRunMessage, setLastRunMessage] = useState('');

  const selectedSuite = regressionSuites.find((s) => s.id === selectedSuiteId);

  useEffect(() => {
    document.title = 'Regression Center - Youval AutoQA';
  }, []);

  const handleSelectSuite = (id) => {
    setSelectedSuiteId(id);
    setLastRunMessage('');
  };

  const handleAddTest = (testId) => {
    const test = availableTests.find((t) => t.id === testId);
    if (!test) return;
    setAvailableTests((prev) => prev.filter((t) => t.id !== testId));
    setPlannedTests((prev) => [...prev, test]);
  };

  const handleRemoveTest = (testId) => {
    const test = plannedTests.find((t) => t.id === testId);
    if (!test) return;
    setPlannedTests((prev) => prev.filter((t) => t.id !== testId));
    setAvailableTests((prev) => [...prev, test]);
  };

  const handleRunRegression = () => {
    setLastRunMessage(
      `Run scheduled for “${selectedSuite.name}” with ${plannedTests.length} focused tests.`
    );
  };

  return (
    <main className={`regression-page app-page--${theme}`}>
      {/* Header */}
      <header className="regression-header">
        <div className="regression-header-main">
          <span className="page-pill">
            <img src={RegressionIcon} alt="Regression" />
            Regression Center
          </span>
          <h1>Control your regression suites</h1>
          <p>
            Plan focused runs, triage failed tests, and compare behavior before and after your fix.
          </p>
        </div>
        <div className="regression-header-actions">
          <button className="btn btn-outline">View execution history</button>
          <button className="btn btn-primary">Create regression suite</button>
        </div>
      </header>

      {/* Top metrics */}
      <section className="regression-metrics">
        <div className="regression-metrics-grid">
          <article className="reg-metric-card">
            <p className="metric-label-lg">Active regression suites</p>
            <p className="metric-value-lg">7</p>
            <p className="metric-note">Web, mobile, and API</p>
          </article>
          <article className="reg-metric-card">
            <p className="metric-label-lg">Automated coverage</p>
            <p className="metric-value-lg">86%</p>
            <p className="metric-note">High-priority flows</p>
          </article>
          <article className="reg-metric-card">
            <p className="metric-label-lg">Flaky or failed tests</p>
            <p className="metric-value-lg">14</p>
            <p className="metric-note">Ready for triage</p>
          </article>
        </div>
      </section>

      {/* Main planner layout */}
      <section className="regression-layout">
        {/* Left column: suites + failed tests */}
        <section className="reg-panel reg-panel--left">
          <header className="reg-panel-header">
            <h2>Regression suites</h2>
            <p>Select a suite to see its health and plan a focused run.</p>
          </header>

          <div className="suite-list">
            {regressionSuites.map((suite) => (
              <button
                key={suite.id}
                className={`suite-row ${
                  suite.id === selectedSuiteId ? 'suite-row--active' : ''
                }`}
                onClick={() => handleSelectSuite(suite.id)}
              >
                <div className="suite-row-main">
                  <span className="suite-name">{suite.name}</span>
                  <span className="suite-meta">
                    {suite.size} · {suite.cadence}
                  </span>
                </div>
                <div className="suite-row-status">
                  <span className="suite-last-run">{suite.lastRun}</span>
                </div>
              </button>
            ))}
          </div>

          <div className="failed-panel">
            <header className="failed-header">
              <h3>Failed-test candidates</h3>
              <p>Add or remove tests for the next regression run.</p>
            </header>

            <div className="failed-columns">
              <div className="failed-column">
                <h4>Available</h4>
                <ul>
                  {availableTests.length === 0 && (
                    <li className="failed-empty">No more failed tests in backlog.</li>
                  )}
                  {availableTests.map((test) => (
                    <li key={test.id} className="failed-row">
                      <div>
                        <span className="failed-id">{test.id}</span>
                        <span className="failed-name">{test.name}</span>
                        <span className="failed-area">{test.area}</span>
                      </div>
                      <button
                        className="btn btn-outline btn-sm"
                        onClick={() => handleAddTest(test.id)}
                      >
                        Add
                      </button>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="failed-column">
                <h4>In next run</h4>
                <ul>
                  {plannedTests.length === 0 && (
                    <li className="failed-empty">No tests planned yet.</li>
                  )}
                  {plannedTests.map((test) => (
                    <li key={test.id} className="failed-row">
                      <div>
                        <span className="failed-id">{test.id}</span>
                        <span className="failed-name">{test.name}</span>
                        <span className="failed-area">{test.area}</span>
                      </div>
                      <button
                        className="btn btn-outline btn-sm"
                        onClick={() => handleRemoveTest(test.id)}
                      >
                        Remove
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </section>

        {/* Right column: planner + comparison */}
        <section className="reg-panel reg-panel--right">
          <header className="reg-panel-header">
            <h2>Run planner & comparison</h2>
            <p>See how the suite behaves before and after your fix.</p>
          </header>

          {/* Planner strip */}
          <div className="planner-strip">
            <div className="planner-step">
              <span className="planner-label">Step 1</span>
              <p>Pick the regression suite to focus on.</p>
            </div>
            <div className="planner-step">
              <span className="planner-label">Step 2</span>
              <p>Add failed or flaky tests to the next run.</p>
            </div>
            <div className="planner-step">
              <span className="planner-label">Step 3</span>
              <p>Run regression and compare before vs after.</p>
            </div>
          </div>

          {/* Run regression planner */}
          <div className="run-panel">
            <div className="run-panel-main">
              <div>
                <h3>Next run: {selectedSuite.name}</h3>
                <p>
                  {plannedTests.length} focused tests will be executed on top of the full suite.
                </p>
              </div>
              <button className="btn btn-primary btn-lg" onClick={handleRunRegression}>
                Run regression
              </button>
            </div>
            {lastRunMessage && <p className="run-panel-message">{lastRunMessage}</p>}
          </div>

          {/* Before / After comparison */}
          <div className="comparison-panel">
            <div className="comparison-grid">
              <article className="comparison-column comparison-column--before">
                <h3>Before fix</h3>
                <dl className="comparison-metrics">
                  <div>
                    <dt>Pass rate</dt>
                    <dd>{selectedSuite.passRateBefore}%</dd>
                  </div>
                  <div>
                    <dt>Average duration</dt>
                    <dd>{selectedSuite.durationBefore}</dd>
                  </div>
                  <div>
                    <dt>Risk level</dt>
                    <dd>{selectedSuite.riskBefore}</dd>
                  </div>
                </dl>
                <ul className="comparison-notes">
                  <li>Higher volume of failed or flaky tests.</li>
                  <li>Broader impact across {selectedSuite.owner}.</li>
                  <li>More manual verification required.</li>
                </ul>
              </article>

              <article className="comparison-column comparison-column--after">
                <h3>After fix</h3>
                <dl className="comparison-metrics">
                  <div>
                    <dt>Pass rate</dt>
                    <dd>{selectedSuite.passRateAfter}%</dd>
                  </div>
                  <div>
                    <dt>Average duration</dt>
                    <dd>{selectedSuite.durationAfter}</dd>
                  </div>
                  <div>
                    <dt>Risk level</dt>
                    <dd>{selectedSuite.riskAfter}</dd>
                  </div>
                </dl>
                <ul className="comparison-notes">
                  <li>Key failed candidates are re‑run automatically.</li>
                  <li>Risk is reduced for the most changed modules.</li>
                  <li>Signals are ready to share with stakeholders.</li>
                </ul>
              </article>
            </div>

            <div className="comparison-summary">
              <h4>Differences summary</h4>
              <p>
                Pass rate improves from {selectedSuite.passRateBefore}% to{' '}
                {selectedSuite.passRateAfter}% and risk drops from {selectedSuite.riskBefore} to{' '}
                {selectedSuite.riskAfter} for <strong>{selectedSuite.name}</strong>.
              </p>
            </div>
          </div>
        </section>
      </section>
    </main>
  );
};

export default RegressionCenter;
