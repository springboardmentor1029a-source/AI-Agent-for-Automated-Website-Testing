import React, { useEffect } from 'react';
import { useTheme } from '../context/ThemeContext';
import '../styles/TestConsolePage.css';

import ConsoleIcon from '../assets/icons/Env.png';

const TestConsolePage = () => {
  const { theme } = useTheme();

  useEffect(() => {
    document.title = 'Test Console - Youval AutoQA';
  }, []);

  return (
    <main className={`test-console-page app-page--${theme}`}>
      <header className="page-header-block page-header-center">
        <span className="page-pill">
          <img src={ConsoleIcon} alt="Console" />
          Test Console
        </span>
        <h1>Experiment, tweak, and run tests</h1>
        <p>
          Paste or edit scenarios, choose environments, and trigger executions without
          leaving your browser.
        </p>
      </header>

      <section className="console-layout">
        <section className="console-panel">
          <header className="panel-header">
            <h2>Input & configuration</h2>
            <p>Provide or adjust test content before executing.</p>
          </header>

          <div className="console-section">
            <label className="field-label" htmlFor="scenario">
              Test scenario input
            </label>
            <textarea
              id="scenario"
              className="console-textarea"
              placeholder="Describe the flow you want to test, or paste a generated scenario here..."
              rows={10}
            />
            <div className="field-hint">Supports plain text, Gherkin, and JSON.</div>
          </div>

          <div className="console-grid-2">
            <div className="console-section">
              <label className="field-label" htmlFor="env">
                Environment
              </label>
              <select id="env" className="form-select">
                <option>Staging · Chrome</option>
                <option>Staging · Firefox</option>
                <option>Production · Smoke only</option>
              </select>
            </div>
            <div className="console-section">
              <label className="field-label" htmlFor="runType">
                Run type
              </label>
              <select id="runType" className="form-select">
                <option>Dry run (no side effects)</option>
                <option>Full execution</option>
                <option>Debug single step</option>
              </select>
            </div>
          </div>

          <div className="console-actions">
            <button className="btn btn-primary btn-lg">Run in console</button>
            <button className="btn btn-outline btn-lg">Save as template</button>
          </div>
        </section>

        <section className="console-panel">
          <header className="panel-header">
            <h2>Preview & last run</h2>
            <p>Quick feedback on the most recent console execution.</p>
          </header>

          <div className="console-preview-card">
            <div className="preview-row">
              <span className="preview-label">Last run ID</span>
              <span className="preview-value">CONSOLE-2025.12.06-001</span>
            </div>
            <div className="preview-row">
              <span className="preview-label">Status</span>
              <span className="preview-badge preview-badge--success">
                Passed · 12 assertions
              </span>
            </div>
            <div className="preview-row">
              <span className="preview-label">Duration</span>
              <span className="preview-value">00:19</span>
            </div>
            <div className="preview-log">
              <h3>Key steps executed</h3>
              <ul>
                <li>Open /login and authenticate test user.</li>
                <li>Navigate to /checkout with 2 items in cart.</li>
                <li>Apply coupon and verify discount amount.</li>
                <li>Complete payment and validate success receipt.</li>
              </ul>
            </div>
          </div>
        </section>
      </section>
    </main>
  );
};

export default TestConsolePage;
