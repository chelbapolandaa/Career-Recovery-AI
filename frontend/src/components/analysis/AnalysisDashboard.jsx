import React, { useState, useEffect } from 'react';
import { analysisAPI } from "../../services/api";

const AnalysisDashboard = () => {
  const [insights, setInsights] = useState(null);
  const [rolePerformance, setRolePerformance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('insights');

  useEffect(() => {
    fetchAnalysisData();
  }, []);

  const fetchAnalysisData = async () => {
    try {
      setLoading(true);
      const [insightsRes, roleRes] = await Promise.all([
        analysisAPI.getQuickInsights(),
        analysisAPI.getRolePerformance()
      ]);
      setInsights(insightsRes.data);
      setRolePerformance(roleRes.data);
    } catch (error) {
      console.error('Error fetching analysis data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '400px',
        fontSize: '1.2rem',
        color: '#667eea'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{
            width: '40px',
            height: '40px',
            border: '4px solid #f3f3f3',
            borderTop: '4px solid #667eea',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
            margin: '0 auto 20px'
          }}></div>
          <p>🧠 AI sedang menganalisis data aplikasimu...</p>
        </div>
        <style>{`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    );
  }

  const renderInsights = () => {
    if (!insights || insights.status === 'no_data') {
      return (
        <div style={{
          background: '#fff3cd',
          border: '1px solid #ffeaa7',
          borderRadius: '10px',
          padding: '2rem',
          textAlign: 'center',
          marginBottom: '2rem'
        }}>
          <h3 style={{ color: '#856404', marginBottom: '1rem' }}>📭 Data belum cukup</h3>
          <p style={{ color: '#856404', marginBottom: '1rem' }}>
            {insights?.message || 'Tambahkan lebih banyak aplikasi untuk mendapatkan analisis AI'}
          </p>
          <p style={{ color: '#666' }}>
            Rekomendasi: Coba tambahkan minimal 5 aplikasi dengan status berbeda
          </p>
        </div>
      );
    }

    return (
      <div>
        {/* Summary Cards */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '1.5rem',
          marginBottom: '2rem'
        }}>
          <div style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            padding: '1.5rem',
            borderRadius: '10px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>Total Aplikasi</div>
            <div style={{ fontSize: '2.5rem', fontWeight: 'bold', margin: '0.5rem 0' }}>
              {insights.summary?.total_applications || 0}
            </div>
            <div style={{ fontSize: '0.8rem' }}>30 hari terakhir</div>
          </div>

          <div style={{
            background: 'linear-gradient(135deg, #4cd964 0%, #5ac8fa 100%)',
            color: 'white',
            padding: '1.5rem',
            borderRadius: '10px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>Response Rate</div>
            <div style={{ fontSize: '2.5rem', fontWeight: 'bold', margin: '0.5rem 0' }}>
              {insights.summary?.response_rate || 0}%
            </div>
            <div style={{ fontSize: '0.8rem' }}>Dibalas / Total</div>
          </div>

          <div style={{
            background: 'linear-gradient(135deg, #ff9500 0%, #ff5e3a 100%)',
            color: 'white',
            padding: '1.5rem',
            borderRadius: '10px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>Interview Rate</div>
            <div style={{ fontSize: '2.5rem', fontWeight: 'bold', margin: '0.5rem 0' }}>
              {insights.summary?.interview_rate || 0}%
            </div>
            <div style={{ fontSize: '0.8rem' }}>Interview / Total</div>
          </div>
        </div>

        {/* Insights */}
        <div style={{
          background: 'white',
          borderRadius: '12px',
          padding: '2rem',
          marginBottom: '2rem',
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)'
        }}>
          <h3 style={{ marginBottom: '1.5rem', color: '#333', display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span style={{ fontSize: '1.5rem' }}>💡</span> AI Insights
          </h3>
          
          {insights.insights && Array.isArray(insights.insights) ? (
            <div style={{ lineHeight: '1.8' }}>
              {insights.insights.map((insight, index) => (
                <div key={index} style={{
                  padding: '1rem',
                  marginBottom: '0.5rem',
                  background: index % 2 === 0 ? '#f8f9fa' : 'white',
                  borderRadius: '8px',
                  borderLeft: '4px solid #667eea'
                }}>
                  {insight}
                </div>
              ))}
            </div>
          ) : (
            <div style={{
              padding: '1.5rem',
              background: '#f8f9fa',
              borderRadius: '8px',
              color: '#666'
            }}>
              {insights.insights || 'Tidak ada insights yang tersedia'}
            </div>
          )}
        </div>

        {/* Recommendations */}
        {insights.recommendations && insights.recommendations.length > 0 && (
          <div style={{
            background: 'white',
            borderRadius: '12px',
            padding: '2rem',
            marginBottom: '2rem',
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)'
          }}>
            <h3 style={{ marginBottom: '1.5rem', color: '#333', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ fontSize: '1.5rem' }}>🎯</span> AI Recommendations
            </h3>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {insights.recommendations.map((rec, index) => (
                <div key={index} style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '1rem',
                  padding: '1.2rem',
                  background: index === 0 ? '#e8f4fd' : '#f8f9fa',
                  borderRadius: '8px',
                  border: index === 0 ? '2px solid #2196f3' : '1px solid #e0e0e0'
                }}>
                  <div style={{
                    background: index === 0 ? '#2196f3' : '#6c757d',
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
                  <div>
                    <div style={{ fontWeight: '600', color: '#333', marginBottom: '0.3rem' }}>
                      {typeof rec === 'object' ? rec.action : rec}
                    </div>
                    {typeof rec === 'object' && rec.reason && (
                      <div style={{ color: '#666', fontSize: '0.9rem' }}>
                        {rec.reason}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  };

  const renderRolePerformance = () => {
    if (!rolePerformance || rolePerformance.status === 'no_data') {
      return (
        <div style={{
          background: '#fff3cd',
          border: '1px solid #ffeaa7',
          borderRadius: '10px',
          padding: '2rem',
          textAlign: 'center'
        }}>
          <h3 style={{ color: '#856404', marginBottom: '1rem' }}>📊 Data Role Belum Cukup</h3>
          <p style={{ color: '#856404' }}>
            Tambahkan aplikasi dengan berbagai role category untuk analisis
          </p>
        </div>
      );
    }

    return (
      <div>
        {/* Best Role Highlight */}
        {rolePerformance.best_role && (
          <div style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            padding: '2rem',
            borderRadius: '12px',
            marginBottom: '2rem',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '1rem', opacity: 0.9, marginBottom: '0.5rem' }}>⭐ ROLE TERBAIK</div>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>
              {rolePerformance.best_role.role.toUpperCase()}
            </div>
            <div style={{ fontSize: '1.1rem', marginBottom: '1rem' }}>
              {rolePerformance.best_role.interview_rate}% interview rate
            </div>
            <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>
              {rolePerformance.recommendation}
            </div>
          </div>
        )}

        {/* Role Performance Table */}
        <div style={{
          background: 'white',
          borderRadius: '12px',
          padding: '2rem',
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)'
        }}>
          <h3 style={{ marginBottom: '1.5rem', color: '#333' }}>📈 Performance per Role</h3>
          
          {rolePerformance.role_performance && rolePerformance.role_performance.length > 0 ? (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ background: '#f8f9fa' }}>
                    <th style={{ padding: '1rem', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>Role</th>
                    <th style={{ padding: '1rem', textAlign: 'center', borderBottom: '2px solid #dee2e6' }}>Total</th>
                    <th style={{ padding: '1rem', textAlign: 'center', borderBottom: '2px solid #dee2e6' }}>Interviews</th>
                    <th style={{ padding: '1rem', textAlign: 'center', borderBottom: '2px solid #dee2e6' }}>Interview Rate</th>
                    <th style={{ padding: '1rem', textAlign: 'center', borderBottom: '2px solid #dee2e6' }}>Rejection Rate</th>
                  </tr>
                </thead>
                <tbody>
                  {rolePerformance.role_performance.map((role, index) => (
                    <tr key={index} style={{
                      borderBottom: '1px solid #e9ecef',
                      background: index === 0 ? '#f0f7ff' : 'white'
                    }}>
                      <td style={{ padding: '1rem', fontWeight: index === 0 ? 'bold' : 'normal' }}>
                        {role.role}
                        {index === 0 && ' 🥇'}
                        {index === rolePerformance.role_performance.length - 1 && ' ⚠️'}
                      </td>
                      <td style={{ padding: '1rem', textAlign: 'center' }}>{role.total_applications}</td>
                      <td style={{ padding: '1rem', textAlign: 'center' }}>{role.interviews}</td>
                      <td style={{ padding: '1rem', textAlign: 'center' }}>
                        <span style={{
                          color: role.interview_rate >= 50 ? '#28a745' : 
                                 role.interview_rate >= 20 ? '#ffc107' : '#dc3545',
                          fontWeight: 'bold'
                        }}>
                          {role.interview_rate}%
                        </span>
                      </td>
                      <td style={{ padding: '1rem', textAlign: 'center' }}>
                        <span style={{
                          color: role.rejection_rate <= 30 ? '#28a745' : 
                                 role.rejection_rate <= 60 ? '#ffc107' : '#dc3545',
                          fontWeight: 'bold'
                        }}>
                          {role.rejection_rate}%
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '2rem', color: '#666' }}>
              Tidak ada data role yang cukup untuk analisis
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem' }}>
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2.5rem', color: '#333', marginBottom: '0.5rem' }}>
          🧠 Career Recovery AI - Analysis
        </h1>
        <p style={{ color: '#666', fontSize: '1.1rem' }}>
          AI-powered insights untuk meningkatkan strategi job search Anda
        </p>
      </div>

      {/* Tabs */}
      <div style={{
        display: 'flex',
        gap: '1rem',
        marginBottom: '2rem',
        borderBottom: '2px solid #e0e0e0',
        paddingBottom: '1rem'
      }}>
        <button
          onClick={() => setActiveTab('insights')}
          style={{
            padding: '0.75rem 1.5rem',
            background: activeTab === 'insights' ? '#667eea' : 'white',
            color: activeTab === 'insights' ? 'white' : '#667eea',
            border: '2px solid #667eea',
            borderRadius: '8px',
            cursor: 'pointer',
            fontWeight: 'bold',
            fontSize: '1rem',
            transition: 'all 0.3s'
          }}
        >
          💡 AI Insights
        </button>
        <button
          onClick={() => setActiveTab('roles')}
          style={{
            padding: '0.75rem 1.5rem',
            background: activeTab === 'roles' ? '#667eea' : 'white',
            color: activeTab === 'roles' ? 'white' : '#667eea',
            border: '2px solid #667eea',
            borderRadius: '8px',
            cursor: 'pointer',
            fontWeight: 'bold',
            fontSize: '1rem',
            transition: 'all 0.3s'
          }}
        >
          👔 Role Performance
        </button>
      </div>

      {/* Content */}
      <div>
        {activeTab === 'insights' ? renderInsights() : renderRolePerformance()}
      </div>

      {/* Refresh Button */}
      <div style={{ textAlign: 'center', marginTop: '3rem' }}>
        <button
          onClick={fetchAnalysisData}
          style={{
            padding: '0.75rem 2rem',
            background: '#48bb78',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontWeight: 'bold',
            fontSize: '1rem',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '10px'
          }}
        >
          🔄 Refresh Analysis
        </button>
        <p style={{ marginTop: '1rem', color: '#666', fontSize: '0.9rem' }}>
          Data dianalisis dari {insights?.metadata?.applications_analyzed || 0} aplikasi terakhir
        </p>
      </div>
    </div>
  );
};

export default AnalysisDashboard;