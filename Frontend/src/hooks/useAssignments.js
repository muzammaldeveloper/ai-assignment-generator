/**
 * @fileoverview Custom hook for fetching and managing assignment data.
 * Provides list, detail, generation, and polling capabilities.
 */
'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import api from '@/lib/api';
import { PROCESSING_STATUSES } from '@/lib/constants';

/**
 * Hook to list assignments with pagination.
 */
export function useAssignments(page = 1, perPage = 10) {
  const [assignments, setAssignments] = useState([]);
  const [pagination, setPagination] = useState(null);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({ total: 0, completed: 0, inProgress: 0, failed: 0 });

  const fetchAssignments = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await api.get('/assignments', { params: { page, per_page: perPage } });
      setAssignments(data.data.assignments);
      setPagination(data.data.pagination);

      // Compute stats from first-page data (good enough for dashboard)
      const all = data.data.assignments;
      setStats({
        total: data.data.pagination.total,
        completed: all.filter((a) => a.status === 'completed').length,
        inProgress: all.filter((a) => PROCESSING_STATUSES.includes(a.status)).length,
        failed: all.filter((a) => a.status === 'failed').length,
      });
    } catch {
      // handled by interceptor
    } finally {
      setLoading(false);
    }
  }, [page, perPage]);

  useEffect(() => {
    fetchAssignments();
  }, [fetchAssignments]);

  return { assignments, pagination, loading, stats, refetch: fetchAssignments };
}

/**
 * Hook to fetch a single assignment and auto-poll while processing.
 */
export function useAssignmentDetail(id) {
  const [assignment, setAssignment] = useState(null);
  const [loading, setLoading] = useState(true);
  const intervalRef = useRef(null);

  const fetchDetail = useCallback(async () => {
    try {
      const { data } = await api.get(`/assignments/${id}`);
      setAssignment(data.data);
      return data.data;
    } catch {
      return null;
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    if (!id) return;
    fetchDetail();

    // Start polling
    intervalRef.current = setInterval(async () => {
      const detail = await fetchDetail();
      if (detail && !PROCESSING_STATUSES.includes(detail.status)) {
        clearInterval(intervalRef.current);
      }
    }, 5000);

    return () => clearInterval(intervalRef.current);
  }, [id, fetchDetail]);

  return { assignment, loading, refetch: fetchDetail };
}

/**
 * Hook to generate a new assignment.
 */
export function useGenerateAssignment() {
  const [generating, setGenerating] = useState(false);

  const generate = useCallback(async (payload) => {
    setGenerating(true);
    try {
      const { data } = await api.post('/assignments/generate', payload);
      return data.data;
    } finally {
      setGenerating(false);
    }
  }, []);

  return { generate, generating };
}
