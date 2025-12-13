import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./components/dashboard/Dashboard";
import ApplicationTracker from "./components/applications/ApplicationList";
import AnalysisDashboard from "./components/analysis/AnalysisDashboard";

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/applications" element={<ApplicationTracker />} />
          <Route path="/analysis" element={<AnalysisDashboard />} />
          <Route path="/strategy" element={<ComingSoon title="Strategy Engine" module="C" />} />
          <Route path="/wellbeing" element={<ComingSoon title="Burnout Monitor" module="D" />} />
          <Route path="/reports" element={<ComingSoon title="Weekly Reports" module="E" />} />
        </Routes>
      </Layout>
    </Router>
  );
}

const ComingSoon = ({ title, module }) => (
  <div style={{
    maxWidth: '800px',
    margin: '3rem auto',
    padding: '3rem',
    textAlign: 'center',
    background: 'white',
    borderRadius: '12px',
    boxShadow: '0 4px 20px rgba(0,0,0,0.08)'
  }}>
    <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>
      {module === 'C' ? '🎯' : module === 'D' ? '😌' : '📋'}
    </div>
    <h1 style={{ fontSize: '2.5rem', marginBottom: '1rem', color: '#333' }}>
      {title}
    </h1>
    <p style={{ color: '#666', fontSize: '1.2rem', marginBottom: '2rem' }}>
      Module {module} - Coming Soon
    </p>
    <div style={{
      display: 'inline-block',
      padding: '1rem 2rem',
      background: '#f0f0f0',
      borderRadius: '8px',
      color: '#888',
      fontSize: '0.9rem'
    }}>
      🚧 Under Development
    </div>
  </div>
);

export default App;