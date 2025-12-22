import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: parseInt(import.meta.env.VITE_TIMEOUT || '30000'),
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    config.headers['X-Request-ID'] = `${Date.now()}-${Math.random()
      .toString(36)
      .slice(2, 9)}`;
    config.headers['X-Timestamp'] = new Date().toISOString();
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;

    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      const refresh = localStorage.getItem('refreshToken');
      if (refresh) {
        try {
          const res = await axios.post(
            `${import.meta.env.VITE_API_BASE_URL}/api/v1/auth/refresh`,
            { refresh_token: refresh }
          );
          const access = res.data.access_token;
          localStorage.setItem('authToken', access);
          original.headers.Authorization = `Bearer ${access}`;
          return api(original);
        } catch {
          localStorage.removeItem('authToken');
          localStorage.removeItem('refreshToken');
          window.location.href = '/login';
        }
      }
    }

    return Promise.reject(error);
  }
);

export default api;
