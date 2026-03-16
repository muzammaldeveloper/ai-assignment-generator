/**
 * @fileoverview Protected route wrapper — redirects unauthenticated users to /login.
 */
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated } from '@/lib/auth';
import LoadingSpinner from './LoadingSpinner';

export default function ProtectedRoute({ children }) {
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated()) {
      router.replace('/login');
    }
  }, [router]);

  if (typeof window !== 'undefined' && !isAuthenticated()) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size={40} />
      </div>
    );
  }

  return children;
}
