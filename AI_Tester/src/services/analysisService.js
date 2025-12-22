import api from './api';

export const analysisService = {
  getAnalysis: async (workflowId) => {
    const res = await api.get(`/api/v1/workflows/${workflowId}/analysis`);
    return res.data;
  },

  getRequirements: async (workflowId) => {
    const res = await api.get(`/api/v1/workflows/${workflowId}/requirements`);
    return res.data;
  },

  getCoverageAnalysis: async (workflowId) => {
    const res = await api.get(
      `/api/v1/workflows/${workflowId}/coverage-analysis`
    );
    return res.data;
  },

  getEdgeCases: async (workflowId) => {
    const res = await api.get(`/api/v1/workflows/${workflowId}/edge-cases`);
    return res.data;
  },
};
