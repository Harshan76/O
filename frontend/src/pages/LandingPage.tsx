import React from 'react';
import { Link } from 'react-router-dom';
import { useLearner } from '../context/LearnerContext';
import { Sparkles, Brain, Bot, Compass, CheckCircle2, ArrowRight, ShieldCheck, Zap, BookOpen } from 'lucide-react';

export const LandingPage: React.FC = () => {
  const { scenarios, switchScenario } = useLearner();

  return (
    <div className="space-y-16 pb-20">
      {/* Hero Section */}
      <section className="relative pt-12 sm:pt-20 text-center max-w-5xl mx-auto px-4">
        <div className="inline-flex items-center gap-2 bg-[#DDD6FE] border-2 border-black rounded-full px-4 py-1.5 shadow-neo-sm font-mono text-xs font-bold mb-6">
          <Sparkles className="w-4 h-4 fill-yellow-400" />
          <span>Learner-First AI Education • Zero Teachers • Pure Mastery</span>
        </div>

        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-black leading-tight">
          Your Personal <span className="bg-[#FEF08A] px-2 border-2 border-black rounded-lg shadow-neo inline-block transform -rotate-1">AI Tutor</span> & Adaptive Engine
        </h1>

        <p className="mt-6 text-lg sm:text-xl text-zinc-700 max-w-3xl mx-auto font-medium">
          SkillForge AI diagnoses what you know, pinpoints missing prerequisites, provides progressive hints before giving away answers, and dynamically rebuilds your learning roadmap after every challenge.
        </p>

        <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
          <Link
            to="/onboarding"
            className="bg-[#A78BFA] hover:bg-[#906cf8] text-black font-extrabold px-8 py-3.5 rounded-xl border-3 border-black shadow-neo-lg hover:shadow-neo hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-base flex items-center gap-2"
          >
            <span>Start Free Learner Onboarding</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
          <Link
            to="/dashboard"
            className="bg-white hover:bg-zinc-100 text-black font-extrabold px-7 py-3.5 rounded-xl border-3 border-black shadow-neo hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-base"
          >
            Open Learner Dashboard
          </Link>
        </div>

        <div className="mt-8 flex flex-wrap items-center justify-center gap-6 text-xs font-mono font-bold text-zinc-600">
          <div className="flex items-center gap-1.5"><CheckCircle2 className="w-4 h-4 text-emerald-600" /> No Teacher Dashboards</div>
          <div className="flex items-center gap-1.5"><CheckCircle2 className="w-4 h-4 text-emerald-600" /> Deterministic Adaptation</div>
          <div className="flex items-center gap-1.5"><CheckCircle2 className="w-4 h-4 text-emerald-600" /> Safe Sandboxed Code Runner</div>
          <div className="flex items-center gap-1.5"><CheckCircle2 className="w-4 h-4 text-emerald-600" /> Grounded Smart Notes</div>
        </div>
      </section>

      {/* 10 Seeded Demonstration Scenarios Showcase */}
      <section className="max-w-6xl mx-auto px-4">
        <div className="bg-white border-3 border-black rounded-2xl p-6 sm:p-8 shadow-neo-lg">
          <div className="flex flex-wrap items-center justify-between gap-4 mb-6 pb-4 border-b-2 border-black">
            <div>
              <div className="inline-block bg-[#FEF08A] text-black text-xs font-mono font-bold px-2 py-0.5 rounded border border-black mb-1">
                EVALUATOR & JUDGE PLAYGROUND
              </div>
              <h2 className="text-2xl font-extrabold text-black">10 Seeded Demonstration Scenarios</h2>
              <p className="text-sm text-zinc-600">Instant one-click presets covering beginner gaps, failed attempts, incorrect code, note uploads, and verified mastery.</p>
            </div>
            <Link
              to="/dashboard"
              className="bg-black text-[#FEF08A] px-4 py-2 rounded-lg border-2 border-black font-bold text-xs shadow-neo-xs flex items-center gap-1.5"
            >
              <span>Explore Active Scenario</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {scenarios.map((s) => (
              <div
                key={s.id}
                className="bg-[#FAF7F2] border-2 border-black rounded-xl p-4 shadow-neo-sm hover:shadow-neo transition-all flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="bg-black text-white text-[11px] font-mono px-2 py-0.5 rounded font-bold">
                      Scenario #{s.id}
                    </span>
                    <span className="bg-[#DDD6FE] text-black text-[10px] font-bold px-2 py-0.5 rounded border border-black">
                      {s.experience_level}
                    </span>
                  </div>
                  <h3 className="font-extrabold text-sm text-black leading-snug mb-1">{s.title}</h3>
                  <p className="text-xs text-zinc-600 line-clamp-2 mb-3">{s.description}</p>
                </div>
                <div className="pt-3 border-t border-zinc-300 flex items-center justify-between">
                  <div className="text-[11px] font-mono font-bold text-zinc-700">
                    {s.learner_name} • {s.overall_mastery}%
                  </div>
                  <button
                    onClick={() => switchScenario(s.id)}
                    className="bg-white hover:bg-[#FEF08A] border-2 border-black text-black px-2.5 py-1 rounded text-xs font-bold shadow-neo-xs hover:translate-x-0.5 hover:translate-y-0.5 transition-all"
                  >
                    Load
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Feature Pillars */}
      <section className="max-w-6xl mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-[#FECDD3] border-3 border-black rounded-2xl p-6 shadow-neo">
          <div className="w-12 h-12 bg-white border-2 border-black rounded-xl shadow-neo-xs flex items-center justify-center mb-4">
            <Brain className="w-6 h-6 text-black" />
          </div>
          <h3 className="text-xl font-extrabold text-black mb-2">Deterministic Diagnosis</h3>
          <p className="text-sm text-zinc-800 font-medium leading-relaxed">
            Evaluates objective answers and code AST structure against predefined keys and rubrics. Pinpoints prerequisites and marks skills as strong, weak, or validating.
          </p>
        </div>

        <div className="bg-[#DDD6FE] border-3 border-black rounded-2xl p-6 shadow-neo">
          <div className="w-12 h-12 bg-white border-2 border-black rounded-xl shadow-neo-xs flex items-center justify-center mb-4">
            <Bot className="w-6 h-6 text-black" />
          </div>
          <h3 className="text-xl font-extrabold text-black mb-2">Pedagogical AI Tutor</h3>
          <p className="text-sm text-zinc-800 font-medium leading-relaxed">
            Never simply gives away answers. Supplies progressive hints, provides relatable real-world analogies, explains syntax errors line-by-line, and tests understanding with check-questions.
          </p>
        </div>

        <div className="bg-[#A7F3D0] border-3 border-black rounded-2xl p-6 shadow-neo">
          <div className="w-12 h-12 bg-white border-2 border-black rounded-xl shadow-neo-xs flex items-center justify-center mb-4">
            <Zap className="w-6 h-6 text-black" />
          </div>
          <h3 className="text-xl font-extrabold text-black mb-2">Adaptive Roadmaps</h3>
          <p className="text-sm text-zinc-800 font-medium leading-relaxed">
            Rules strictly enforced: &lt;50% drops difficulty and revisits prerequisites; 50–79% triggers targeted practice; &ge;80% promotes to capstone mini-projects.
          </p>
        </div>
      </section>
    </div>
  );
};
