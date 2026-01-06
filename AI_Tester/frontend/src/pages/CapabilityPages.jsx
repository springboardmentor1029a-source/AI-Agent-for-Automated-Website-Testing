import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import '../styles/CapabilityPages.css';

// Icons from /src/icons (under assets/icons)
import InputIcon from '../assets/icons/Requirements.png';
import AnalysisIcon from '../assets/icons/Process.png';
import ExecutionIcon from '../assets/icons/Testing.png';
import ReportingIcon from '../assets/icons/Interface_Testing.png';
import RegressionIcon from '../assets/icons/Risk.png';
import IntegrationsIcon from '../assets/icons/Deployment.png';

import SmokeIcon from '../assets/icons/Beta_Testing.png';
import SanityIcon from '../assets/icons/Checklist.png';
import UnitIcon from '../assets/icons/Unit_Testing.png';
import IntegrationIcon from '../assets/icons/Integration_Testing.png';
import E2EIcon from '../assets/icons/Navigation_Flow.png';
import APIIcon from '../assets/icons/Code.png';
import UIUXIcon from '../assets/icons/Usability.png';
import PerformanceIcon from '../assets/icons/Performance_Testing.png';
import SecurityIcon from '../assets/icons/Security_Testing.png';
import RegressionTypeIcon from '../assets/icons/Risk.png';

const capabilityCards = [
  {
    id: 'input',
    title: 'Input',
    description: 'Ingest requirements from text, documents, or file bundles with full project context.',
    icon: InputIcon,
    to: '/data-input'
  },
  {
    id: 'analysis',
    title: 'AI Analysis',
    description: 'Transform natural language into structured scenarios, gaps, and coverage insights.',
    icon: AnalysisIcon,
    to: '/analysis-review'
  },
  {
    id: 'execution',
    title: 'Execution',
    description: 'Run suites across browsers and environments with live status and rich artifacts.',
    icon: ExecutionIcon,
    to: '/execution-dashboard'
  },
  {
    id: 'reporting',
    title: 'Reporting',
    description: 'Track pass rate, duration, and coverage with exportable analytics and trends.',
    icon: ReportingIcon,
    to: '/reports'
  },
  {
    id: 'regression',
    title: 'Regression',
    description: 'Protect critical journeys with curated suites, impact insights, and baselines.',
    icon: RegressionIcon,
    to: '/regression-center'
  },
  {
    id: 'integrations',
    title: 'Integrations',
    description: 'Connect issue trackers, CI/CD, and collaboration tools into a unified workflow.',
    icon: IntegrationsIcon,
    to: '/settings'
  }
];

const testingTypes = [
  { id: 'smoke', label: 'Smoke', icon: SmokeIcon },
  { id: 'sanity', label: 'Sanity', icon: SanityIcon },
  { id: 'unit', label: 'Unit', icon: UnitIcon },
  { id: 'integration', label: 'Integration', icon: IntegrationIcon },
  { id: 'e2e', label: 'E2E', icon: E2EIcon },
  { id: 'api', label: 'API', icon: APIIcon },
  { id: 'uiux', label: 'UI / UX', icon: UIUXIcon },
  { id: 'performance', label: 'Performance', icon: PerformanceIcon },
  { id: 'security', label: 'Security', icon: SecurityIcon },
  { id: 'regression', label: 'Regression', icon: RegressionTypeIcon }
];

const CapabilityPages = () => {
  const { theme } = useTheme();

  useEffect(() => {
    document.title = 'Capabilities - Youval AutoQA';
  }, []);

  return (
    <main className={`cap-page cap-page--${theme}`}>
      {/* Header */}
      <header className="cap-header">
        <h1>Capability Matrix</h1>
        <p>
          Explore how Youval AutoQA covers every part of the testing lifecycle,
          from inputs and AI analysis to execution, reporting, and regression.
        </p>
      </header>

      {/* Capability Matrix */}
      <section className="cap-matrix">
        <div className="cap-matrix-grid">
          {capabilityCards.map((card) => (
            <article key={card.id} className="cap-card">
              <div className="cap-card-icon-wrap">
                <img src={card.icon} alt={card.title} />
              </div>
              <h2>{card.title}</h2>
              <p>{card.description}</p>
              <Link to={card.to} className="cap-card-btn">
                Go to Module
              </Link>
            </article>
          ))}
        </div>
      </section>

      {/* Testing Types */}
      <section className="cap-testing">
        <header className="cap-section-header">
          <h2>Testing Types</h2>
          <p>
            Support for a wide spectrum of functional, non-functional, and
            workflow-focused testing styles.
          </p>
        </header>

        <div className="cap-testing-grid">
          {testingTypes.map((item) => (
            <div key={item.id} className="cap-testing-chip">
              <div className="cap-testing-icon">
                <img src={item.icon} alt={item.label} />
              </div>
              <span className="cap-testing-label">{item.label}</span>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
};

export default CapabilityPages;
