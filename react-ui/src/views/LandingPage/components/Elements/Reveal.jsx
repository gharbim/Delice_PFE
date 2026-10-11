import React from "react";
import { motion } from "framer-motion";
import useInView from "../../hooks/useInView";

export default function Reveal({ children, delay = 0, y = 28, width = "100%", style }) {
  const [ref, inView] = useInView({ threshold: 0.15, triggerOnce: true });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y }}
      animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y }}
      transition={{ duration: 0.6, delay, ease: [0.22, 1, 0.36, 1] }}
      style={{ width, ...style }}
    >
      {children}
    </motion.div>
  );
}
