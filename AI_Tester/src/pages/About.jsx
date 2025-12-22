import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import '../styles/About.css';

// Background image for hero
import HeroBg from '../assets/hero-bg.jpg';

// Icons from /src/icons
import QAIcon from '../assets/icons/Testing.png';
import DevIcon from '../assets/icons/Code.png';
import PMIcon from '../assets/icons/Requirements.png';
import DevOpsIcon from '../assets/icons/Deployment.png';
import TeamIcon from '../assets/icons/Goal.png';

const whoBlocks = [
  {
    id: 'qa',
    title: 'QA Engineers',
    description:
      'Transform manual test cases into AI-generated suites with full traceability and faster feedback.',
    icon: QAIcon
  },
  {
    id: 'devs',
    title: 'Developers',
    description:
      'Shift testing left with natural language test definitions that stay close to the codebase.',
    icon: DevIcon
  },
  {
    id: 'pm',
    title: 'Product Managers',
    description:
      'Express acceptance criteria in plain English and see them validated automatically in every release.',
    icon: PMIcon
  },
  {
    id: 'devops',
    title: 'DevOps',
    description:
      'Embed intelligent test execution into your pipelines without adding maintenance overhead.',
    icon: DevOpsIcon
  },
  {
    id: 'teams',
    title: 'Product Teams',
    description:
      'Align engineering, QA, and product on a shared view of quality, risk, and coverage.',
    icon: TeamIcon
  }
];

const roadmap = [
  {
    id: 'v1',
    label: 'v1',
    title: 'Requirements → Tests Engine',
    timeframe: 'Shipped',
    summary:
      'Turn natural language requirements into structured test cases with coverage mapping.'
  },
  {
    id: 'v2',
    label: 'v2',
    title: 'AI Execution Engine',
    timeframe: 'In Use',
    summary:
      'Smart orchestration that selects, schedules, and optimizes test runs for each change.'
  },
  {
    id: 'v3',
    label: 'v3',
    title: 'Cross-browser Grid',
    timeframe: 'Next',
    summary:
      'Scale execution across browsers and devices with built-in flakiness detection.'
  },
  {
    id: 'v4',
    label: 'v4',
    title: 'Integrations Hub',
    timeframe: 'Planned',
    summary:
      'Deep links into issue trackers, CI/CD, and communication tools for end-to-end workflows.'
  },
  {
    id: 'v5',
    label: 'v5',
    title: 'Autonomous Regression',
    timeframe: 'Vision',
    summary:
      'Continuously learns which tests to run based on real usage, change history, and risk.'
  }
];

const About = () => {
  const { theme } = useTheme();

  useEffect(() => {
    document.title = 'About Us - Youval AutoQA';
  }, []);

  return (
    <main className={`about-page about-page--${theme}`}>
      {/* Our Vision */}
      <section
        className="about-hero"
        style={{ backgroundImage: `url(${HeroBg})` }}
      >
        <div className="about-hero-layer" />
        <div className="about-hero-inner">
          <div className="about-hero-chip">About Youval AutoQA</div>
          <h1>Our Vision</h1>
          <p>
            Youval AutoQA exists to make high-quality software delivery the
            default, not a luxury.
          </p>
          <p>
            By combining natural language understanding with intelligent
            execution, the platform turns everyday requirements into living
            regression suites that keep pace with change.
          </p>
          <p>
            The goal is simple: testing that feels invisible, reliable, and
            deeply aligned with how modern teams actually build products.
          </p>
        </div>
      </section>

      {/* Who This Is For */}
      <section className="about-who">
        <header className="about-section-header">
          <h2>Who This Is For</h2>
          <p>
            Youval AutoQA supports the entire delivery chain, from idea to
            production, with shared quality signals.
          </p>
        </header>
        <div className="about-who-grid">
          {whoBlocks.map((item) => (
            <article key={item.id} className="about-who-card">
              <div className="about-who-icon-wrap">
                <img src={item.icon} alt={item.title} />
              </div>
              <h3>{item.title}</h3>
              <p>{item.description}</p>
            </article>
          ))}
        </div>
      </section>

      {/* Architecture Overview */}
      <section className="about-architecture">
        <header className="about-section-header">
          <h2>Architecture Overview</h2>
          <p>
            A modular, AI-first architecture that connects your inputs to
            reliable, repeatable test execution.
          </p>
        </header>

        <div className="about-arch-diagram">
          <div className="about-arch-layer">
            <span className="about-arch-label">Input Layer</span>
            <span className="about-arch-desc">
              Requirements, specs, and production signals ingested in any format.
            </span>
          </div>
          <div className="about-arch-layer">
            <span className="about-arch-label">AI Analysis Engine</span>
            <span className="about-arch-desc">
              Understands intent, extracts scenarios, and maps coverage.
            </span>
          </div>
          <div className="about-arch-layer">
            <span className="about-arch-label">Execution Engine</span>
            <span className="about-arch-desc">
              Orchestrates parallel runs across browsers, devices, and
              environments.
            </span>
          </div>
          <div className="about-arch-layer">
            <span className="about-arch-label">Reporting</span>
            <span className="about-arch-desc">
              Surfaces pass rate, duration, and risk in a single unified view.
            </span>
          </div>
          <div className="about-arch-layer">
            <span className="about-arch-label">Regression Intelligence</span>
            <span className="about-arch-desc">
              Learns over time which tests protect the journeys that matter most.
            </span>
          </div>
        </div>
      </section>

      {/* Roadmap */}
      <section className="about-roadmap">
        <header className="about-section-header">
          <h2>Product Roadmap</h2>
          <p>
            A focused sequence of versions that gradually moves from assisted to
            autonomous quality.
          </p>
        </header>

        <div className="about-roadmap-timeline">
          {roadmap.map((item) => (
            <article key={item.id} className="about-roadmap-card">
              <div className="about-roadmap-dot" />
              <div className="about-roadmap-body">
                <div className="about-roadmap-meta">
                  <span className="about-roadmap-version">{item.label}</span>
                  <span className="about-roadmap-time">{item.timeframe}</span>
                </div>
                <h3>{item.title}</h3>
                <p>{item.summary}</p>
              </div>
            </article>
          ))}
        </div>
      </section>

      {/* Technical docs CTA */}
      <section className="about-docs">
        <div className="about-docs-inner">
          <div>
            <h2>Documentation and Guides</h2>
            <p>
              Explore integration patterns, deployment options, and API
              references to adapt Youval AutoQA to your environment.
            </p>
          </div>
          <Link to="/contact" className="about-docs-btn">
            View Technical Docs
          </Link>
        </div>
      </section>
    </main>
  );
};

export default About;
