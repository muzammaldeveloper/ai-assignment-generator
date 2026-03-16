/**
 * @fileoverview Features grid section — lives in a Client Component so Lucide icons
 * can be used directly without crossing the server/client serialization boundary.
 */
'use client';

import { Globe, Cpu, Image, FileText, Shield, Zap } from 'lucide-react';
import FeatureCard from './FeatureCard';

const features = [
  { icon: Globe, title: 'Real-Time Web Research', description: 'Our AI searches and analyzes current web sources to include accurate, up-to-date information in your assignments.' },
  { icon: Cpu, title: 'AI Content Generation', description: 'Powered by GPT-4o, generating structured, coherent academic content that meets university standards.' },
  { icon: Image, title: 'AI-Generated Images', description: 'Automatically creates relevant diagrams and illustrations using Gemini AI to enhance your assignments.' },
  { icon: FileText, title: 'DOCX & PDF Export', description: 'Download professionally formatted documents ready for submission in DOCX or PDF format.' },
  { icon: Shield, title: 'Secure & Private', description: 'Your data is encrypted and never shared. JWT authentication keeps your account safe.' },
  { icon: Zap, title: 'Fast Generation', description: 'Complete assignments generated in minutes, not hours. Our AI pipeline works efficiently in the background.' },
];

export default function FeaturesSection() {
  return (
    <section className="py-24 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">
            Powerful{' '}
            <span className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 bg-clip-text text-transparent">
              Features
            </span>
          </h2>
          <p className="text-gray-400 max-w-lg mx-auto">
            Everything you need to generate professional academic assignments.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {features.map((f, i) => (
            <FeatureCard key={f.title} {...f} delay={i * 0.1} />
          ))}
        </div>
      </div>
    </section>
  );
}
