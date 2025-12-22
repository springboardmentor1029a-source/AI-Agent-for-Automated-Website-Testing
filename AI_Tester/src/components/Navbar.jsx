// src/components/Navbar/index.jsx
import React from 'react';
import { NavLink, Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext.jsx';

// images from assets only
import LogoImg from '../assets/Logo.png';
import SettingIcon from '../assets/icons/Setting.png'; // theme/settings icon

import '../styles/Navbar.css';

const NAV_ITEMS = [
  { path: '/', label: 'Home' },
  { path: '/about', label: 'About' },
  { path: '/how-it-works', label: 'How It Works' },
  { path: '/capability', label: 'Capability' },
  { path: '/data-input', label: 'Data Input' },
  { path: '/analysis-review', label: 'Analysis Review' },
  { path: '/execution-dashboard', label: 'Execution Dashboard' },
  { path: '/reports', label: 'Reports' },
  { path: '/regression-center', label: 'Regression Center' },
  { path: '/test-console', label: 'Test Console' },
  { path: '/settings', label: 'Settings' },
  { path: '/contact', label: 'Contact' }
];

const Navbar = () => {
  const { mode, toggle } = useTheme();

  return (
    <header className="ya-navbar">
      <div className="ya-navbar-inner">
        {/* Left: logo + brand */}
        <div className="ya-nav-left">
          <button
            type="button"
            className="ya-nav-hamburger"
            aria-label="Toggle navigation"
            onClick={() => {
              const menu = document.querySelector('.ya-nav-mobile');
              if (menu) {
                menu.classList.toggle('ya-nav-mobile--open');
              }
            }}
          >
            <span />
            <span />
            <span />
          </button>

          <Link to="/" className="ya-nav-logo">
            <img src={LogoImg} alt="Youval AutoQA logo" />
            <span className="ya-nav-logo-text">
              <span className="ya-nav-logo-main">Youval AutoQA</span>
              <span className="ya-nav-logo-sub">AI Test Assistant</span>
            </span>
          </Link>
        </div>

        {/* Center: desktop nav links */}
        <nav className="ya-nav-center">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                'ya-nav-link' + (isActive ? ' ya-nav-link--active' : '')
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>

        {/* Right: search + theme toggle */}
        <div className="ya-nav-right">
          <form
            className="ya-nav-search"
            onSubmit={(e) => {
              e.preventDefault();
            }}
          >
            <input
              type="search"
              placeholder="Search tests, runs, reports"
              className="ya-nav-search-input"
            />
            <button type="submit" className="ya-nav-search-btn">
              Search
            </button>
          </form>

          <button
            type="button"
            className="ya-nav-theme-btn"
            aria-label="Toggle theme"
            onClick={toggle}
          >
            <img src={SettingIcon} alt="Theme" />
            <span className="ya-nav-theme-label">
              {mode === 'dark' ? 'Dark' : 'Light'}
            </span>
          </button>
        </div>
      </div>

      {/* Mobile slide-down menu (no overlap with logo) */}
      <nav className="ya-nav-mobile">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              'ya-nav-mobile-link' +
              (isActive ? ' ya-nav-mobile-link--active' : '')
            }
            onClick={() => {
              const menu = document.querySelector('.ya-nav-mobile');
              if (menu) {
                menu.classList.remove('ya-nav-mobile--open');
              }
            }}
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </header>
  );
};

export default Navbar;
