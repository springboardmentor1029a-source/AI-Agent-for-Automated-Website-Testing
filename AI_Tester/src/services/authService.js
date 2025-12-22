import api from './api';

export const authService = {
  register: async (email, password, fullName) => {
    const res = await api.post('/api/v1/auth/register', {
      email,
      password,
      full_name: fullName,
    });
    if (res.data.access_token) {
      localStorage.setItem('authToken', res.data.access_token);
      if (res.data.refresh_token) {
        localStorage.setItem('refreshToken', res.data.refresh_token);
      }
    }
    return res.data;
  },

  login: async (email, password) => {
    const res = await api.post('/api/v1/auth/login', { email, password });
    if (res.data.access_token) {
      localStorage.setItem('authToken', res.data.access_token);
      if (res.data.refresh_token) {
        localStorage.setItem('refreshToken', res.data.refresh_token);
      }
    }
    return res.data;
  },

  logout: async () => {
    try {
      await api.post('/api/v1/auth/logout');
    } catch {
      // ignore
    }
    localStorage.removeItem('authToken');
    localStorage.removeItem('refreshToken');
  },

  getCurrentUser: async () => {
    const res = await api.get('/api/v1/auth/me');
    return res.data;
  },

  isAuthenticated: () => !!localStorage.getItem('authToken'),
};
