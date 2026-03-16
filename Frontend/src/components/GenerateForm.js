/**
 * @fileoverview Multi-step wizard form for generating assignments.
 * 4 steps: Topic → Level & Words → Citation → Template. Animated transitions.
 */
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, ArrowRight, Sparkles, Type, GraduationCap, Quote, Palette } from 'lucide-react';
import toast from 'react-hot-toast';
import { useGenerateAssignment } from '@/hooks/useAssignments';
import { ACADEMIC_LEVELS, WORD_COUNTS, CITATION_STYLES, TEMPLATES } from '@/lib/constants';
import LoadingSpinner from './LoadingSpinner';

const stepIcons = [Type, GraduationCap, Quote, Palette];
const stepLabels = ['Topic', 'Level & Words', 'Citation', 'Template'];

const slideVariants = {
  enter: (dir) => ({ x: dir > 0 ? 300 : -300, opacity: 0 }),
  center: { x: 0, opacity: 1 },
  exit: (dir) => ({ x: dir < 0 ? 300 : -300, opacity: 0 }),
};

export default function GenerateForm() {
  const router = useRouter();
  const { generate, generating } = useGenerateAssignment();
  const [step, setStep] = useState(0);
  const [direction, setDirection] = useState(1);
  const [form, setForm] = useState({
    topic: '',
    academic_level: 'university',
    word_count: 1500,
    citation_style: 'apa',
    template: 'professional',
  });

  const next = () => {
    if (step === 0 && form.topic.trim().length < 5) {
      toast.error('Topic must be at least 5 characters');
      return;
    }
    setDirection(1);
    setStep((s) => Math.min(s + 1, 3));
  };

  const prev = () => {
    setDirection(-1);
    setStep((s) => Math.max(s - 1, 0));
  };

  const handleSubmit = async () => {
    try {
      const data = await generate(form);
      toast.success('Assignment generation started!');
      router.push(`/dashboard/${data.assignment_id}`);
    } catch {
      // handled by interceptor
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      {/* Progress bar */}
      <div className="mb-10">
        <div className="flex items-center justify-between mb-4">
          {stepLabels.map((label, i) => {
            const Icon = stepIcons[i];
            return (
              <div key={label} className="flex flex-col items-center gap-1.5">
                <motion.div
                  animate={{
                    scale: i === step ? 1.1 : 1,
                    backgroundColor: i <= step ? 'rgba(99,102,241,0.2)' : 'rgba(255,255,255,0.05)',
                  }}
                  className={`w-10 h-10 rounded-full border flex items-center justify-center transition-colors ${
                    i <= step ? 'border-indigo-500/50 text-indigo-400' : 'border-white/10 text-gray-600'
                  }`}
                >
                  <Icon size={16} />
                </motion.div>
                <span className={`text-xs hidden sm:inline ${i <= step ? 'text-indigo-400' : 'text-gray-600'}`}>
                  {label}
                </span>
              </div>
            );
          })}
        </div>
        <div className="w-full h-1 bg-white/5 rounded-full overflow-hidden">
          <motion.div
            animate={{ width: `${((step + 1) / 4) * 100}%` }}
            className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full"
          />
        </div>
      </div>

      {/* Steps */}
      <div className="relative overflow-hidden min-h-[320px]">
        <AnimatePresence mode="wait" custom={direction}>
          <motion.div
            key={step}
            custom={direction}
            variants={slideVariants}
            initial="enter"
            animate="center"
            exit="exit"
            transition={{ duration: 0.3 }}
          >
            {step === 0 && (
              <div>
                <h2 className="text-2xl font-bold mb-2">What&apos;s your assignment about?</h2>
                <p className="text-gray-400 text-sm mb-6">Enter a detailed topic for best results.</p>
                <div className="relative">
                  <textarea
                    value={form.topic}
                    onChange={(e) => setForm({ ...form, topic: e.target.value })}
                    placeholder="e.g., The Impact of Artificial Intelligence on Modern Healthcare Systems"
                    rows={5}
                    maxLength={500}
                    className="input-glass resize-none"
                  />
                  <span className="absolute bottom-3 right-3 text-xs text-gray-600">
                    {form.topic.length}/500
                  </span>
                </div>
              </div>
            )}

            {step === 1 && (
              <div>
                <h2 className="text-2xl font-bold mb-2">Academic Level & Length</h2>
                <p className="text-gray-400 text-sm mb-6">Choose the level and word count.</p>

                <div className="grid grid-cols-2 gap-3 mb-8">
                  {ACADEMIC_LEVELS.map((level) => (
                    <motion.button
                      key={level.value}
                      type="button"
                      whileHover={{ scale: 1.03 }}
                      whileTap={{ scale: 0.97 }}
                      onClick={() => setForm({ ...form, academic_level: level.value })}
                      className={`p-4 rounded-xl border text-left transition-all ${
                        form.academic_level === level.value
                          ? 'bg-indigo-500/10 border-indigo-500/50 text-white'
                          : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/[0.08]'
                      }`}
                    >
                      <span className="text-2xl mb-1 block">{level.icon}</span>
                      <span className="font-medium text-sm">{level.label}</span>
                      <p className="text-xs text-gray-500 mt-1">{level.description}</p>
                    </motion.button>
                  ))}
                </div>

                <h3 className="text-sm font-medium text-gray-300 mb-3">Word Count</h3>
                <div className="flex flex-wrap gap-2">
                  {WORD_COUNTS.map((wc) => (
                    <motion.button
                      key={wc}
                      type="button"
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={() => setForm({ ...form, word_count: wc })}
                      className={`px-4 py-2 rounded-full text-sm font-medium border transition-all ${
                        form.word_count === wc
                          ? 'bg-indigo-500/10 border-indigo-500/50 text-indigo-300'
                          : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/[0.08]'
                      }`}
                    >
                      {wc.toLocaleString()}
                    </motion.button>
                  ))}
                </div>
              </div>
            )}

            {step === 2 && (
              <div>
                <h2 className="text-2xl font-bold mb-2">Citation Style</h2>
                <p className="text-gray-400 text-sm mb-6">Select the citation format.</p>
                <div className="grid grid-cols-2 gap-3">
                  {CITATION_STYLES.map((cs) => (
                    <motion.button
                      key={cs.value}
                      type="button"
                      whileHover={{ scale: 1.03 }}
                      whileTap={{ scale: 0.97 }}
                      onClick={() => setForm({ ...form, citation_style: cs.value })}
                      className={`p-5 rounded-xl border text-left transition-all ${
                        form.citation_style === cs.value
                          ? 'bg-indigo-500/10 border-indigo-500/50 text-white'
                          : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/[0.08]'
                      }`}
                    >
                      <span className="font-bold text-lg">{cs.label}</span>
                      <p className="text-xs text-gray-500 mt-1">{cs.description}</p>
                    </motion.button>
                  ))}
                </div>
              </div>
            )}

            {step === 3 && (
              <div>
                <h2 className="text-2xl font-bold mb-2">Choose Template</h2>
                <p className="text-gray-400 text-sm mb-6">Pick the visual style for your document.</p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {TEMPLATES.map((tmpl) => (
                    <motion.button
                      key={tmpl.value}
                      type="button"
                      whileHover={{ scale: 1.03 }}
                      whileTap={{ scale: 0.97 }}
                      onClick={() => setForm({ ...form, template: tmpl.value })}
                      className={`p-5 rounded-xl border text-left transition-all overflow-hidden relative ${
                        form.template === tmpl.value
                          ? 'bg-indigo-500/10 border-indigo-500/50 text-white'
                          : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/[0.08]'
                      }`}
                    >
                      <div className={`absolute top-0 left-0 right-0 h-1 bg-gradient-to-r ${tmpl.color}`} />
                      <span className="font-bold">{tmpl.label}</span>
                      <p className="text-xs text-gray-500 mt-1">{tmpl.description}</p>
                    </motion.button>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Navigation */}
      <div className="flex items-center justify-between mt-8">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={prev}
          disabled={step === 0}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-medium transition-all ${
            step === 0 ? 'text-gray-600 cursor-not-allowed' : 'glass text-gray-300 hover:text-white'
          }`}
        >
          <ArrowLeft size={16} /> Back
        </motion.button>

        {step < 3 ? (
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={next}
            className="gradient-btn px-6 py-2.5 text-sm flex items-center gap-2"
          >
            Next <ArrowRight size={16} />
          </motion.button>
        ) : (
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleSubmit}
            disabled={generating}
            className="gradient-btn px-6 py-2.5 text-sm flex items-center gap-2 disabled:opacity-50"
          >
            {generating ? <LoadingSpinner size={16} /> : <Sparkles size={16} />}
            {generating ? 'Generating...' : 'Generate Assignment'}
          </motion.button>
        )}
      </div>
    </div>
  );
}
