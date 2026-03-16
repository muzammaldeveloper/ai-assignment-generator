/**
 * @fileoverview Dashboard page — assignment list, pagination, stats, and empty state.
 */
'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Plus, BarChart3, CheckCircle, Clock, AlertCircle, ChevronLeft, ChevronRight } from 'lucide-react';
import Link from 'next/link';
import PageTransition from '@/components/PageTransition';
import AssignmentCard from '@/components/AssignmentCard';
import StatsCard from '@/components/StatsCard';
import EmptyState from '@/components/EmptyState';
import LoadingSpinner from '@/components/LoadingSpinner';
import { useAssignments } from '@/hooks/useAssignments';

export default function DashboardPage() {
  const [page, setPage] = useState(1);
  const { assignments, pagination, loading, stats } = useAssignments(page, 10);

  return (
    <PageTransition>
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white">My Assignments</h1>
          <p className="text-gray-400 text-sm mt-1">Manage and view your generated assignments</p>
        </div>
        <Link href="/generate">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="gradient-btn px-6 py-3 flex items-center gap-2"
          >
            <Plus size={18} />
            New Assignment
          </motion.button>
        </Link>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatsCard label="Total" value={stats.total} icon={BarChart3} color="indigo" />
        <StatsCard label="Completed" value={stats.completed} icon={CheckCircle} color="green" />
        <StatsCard label="In Progress" value={stats.inProgress} icon={Clock} color="yellow" />
        <StatsCard label="Failed" value={stats.failed} icon={AlertCircle} color="red" />
      </div>

      {/* Assignment list */}
      {loading ? (
        <div className="flex items-center justify-center py-20">
          <LoadingSpinner size={36} />
        </div>
      ) : assignments.length === 0 ? (
        <EmptyState />
      ) : (
        <>
          <div className="grid grid-cols-1 gap-4">
            {assignments.map((a, i) => (
              <AssignmentCard key={a.id} assignment={a} index={i} />
            ))}
          </div>

          {/* Pagination */}
          {pagination && pagination.total_pages > 1 && (
            <div className="flex items-center justify-center gap-4 mt-8">
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={!pagination.has_prev}
                className="glass p-2.5 disabled:opacity-30"
              >
                <ChevronLeft size={18} />
              </motion.button>
              <span className="text-sm text-gray-400">
                Page {pagination.page} of {pagination.total_pages}
              </span>
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => setPage((p) => p + 1)}
                disabled={!pagination.has_next}
                className="glass p-2.5 disabled:opacity-30"
              >
                <ChevronRight size={18} />
              </motion.button>
            </div>
          )}
        </>
      )}
    </PageTransition>
  );
}
