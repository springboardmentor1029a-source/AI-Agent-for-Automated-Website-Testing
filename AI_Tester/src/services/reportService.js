import api from './api';

export const reportService = {
  getReport: async (workflowId) => {
    const res = await api.get(`/api/v1/reports/${workflowId}`);
    return res.data;
  },

  getReportStats: async (workflowId) => {
    const res = await api.get(`/api/v1/reports/${workflowId}/statistics`);
    return res.data;
  },
};
