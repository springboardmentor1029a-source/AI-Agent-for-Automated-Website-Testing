import api from './api';

export const logService = {
  log: async (level, message, extra = {}) => {
    try {
      if (import.meta.env.DEV) {
        console.log(`[${level}]`, message, extra);
        return;
      }
      await api.post('/api/v1/logs', {
        level,
        message,
        extra,
        timestamp: new Date().toISOString(),
      });
    } catch (e) {
      console.error('Failed to send log', e);
    }
  },

  info: (msg, extra) => logService.log('INFO', msg, extra),
  warn: (msg, extra) => logService.log('WARN', msg, extra),
  error: (msg, extra) => logService.log('ERROR', msg, extra),
};
