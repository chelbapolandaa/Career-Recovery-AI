import React, { useState, useEffect } from "react";
import { applicationsAPI, analysisAPI } from "../../services/api";
import { Link } from "react-router-dom";

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [applications, setApplications] = useState([]);
  const [aiInsights, setAiInsights] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [statsRes, appsRes, insightsRes] = await Promise.all([
        applicationsAPI.getStats(30),
        applicationsAPI.getAll(),
        analysisAPI.getQuickInsights()
      ]);
      setStats(statsRes.data);
      setApplications(appsRes.data);
      setAiInsights(insightsRes.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
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
          <p>Loading dashboard data...</p>
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

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2rem', color: '#333', marginBottom: '0.5rem' }}>
          🧠 Career Recovery AI Dashboard
        </h1>
        <p style={{ color: '#666' }}>
          Track your job applications and get AI-powered insights
        </p>
      </div>

      {/* Quick Stats */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
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
          <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>Total Applications</div>
          <div style={{ fontSize: '2.5rem', fontWeight: 'bold', margin: '0.5rem 0' }}>
            {stats?.total_applications || 0}
          </div>
          <div style={{ fontSize: '0.8rem' }}>30 days</div>
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
            {stats?.response_rate || 0}%
          </div>
          <div style={{ fontSize: '0.8rem' }}>Got response</div>
        </div>

        <div style={{
          background: 'linear-gradient(135deg, #ff9500 0%, #ff5e3a 100%)',
          color: 'white',
          padding: '1.5rem',
          borderRadius: '10px',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>Interviews</div>
          <div style={{ fontSize: '2.5rem', fontWeight: 'bold', margin: '0.5rem 0' }}>
            {stats?.status_breakdown?.interview || 0}
          </div>
          <div style={{ fontSize: '0.8rem' }}>Scheduled</div>
        </div>

        <div style={{
          background: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
          color: '#333',
          padding: '1.5rem',
          borderRadius: '10px',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>Ghosted</div>
          <div style={{ fontSize: '2.5rem', fontWeight: 'bold', margin: '0.5rem 0' }}>
            {stats?.status_breakdown?.ghosted || 0}
          </div>
          <div style={{ fontSize: '0.8rem' }}>No response</div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '2fr 1fr',
        gap: '2rem',
        marginBottom: '2rem'
      }}>
        {/* Left Column: Applications & AI Insights */}
        <div>
          {/* Recent Applications */}
          <div style={{
            background: 'white',
            borderRadius: '12px',
            padding: '1.5rem',
            marginBottom: '1.5rem',
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h2 style={{ color: '#333' }}>📋 Recent Applications</h2>
              <Link to="/applications" style={{
                color: '#667eea',
                textDecoration: 'none',
                fontWeight: '600',
                fontSize: '0.9rem'
              }}>
                View All →
              </Link>
            </div>
            
            {applications.length > 0 ? (
              <div style={{ overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                  <thead>
                    <tr style={{ background: '#f8f9fa' }}>
                      <th style={{ padding: '0.75rem', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>Job</th>
                      <th style={{ padding: '0.75rem', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>Company</th>
                      <th style={{ padding: '0.75rem', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>Status</th>
                      <th style={{ padding: '0.75rem', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    {applications.slice(0, 5).map(app => (
                      <tr key={app.id} style={{ borderBottom: '1px solid #e9ecef' }}>
                        <td style={{ padding: '0.75rem' }}>{app.job_title}</td>
                        <td style={{ padding: '0.75rem' }}>{app.company}</td>
                        <td style={{ padding: '0.75rem' }}>
                          <span style={{
                            display: 'inline-block',
                            padding: '4px 12px',
                            borderRadius: '20px',
                            fontSize: '0.8rem',
                            fontWeight: '600',
                            background: app.status === 'ghosted' ? '#e2e8f0' :
                                      app.status === 'rejected' ? '#fed7d7' :
                                      app.status === 'interview' ? '#feebc8' : '#c6f6d5',
                            color: app.status === 'ghosted' ? '#4a5568' :
                                  app.status === 'rejected' ? '#c53030' :
                                  app.status === 'interview' ? '#c05621' : '#22543d'
                          }}>
                            {app.status}
                          </span>
                        </td>
                        <td style={{ padding: '0.75rem', color: '#666' }}>{app.date_applied}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div style={{ textAlign: 'center', padding: '2rem', color: '#666' }}>
                <p>No applications yet.</p>
                <Link to="/applications" style={{
                  display: 'inline-block',
                  marginTop: '1rem',
                  padding: '0.5rem 1.5rem',
                  background: '#667eea',
                  color: 'white',
                  borderRadius: '6px',
                  textDecoration: 'none',
                  fontWeight: '600'
                }}>
                  Add Your First Application
                </Link>
              </div>
            )}
          </div>

          {/* AI Insights */}
          {aiInsights && aiInsights.status === 'success' && (
            <div style={{
              background: 'white',
              borderRadius: '12px',
              padding: '1.5rem',
              boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)',
              borderLeft: '5px solid #667eea'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h2 style={{ color: '#333', display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <span style={{ fontSize: '1.5rem' }}>🤖</span> AI Insights
                </h2>
                <Link to="/analysis" style={{
                  color: '#667eea',
                  textDecoration: 'none',
                  fontWeight: '600',
                  fontSize: '0.9rem'
                }}>
                  Full Analysis →
                </Link>
              </div>
              
              {aiInsights.insights && Array.isArray(aiInsights.insights) && (
                <div style={{ marginBottom: '1rem' }}>
                  {aiInsights.insights.slice(0, 3).map((insight, idx) => (
                    <div key={idx} style={{
                      padding: '0.75rem',
                      marginBottom: '0.5rem',
                      background: '#f8f9fa',
                      borderRadius: '6px',
                      fontSize: '0.95rem'
                    }}>
                      {insight}
                    </div>
                  ))}
                </div>
              )}
              
              {aiInsights.recommendations && aiInsights.recommendations.length > 0 && (
                <div>
                  <div style={{ fontWeight: '600', color: '#555', marginBottom: '0.5rem' }}>
                    🎯 Top Recommendation:
                  </div>
                  <div style={{
                    padding: '0.75rem',
                    background: '#e8f4fd',
                    borderRadius: '6px',
                    border: '1px solid #bbdefb',
                    fontSize: '0.9rem'
                  }}>
                    {typeof aiInsights.recommendations[0] === 'object' 
                      ? aiInsights.recommendations[0].action 
                      : aiInsights.recommendations[0]}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Right Column: Quick Actions & Stats */}
        <div>
          {/* Quick Actions */}
          <div style={{
            background: 'white',
            borderRadius: '12px',
            padding: '1.5rem',
            marginBottom: '1.5rem',
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)'
          }}>
            <h2 style={{ color: '#333', marginBottom: '1rem' }}>⚡ Quick Actions</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              <Link to="/applications" style={{
                display: 'block',
                padding: '0.75rem 1rem',
                background: '#e6f7ff',
                color: '#1890ff',
                borderRadius: '8px',
                textDecoration: 'none',
                fontWeight: '600',
                border: '2px solid #91d5ff',
                textAlign: 'center'
              }}>
                📝 Add New Application
              </Link>
              <Link to="/analysis" style={{
                display: 'block',
                padding: '0.75rem 1rem',
                background: '#f6ffed',
                color: '#52c41a',
                borderRadius: '8px',
                textDecoration: 'none',
                fontWeight: '600',
                border: '2px solid #b7eb8f',
                textAlign: 'center'
              }}>
                📊 Run AI Analysis
              </Link>
              <button onClick={fetchDashboardData} style={{
                width: '100%',
                padding: '0.75rem 1rem',
                background: '#fff7e6',
                color: '#fa8c16',
                borderRadius: '8px',
                border: '2px solid #ffd591',
                fontWeight: '600',
                cursor: 'pointer',
                fontSize: '1rem'
              }}>
                🔄 Refresh Data
              </button>
            </div>
          </div>

          {/* Role Breakdown */}
          {stats?.role_breakdown && (
            <div style={{
              background: 'white',
              borderRadius: '12px',
              padding: '1.5rem',
              boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)'
            }}>
              <h2 style={{ color: '#333', marginBottom: '1rem' }}>👔 Applications by Role</h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {Object.entries(stats.role_breakdown).map(([role, count]) => (
                  <div key={role} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ color: '#555' }}>{role}</span>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <span style={{ fontWeight: '600' }}>{count}</span>
                      <div style={{
                        width: '60px',
                        height: '8px',
                        background: '#e0e0e0',
                        borderRadius: '4px',
                        overflow: 'hidden'
                      }}>
                        <div style={{
                          width: `${(count / stats.total_applications) * 100}%`,
                          height: '100%',
                          background: '#667eea',
                          borderRadius: '4px'
                        }}></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Bottom Info */}
      <div style={{
        background: 'white',
        borderRadius: '12px',
        padding: '1rem',
        marginTop: '1rem',
        textAlign: 'center',
        color: '#666',
        fontSize: '0.9rem',
        boxShadow: '0 2px 10px rgba(0, 0, 0, 0.05)'
      }}>
        <p>
          🧠 <strong>Career Recovery AI v1.0</strong> • 
          Module A: <span style={{ color: '#48bb78', fontWeight: '600' }}>✅ Ready</span> • 
          Module B: <span style={{ color: '#48bb78', fontWeight: '600' }}>✅ Ready</span>
        </p>
      </div>
    </div>
  );
};

export default Dashboard;