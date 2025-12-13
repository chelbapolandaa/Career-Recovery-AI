import axios from 'axios';

const API = axios.create({
  baseURL: '/api',
  timeout: 10000,
});

// Applications endpoints (Module A)
export const applicationsAPI = {
  getAll: () => API.get('/applications'),
  getById: (id) => API.get(`/applications/${id}`),
  create: (data) => API.post('/applications', data),
  update: (id, data) => API.put(`/applications/${id}`, data),
  delete: (id) => API.delete(`/applications/${id}`),
  getStats: (days = 30) => API.get(`/applications/stats/summary?days=${days}`),
};

// Analysis endpoints (Module B - NEW!)
export const analysisAPI = {
  getQuickInsights: () => API.get('/analysis/quick-insights'),
  getRolePerformance: () => API.get('/analysis/role-performance'),
  getRejectionPatterns: (days = 30) => API.get(`/analysis/rejection-patterns?days=${days}`),
  testAnalysis: () => API.get('/analysis/test'),
};

export default API;