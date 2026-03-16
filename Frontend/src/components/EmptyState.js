/**
 * @fileoverview Empty state illustration shown when no assignments exist.
 */
'use client';

import { motion } from 'framer-motion';
import { FileText, Plus } from 'lucide-react';
import Link from 'next/link';

export default function EmptyState() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex flex-col items-center justify-center py-20 text-center"
    >
      <motion.div
        animate={{ y: [0, -10, 0] }}
        transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
        className="w-24 h-24 rounded-full bg-white/5 border border-white/10 flex items-center justify-center mb-6"
      >
        <FileText size={40} className="text-gray-500" />
      </motion.div>
      <h3 className="text-xl font-semibold text-white mb-2">No assignments yet</h3>
      <p className="text-gray-400 mb-8 max-w-sm">
        Generate your first AI-powered assignment and it will appear here.
      </p>
      <Link href="/generate">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="gradient-btn px-6 py-3 flex items-center gap-2"
        >
          <Plus size={18} />
          Generate Assignment
        </motion.button>
      </Link>
    </motion.div>
  );
}
