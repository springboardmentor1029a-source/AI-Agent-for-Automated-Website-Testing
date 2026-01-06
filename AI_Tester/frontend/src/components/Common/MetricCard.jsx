// src/components/Common/MetricCard.jsx
import React from 'react';

export function MetricCard({ icon, label, value, subtext, trend }) {
  return (
    <div style={{
      background: 'white',
      borderRadius: '8px',
      padding: '16px',
      boxShadow: 'var(--shadow-sm)',
      border: '1px solid var(--border-color)',
      transition: 'all 0.3s ease'
    }}
    onMouseEnter={(e) => {
      e.currentTarget.style.boxShadow = 'var(--shadow-md)';
      e.currentTarget.style.transform = 'translateY(-4px)';
    }}
    onMouseLeave={(e) => {
      e.currentTarget.style.boxShadow = 'var(--shadow-sm)';
      e.currentTarget.style.transform = 'translateY(0)';
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '12px' }}>
        <span style={{ fontSize: '24px' }}>{icon}</span>
        {trend && (
          <span style={{
            fontSize: '12px',
            fontWeight: '600',
            color: trend.startsWith('+') ? 'rgb(81, 207, 102)' : 'rgb(255, 107, 107)',
            background: trend.startsWith('+') ? 'rgba(81, 207, 102, 0.1)' : 'rgba(255, 107, 107, 0.1)',
            padding: '4px 8px',
            borderRadius: '4px'
          }}>
            {trend}
          </span>
        )}
      </div>
      <p style={{ margin: '0 0 4px 0', color: 'var(--text-light)', fontSize: '12px' }}>{label}</p>
      <p style={{ margin: '0 0 8px 0', fontSize: '24px', fontWeight: '700', color: 'var(--text-dark)' }}>{value}</p>
      {subtext && <p style={{ margin: 0, fontSize: '12px', color: 'var(--text-light)' }}>{subtext}</p>}
    </div>
  );
}