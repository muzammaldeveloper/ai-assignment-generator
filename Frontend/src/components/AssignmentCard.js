/**
 * @fileoverview Assignment list card for the dashboard — shows topic, status, metadata, and progress.
 */
'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { Clock, BookOpen, FileText } from 'lucide-react';
import StatusBadge from './StatusBadge';
import { PROCESSING_STATUSES } from '@/lib/constants';

export default function AssignmentCard({ assignment, index = 0 }) {
  const isProcessing = PROCESSING_STATUSES.includes(assignment.status);
  const date = new Date(assignment.created_at).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric',
  });

  return (
    <Link href={`/dashboard/${assignment.id}`}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: index * 0.05 }}
        whileHover={{ y: -4, transition: { duration: 0.2 } }}
        className="glass-hover p-5 cursor-pointer group"
      >
        <div className="flex items-start justify-between mb-3">
          <h3 className="text-base font-semibold text-white group-hover:text-indigo-300 transition-colors line-clamp-2 flex-1 mr-3">
            {assignment.topic}
          </h3>
          <StatusBadge status={assignment.status} />
        </div>

        {/* Progress bar for in-progress */}
        {isProcessing && (
          <div className="mb-3">
            <div className="flex items-center justify-between text-xs text-gray-500 mb-1">
              <span>Progress</span>
              <span>{assignment.progress_percent}%</span>
            </div>
            <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${assignment.progress_percent}%` }}
                transition={{ duration: 1, ease: 'easeOut' }}
                className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full"
              />
            </div>
          </div>
        )}

        <div className="flex items-center gap-4 text-xs text-gray-500">
          <span className="flex items-center gap-1">
            <Clock size={12} /> {date}
          </span>
          <span className="flex items-center gap-1">
            <FileText size={12} /> {assignment.word_count?.toLocaleString()} words
          </span>
          <span className="flex items-center gap-1 capitalize">
            <BookOpen size={12} /> {assignment.academic_level}
          </span>
        </div>
      </motion.div>
    </Link>
  );
}
