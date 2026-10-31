import React from "react";
import { Link } from "react-router-dom";
import { BookOpen, Map, GraduationCap, Award, Compass } from "lucide-react";
import { BRAND_CONFIG } from "../config/brand";

export const Learn: React.FC = () => {
  const pathways = [
    {
      title: "Foundational ML Mathematics",
      level: "Beginner",
      modules: 4,
      desc: "Calculus, Linear Algebra, Probability, and optimization algorithms behind learning models.",
      xp: 200,
      active: true
    },
    {
      title: "Introduction to Machine Learning",
      level: "Beginner",
      modules: 8,
      desc: "Supervised and unsupervised learning, loss functions, regression, decision trees, and metrics.",
      xp: 450,
      active: true
    },
    {
      title: "Deep Learning Foundations",
      level: "Intermediate",
      modules: 12,
      desc: "Backpropagation, neural architectures, activation layers, PyTorch syntax, and neural networks.",
      xp: 600,
      active: false
    },
    {
      title: "Large Language Models & Transformers",
      level: "Advanced",
      modules: 6,
      desc: "Self-attention weights, tokenizer architectures, sequence decoding, and transformer blocks.",
      xp: 800,
      active: false
    }
  ];

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <GraduationCap className="w-6 h-6 text-brand" />
          Learning Curriculum
        </h1>
        <p className="text-sm text-dark-muted mt-1">
          Follow structured pathways to master AI/ML concepts by coding them from scratch.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 select-none">
        {pathways.map((path, idx) => (
          <div key={idx} className="p-5 bg-dark-card border border-dark-border rounded flex flex-col justify-between hover:border-brand/40 transition-all group">
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className={`text-[9px] font-bold px-2 py-0.5 rounded border uppercase tracking-wider font-mono ${
                  path.level === "Beginner" 
                    ? "bg-dark-panel text-brand-green border-brand-green/20" 
                    : path.level === "Intermediate" 
                    ? "bg-dark-panel text-brand-yellow border-brand-yellow/20" 
                    : "bg-dark-panel text-brand-pink border-brand-pink/20"
                }`}>
                  {path.level}
                </span>
                <span className="text-xs text-brand font-mono font-bold flex items-center gap-1">
                  <Award className="w-3.5 h-3.5" /> +{path.xp} XP
                </span>
              </div>

              <h3 className="text-sm font-bold text-white font-mono group-hover:text-brand transition-colors">
                {path.title}
              </h3>
              <p className="text-xs text-[#8B958E] mt-2 leading-relaxed font-sans">
                {path.desc}
              </p>
            </div>

            <div className="mt-5 pt-3.5 border-t border-dark-border flex items-center justify-between">
              <span className="text-xs text-slate-500 font-mono">
                {path.modules} Core Sections
              </span>
              {path.active ? (
                <Link
                  to="/problems"
                  className="bg-dark-panel hover:bg-brand text-[#C8D0CA] hover:text-dark-deep border border-dark-border hover:border-brand px-3.5 py-1.5 rounded text-xs transition-all font-bold font-mono"
                >
                  Continue Path
                </Link>
              ) : (
                <span className="text-xs text-slate-500 italic flex items-center gap-1 font-mono">
                  <Compass className="w-3.5 h-3.5" /> Coming soon
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
