/**
 * @fileoverview "How it works" section with a 4-step numbered timeline.
 */
'use client';

import { motion } from 'framer-motion';
import { PenLine, Search, Cpu, Download } from 'lucide-react';

const steps = [
  { icon: PenLine, title: 'Enter Your Topic', description: 'Type any academic topic and choose your settings.' },
  { icon: Search, title: 'AI Researches the Web', description: 'Our AI crawls real-time web sources for accurate data.' },
  { icon: Cpu, title: 'Content is Generated', description: 'GPT-4o writes structured, cited academic content.' },
  { icon: Download, title: 'Download Your Assignment', description: 'Get a beautifully formatted DOCX or PDF file.' },
];

export default function HowItWorks() {
  return (
    <section className="py-24 px-4">
      <div className="max-w-5xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">
            How It <span className="gradient-text">Works</span>
          </h2>
          <p className="text-gray-400 max-w-lg mx-auto">
            Four simple steps to go from idea to polished assignment.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 relative">
          {/* Connecting line */}
          <div className="hidden md:block absolute top-12 left-[12%] right-[12%] h-px bg-gradient-to-r from-indigo-500/50 via-purple-500/50 to-pink-500/50" />

          {steps.map((step, i) => (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.15 }}
              className="flex flex-col items-center text-center"
            >
              <motion.div
                whileHover={{ scale: 1.1, rotate: 5 }}
                className="relative w-24 h-24 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center mb-4"
              >
                <step.icon size={28} className="text-indigo-400" />
                <span className="absolute -top-2 -right-2 w-7 h-7 rounded-full gradient-btn text-xs flex items-center justify-center font-bold">
                  {i + 1}
                </span>
              </motion.div>
              <h3 className="text-base font-semibold text-white mb-2">{step.title}</h3>
              <p className="text-sm text-gray-500">{step.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
