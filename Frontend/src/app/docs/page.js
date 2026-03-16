/**
 * @fileoverview API Documentation page — beautiful, interactive endpoint docs with expandable sections.
 */
'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, Lock, Unlock, Copy, Check } from 'lucide-react';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import PageTransition from '@/components/PageTransition';

const MethodBadge = ({ method }) => {
  const colors = {
    GET: 'bg-green-500/10 text-green-400 border-green-500/20',
    POST: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    PUT: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
    DELETE: 'bg-red-500/10 text-red-400 border-red-500/20',
  };
  return (
    <span className={`px-2.5 py-0.5 rounded-md text-xs font-bold border ${colors[method]}`}>
      {method}
    </span>
  );
};

const CodeBlock = ({ code }) => {
  const [copied, setCopied] = useState(false);
  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  return (
    <div className="relative group">
      <pre className="bg-black/40 border border-white/5 rounded-xl p-4 text-xs text-gray-300 overflow-x-auto">
        <code>{code}</code>
      </pre>
      <button
        onClick={handleCopy}
        className="absolute top-3 right-3 p-1.5 rounded-lg bg-white/5 border border-white/10 opacity-0 group-hover:opacity-100 transition-opacity"
      >
        {copied ? <Check size={12} className="text-green-400" /> : <Copy size={12} className="text-gray-400" />}
      </button>
    </div>
  );
};

const EndpointCard = ({ method, path, description, auth, requestBody, responseBody, curl }) => {
  const [open, setOpen] = useState(false);
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      className="glass overflow-hidden"
    >
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center gap-3 p-4 sm:p-5 text-left hover:bg-white/[0.03] transition-colors"
      >
        <MethodBadge method={method} />
        <code className="text-sm text-white font-medium flex-1">{path}</code>
        {auth ? (
          <Lock size={14} className="text-yellow-400 shrink-0" />
        ) : (
          <Unlock size={14} className="text-green-400 shrink-0" />
        )}
        <motion.div animate={{ rotate: open ? 180 : 0 }} transition={{ duration: 0.2 }}>
          <ChevronDown size={16} className="text-gray-500" />
        </motion.div>
      </button>
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="overflow-hidden"
          >
            <div className="px-4 sm:px-5 pb-5 space-y-4 border-t border-white/5 pt-4">
              <p className="text-sm text-gray-400">{description}</p>
              {auth && (
                <div className="flex items-center gap-2 text-xs text-yellow-400/70">
                  <Lock size={12} />
                  Requires JWT authentication (Authorization: Bearer &lt;token&gt;)
                </div>
              )}
              {requestBody && (
                <div>
                  <h4 className="text-xs font-semibold text-gray-400 uppercase mb-2">Request Body</h4>
                  <CodeBlock code={requestBody} />
                </div>
              )}
              {responseBody && (
                <div>
                  <h4 className="text-xs font-semibold text-gray-400 uppercase mb-2">Response</h4>
                  <CodeBlock code={responseBody} />
                </div>
              )}
              {curl && (
                <div>
                  <h4 className="text-xs font-semibold text-gray-400 uppercase mb-2">cURL Example</h4>
                  <CodeBlock code={curl} />
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

const endpoints = {
  Authentication: [
    {
      method: 'POST',
      path: '/api/v1/auth/register',
      description: 'Register a new user account. Returns user data and JWT tokens.',
      auth: false,
      requestBody: JSON.stringify({ name: 'Muzammal', email: 'muzammal@test.com', password: 'MyPass123' }, null, 2),
      responseBody: JSON.stringify({
        success: true,
        data: {
          user: { id: 'uuid', name: 'Muzammal', email: 'muzammal@test.com' },
          access_token: 'eyJ...',
          refresh_token: 'eyJ...',
        },
      }, null, 2),
      curl: `curl -X POST http://localhost:5000/api/v1/auth/register \\
  -H "Content-Type: application/json" \\
  -d '{"name":"Muzammal","email":"muzammal@test.com","password":"MyPass123"}'`,
    },
    {
      method: 'POST',
      path: '/api/v1/auth/login',
      description: 'Authenticate an existing user. Returns JWT access and refresh tokens.',
      auth: false,
      requestBody: JSON.stringify({ email: 'muzammal@test.com', password: 'MyPass123' }, null, 2),
      responseBody: JSON.stringify({
        success: true,
        data: {
          user: { id: 'uuid', name: 'Muzammal', email: 'muzammal@test.com' },
          access_token: 'eyJ...',
          refresh_token: 'eyJ...',
        },
      }, null, 2),
      curl: `curl -X POST http://localhost:5000/api/v1/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{"email":"muzammal@test.com","password":"MyPass123"}'`,
    },
    {
      method: 'POST',
      path: '/api/v1/auth/refresh',
      description: 'Refresh an expired access token using the refresh token.',
      auth: true,
      responseBody: JSON.stringify({ success: true, data: { access_token: 'eyJ...' } }, null, 2),
      curl: `curl -X POST http://localhost:5000/api/v1/auth/refresh \\
  -H "Authorization: Bearer <refresh_token>"`,
    },
    {
      method: 'GET',
      path: '/api/v1/auth/me',
      description: 'Get the currently authenticated user profile.',
      auth: true,
      responseBody: JSON.stringify({
        success: true,
        data: { id: 'uuid', name: 'Muzammal', email: 'muzammal@test.com' },
      }, null, 2),
      curl: `curl http://localhost:5000/api/v1/auth/me \\
  -H "Authorization: Bearer <access_token>"`,
    },
  ],
  Assignments: [
    {
      method: 'POST',
      path: '/api/v1/assignments/generate',
      description: 'Start generating a new AI-powered assignment. Returns immediately with assignment ID and status URL. The generation runs asynchronously in the background.',
      auth: true,
      requestBody: JSON.stringify({
        topic: 'Artificial Intelligence in Healthcare',
        academic_level: 'university',
        word_count: 1500,
        citation_style: 'apa',
        template: 'professional',
      }, null, 2),
      responseBody: JSON.stringify({
        success: true,
        message: 'Assignment generation started!',
        data: { assignment_id: 'uuid', status: 'pending', status_url: '/api/v1/assignments/uuid' },
      }, null, 2),
      curl: `curl -X POST http://localhost:5000/api/v1/assignments/generate \\
  -H "Authorization: Bearer <token>" \\
  -H "Content-Type: application/json" \\
  -d '{"topic":"AI in Healthcare","academic_level":"university","word_count":1500,"citation_style":"apa","template":"professional"}'`,
    },
    {
      method: 'GET',
      path: '/api/v1/assignments',
      description: 'List all assignments for the current user with pagination. Supports page, per_page, and status query parameters.',
      auth: true,
      responseBody: JSON.stringify({
        success: true,
        data: {
          assignments: [{ id: 'uuid', topic: 'AI in Healthcare', status: 'completed', progress_percent: 100 }],
          pagination: { page: 1, per_page: 10, total: 5, total_pages: 1, has_next: false, has_prev: false },
        },
      }, null, 2),
      curl: `curl "http://localhost:5000/api/v1/assignments?page=1&per_page=10" \\
  -H "Authorization: Bearer <token>"`,
    },
    {
      method: 'GET',
      path: '/api/v1/assignments/:id',
      description: 'Get full assignment details including sections, images, and references. Use this endpoint to poll for status updates during generation.',
      auth: true,
      responseBody: JSON.stringify({
        success: true,
        data: {
          id: 'uuid',
          topic: 'AI in Healthcare',
          status: 'completed',
          sections: [{ title: 'Introduction', content: '...', order: 0 }],
          images: [{ image_url: '/path/to/image.png', caption: 'Figure 1' }],
          references: [{ citation: 'Smith, J. (2025). AI in Healthcare...', source_url: '...' }],
        },
      }, null, 2),
      curl: `curl http://localhost:5000/api/v1/assignments/<id> \\
  -H "Authorization: Bearer <token>"`,
    },
    {
      method: 'GET',
      path: '/api/v1/assignments/:id/download?format=docx',
      description: 'Download the completed assignment as a DOCX or PDF file. Supports format=docx and format=pdf query parameters.',
      auth: true,
      responseBody: 'Binary file blob (application/octet-stream)',
      curl: `curl -O http://localhost:5000/api/v1/assignments/<id>/download?format=docx \\
  -H "Authorization: Bearer <token>"`,
    },
  ],
  System: [
    {
      method: 'GET',
      path: '/api/v1/health',
      description: 'Health check endpoint. Returns service status and uptime. No authentication required.',
      auth: false,
      responseBody: JSON.stringify({ success: true, data: { status: 'healthy' } }, null, 2),
      curl: 'curl http://localhost:5000/api/v1/health',
    },
  ],
};

export default function DocsPage() {
  return (
    <main className="min-h-screen">
      <Navbar />
      <PageTransition className="pt-24 pb-16 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-3xl sm:text-4xl font-bold mb-3">
            API <span className="gradient-text">Documentation</span>
          </h1>
          <p className="text-gray-400 max-w-lg mx-auto">
            Complete reference for the AI Assignment Generator REST API.
          </p>
        </div>

        {/* Auth flow info */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass p-6 mb-10"
        >
          <h2 className="text-lg font-semibold text-white mb-3">🔐 Authentication Flow</h2>
          <ol className="list-decimal list-inside space-y-2 text-sm text-gray-400">
            <li>Register a new account or login to get JWT tokens</li>
            <li>Include the access token in all protected requests: <code className="text-indigo-400">Authorization: Bearer &lt;token&gt;</code></li>
            <li>When the access token expires (401), use the refresh endpoint with your refresh token</li>
            <li>If the refresh token is also expired, log in again</li>
          </ol>
        </motion.div>

        {/* Endpoint groups */}
        <div className="space-y-10">
          {Object.entries(endpoints).map(([group, items]) => (
            <div key={group}>
              <h2 className="text-xl font-bold text-white mb-4">{group}</h2>
              <div className="space-y-3">
                {items.map((ep) => (
                  <EndpointCard key={`${ep.method}-${ep.path}`} {...ep} />
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Error format */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="glass p-6 mt-10"
        >
          <h2 className="text-lg font-semibold text-white mb-3">⚠️ Error Response Format</h2>
          <CodeBlock
            code={JSON.stringify(
              { success: false, message: 'Error description', errors: { field: ['Validation error'] } },
              null,
              2
            )}
          />
        </motion.div>
      </PageTransition>
      <Footer />
    </main>
  );
}
