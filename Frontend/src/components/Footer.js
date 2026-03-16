/**
 * @fileoverview Site footer with branding and social links.
 */
'use client';

import { motion } from 'framer-motion';
import { Sparkles, Github, Twitter, Heart } from 'lucide-react';
import Link from 'next/link';

export default function Footer() {
  return (
    <motion.footer
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true }}
      className="border-t border-white/5 bg-[#0a0a0f]"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="md:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <Sparkles size={20} className="text-indigo-400" />
              <span className="font-bold gradient-text">AI Assignment Generator</span>
            </div>
            <p className="text-gray-500 text-sm max-w-sm">
              Generate professional, AI-powered academic assignments with real-time web research,
              AI images, and beautiful document formatting.
            </p>
          </div>

          {/* Links */}
          <div>
            <h4 className="text-sm font-semibold text-white mb-4">Product</h4>
            <ul className="space-y-2 text-sm text-gray-500">
              <li><Link href="/generate" className="hover:text-white transition-colors">Generate</Link></li>
              <li><Link href="/dashboard" className="hover:text-white transition-colors">Dashboard</Link></li>
              <li><Link href="/docs" className="hover:text-white transition-colors">API Docs</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-sm font-semibold text-white mb-4">Account</h4>
            <ul className="space-y-2 text-sm text-gray-500">
              <li><Link href="/login" className="hover:text-white transition-colors">Login</Link></li>
              <li><Link href="/register" className="hover:text-white transition-colors">Register</Link></li>
            </ul>
          </div>
        </div>

        <div className="mt-12 pt-8 border-t border-white/5 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-gray-600 flex items-center gap-1">
            Made with <Heart size={12} className="text-red-500" /> by AI Assignment Generator Team
          </p>
          <p className="text-xs text-gray-600">&copy; {new Date().getFullYear()} All rights reserved.</p>
        </div>
      </div>
    </motion.footer>
  );
}
