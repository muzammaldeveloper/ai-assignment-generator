/**
 * @fileoverview Assignment detail page — shows full assignment content with auto-polling.
 */
'use client';

import { use } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { ArrowLeft } from 'lucide-react';
import PageTransition from '@/components/PageTransition';
import AssignmentViewer from '@/components/AssignmentViewer';
import { useAssignmentDetail } from '@/hooks/useAssignments';

export default function AssignmentDetailPage({ params }) {
  const { id } = use(params);
  const { assignment, loading, refetch } = useAssignmentDetail(id);

  return (
    <PageTransition>
      <div className="mb-6">
        <Link href="/dashboard">
          <motion.button
            whileHover={{ x: -4 }}
            className="flex items-center gap-2 text-sm text-gray-400 hover:text-white transition-colors"
          >
            <ArrowLeft size={16} />
            Back to Dashboard
          </motion.button>
        </Link>
      </div>

      <AssignmentViewer assignment={assignment} loading={loading} refetch={refetch} />
    </PageTransition>
  );
}
