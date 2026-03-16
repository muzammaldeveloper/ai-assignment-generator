/**
 * @fileoverview Assignment detail viewer — shows header, sections, images, references, and download buttons.
 * Auto-polls while assignment is processing.
 */
'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Download, RefreshCw, BookOpen, FileText, Clock, AlertTriangle,
  Image as ImageIcon, BookMarked, Pencil, Check, X, RotateCcw,
} from 'lucide-react';
import StatusBadge from './StatusBadge';
import LoadingSpinner from './LoadingSpinner';
import { PROCESSING_STATUSES } from '@/lib/constants';
import api from '@/lib/api';
import toast from 'react-hot-toast';

export default function AssignmentViewer({ assignment, loading, refetch }) {
  const [editingSectionId, setEditingSectionId] = useState(null);
  const [editedContent, setEditedContent] = useState('');
  const [saving, setSaving] = useState(false);
  const [regenerating, setRegenerating] = useState(false);

  if (loading || !assignment) {
    return (
      <div className="flex items-center justify-center py-32">
        <LoadingSpinner size={40} />
      </div>
    );
  }

  const isProcessing = PROCESSING_STATUSES.includes(assignment.status);
  const isCompleted = assignment.status === 'completed';
  const isFailed = assignment.status === 'failed';

  const handleDownload = async (format) => {
    const toastId = toast.loading(`Preparing ${format.toUpperCase()}...`);
    try {
      const mimeType = format === 'pdf'
        ? 'application/pdf'
        : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
      const response = await api.get(
        `/assignments/${assignment.id}/download?format=${format}`,
        { responseType: 'blob' },
      );
      const blob = new Blob([response.data], { type: mimeType });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      const safeName = assignment.topic.replace(/[^\w\s-]/g, '').trim().replace(/\s+/g, '_');
      link.setAttribute('download', `${safeName}.${format}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      toast.success(`${format.toUpperCase()} downloaded!`, { id: toastId });
    } catch (err) {
      const msg = err?.response?.status === 404
        ? 'File not ready yet — try again after generation completes.'
        : 'Download failed. Please try again.';
      toast.error(msg, { id: toastId });
    }
  };

  const handleEditStart = (section) => {
    setEditingSectionId(section.id);
    setEditedContent(section.content);
  };

  const handleEditCancel = () => {
    setEditingSectionId(null);
    setEditedContent('');
  };

  const handleEditSave = async (sectionId) => {
    setSaving(true);
    try {
      await api.patch(`/assignments/${assignment.id}/sections/${sectionId}`, {
        content: editedContent,
      });
      toast.success('Section saved!');
      setEditingSectionId(null);
      setEditedContent('');
      if (refetch) refetch();
    } catch {
      toast.error('Failed to save. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const handleRegenerateDocs = async () => {
    setRegenerating(true);
    const toastId = toast.loading('Regenerating documents...');
    try {
      await api.post(`/assignments/${assignment.id}/regenerate-docs`);
      toast.success('Documents regenerated! You can now download.', { id: toastId });
      if (refetch) refetch();
    } catch {
      toast.error('Failed to regenerate documents.', { id: toastId });
    } finally {
      setRegenerating(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass p-6 sm:p-8"
      >
        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-4">
          <h1 className="text-2xl sm:text-3xl font-bold gradient-text">{assignment.topic}</h1>
          <StatusBadge status={assignment.status} />
        </div>

        {/* Metadata pills */}
        <div className="flex flex-wrap gap-2 mb-5">
          <span className="flex items-center gap-1 px-3 py-1 glass rounded-full text-xs text-gray-300 capitalize">
            <BookOpen size={12} /> {assignment.academic_level}
          </span>
          <span className="flex items-center gap-1 px-3 py-1 glass rounded-full text-xs text-gray-300">
            <FileText size={12} /> {assignment.word_count?.toLocaleString()} words
          </span>
          <span className="flex items-center gap-1 px-3 py-1 glass rounded-full text-xs text-gray-300 uppercase">
            <BookMarked size={12} /> {assignment.citation_style}
          </span>
          <span className="flex items-center gap-1 px-3 py-1 glass rounded-full text-xs text-gray-300">
            <Clock size={12} /> {new Date(assignment.created_at).toLocaleDateString()}
          </span>
        </div>

        {/* Progress bar */}
        {isProcessing && (
          <div className="mb-5">
            <div className="flex items-center justify-between text-xs text-gray-400 mb-2">
              <span>Generating your assignment...</span>
              <span>{assignment.progress_percent}%</span>
            </div>
            <div className="w-full h-2 bg-white/5 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${assignment.progress_percent}%` }}
                transition={{ duration: 0.8, ease: 'easeOut' }}
                className="h-full bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-full"
              />
            </div>
          </div>
        )}

        {/* Error */}
        {isFailed && assignment.error_message && (
          <div className="flex items-start gap-3 p-4 rounded-xl bg-red-500/10 border border-red-500/20 mb-5">
            <AlertTriangle size={18} className="text-red-400 mt-0.5 shrink-0" />
            <p className="text-sm text-red-300">{assignment.error_message}</p>
          </div>
        )}

        {/* Action buttons */}
        <div className="flex flex-wrap gap-3">
          {isProcessing && (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={refetch}
              className="glass px-4 py-2 text-sm text-gray-300 hover:text-white flex items-center gap-2"
            >
              <RefreshCw size={14} /> Refresh Status
            </motion.button>
          )}
          {isCompleted && (
            <>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => handleDownload('docx')}
                className="gradient-btn px-5 py-2.5 text-sm flex items-center gap-2"
              >
                <Download size={14} /> Download DOCX
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => handleDownload('pdf')}
                className="glass px-5 py-2.5 text-sm text-gray-300 hover:text-white flex items-center gap-2"
              >
                <Download size={14} /> Download PDF
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleRegenerateDocs}
                disabled={regenerating}
                className="glass px-5 py-2.5 text-sm text-gray-300 hover:text-white flex items-center gap-2 disabled:opacity-50"
              >
                <RotateCcw size={14} className={regenerating ? 'animate-spin' : ''} />
                {regenerating ? 'Regenerating...' : 'Regenerate Docs'}
              </motion.button>
            </>
          )}
        </div>
      </motion.div>

      {/* Sections */}
      {assignment.sections?.length > 0 && (
        <div className="space-y-4">
          {assignment.sections
            .sort((a, b) => a.order - b.order)
            .map((section, i) => (
              <motion.div
                key={section.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="glass p-6"
              >
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold text-white">{section.title}</h2>
                  {editingSectionId !== section.id ? (
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={() => handleEditStart(section)}
                      className="glass px-3 py-1.5 text-xs text-gray-300 hover:text-white flex items-center gap-1.5"
                    >
                      <Pencil size={12} /> Edit
                    </motion.button>
                  ) : (
                    <div className="flex gap-2">
                      <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => handleEditSave(section.id)}
                        disabled={saving}
                        className="gradient-btn px-3 py-1.5 text-xs flex items-center gap-1.5 disabled:opacity-50"
                      >
                        <Check size={12} /> {saving ? 'Saving...' : 'Save'}
                      </motion.button>
                      <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={handleEditCancel}
                        className="glass px-3 py-1.5 text-xs text-gray-300 hover:text-white flex items-center gap-1.5"
                      >
                        <X size={12} /> Cancel
                      </motion.button>
                    </div>
                  )}
                </div>
                {editingSectionId === section.id ? (
                  <textarea
                    value={editedContent}
                    onChange={(e) => setEditedContent(e.target.value)}
                    rows={12}
                    className="w-full bg-white/5 border border-white/10 rounded-xl p-4 text-gray-300 text-sm leading-relaxed resize-y focus:outline-none focus:border-indigo-500/50 transition-colors"
                  />
                ) : (
                  <div className="prose prose-invert prose-sm max-w-none">
                    {section.content?.split('\n').map((para, j) => (
                      <p key={j} className="text-gray-300 leading-relaxed mb-3">{para}</p>
                    ))}
                  </div>
                )}
              </motion.div>
            ))}
        </div>
      )}

      {/* Images */}
      {assignment.images?.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass p-6"
        >
          <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
            <ImageIcon size={20} className="text-indigo-400" /> Images
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {assignment.images.map((img) => (
              <div key={img.id} className="rounded-xl overflow-hidden border border-white/10">
                <img src={img.image_url} alt={img.caption} className="w-full h-48 object-cover" />
                {img.caption && (
                  <p className="text-xs text-gray-400 p-3 bg-white/5">{img.caption}</p>
                )}
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* References */}
      {assignment.references?.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass p-6"
        >
          <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
            <BookMarked size={20} className="text-indigo-400" /> References
          </h2>
          <ol className="space-y-3 list-decimal list-inside">
            {assignment.references.map((ref) => (
              <li key={ref.id} className="text-sm text-gray-300">
                {ref.citation}
                {ref.source_url && (
                  <a
                    href={ref.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="ml-2 text-indigo-400 hover:text-indigo-300 underline"
                  >
                    [Link]
                  </a>
                )}
              </li>
            ))}
          </ol>
        </motion.div>
      )}
    </div>
  );
}
