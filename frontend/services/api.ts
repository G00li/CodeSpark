import axios from 'axios';

// Obter URL da API do ambiente
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Criar instância do axios com configuração base
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para incluir token de autenticação em todas as requisições
api.interceptors.request.use(
  async (config) => {
    // Se estivermos no lado do cliente
    if (typeof window !== 'undefined') {
      const session = JSON.parse(localStorage.getItem('next-auth.session-token') || '{}');
      if (session?.access_token) {
        config.headers.Authorization = `Bearer ${session.access_token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api; 