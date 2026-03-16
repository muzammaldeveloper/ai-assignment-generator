/**
 * @fileoverview Landing page — Hero, Features grid, How-it-works, and Footer.
 */
'use client';

import { useState, useEffect } from 'react';
import Navbar from '@/components/Navbar';
import HeroSection from '@/components/HeroSection';
import FeaturesSection from '@/components/FeaturesSection';
import HowItWorks from '@/components/HowItWorks';
import Footer from '@/components/Footer';

export default function HomePage() {
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  if (!mounted) return <main className="min-h-screen bg-[#0a0a0f]" />;

  return (
    <main className="min-h-screen">
      <Navbar />
      <HeroSection />
      <FeaturesSection />
      <HowItWorks />
      <Footer />
    </main>
  );
}
