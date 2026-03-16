/**
 * @fileoverview Dashboard stats card with animated counter.
 */
'use client';

import { motion, useMotionValue, useTransform, animate } from 'framer-motion';
import { useEffect, useState } from 'react';

export default function StatsCard({ label, value, icon: Icon, color = 'indigo' }) {
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    const controls = animate(0, value, {
      duration: 1.2,
      ease: 'easeOut',
      onUpdate: (v) => setDisplay(Math.round(v)),
    });
    return () => controls.stop();
  }, [value]);

  const colorMap = {
    indigo: 'from-indigo-500/20 to-indigo-500/5 text-indigo-400 border-indigo-500/20',
    green: 'from-green-500/20 to-green-500/5 text-green-400 border-green-500/20',
    yellow: 'from-yellow-500/20 to-yellow-500/5 text-yellow-400 border-yellow-500/20',
    red: 'from-red-500/20 to-red-500/5 text-red-400 border-red-500/20',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -2, scale: 1.02 }}
      className={`glass p-5 bg-gradient-to-br ${colorMap[color]}`}
    >
      <div className="flex items-center justify-between mb-3">
        <span className="text-sm text-gray-400">{label}</span>
        {Icon && <Icon size={20} className={colorMap[color].split(' ').find((c) => c.startsWith('text-'))} />}
      </div>
      <p className="text-3xl font-bold text-white">{display}</p>
    </motion.div>
  );
}
