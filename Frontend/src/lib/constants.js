/**
 * @fileoverview Constants used throughout the application.
 */

export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api/v1';

export const ACADEMIC_LEVELS = [
  { value: 'school', label: 'School', description: 'High school level assignments', icon: '🏫' },
  { value: 'college', label: 'College', description: 'Undergraduate college work', icon: '🎓' },
  { value: 'university', label: 'University', description: 'Advanced university papers', icon: '🏛️' },
  { value: 'research', label: 'Research', description: 'Research-level academic papers', icon: '🔬' },
];

export const WORD_COUNTS = [800, 1000, 1200, 1500, 2000, 3000, 5000];

export const CITATION_STYLES = [
  { value: 'apa', label: 'APA', description: 'American Psychological Association (7th ed.)' },
  { value: 'mla', label: 'MLA', description: 'Modern Language Association (9th ed.)' },
  { value: 'harvard', label: 'Harvard', description: 'Harvard referencing system' },
  { value: 'ieee', label: 'IEEE', description: 'Institute of Electrical and Electronics Engineers' },
];

export const TEMPLATES = [
  { value: 'professional', label: 'Professional', color: 'from-blue-500 to-cyan-500', description: 'Clean and corporate look' },
  { value: 'academic', label: 'Academic', color: 'from-indigo-500 to-purple-500', description: 'Traditional academic style' },
  { value: 'modern', label: 'Modern', color: 'from-purple-500 to-pink-500', description: 'Contemporary minimalist design' },
  { value: 'minimal', label: 'Minimal', color: 'from-gray-400 to-gray-600', description: 'Simple and elegant' },
  { value: 'colorful', label: 'Colorful', color: 'from-orange-500 to-red-500', description: 'Vibrant and eye-catching' },
];

export const STATUS_CONFIG = {
  pending: { label: 'Pending', emoji: '⏳', color: 'text-yellow-400', bg: 'bg-yellow-400/10 border-yellow-400/20' },
  researching: { label: 'Researching', emoji: '🔍', color: 'text-blue-400', bg: 'bg-blue-400/10 border-blue-400/20' },
  outlining: { label: 'Outlining', emoji: '📝', color: 'text-cyan-400', bg: 'bg-cyan-400/10 border-cyan-400/20' },
  generating: { label: 'Generating', emoji: '✍️', color: 'text-purple-400', bg: 'bg-purple-400/10 border-purple-400/20' },
  imaging: { label: 'Creating Images', emoji: '🎨', color: 'text-pink-400', bg: 'bg-pink-400/10 border-pink-400/20' },
  formatting: { label: 'Formatting', emoji: '📄', color: 'text-indigo-400', bg: 'bg-indigo-400/10 border-indigo-400/20' },
  completed: { label: 'Completed', emoji: '✅', color: 'text-green-400', bg: 'bg-green-400/10 border-green-400/20' },
  failed: { label: 'Failed', emoji: '❌', color: 'text-red-400', bg: 'bg-red-400/10 border-red-400/20' },
};

export const PROCESSING_STATUSES = ['pending', 'researching', 'outlining', 'generating', 'imaging', 'formatting'];
