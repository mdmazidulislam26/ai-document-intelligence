/**
 * Centralized API client, authentication header management, and base URL configuration.
 */

import axios from 'axios';

const API_KEY_STORAGE_KEY = 'docintel_api_key';
const DEFAULT_DEV_KEY = 'dev-local-api-key-change-me';

export const getApiBaseUrl = (): string => {
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL.replace(/\/+$/, '');
  }
  if (typeof window !== 'undefined') {
    const host = window.location.hostname;
    if (host.includes('github.dev') || host.includes('app.github.dev')) {
      return window.location.origin.replace('-3000', '-8000');
    }
  }
  return 'http://localhost:8000';
};

export const API_BASE_URL = getApiBaseUrl();

export function getStoredApiKey(): string {
  if (typeof window === 'undefined') return '';
  const stored = window.localStorage.getItem(API_KEY_STORAGE_KEY);
  if (stored) return stored;
  if (process.env.NODE_ENV === 'development') {
    return DEFAULT_DEV_KEY;
  }
  return '';
}

export function setStoredApiKey(key: string): void {
  if (typeof window === 'undefined') return;
  if (key.trim()) {
    window.localStorage.setItem(API_KEY_STORAGE_KEY, key.trim());
  } else {
    window.localStorage.removeItem(API_KEY_STORAGE_KEY);
  }
}

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

apiClient.interceptors.request.use((config) => {
  const key = getStoredApiKey();
  if (key) {
    config.headers['X-API-Key'] = key;
  }
  return config;
});
