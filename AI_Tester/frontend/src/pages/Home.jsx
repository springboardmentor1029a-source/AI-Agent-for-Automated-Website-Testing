import React from 'react';
import { Link } from 'react-router-dom';

import HeroImg from '../assets/hero-bg.jpg';
import MainImg from '../assets/main.png';

// Non-icon assets for 3D panels
import StepsImg from '../assets/AI_Analysis.png';
import ReportImg from '../assets/report-preview.png';
import UploadIllustration from '../assets/upload-illustration.png';
import AiAvatar from '../assets/ai-agent-avatar.png';
import BlueImg from '../assets/blue.png';
import BlueSpaceImg from '../assets/blue-space.avif';
import WaaveImg from '../assets/waave.avif';
import MarvelImg from '../assets/marvel.avif'; // note: .avif, not .png
import SpiralImg from '../assets/web_spiral.avif';

// Icons for workflow section
import RequirementsIcon from '../assets/icons/Requirements.png';
import AnalyzeIcon from '../assets/icons/Analyze.png';
import TestingIcon from '../assets/icons/Testing.png';
import QualityIcon from '../assets/icons/Quality.png';
import ProcessIcon from '../assets/icons/Process.png';

import '../styles/Home.css';

const FlipCard = ({
  frontImage,
  frontTitle,
  backTitle,
  backLines,
  size = 'grid'
}) => {
  const [flipped, setFlipped] = React.useState(false);

  const regularLines = backLines.filter(
    (line) => !line.startsWith('__QUOTE__')
  );
  const quoteLine = backLines.find((line) => line.startsWith('__QUOTE__'));
  const quoteText = quoteLine ? quoteLine.replace('__QUOTE__', '') : '';

  return (
    <div
      className={`flip-card flip-card--${size} ${
        flipped ? 'is-flipped' : ''
      }`}
      onClick={() => setFlipped((prev) => !prev)}
    >
      <div className="flip-card-inner">
        <div className="flip-card-face flip-card-front">
          {frontImage && (
            <div className="flip-card-image-wrap">
              <img src={frontImage} alt={frontTitle} />
            </div>
          )}
          <h3>{frontTitle}</h3>
        </div>
        <div className="flip-card-face flip-card-back">
          <h3>{backTitle}</h3>
          {regularLines.length > 0 && (
            <ul>
              {regularLines.map((line) => (
                <li key={line}>{line}</li>
              ))}
            </ul>
          )}
          {quoteText && (
            <p className="flip-card-quote">
              <strong>{quoteText}</strong>
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

const Home = () => {
  const workflowSteps = [
    {
      frontImage: RequirementsIcon,
      frontTitle: 'Provide requirements',
      backTitle: 'Provide requirements',
      backLines: [
        'Upload PDF, DOCX, XLSX or ZIP collections',
        'Paste raw requirements or test plans',
        'Associate inputs with projects and releases'
      ]
    },
    {
      frontImage: AnalyzeIcon,
      frontTitle: 'Let AI analyse',
      backTitle: 'AI analysis',
      backLines: [
        'Extract structured test cases via NLP',
        'Highlight gaps, risks and ambiguities',
        'Recommend suitable testing types'
      ]
    },
    {
      frontImage: TestingIcon,
      frontTitle: 'Execute tests',
      backTitle: 'Automated execution',
      backLines: [
        'Run across browsers and environments',
        'Track real-time execution status',
        'Capture logs, screenshots and videos'
      ]
    },
    {
      frontImage: QualityIcon,
      frontTitle: 'Review and refine',
      backTitle: 'Reports and regression',
      backLines: [
        'Inspect detailed execution reports',
        'Convert failures into regression suites',
        'Share results with teams and stakeholders'
      ]
    }
  ];

  const capabilities = [
    {
      frontImage: UploadIllustration,
      frontTitle: 'Multi-format input',
      backTitle: 'Multi-format input',
      backLines: [
        'Support for text, PDF, DOCX, XLSX and ZIP',
        'Centralised storage per project',
        'Connectivity validation for target apps'
      ]
    },
    {
      frontImage: StepsImg,
      frontTitle: 'AI analysis',
      backTitle: 'AI analysis',
      backLines: [
        'Automatic test case extraction',
        'Coverage and completeness checks',
        'Recommendations for test types'
      ]
    },
    {
      frontImage: BlueImg,
      frontTitle: 'Automated execution',
      backTitle: 'Automated execution',
      backLines: [
        'Playwright-based execution engine',
        'Parallel and batch test runs',
        'Environment and browser selection'
      ]
    },
    {
      frontImage: ReportImg,
      frontTitle: 'Reporting',
      backTitle: 'Reporting',
      backLines: [
        'Summary and detailed test reports',
        'Trend and coverage visualisation',
        'PDF, Excel and JSON export options'
      ]
    },
    {
      frontImage: SpiralImg,
      frontTitle: 'Regression management',
      backTitle: 'Regression management',
      backLines: [
        'Identify regression candidates automatically',
        'Build reusable regression suites',
        'Compare before and after test runs'
      ]
    }
  ];

  const metrics = [
    {
      frontImage: BlueSpaceImg,
      frontTitle: 'Time saved',
      backTitle: 'Time saved',
      backLines: [
        'Reduce manual test design effort',
        'Generate documentation automatically',
        'Shorten feedback cycles for each release'
      ]
    },
    {
      frontImage: MarvelImg,
      frontTitle: 'Accuracy',
      backTitle: 'Accuracy',
      backLines: [
        'Enforce consistent test structures',
        'Lower risk of missing critical flows',
        'Use AI validation to catch gaps early'
      ]
    },
    {
      frontImage: WaaveImg,
      frontTitle: 'Coverage improvement',
      backTitle: 'Coverage improvement',
      backLines: [
        'Visualise coverage at project level',
        'Track progression across sprints',
        'Link tests to requirements and risks'
      ]
    }
  ];

  return (
    <div className="home">
      {/* HERO */}
      <section
        className="hero-section"
        style={{ backgroundImage: `url(${HeroImg})` }}
      >
        <div className="hero-overlay" />
        <div className="hero-layout">
          <div className="hero-text">
            <h1>AI-powered test automation from requirements to reports</h1>
            <p className="hero-subtitle">
              Youval AutoQA converts your project documentation into executable
              tests, orchestrates automated execution, and delivers clear
              reports for every release.
            </p>
            <div className="hero-buttons hero-buttons--stacked">
              <Link to="/data-input" className="btn btn--primary btn--lg">
                Start a New Test Session
              </Link>
              <Link to="/how-it-works" className="btn btn--outline btn--lg">
                How It Works
              </Link>
            </div>
          </div>

          {/* Right side: only 3D panel now */}
          <div className="hero-right">
            <div className="hero-visual">
              <FlipCard
                size="hero"
                frontImage={MainImg}
                frontTitle="Your AI test automation co-pilot"
                backTitle="Designed for modern QA teams"
                backLines={[
                  'Surface high-value tests from real documentation.',
                  'Keep execution and reporting fully traceable.',
                  'Support collaborative workflows across QA and development.',
                  '__QUOTE__A disciplined mind turns uncertainty into understanding. Even the smallest inconsistency can light the path to improvement. True progress is shaped by careful reflection.'
                ]}
              />
            </div>
          </div>
        </div>
      </section>

      {/* WORKFLOW */}
      <section className="workflow-section">
        <div className="container">
          <h2>From requirements to executable tests</h2>
          <div className="workflow-grid">
            {workflowSteps.map((step) => (
              <FlipCard
                key={step.frontTitle}
                frontImage={step.frontImage}
                frontTitle={step.frontTitle}
                backTitle={step.backTitle}
                backLines={step.backLines}
              />
            ))}
          </div>
        </div>
      </section>

      {/* CAPABILITIES */}
      <section className="capabilities-section">
        <div className="container">
          <h2>Key capabilities in one platform</h2>
          <div className="capabilities-grid">
            {capabilities.map((capability) => (
              <FlipCard
                key={capability.frontTitle}
                frontImage={capability.frontImage}
                frontTitle={capability.frontTitle}
                backTitle={capability.backTitle}
                backLines={capability.backLines}
              />
            ))}
          </div>
        </div>
      </section>

      {/* METRICS */}
      <section className="metrics-section">
        <div className="container">
          <h2>Measurable impact for your testing process</h2>
          <div className="metrics-grid">
            {metrics.map((metric) => (
              <FlipCard
                key={metric.frontTitle}
                frontImage={metric.frontImage}
                frontTitle={metric.frontTitle}
                backTitle={metric.backTitle}
                backLines={metric.backLines}
              />
            ))}
          </div>
        </div>
      </section>

      {/* PERSONAS */}
      <section className="personas-section">
        <div className="container">
          <h2>Who is Youval AutoQA for?</h2>
          <div className="personas-grid">
            <div className="persona-card">
              <h3>QA engineers</h3>
              <p>
                Accelerate test design, maintain stronger coverage, and manage
                regression suites with AI support.
              </p>
            </div>
            <div className="persona-card">
              <h3>Test leads and managers</h3>
              <p>
                Approve suites, monitor execution health, and communicate
                quality status with reports and dashboards.
              </p>
            </div>
            <div className="persona-card">
              <h3>Developers</h3>
              <p>
                Reproduce failures quickly, validate fixes with focused
                regression runs, and keep quality signals close to the codebase.
              </p>
            </div>
            <div className="persona-card">
              <h3>Product owners and PMs</h3>
              <p>
                Ensure critical journeys stay protected and inform
                release-readiness decisions with transparent test results.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* BOTTOM CTA */}
      <section className="cta-section">
        <div className="container">
          <h2>Ready to discuss your testing strategy?</h2>
          <p>
            Connect with the Youval AutoQA team for onboarding support,
            implementation guidance and tailored demonstrations for your
            projects.
          </p>
          <div className="cta-actions">
            <Link to="/contact" className="btn btn--outline btn--lg cta-btn">
              Contact Us
            </Link>
            <Link to="/data-input" className="btn btn--primary btn--lg cta-btn">
              Start a New Test Session
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
