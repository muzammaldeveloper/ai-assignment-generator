/**
 * @fileoverview Authentication helpers — login, register, logout, and user retrieval.
 */

import Cookies from 'js-cookie';
import api from './api';

/**
 * Register a new user.
 * @param {{ name: string, email: string, password: string }} payload
 */
export async function register(payload) {
  const { data } = await api.post('/auth/register', payload);
  saveSession(data.data);
  return data.data;
}

/**
 * Log in an existing user.
 * @param {{ email: string, password: string }} payload
 */
export async function login(payload) {
  const { data } = await api.post('/auth/login', payload);
  saveSession(data.data);
  return data.data;
}

/**
 * Log out: clear cookies and redirect to landing.
 */
export function logout() {
  Cookies.remove('access_token');
  Cookies.remove('refresh_token');
  Cookies.remove('user');
  if (typeof window !== 'undefined') {
    window.location.href = '/';
  }
}

/**
 * Fetch the current authenticated user profile.
 */
export async function fetchUser() {
  const { data } = await api.get('/auth/me');
  return data.data;
}

/**
 * Get stored user from cookies.
 * @returns {object|null}
 */
export function getStoredUser() {
  try {
    const raw = Cookies.get('user');
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

/**
 * Check if user is authenticated (has access token).
 */
export function isAuthenticated() {
  return !!Cookies.get('access_token');
}

/** Persist session tokens and user data in cookies. */
function saveSession({ user, access_token, refresh_token }) {
  Cookies.set('access_token', access_token, { sameSite: 'Lax' });
  Cookies.set('refresh_token', refresh_token, { sameSite: 'Lax' });
  Cookies.set('user', JSON.stringify(user), { sameSite: 'Lax' });
}
