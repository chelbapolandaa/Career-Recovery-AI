import React, { useState } from 'react';

const AIAnalysisTab = ({ aiAnalysis, onRefresh }) => {
  const [expandedRec, setExpandedRec] = useState(null);

  if (!aiAnalysis || aiAnalysis.status === 'error') {
    return (
      <div style={{
        background: '#fff3cd',
        border: '1px solid #ffeaa7',
        borderRadius: '10px',
        padding: '2rem',
        textAlign: 'center',
        marginBottom: '2rem'
      }}>
        <h3 style={{ color: '#856404', marginBottom: '1rem' }}>🤖 AI Analysis Not Available</h3>
        <p style={{ color: '#856404', marginBottom: '1rem' }}>
          {aiAnalysis?.message || 'AI analysis is currently unavailable'}
        </p>
        <button 
          onClick={onRefresh}
          style={{
            padding: '0.5rem 1.5rem',
            background: '#667eea',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer'
          }}
        >
          Retry AI Analysis
        </button>
      </div>
    );
  }

  const { summary, ai_insights, recommendations, problem_patterns, metadata } = aiAnalysis;
  const aiData = ai_insights || {};

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        padding: '2rem',
        borderRadius: '12px',
        marginBottom: '2rem',
        textAlign: 'center'
      }}>
        <div style={{ fontSize: '1.5rem', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
          <span>🤖</span>
          <span>AI-POWERED CAREER ANALYSIS</span>
        </div>
        <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>
          Powered by {aiData?.model || 'Groq AI'} • {metadata?.applications_analyzed || 0} applications analyzed
          {aiData?.cached && ' • 📦 Using cached insights'}
        </div>
      </div>

      {aiData?.executive_summary && (
        <div style={{
          background: 'white',
          borderRadius: '12px',
          padding: '2rem',
          marginBottom: '2rem',
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)'
        }}>
          <h3 style={{ marginBottom: '1rem', color: '#333', display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span>📊</span> Executive Summary
          </h3>
          <div style={{
            padding: '1.5rem',
            background: '#f8f9fa',
            borderRadius: '8px',
            lineHeight: '1.6',
            fontSize: '1.1rem'
          }}>
            {aiData.executive_summary}
          </div>
        </div>
      )}

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '1.5rem',
        marginBottom: '2rem'
      }}>
        <div style={{
          background: 'white',
          padding: '1.5rem',
          borderRadius: '10px',
          textAlign: 'center',
          boxShadow: '0 2px 10px rgba(0, 0, 0, 0.05)'
        }}>
          <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Applications</div>
          <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#667eea' }}>
            {summary?.total_applications || 0}
          </div>
        </div>

        <div style={{
          background: 'white',
          padding: '1.5rem',
          borderRadius: '10px',
          textAlign: 'center',
          boxShadow: '0 2px 10px rgba(0, 0, 0, 0.05)'
        }}>
          <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Interview Rate</div>
          <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: summary?.interview_rate > 15 ? '#4cd964' : '#ff9500' }}>
            {summary?.interview_rate || 0}%
          </div>
        </div>

        <div style={{
          background: 'white',
          padding: '1.5rem',
          borderRadius: '10px',
          textAlign: 'center',
          boxShadow: '0 2px 10px rgba(0, 0, 0, 0.05)'
        }}>
          <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Response Rate</div>
          <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: summary?.response_rate > 50 ? '#4cd964' : '#ff9500' }}>
            {summary?.response_rate || 0}%
          </div>
        </div>

        <div style={{
          background: 'white',
          padding: '1.5rem',
          borderRadius: '10px',
          textAlign: 'center',
          boxShadow: '0 2px 10px rgba(0, 0, 0, 0.05)'
        }}>
          <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Rejection Rate</div>
          <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: summary?.rejection_rate < 50 ? '#4cd964' : '#ff5e3a' }}>
            {summary?.rejection_rate || 0}%
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '2rem' }}>
        {aiData?.key_strengths && aiData.key_strengths.length > 0 && (
          <div style={{
            background: 'white',
            borderRadius: '12px',
            padding: '1.5rem',
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)'
          }}>
            <h3 style={{ marginBottom: '1rem', color: '#333', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ color: '#4cd964' }}>✅</span> Key Strengths
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {aiData.key_strengths.map((strength, index) => (
                <div key={index} style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '0.75rem',
                  padding: '0.75rem',
                  background: '#f0fff4',
                  borderRadius: '8px',
                  borderLeft: '4px solid #4cd964'
                }}>
                  <div style={{ color: '#4cd964', fontWeight: 'bold' }}>✓</div>
                  <div>{strength}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {aiData?.critical_issues && aiData.critical_issues.length > 0 && (
          <div style={{
            background: 'white',
            borderRadius: '12px',
            padding: '1.5rem',
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)'
          }}>
            <h3 style={{ marginBottom: '1rem', color: '#333', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ color: '#ff5e3a' }}>⚠️</span> Critical Issues
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {aiData.critical_issues.map((issue, index) => (
                <div key={index} style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '0.75rem',
                  padding: '0.75rem',
                  background: '#fff5f5',
                  borderRadius: '8px',
                  borderLeft: '4px solid #ff5e3a'
                }}>
                  <div style={{ color: '#ff5e3a', fontWeight: 'bold' }}>!</div>
                  <div>{issue}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {aiData?.actionable_recommendations && aiData.actionable_recommendations.length > 0 && (
        <div style={{
          background: 'white',
          borderRadius: '12px',
          padding: '2rem',
          marginBottom: '2rem',
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)'
        }}>
          <h3 style={{ marginBottom: '1.5rem', color: '#333', display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span style={{ color: '#667eea' }}>🎯</span> Actionable Recommendations
          </h3>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {aiData.actionable_recommendations.map((rec, index) => (
              <div key={index} style={{
                display: 'flex',
                alignItems: 'flex-start',
                gap: '1rem',
                padding: '1.2rem',
                background: expandedRec === index ? '#e8f4fd' : '#f8f9fa',
                borderRadius: '8px',
                border: expandedRec === index ? '2px solid #2196f3' : '1px solid #e0e0e0',
                cursor: 'pointer'
              }}
              onClick={() => setExpandedRec(expandedRec === index ? null : index)}
              >
                <div style={{
                  background: rec.priority === 'high' ? '#f56565' : 
                             rec.priority === 'medium' ? '#ed8936' : '#48bb78',
                  color: 'white',
                  width: '30px',
                  height: '30px',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0,
                  fontWeight: 'bold'
                }}>
                  {index + 1}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                    <div style={{ fontWeight: '600', color: '#333', fontSize: '1.1rem' }}>
                      {rec.title}
                    </div>
                    <span style={{
                      padding: '4px 12px',
                      borderRadius: '20px',
                      fontSize: '0.8rem',
                      fontWeight: '600',
                      background: rec.priority === 'high' ? '#fed7d7' : 
                                 rec.priority === 'medium' ? '#feebc8' : '#c6f6d5',
                      color: rec.priority === 'high' ? '#c53030' : 
                             rec.priority === 'medium' ? '#c05621' : '#22543d'
                    }}>
                      {rec.priority?.toUpperCase() || 'MEDIUM'}
                    </span>
                  </div>
                  <div style={{ color: '#555', marginBottom: '0.5rem' }}>
                    {rec.action}
                  </div>
                  
                  {expandedRec === index && (
                    <div style={{
                      marginTop: '1rem',
                      padding: '1rem',
                      background: 'white',
                      borderRadius: '6px',
                      border: '1px solid #e0e0e0'
                    }}>
                      <div style={{ fontWeight: '600', marginBottom: '0.5rem' }}>📋 Detailed Action Plan:</div>
                      <div style={{ lineHeight: '1.6' }}>
                        {rec.action} - This recommendation focuses on improving your job application strategy by addressing specific areas that need improvement.
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '2rem' }}>
        {aiData?.encouragement && (
          <div style={{
            background: 'white',
            borderRadius: '12px',
            padding: '1.5rem',
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)'
          }}>
            <h3 style={{ marginBottom: '1rem', color: '#333', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ color: '#4cd964' }}>💪</span> Encouragement
            </h3>
            <div style={{
              padding: '1rem',
              background: '#f0fff4',
              borderRadius: '8px',
              fontStyle: 'italic',
              lineHeight: '1.6'
            }}>
              {aiData.encouragement}
            </div>
          </div>
        )}

        {aiData?.next_week_focus && (
          <div style={{
            background: 'white',
            borderRadius: '12px',
            padding: '1.5rem',
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)'
          }}>
            <h3 style={{ marginBottom: '1rem', color: '#333', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ color: '#667eea' }}>🎯</span> Next Week Focus
            </h3>
            <div style={{
              padding: '1rem',
              background: '#e8f4fd',
              borderRadius: '8px',
              fontWeight: '600'
            }}>
              {aiData.next_week_focus}
            </div>
          </div>
        )}
      </div>

      <div style={{
        textAlign: 'center',
        padding: '1.5rem',
        color: '#666',
        fontSize: '0.9rem',
        background: 'white',
        borderRadius: '12px',
        boxShadow: '0 2px 10px rgba(0, 0, 0, 0.05)'
      }}>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '1rem', marginBottom: '0.5rem' }}>
          <span>🤖 AI-Powered by Groq {aiData?.model && `(${aiData.model})`}</span>
          {aiData?.cached && <span style={{ background: '#c6f6d5', padding: '2px 8px', borderRadius: '12px' }}>📦 Cached</span>}
        </div>
        <div>Analysis generated on: {aiData?.generated_at ? new Date(aiData.generated_at).toLocaleString() : 'Just now'}</div>
      </div>
    </div>
  );
};

export default AIAnalysisTab;