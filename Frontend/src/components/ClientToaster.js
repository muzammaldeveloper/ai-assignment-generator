'use client';

import { useState, useEffect } from 'react';
import { Toaster } from 'react-hot-toast';

export default function ClientToaster() {
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  if (!mounted) return null;

  return (
    <Toaster
      position="top-right"
      toastOptions={{
        duration: 4000,
        style: {
          background: 'rgba(24, 24, 27, 0.9)',
          color: '#fff',
          border: '1px solid rgba(255,255,255,0.1)',
          backdropFilter: 'blur(12px)',
          borderRadius: '12px',
        },
        success: { iconTheme: { primary: '#6366f1', secondary: '#fff' } },
        error: { iconTheme: { primary: '#ef4444', secondary: '#fff' } },
      }}
    />
  );
}
