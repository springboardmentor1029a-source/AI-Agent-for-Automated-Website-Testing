import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import '../styles/HowItWorks.css';

// Hero background
import WaaveBg from '../assets/waave.avif';

// Step images (all from assets)
import InputImg from '../assets/upload-illustration.png';
import AnalysisImg from '../assets/AI.png';
import ReviewImg from '../assets/Approval.png';
import ExecutionImg from '../assets/steps-flow.png';
import ReportingImg from '../assets/Rpt.png';
import RegressionImg from '../assets/web_spiral.avif';

// Technology stack images (icons from /src/icons)
import LLMIcon from '../assets/blue.png';
import PlaywrightIcon from '../assets/icons/Testing.png';
import PostgresIcon from '../assets/blue-space.avif';

const STEPS = [
  {
    id: 'input',
    title: 'Input',
    bullets: [
      'Capture requirements via plain text, documents, or file bundles.',
      'Assign inputs to projects, modules, and releases for context.',
      'Tag scope, priority, and owners for clear traceability.'
    ],
    link: '/data-input',
    image: InputImg
  },
  {
    id: 'analysis',
    title: 'AI Analysis',
    bullets: [
      'Parse requirements into structured flows and scenarios.',
      'Detect gaps, edge cases, and ambiguous statements.',
      'Recommend coverage across test types and risk areas.'
    ],
    link: '/analysis-review',
    image: AnalysisImg
  },
  {
    id: 'review',
    title: 'Review & Approval',
    bullets: [
      'Review AI generated test cases with full context.',
      'Refine steps, data, and assertions directly in the UI.',
      'Approve into reusable suites that stay versioned.'
    ],
    link: '/analysis-review',
    image: ReviewImg
  },
  {
    id: 'execution',
    title: 'Test Execution',
    bullets: [
      'Run suites on your preferred environments and browsers.',
      'Monitor execution status, flakiness, and bottlenecks in real time.',
      'Capture screenshots, network traces, and console logs.'
    ],
    link: '/execution-dashboard',
    image: ExecutionImg
  },
  {
    id: 'reporting',
    title: 'Reporting',
    bullets: [
      'See pass rate, duration, and coverage at a glance.',
      'Drill down into specific runs, tests, and step results.',
      'Share exports with stakeholders in consistent formats.'
    ],
    link: '/reports',
    image: ReportingImg
  },
  {
    id: 'regression',
    title: 'Regression',
    bullets: [
      'Curate suites that protect your highest value journeys.',
      'Surface candidates from recent failures and incidents.',
      'Compare behaviour before and after important fixes.'
    ],
    link: '/regression-center',
    image: RegressionImg
  }
];

const HowItWorks = () => {
  const { theme } = useTheme();
  const [activeId, setActiveId] = useState('input');

  useEffect(() => {
    document.title = 'How It Works - Youval AutoQA';
  }, []);

  const activeStep = STEPS.find((s) => s.id === activeId) || STEPS[0];

  return (
    <main className={`hiw-page hiw-page--${theme}`}>
      {/* Hero with waave background and white italic text */}
      <section
        className="hiw-hero"
        style={{ backgroundImage: `url(${WaaveBg})` }}
      >
        <div className="hiw-hero-layer" />
        <div className="hiw-hero-inner">
          <h1>How It Works</h1>
          <p>
            A clear, six step flow from raw requirements to dependable
            regression intelligence.
          </p>
        </div>
      </section>

      {/* Stepper: left = tabs, right = text + image */}
      <section className="hiw-stepper">
        <div className="hiw-stepper-nav-column">
          {STEPS.map((step, index) => (
            <button
              key={step.id}
              type="button"
              className={
                'hiw-stepper-tab' +
                (step.id === activeId ? ' hiw-stepper-tab--active' : '')
              }
              onClick={() => setActiveId(step.id)}
            >
              <span className="hiw-step-index">{index + 1}</span>
              <span className="hiw-step-title">{step.title}</span>
            </button>
          ))}
        </div>

        <div className="hiw-stepper-panel">
          <div className="hiw-step-panel-layout">
            <div className="hiw-step-text">
              <h2>{activeStep.title}</h2>
              <ul>
                {activeStep.bullets.map((line) => (
                  <li key={line}>{line}</li>
                ))}
              </ul>
              <Link to={activeStep.link} className="hiw-view-link">
                View in App
              </Link>
            </div>

            <div className="hiw-step-image-card">
              <img src={activeStep.image} alt={activeStep.title} />
              <div className="hiw-step-image-caption">
                <span className="hiw-step-image-label">Current Step</span>
                <span className="hiw-step-image-title">
                  {activeStep.title}
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Technology stack with larger rectangular images */}
      <section className="hiw-tech">
        <h2>Technology Stack</h2>
        <div className="hiw-tech-grid">
          <div className="hiw-tech-card">
            <div className="hiw-tech-image-wrap">
              <img src={LLMIcon} alt="LLM" />
            </div>
            <h3>LLM</h3>
            <p>
              Understands natural language requirements and converts them into
              structured, testable artefacts.
            </p>
          </div>

          <div className="hiw-tech-card">
            <div className="hiw-tech-image-wrap">
              <img src={PlaywrightIcon} alt="Playwright" />
            </div>
            <h3>Playwright</h3>
            <p>
              Powers browser based execution with fast, resilient automation for
              modern web applications.
            </p>
          </div>

          <div className="hiw-tech-card">
            <div className="hiw-tech-image-wrap">
              <img src={PostgresIcon} alt="PostgreSQL" />
            </div>
            <h3>PostgreSQL</h3>
            <p>
              Stores projects, runs, test cases, and metrics with strong data
              integrity and history.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
};

export default HowItWorks;
