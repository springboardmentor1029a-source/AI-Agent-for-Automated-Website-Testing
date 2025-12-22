import React, { useEffect } from 'react';
import { useTheme } from '../context/ThemeContext';
import '../styles/SettingsPage.css';

import SettingsIcon from '../assets/icons/Setting.png';

const SettingsPage = () => {
  const { theme } = useTheme();

  useEffect(() => {
    document.title = 'Settings - Youval AutoQA';
  }, []);

  return (
    <main className={`settings-page app-page--${theme}`}>
      <header className="page-header-block">
        <div className="page-header-left">
          <span className="page-pill">
            <img src={SettingsIcon} alt="Settings" />
            Workspace settings
          </span>
          <h1>Configure your AutoQA workspace</h1>
          <p>Manage profile, notifications, and integrations for this project.</p>
        </div>
      </header>

      <section className="settings-layout">
        <section className="settings-panel">
          <header className="panel-header">
            <h2>Profile</h2>
            <p>Basic information used across reports and notifications.</p>
          </header>
          <div className="settings-section">
            <label className="field-label" htmlFor="name">
              Full name
            </label>
            <input id="name" className="form-input" placeholder="Your name" />
          </div>
          <div className="settings-section">
            <label className="field-label" htmlFor="email">
              Email for alerts
            </label>
            <input
              id="email"
              type="email"
              className="form-input"
              placeholder="you@example.com"
            />
          </div>
        </section>

        <section className="settings-panel">
          <header className="panel-header">
            <h2>Notifications & integrations</h2>
            <p>Where and how you receive execution updates.</p>
          </header>

          <div className="toggle-row">
            <div>
              <p className="toggle-title">Email summaries</p>
              <p className="toggle-sub">
                Send daily summary reports when executions are active.
              </p>
            </div>
            <label className="switch">
              <input type="checkbox" defaultChecked />
              <span className="slider" />
            </label>
          </div>

          <div className="toggle-row">
            <div>
              <p className="toggle-title">Slack notifications</p>
              <p className="toggle-sub">
                Post execution status to a selected Slack channel.
              </p>
            </div>
            <label className="switch">
              <input type="checkbox" />
              <span className="slider" />
            </label>
          </div>

          <div className="settings-section">
            <label className="field-label" htmlFor="jira">
              Jira project key
            </label>
            <input
              id="jira"
              className="form-input"
              placeholder="e.g. WEB or QA"
            />
          </div>
        </section>
      </section>
    </main>
  );
};

export default SettingsPage;
