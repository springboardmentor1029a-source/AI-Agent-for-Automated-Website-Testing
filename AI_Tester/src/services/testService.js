import api from './api';

export const testService = {
  submitRequirements: async (documentContent, documentTitle) => {
    const res = await api.post('/api/v1/requirements/submit', {
      document_content: documentContent,
      document_title: documentTitle || 'Untitled Requirements',
    });
    return res.data;
  },

  getExecutionStatus: async (workflowId) => {
    const res = await api.get(`/api/v1/execution/${workflowId}/status`);
    return res.data;
  },

  getResults: async (workflowId) => {
    const res = await api.get(`/api/v1/workflows/${workflowId}/results`);
    return res.data;
  },

  downloadReport: async (workflowId, format = 'pdf') => {
    const res = await api.get(
      `/api/v1/workflows/${workflowId}/report?format=${format}`,
      { responseType: 'blob' }
    );
    const url = window.URL.createObjectURL(res.data);
    const a = document.createElement('a');
    a.href = url;
    a.download = `test-report-${workflowId}.${format}`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  },
};
