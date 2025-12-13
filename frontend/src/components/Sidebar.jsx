import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Sidebar = () => {
  const location = useLocation();
  
  const isActive = (path) => location.pathname === path;
  
  const menuItems = [
    { 
      path: '/', 
      label: 'Dashboard', 
      icon: '📊',
      badge: null,
      description: 'Overview & stats'
    },
    { 
      path: '/applications', 
      label: 'Applications', 
      icon: '📝',
      badge: 'A',
      description: 'Track job apps'
    },
    { 
      path: '/analysis', 
      label: 'AI Analysis', 
      icon: '📈',
      badge: 'B', 
      description: 'Smart insights'
    },
    { 
      path: '/strategy', 
      label: 'Strategy', 
      icon: '🎯',
      badge: 'C',
      description: 'Coming soon'
    },
    { 
      path: '/wellbeing', 
      label: 'Wellbeing', 
      icon: '😌',
      badge: 'D',
      description: 'Coming soon'
    },
    { 
      path: '/reports', 
      label: 'Reports', 
      icon: '📋',
      badge: 'E',
      description: 'Coming soon'
    },
  ];

  return (
    <div style={{
      width: '280px',
      background: 'linear-gradient(180deg, #1a202c 0%, #2d3748 100%)',
      color: 'white',
      display: 'flex',
      flexDirection: 'column',
      boxShadow: '2px 0 10px rgba(0,0,0,0.1)',
      zIndex: 100
    }}>
      {/* Logo Section */}
      <div style={{
        padding: '2rem 1.5rem',
        borderBottom: '1px solid rgba(255,255,255,0.1)'
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '1rem',
          marginBottom: '0.5rem'
        }}>
          <div style={{
            fontSize: '2.2rem',
            fontWeight: 'bold',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            width: '50px',
            height: '50px',
            borderRadius: '12px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            🧠
          </div>
          <div>
            <div style={{
              fontSize: '1.5rem',
              fontWeight: 'bold',
              background: 'linear-gradient(to right, #fff, #a0aec0)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent'
            }}>
              CRAI
            </div>
            <div style={{
              fontSize: '0.8rem',
              opacity: 0.7,
              marginTop: '2px'
            }}>
              Career Recovery AI
            </div>
          </div>
        </div>
        <div style={{
          fontSize: '0.75rem',
          opacity: 0.6,
          marginTop: '0.5rem',
          lineHeight: '1.4'
        }}>
          AI-powered job search assistant
        </div>
      </div>

      {/* Navigation Menu */}
      <nav style={{
        flex: 1,
        padding: '1.5rem 1rem',
        overflowY: 'auto'
      }}>
        <div style={{
          fontSize: '0.75rem',
          textTransform: 'uppercase',
          letterSpacing: '1px',
          opacity: 0.5,
          marginBottom: '1rem',
          paddingLeft: '0.5rem'
        }}>
          Modules
        </div>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          {menuItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              style={{
                display: 'flex',
                alignItems: 'center',
                padding: '1rem 1.25rem',
                color: isActive(item.path) ? 'white' : 'rgba(255,255,255,0.7)',
                textDecoration: 'none',
                borderRadius: '10px',
                background: isActive(item.path) 
                  ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' 
                  : 'transparent',
                border: isActive(item.path) ? 'none' : '1px solid transparent',
                transition: 'all 0.3s ease',
                position: 'relative',
                ':hover': {
                  background: isActive(item.path) 
                    ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' 
                    : 'rgba(255,255,255,0.1)',
                  transform: 'translateX(5px)'
                }
              }}
            >
              <div style={{
                fontSize: '1.3rem',
                marginRight: '1rem',
                width: '30px',
                textAlign: 'center'
              }}>
                {item.icon}
              </div>
              <div style={{ flex: 1 }}>
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  marginBottom: '2px'
                }}>
                  <span style={{
                    fontWeight: isActive(item.path) ? '600' : '500',
                    fontSize: '0.95rem'
                  }}>
                    {item.label}
                  </span>
                  {item.badge && (
                    <span style={{
                      background: item.badge === 'A' || item.badge === 'B' 
                        ? '#48bb78' 
                        : 'rgba(255,255,255,0.2)',
                      color: 'white',
                      fontSize: '0.65rem',
                      padding: '2px 6px',
                      borderRadius: '10px',
                      fontWeight: 'bold'
                    }}>
                      {item.badge}
                    </span>
                  )}
                </div>
                <div style={{
                  fontSize: '0.75rem',
                  opacity: 0.6,
                  lineHeight: '1.3'
                }}>
                  {item.description}
                </div>
              </div>
              
              {isActive(item.path) && (
                <div style={{
                  width: '4px',
                  height: '20px',
                  background: 'white',
                  borderRadius: '2px',
                  position: 'absolute',
                  right: '10px'
                }}></div>
              )}
            </Link>
          ))}
        </div>

        {/* Divider */}
        <div style={{
          height: '1px',
          background: 'rgba(255,255,255,0.1)',
          margin: '1.5rem 0'
        }}></div>

        {/* System Status */}
        <div style={{
          background: 'rgba(255,255,255,0.05)',
          borderRadius: '10px',
          padding: '1rem',
          marginTop: 'auto'
        }}>
          <div style={{
            fontSize: '0.8rem',
            opacity: 0.7,
            marginBottom: '0.5rem'
          }}>
            System Status
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '0.85rem' }}>Backend API</span>
              <span style={{
                color: '#48bb78',
                fontSize: '0.75rem',
                fontWeight: '600',
                display: 'flex',
                alignItems: 'center',
                gap: '4px'
              }}>
                <span style={{ fontSize: '0.6rem' }}>●</span> Connected
              </span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '0.85rem' }}>AI Engine</span>
              <span style={{
                color: '#48bb78',
                fontSize: '0.75rem',
                fontWeight: '600',
                display: 'flex',
                alignItems: 'center',
                gap: '4px'
              }}>
                <span style={{ fontSize: '0.6rem' }}>●</span> Ready
              </span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '0.85rem' }}>Database</span>
              <span style={{
                color: '#48bb78',
                fontSize: '0.75rem',
                fontWeight: '600',
                display: 'flex',
                alignItems: 'center',
                gap: '4px'
              }}>
                <span style={{ fontSize: '0.6rem' }}>●</span> Online
              </span>
            </div>
          </div>
        </div>
      </nav>

      {/* User/Footer Section */}
      <div style={{
        padding: '1.5rem',
        borderTop: '1px solid rgba(255,255,255,0.1)',
        fontSize: '0.8rem',
        opacity: 0.7
      }}>
        <div style={{ marginBottom: '0.5rem' }}>
          Active: Modules A & B
        </div>
        <div>
          Total Applications: <span style={{ color: '#48bb78', fontWeight: '600' }}>3</span>
        </div>
      </div>
    </div>
  );
};

// Inline styles for hover effect (React doesn't support :hover in inline styles)
// We'll add a global style instead
const SidebarWithStyles = () => {
  return (
    <>
      <Sidebar />
      <style>{`
        a:hover {
          background: rgba(255,255,255,0.1) !important;
          transform: translateX(5px) !important;
        }
      `}</style>
    </>
  );
};

export default SidebarWithStyles;