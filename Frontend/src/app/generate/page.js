/**
 * @fileoverview Generate page — multi-step wizard for creating a new assignment.
 */
'use client';

import Navbar from '@/components/Navbar';
import ProtectedRoute from '@/components/ProtectedRoute';
import PageTransition from '@/components/PageTransition';
import GenerateForm from '@/components/GenerateForm';

export default function GeneratePage() {
  return (
    <ProtectedRoute>
      <Navbar />
      <main className="pt-24 pb-16 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto">
        <PageTransition>
          <div className="text-center mb-10">
            <h1 className="text-3xl sm:text-4xl font-bold mb-3">
              Generate <span className="gradient-text">Assignment</span>
            </h1>
            <p className="text-gray-400">Configure your assignment and let AI do the rest.</p>
          </div>
          <GenerateForm />
        </PageTransition>
      </main>
    </ProtectedRoute>
  );
}
