import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { ApiError } from '../types';

const runtimeDefault = (typeof window !== 'undefined' && window.location.hostname !== 'localhost')
  ? 'https://tripeasy-backend.vercel.app'
  : 'http://localhost:8000';

const API_BASE_URL = process.env.REACT_APP_API_URL || runtimeDefault;

console.info('[TripEasy] API_BASE_URL =', API_BASE_URL);

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add auth token if available
        const token = localStorage.getItem('auth_token');
        if (token) {
          (config.headers as any).Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response: AxiosResponse) => {
        return response;
      },
      (error) => {
        const apiError: ApiError = {
          detail: error.response?.data?.detail || error.message || 'Đã xảy ra lỗi',
          status_code: error.response?.status || 500,
        };
        return Promise.reject(apiError);
      }
    );
  }

  async get<T>(url: string, params?: any): Promise<T> {
    const response = await this.client.get<T>(url, { params });
    return response.data;
  }

  async post<T>(url: string, data?: any): Promise<T> {
    const response = await this.client.post<T>(url, data);
    return response.data;
  }

  async put<T>(url: string, data?: any): Promise<T> {
    const response = await this.client.put<T>(url, data);
    return response.data;
  }

  async delete<T>(url: string): Promise<T> {
    const response = await this.client.delete<T>(url);
    return response.data;
  }
}

export const apiClient = new ApiClient();
