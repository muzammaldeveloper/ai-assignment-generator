/**
 * @fileoverview Register page — glass card form with name, email, password, and strength indicator.
 */
'use client';

import { useState, useMemo, useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Mail, Lock, User, UserPlus, Eye, EyeOff } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import LoadingSpinner from '@/components/LoadingSpinner';
import Navbar from '@/components/Navbar';
import PageTransition from '@/components/PageTransition';

function getPasswordStrength(pwd) {
  let score = 0;
  if (pwd.length >= 6) score++;
  if (pwd.length >= 10) score++;
  if (/[A-Z]/.test(pwd)) score++;
  if (/[0-9]/.test(pwd)) score++;
  if (/[^A-Za-z0-9]/.test(pwd)) score++;
  return score; // 0-5
}

const strengthColors = ['bg-red-500', 'bg-red-500', 'bg-orange-500', 'bg-yellow-500', 'bg-green-500', 'bg-emerald-500'];
const strengthLabels = ['', 'Weak', 'Fair', 'Good', 'Strong', 'Very Strong'];

export default function RegisterPage() {
  const { register } = useAuth();
  const [name, setName] = useState('');
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPwd, setShowPwd] = useState(false);
  const [loading, setLoading] = useState(false);

  const strength = useMemo(() => getPasswordStrength(password), [password]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await register(name, email, password);
    } catch {
      // handled by interceptor
    } finally {
      setLoading(false);
    }
  };

  if (!mounted) return <main className="min-h-screen bg-[#0a0a0f]" />;

  return (
    <main className="min-h-screen relative">
      <Navbar />
      {/* Background blobs */}
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute top-1/3 right-1/3 w-80 h-80 bg-pink-500/20 rounded-full blur-3xl animate-blob" />
        <div className="absolute bottom-1/3 left-1/4 w-80 h-80 bg-indigo-500/20 rounded-full blur-3xl animate-blob animation-delay-4000" />
      </div>

      <PageTransition className="flex items-center justify-center min-h-screen pt-16 px-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="w-full max-w-md glass p-8"
        >
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold gradient-text mb-2">Create Account</h1>
            <p className="text-gray-400 text-sm">Start generating assignments for free</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="relative">
              <User size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" />
              <input
                type="text"
                placeholder="Full name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                className="input-glass pl-11"
              />
            </div>

            <div className="relative">
              <Mail size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" />
              <input
                type="email"
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="input-glass pl-11"
              />
            </div>

            <div>
              <div className="relative">
                <Lock size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" />
                <input
                  type={showPwd ? 'text' : 'password'}
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  minLength={6}
                  className="input-glass pl-11 pr-11"
                />
                <button
                  type="button"
                  onClick={() => setShowPwd(!showPwd)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300"
                >
                  {showPwd ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
              {/* Strength indicator */}
              {password.length > 0 && (
                <div className="mt-2">
                  <div className="flex gap-1 mb-1">
                    {[...Array(5)].map((_, i) => (
                      <div
                        key={i}
                        className={`h-1 flex-1 rounded-full transition-all ${
                          i < strength ? strengthColors[strength] : 'bg-white/10'
                        }`}
                      />
                    ))}
                  </div>
                  <p className="text-xs text-gray-500">{strengthLabels[strength]}</p>
                </div>
              )}
            </div>

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              type="submit"
              disabled={loading}
              className="w-full gradient-btn py-3.5 flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {loading ? <LoadingSpinner size={18} /> : <UserPlus size={18} />}
              {loading ? 'Creating account...' : 'Create Account'}
            </motion.button>
          </form>

          <p className="mt-6 text-center text-sm text-gray-500">
            Already have an account?{' '}
            <Link href="/login" className="text-indigo-400 hover:text-indigo-300 font-medium">
              Sign in
            </Link>
          </p>
        </motion.div>
      </PageTransition>
    </main>
  );
}
