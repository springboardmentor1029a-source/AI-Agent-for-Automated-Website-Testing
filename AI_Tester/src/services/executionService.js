import api from './api';

export const executionService = {
  getExecution: async (executionId) => {
    const res = await api.get(`/api/v1/execution/${executionId}`);
    return res.data;
  },

  getExecutionSummary: async (executionId) => {
    const res = await api.get(`/api/v1/execution/${executionId}/summary`);
    return res.data;
  },

  subscribeToExecutionLogs: (executionId, onMessage, onError) => {
    const es = new EventSource(
      `${import.meta.env.VITE_API_BASE_URL}/api/v1/execution/${executionId}/logs/stream`
    );

    es.onmessage = (ev) => {
      try {
        onMessage(JSON.parse(ev.data));
      } catch (e) {
        console.error('Log parse error', e);
      }
    };

    es.onerror = (err) => {
      console.error('SSE error', err);
      if (onError) onError(err);
      es.close();
    };

    return es;
  },

  stopExecution: async (executionId) => {
    const res = await api.post(`/api/v1/execution/${executionId}/stop`);
    return res.data;
  },

  retryFailedTests: async (executionId) => {
    const res = await api.post(`/api/v1/execution/${executionId}/retry`);
    return res.data;
  },
};
