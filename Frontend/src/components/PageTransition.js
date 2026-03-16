/**
 * @fileoverview Framer Motion page transition wrapper.
 * Wraps page content with fade + slide-up animation.
 */
'use client';

import { motion } from 'framer-motion';

const variants = {
  hidden: { opacity: 0, y: 20 },
  enter: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
};

export default function PageTransition({ children, className = '' }) {
  return (
    <motion.div
      variants={variants}
      initial="hidden"
      animate="enter"
      exit="exit"
      transition={{ duration: 0.4, ease: 'easeInOut' }}
      className={className}
    >
      {children}
    </motion.div>
  );
}
