import React, { useState, useEffect } from 'react';
import { applicationsAPI } from '../../services/api';

const ApplicationTracker = () => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({
    job_title: '',
    company: '',
    role_category: 'dev',
    date_applied: new Date().toISOString().split('T')[0],
    status: 'ghosted',
    notes: ''
  });

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    try {
      const response = await applicationsAPI.getAll();
      setApplications(response.data);
    } catch (error) {
      console.error('Error fetching applications:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await applicationsAPI.create(form);
      alert('✅ Application added!');
      setForm({
        job_title: '',
        company: '',
        role_category: 'dev',
        date_applied: new Date().toISOString().split('T')[0],
        status: 'ghosted',
        notes: ''
      });
      fetchApplications();
    } catch (error) {
      console.error('Error:', error);
      alert('❌ Error adding application');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Delete this application?')) {
      try {
        await applicationsAPI.delete(id);
        fetchApplications();
      } catch (error) {
        console.error('Error:', error);
      }
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '3rem' }}>
        <div style={{
          width: '40px',
          height: '40px',
          border: '4px solid #f3f3f3',
          borderTop: '4px solid #667eea',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite',
          margin: '0 auto 1rem'
        }}></div>
        <p>Loading applications...</p>
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
      <h1 style={{ fontSize: '2rem', marginBottom: '2rem' }}>📝 Application Tracker</h1>
      
      {/* Add Form */}
      <div style={{
        background: 'white',
        borderRadius: '12px',
        padding: '2rem',
        marginBottom: '2rem',
        boxShadow: '0 4px 20px rgba(0,0,0,0.08)'
      }}>
        <h2 style={{ marginBottom: '1.5rem' }}>Add New Application</h2>
        <form onSubmit={handleSubmit}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>Job Title *</label>
              <input
                type="text"
                value={form.job_title}
                onChange={(e) => setForm({...form, job_title: e.target.value})}
                required
                style={{ width: '100%', padding: '0.75rem', border: '2px solid #e2e8f0', borderRadius: '6px' }}
                placeholder="Frontend Developer"
              />
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>Company *</label>
              <input
                type="text"
                value={form.company}
                onChange={(e) => setForm({...form, company: e.target.value})}
                required
                style={{ width: '100%', padding: '0.75rem', border: '2px solid #e2e8f0', borderRadius: '6px' }}
                placeholder="Tech Corp"
              />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>Role Category</label>
              <select
                value={form.role_category}
                onChange={(e) => setForm({...form, role_category: e.target.value})}
                style={{ width: '100%', padding: '0.75rem', border: '2px solid #e2e8f0', borderRadius: '6px' }}
              >
                <option value="dev">Developer</option>
                <option value="va">Virtual Assistant</option>
                <option value="ops">Operations</option>
                <option value="ai">AI/ML</option>
                <option value="it">IT Support</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>Date Applied</label>
              <input
                type="date"
                value={form.date_applied}
                onChange={(e) => setForm({...form, date_applied: e.target.value})}
                required
                style={{ width: '100%', padding: '0.75rem', border: '2px solid #e2e8f0', borderRadius: '6px' }}
              />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>Status</label>
              <select
                value={form.status}
                onChange={(e) => setForm({...form, status: e.target.value})}
                style={{ width: '100%', padding: '0.75rem', border: '2px solid #e2e8f0', borderRadius: '6px' }}
              >
                <option value="ghosted">Ghosted</option>
                <option value="rejected">Rejected</option>
                <option value="interview">Interview</option>
                <option value="offer">Offer</option>
              </select>
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>Notes</label>
              <input
                type="text"
                value={form.notes}
                onChange={(e) => setForm({...form, notes: e.target.value})}
                style={{ width: '100%', padding: '0.75rem', border: '2px solid #e2e8f0', borderRadius: '6px' }}
                placeholder="Any additional notes..."
              />
            </div>
          </div>

          <button
            type="submit"
            style={{
              padding: '0.75rem 2rem',
              background: '#667eea',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              fontWeight: '600',
              cursor: 'pointer',
              fontSize: '1rem'
            }}
          >
            ➕ Add Application
          </button>
        </form>
      </div>

      {/* Applications List */}
      <div style={{
        background: 'white',
        borderRadius: '12px',
        padding: '2rem',
        boxShadow: '0 4px 20px rgba(0,0,0,0.08)'
      }}>
        <h2 style={{ marginBottom: '1.5rem' }}>
          Your Applications ({applications.length})
        </h2>
        
        {applications.length > 0 ? (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: '#f8f9fa' }}>
                  <th style={{ padding: '1rem', textAlign: 'left' }}>Job Title</th>
                  <th style={{ padding: '1rem', textAlign: 'left' }}>Company</th>
                  <th style={{ padding: '1rem', textAlign: 'left' }}>Role</th>
                  <th style={{ padding: '1rem', textAlign: 'left' }}>Date</th>
                  <th style={{ padding: '1rem', textAlign: 'left' }}>Status</th>
                  <th style={{ padding: '1rem', textAlign: 'left' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {applications.map(app => (
                  <tr key={app.id} style={{ borderBottom: '1px solid #e9ecef' }}>
                    <td style={{ padding: '1rem' }}>{app.job_title}</td>
                    <td style={{ padding: '1rem' }}>{app.company}</td>
                    <td style={{ padding: '1rem' }}>{app.role_category}</td>
                    <td style={{ padding: '1rem' }}>{app.date_applied}</td>
                    <td style={{ padding: '1rem' }}>
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
                    <td style={{ padding: '1rem' }}>
                      <button
                        onClick={() => handleDelete(app.id)}
                        style={{
                          padding: '0.5rem 1rem',
                          background: '#fc8181',
                          color: 'white',
                          border: 'none',
                          borderRadius: '4px',
                          cursor: 'pointer',
                          fontSize: '0.9rem'
                        }}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div style={{ textAlign: 'center', padding: '3rem', color: '#666' }}>
            <p style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>No applications yet</p>
            <p>Start by adding your first job application above</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ApplicationTracker;