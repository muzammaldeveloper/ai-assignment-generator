/**
 * @fileoverview Fixed glassmorphism navigation bar with auth state awareness and mobile menu.
 */
'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, Menu, X, LogOut, User } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';

const publicLinks = [
  { href: '/', label: 'Home' },
  { href: '/docs', label: 'API Docs' },
];

const authLinks = [
  { href: '/dashboard', label: 'Dashboard' },
  { href: '/generate', label: 'Generate' },
  { href: '/docs', label: 'API Docs' },
];

export default function Navbar() {
  const { user, logout, isAuthenticated } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);
  const pathname = usePathname();
  const links = isAuthenticated ? authLinks : publicLinks;

  return (
    <motion.nav
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="fixed top-0 left-0 right-0 z-50 bg-gray-950/70 backdrop-blur-xl border-b border-white/5"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 group">
            <motion.div whileHover={{ rotate: 15 }} transition={{ type: 'spring' }}>
              <Sparkles size={24} className="text-indigo-400 group-hover:text-purple-400 transition-colors" />
            </motion.div>
            <span className="font-bold text-lg gradient-text hidden sm:inline">AI Assignment Generator</span>
            <span className="font-bold text-lg gradient-text sm:hidden">AI AssignGen</span>
          </Link>

          {/* Desktop links */}
          <div className="hidden md:flex items-center gap-1">
            {links.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={`relative px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                  pathname === link.href ? 'text-white' : 'text-gray-400 hover:text-white'
                }`}
              >
                {pathname === link.href && (
                  <motion.div
                    layoutId="nav-active"
                    className="absolute inset-0 bg-white/10 rounded-lg"
                    transition={{ type: 'spring', bounce: 0.2, duration: 0.5 }}
                  />
                )}
                <span className="relative z-10">{link.label}</span>
              </Link>
            ))}
          </div>

          {/* Auth buttons */}
          <div className="hidden md:flex items-center gap-3">
            {isAuthenticated ? (
              <>
                <div className="flex items-center gap-2 px-3 py-1.5 glass rounded-full text-sm">
                  <User size={14} className="text-indigo-400" />
                  <span className="text-gray-300">{user?.name}</span>
                </div>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={logout}
                  className="flex items-center gap-1.5 text-sm text-gray-400 hover:text-red-400 transition-colors px-3 py-1.5"
                >
                  <LogOut size={14} />
                  Logout
                </motion.button>
              </>
            ) : (
              <>
                <Link href="/login">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="text-sm text-gray-300 hover:text-white px-4 py-2 transition-colors"
                  >
                    Login
                  </motion.button>
                </Link>
                <Link href="/register">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="gradient-btn text-sm px-5 py-2"
                  >
                    Get Started
                  </motion.button>
                </Link>
              </>
            )}
          </div>

          {/* Mobile hamburger */}
          <button className="md:hidden text-gray-400" onClick={() => setMobileOpen(!mobileOpen)}>
            {mobileOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden bg-gray-950/95 backdrop-blur-xl border-t border-white/5"
          >
            <div className="px-4 py-4 space-y-2">
              {links.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={() => setMobileOpen(false)}
                  className={`block px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                    pathname === link.href
                      ? 'bg-white/10 text-white'
                      : 'text-gray-400 hover:text-white hover:bg-white/5'
                  }`}
                >
                  {link.label}
                </Link>
              ))}
              <div className="pt-3 border-t border-white/10">
                {isAuthenticated ? (
                  <button
                    onClick={() => { logout(); setMobileOpen(false); }}
                    className="flex items-center gap-2 w-full px-4 py-2.5 text-sm text-red-400 hover:bg-white/5 rounded-lg"
                  >
                    <LogOut size={14} /> Logout
                  </button>
                ) : (
                  <div className="flex gap-2">
                    <Link href="/login" className="flex-1" onClick={() => setMobileOpen(false)}>
                      <button className="w-full text-sm text-gray-300 border border-white/10 rounded-lg py-2.5">
                        Login
                      </button>
                    </Link>
                    <Link href="/register" className="flex-1" onClick={() => setMobileOpen(false)}>
                      <button className="w-full gradient-btn text-sm py-2.5">Sign Up</button>
                    </Link>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.nav>
  );
}
