/**
 * @fileoverview Custom hook for authentication state management.
 * Provides user data, loading state, login/register/logout actions.
 */
'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import {
  login as loginFn,
  register as registerFn,
  logout as logoutFn,
  fetchUser,
  getStoredUser,
  isAuthenticated,
} from '@/lib/auth';

export function useAuth() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const stored = getStoredUser();
    if (stored) setUser(stored);

    if (isAuthenticated()) {
      fetchUser()
        .then((u) => setUser(u))
        .catch(() => {})
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = useCallback(
    async (email, password) => {
      const data = await loginFn({ email, password });
      setUser(data.user);
      toast.success('Welcome back!');
      router.push('/dashboard');
      return data;
    },
    [router]
  );

  const register = useCallback(
    async (name, email, password) => {
      const data = await registerFn({ name, email, password });
      setUser(data.user);
      toast.success('Account created successfully!');
      router.push('/dashboard');
      return data;
    },
    [router]
  );

  const logout = useCallback(() => {
    logoutFn();
    setUser(null);
    toast.success('Logged out');
  }, []);

  return { user, loading, login, register, logout, isAuthenticated: !!user };
}
