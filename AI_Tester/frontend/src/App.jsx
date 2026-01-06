import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext.jsx';
import Navbar from './components/Navbar';

// Core pages
import Home from './pages/Home';
import HowItWorks from './pages/HowItWorks';
import DataInput from './pages/DataInput';
import About from './pages/About';
import Contact from './pages/Contact';

// Capability and QA lifecycle pages
import CapabilityPages from './pages/CapabilityPages';
import AnalysisReview from './pages/AnalysisReview';
import ExecutionDashboard from './pages/ExecutionDashboard';
import RegressionCenter from './pages/RegressionCenter';
import Reports from './pages/Reports';
import TestConsole from './pages/TestConsole';
import Settings from './pages/Settings';

import './styles/index.css';

const App = () => {
  return (
    <ThemeProvider>
      <Router>
        {/* Top navigation (fixed by its own CSS) */}
        <Navbar />

        {/* Route configuration */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/how-it-works" element={<HowItWorks />} />
          <Route path="/data-input" element={<DataInput />} />
          <Route path="/capability" element={<CapabilityPages />} />
          <Route path="/analysis-review" element={<AnalysisReview />} />
          <Route path="/execution-dashboard" element={<ExecutionDashboard />} />
          <Route path="/regression-center" element={<RegressionCenter />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/test-console" element={<TestConsole />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />

          {/* Fallback: unknown routes go to Home */}
          <Route path="*" element={<Home />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
};

export default App;
