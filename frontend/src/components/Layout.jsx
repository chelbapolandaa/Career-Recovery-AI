import React from 'react';
import Sidebar from './Sidebar'; // ← Ganti Navbar jadi Sidebar

const Layout = ({ children }) => {
  return (
    <div style={{
      display: 'flex',
      minHeight: '100vh',
      fontFamily: '-apple-system, BlinkMacSystemFont, sans-serif'
    }}>
      <Sidebar />
      <div style={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column'
      }}>
        <main style={{
          flex: 1,
          padding: '2rem',
          background: '#f5f7fa',
          overflowY: 'auto'
        }}>
          {children}
        </main>
        <footer style={{
          padding: '1rem',
          textAlign: 'center',
          background: 'white',
          borderTop: '1px solid #e2e8f0',
          color: '#718096',
          fontSize: '0.85rem'
        }}>
          <p>Career Recovery AI v1.0 • Modules A & B Ready • Built with React & FastAPI</p>
        </footer>
      </div>
    </div>
  );
};

export default Layout;