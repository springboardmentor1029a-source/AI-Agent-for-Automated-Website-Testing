import React, { useEffect } from 'react';
import { useTheme } from '../context/ThemeContext';
import '../styles/ReportsPage.css';
import ReportsIcon from '../assets/Rpt.png';

const reportCards = [
  {
    id: 1,
    title: 'Release 24.12 · Full regression',
    type: 'Execution summary',
    createdAt: 'Dec 4, 2025 · 22:11',
    duration: '09:21',
    passRate: '92%',
    status: 'Ready to share',
  },
  {
    id: 2,
    title: 'Smoke · Production checkout',
    type: 'Smoke suite',
    createdAt: 'Dec 3, 2025 · 09:30',
    duration: '00:18',
    passRate: '100%',
    status: 'Green',
  },
  {
    id: 3,
    title: 'API stability · Weekly',
    type: 'API report',
    createdAt: 'Dec 1, 2025 · 18:45',
    duration: '01:07',
    passRate: '88%',
    status: 'Needs attention',
  },
];

const ReportsPage = () => {
  const { theme } = useTheme();

  useEffect(() => {
    document.title = 'Reports - Youval AutoQA';
  }, []);

  const [selectedSuite, setSelectedSuite] = React.useState('All suites');
  const [timeRange, setTimeRange] = React.useState('Last 7 days');

  return (
    <main className={`reports-page app-page--${theme}`}>
      {/* LEFT SIDEBAR - FILTERS */}
      <aside className="page-filters-sidebar">
        <div className="sidebar-title">⏱ Time Range</div>
        <div className="sidebar-filter-group">
          <select
            className="form-select"
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
          >
            <option>Last 7 days</option>
            <option>Last 14 days</option>
            <option>Last 30 days</option>
            <option>Last 90 days</option>
            <option>Custom range</option>
          </select>
        </div>

        <div className="sidebar-title" style={{ marginTop: '20px' }}>
          🏷 Test Suites
        </div>
        <div className="sidebar-filter-group">
          <label>
            <input
              type="checkbox"
              checked={selectedSuite === 'All suites'}
              onChange={() => setSelectedSuite('All suites')}
            />
            All suites
          </label>
          <label>
            <input
              type="checkbox"
              checked={selectedSuite === 'Smoke'}
              onChange={() => setSelectedSuite('Smoke')}
            />
            Smoke
          </label>
          <label>
            <input
              type="checkbox"
              checked={selectedSuite === 'Full regression'}
              onChange={() => setSelectedSuite('Full regression')}
            />
            Full regression
          </label>
          <label>
            <input
              type="checkbox"
              checked={selectedSuite === 'API only'}
              onChange={() => setSelectedSuite('API only')}
            />
            API only
          </label>
        </div>

        <div className="sidebar-filter-group" style={{ marginTop: '20px' }}>
          <button
            className="btn btn-primary btn-sm"
            style={{ width: '100%' }}
          >
            ➕ New custom report
          </button>
        </div>
      </aside>

      {/* MAIN CONTENT AREA */}
      <div className="page-content-area">
        {/* OPTIMIZED HEADER - SINGLE ROW */}
        <header className="page-header-block">
          <div className="page-header-left">
            <div className="page-pill">
              <img src={ReportsIcon} alt="Reports" />
              Reports
            </div>
            <div className="page-header-text">
              <h1>Reports & analytics</h1>
              <p>Test health across releases · Browse execution summaries, trend charts, and export-ready reports for your stakeholders.</p>
            </div>
          </div>
          <div className="page-header-right">
            <button className="btn btn-primary btn-sm">
              📊 Generate report
            </button>
          </div>
        </header>

        {/* METRICS ROW */}
        <section className="page-metrics">
          <div className="page-metrics-grid">
            <div className="page-metric-card">
              <div className="metric-label-lg">Reports generated (30 days)</div>
              <div className="metric-value-lg">34</div>
              <div className="metric-note">Most from scheduled runs</div>
            </div>
            <div className="page-metric-card">
              <div className="metric-label-lg">Average pass rate</div>
              <div className="metric-value-lg">89%</div>
              <div className="metric-note">Across all environments</div>
            </div>
            <div className="page-metric-card">
              <div className="metric-label-lg">Teams consuming reports</div>
              <div className="metric-value-lg">5</div>
              <div className="metric-note">Engineering, QA, Product, Ops, Support</div>
            </div>
          </div>
        </section>

        {/* TWO-COLUMN LAYOUT */}
        <section className="reports-layout">
          {/* LEFT: Recent Reports List */}
          <div className="reports-list-panel">
            <div className="panel-header">
              <h2>📋 Recent reports</h2>
              <p>Latest execution summaries in {timeRange.toLowerCase()}</p>
            </div>
            <div className="reports-list">
              {reportCards.map((report) => (
                <div key={report.id} className="report-card">
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
                    <span className="report-label">Duration</span>
                    <span className="report-value">{report.duration}</span>
                  </div>
                  <div className="report-row">
                    <span className="report-label">Pass rate</span>
                    <span className="report-value">{report.passRate}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* RIGHT: Preview Panel */}
          <div className="reports-preview-panel">
            <div className="panel-header">
              <h2>✨ Key highlights</h2>
              <p>Insights from recent test runs</p>
            </div>

            <div className="report-preview-card">
              <div className="preview-section">
                <h3>Performance</h3>
                <ul>
                  <li>High-risk checkout areas are fully covered.</li>
                  <li>API error rate remains under 0.5% across the release.</li>
                  <li>Response times improved 12% compared to last sprint.</li>
                </ul>
              </div>

              <div className="preview-section">
                <h3>Quality</h3>
                <ul>
                  <li>Two flaky tests identified and quarantined.</li>
                  <li>Mobile-specific issues resolved in 3 areas.</li>
                  <li>Test coverage increased to 89% on core modules.</li>
                </ul>
              </div>

              <div className="preview-section">
                <h3>Exports</h3>
                <div className="preview-actions">
                  <button className="btn btn-secondary btn-sm">
                    📄 PDF
                  </button>
                  <button className="btn btn-secondary btn-sm">
                    📊 Excel
                  </button>
                  <button className="btn btn-secondary btn-sm">
                    ⚙ JSON
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
};

export default ReportsPage;
