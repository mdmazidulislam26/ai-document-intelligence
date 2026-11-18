/**
 * Centralized API client and base URL configuration.
 * Adapts automatically to browser origin, environment variables, or local development.
 */

export const getApiBaseUrl = (): string => {
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL.replace(/\/+$/, '');
  }
  // If running in browser and no env var provided, fallback to relative or localhost:8000
  if (typeof window !== 'undefined') {
    // If in GitHub Codespaces or reverse proxy, check if port 8000 can be accessed or use same origin
    const host = window.location.hostname;
    if (host.includes('github.dev') || host.includes('app.github.dev')) {
      return window.location.origin.replace('-3000', '-8000');
    }
  }
  return 'http://localhost:8000';
};

export const API_BASE_URL = getApiBaseUrl();
