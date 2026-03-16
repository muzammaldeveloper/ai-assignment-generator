/**
 * @fileoverview Full-screen hero section with animated blobs, gradient text, CTAs, and feature pills.
 */
'use client';

import { motion } from 'framer-motion';
import { Sparkles, Globe, FileText, Image, Zap, ArrowRight } from 'lucide-react';
import Link from 'next/link';

const pills = [
  { icon: Globe, label: 'Web Research' },
  { icon: FileText, label: 'DOCX & PDF' },
  { icon: Image, label: 'AI Images' },
  { icon: Zap, label: 'Smart Formatting' },
];

export default function HeroSection() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-16">
      {/* Background blobs */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-purple-500/30 rounded-full blur-3xl animate-blob" />
        <div className="absolute top-1/3 right-1/4 w-72 h-72 bg-indigo-500/30 rounded-full blur-3xl animate-blob animation-delay-2000" />
        <div className="absolute bottom-1/4 left-1/2 w-72 h-72 bg-pink-500/30 rounded-full blur-3xl animate-blob animation-delay-4000" />
      </div>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        {/* Badge */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="inline-flex items-center gap-2 px-4 py-2 glass rounded-full text-sm text-indigo-300 mb-8"
        >
          <Sparkles size={14} className="text-indigo-400" />
          AI-Powered Assignment Generation
        </motion.div>

        {/* Heading */}
        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-4xl sm:text-5xl md:text-7xl font-extrabold leading-tight mb-6"
        >
          Generate{' '}
          <span className="gradient-text">Professional</span>
          <br />
          Assignments with AI
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="text-lg sm:text-xl text-gray-400 max-w-2xl mx-auto mb-10"
        >
          Transform any topic into a beautifully formatted, research-backed academic assignment
          in minutes — powered by GPT-4o and real-time web research.
        </motion.p>

        {/* CTA buttons */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16"
        >
          <Link href="/register">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="gradient-btn px-8 py-4 text-lg flex items-center gap-2"
            >
              Get Started Free
              <ArrowRight size={18} />
            </motion.button>
          </Link>
          <Link href="/docs">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="glass px-8 py-4 text-lg text-gray-300 hover:text-white hover:bg-white/10 transition-all"
            >
              View Docs
            </motion.button>
          </Link>
        </motion.div>

        {/* Feature pills */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="flex flex-wrap items-center justify-center gap-3"
        >
          {pills.map((pill, i) => (
            <motion.div
              key={pill.label}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.6 + i * 0.1 }}
              whileHover={{ scale: 1.05, y: -2 }}
              className="flex items-center gap-2 px-4 py-2 glass rounded-full text-sm text-gray-300"
            >
              <pill.icon size={14} className="text-indigo-400" />
              {pill.label}
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
