/**
 * @fileoverview Animated loading spinner with gradient colors.
 */
'use client';

import { motion } from 'framer-motion';
import { Loader2 } from 'lucide-react';

export default function LoadingSpinner({ size = 24, className = '' }) {
  return (
    <motion.div
      animate={{ rotate: 360 }}
      transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
      className={`inline-flex ${className}`}
    >
      <Loader2 size={size} className="text-indigo-400" />
    </motion.div>
  );
}
