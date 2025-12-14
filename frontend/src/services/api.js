import axios from 'axios';

const API = axios.create({
  baseURL: '/api',
  timeout: 10000,
});

export const applicationsAPI = {
  getAll: () => API.get('/applications'),
  getById: (id) => API.get(`/applications/${id}`),
  create: (data) => API.post('/applications', data),
  update: (id, data) => API.put(`/applications/${id}`, data),
  delete: (id) => API.delete(`/applications/${id}`),
  getStats: (days = 30) => API.get(`/applications/stats/summary?days=${days}`),
};

export const analysisAPI = {
  getQuickInsights: (days = 30) => API.get(`/analysis/quick-insights?days=${days}`),
  getRolePerformance: (days = 90) => API.get(`/analysis/role-performance?days=${days}`),
  testAnalysis: () => API.get('/analysis/test'),
  getAIAnalysis: (days = 90, useAI = true) => API.get(`/analysis/rejection-patterns?days=${days}&use_ai=${useAI}`),
  testAIIntegration: () => API.get('/analysis/ai-test'),
};

export default API;