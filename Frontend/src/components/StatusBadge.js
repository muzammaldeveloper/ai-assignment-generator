/**
 * @fileoverview Color-coded assignment status badge with emoji and animation.
 */
'use client';

import { motion } from 'framer-motion';
import { STATUS_CONFIG } from '@/lib/constants';

export default function StatusBadge({ status }) {
  const config = STATUS_CONFIG[status] || STATUS_CONFIG.pending;

  return (
    <motion.span
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      className={`inline-flex items-center gap-1.5 px-3 py-1 text-xs font-medium rounded-full border ${config.bg} ${config.color}`}
    >
      <span>{config.emoji}</span>
      {config.label}
    </motion.span>
  );
}
