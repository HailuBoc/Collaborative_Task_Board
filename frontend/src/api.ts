import axios, { AxiosError } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001';

export interface User {
  id: string;
  name: string;
}

export interface Task {
  id: string;
  title: string;
  status: 'TODO' | 'IN_PROGRESS' | 'DONE';
  assigned_to: string | null;
  updated_at: string;
  version: number;
}

export interface ConflictError {
  detail: string;
  latest_task: Task;
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for debugging
api.interceptors.request.use((config) => {
  console.log('API Request:', config.method?.toUpperCase(), config.url, config.data);
  return config;
});

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.data);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.status, error.response?.data, error.message);
    return Promise.reject(error);
  }
);

// User API
export const userAPI = {
  create: (name: string) =>
    api.post<User>('/users', { name }),
  getAll: () =>
    api.get<User[]>('/users'),
};

// Task API
export const taskAPI = {
  create: (title: string, status?: string, assigned_to?: string) =>
    api.post<Task>('/tasks', { title, status, assigned_to }),
  getAll: () =>
    api.get<Task[]>('/tasks'),
  update: (id: string, title?: string, status?: string, assigned_to?: string | null, version?: number) =>
    api.put<Task>(`/tasks/${id}`, { title, status, assigned_to, version }),
  delete: (id: string) =>
    api.delete(`/tasks/${id}`),
};

export const isConflictError = (error: unknown): error is AxiosError<ConflictError> => {
  return axios.isAxiosError(error) && error.response?.status === 409;
};

export const getConflictData = (error: AxiosError<ConflictError>): ConflictError | null => {
  return error.response?.data || null;
};
