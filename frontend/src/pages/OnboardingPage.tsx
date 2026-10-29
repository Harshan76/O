import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLearner } from '../context/LearnerContext';
import { api } from '../services/api';
import { Sparkles, ArrowRight, Brain, Clock, Target, Compass, AlertCircle } from 'lucide-react';

export const OnboardingPage: React.FC = () => {
  const navigate = useNavigate();
  const { refreshAll, showToast } = useLearner();
  const [loading, setLoading] = useState(false);

  const [domain, setDomain] = useState('Python Programming');
  const [title, setTitle] = useState('Master Python Programming & System Scripting');
  const [targetOutcome, setTargetOutcome] = useState('Build automated systems and pass technical coding interviews');
  const [experienceLevel, setExperienceLevel] = useState('beginner');
  const [dailyMinutes, setDailyMinutes] = useState(45);
  const [learningStyle, setLearningStyle] = useState('hands-on');
  const [targetDate, setTargetDate] = useState('2026-12-31');

  const domainPresets: Record<string, { title: string; outcome: string }> = {
    'Python Programming': {
      title: 'Master Python Programming & System Scripting',
      outcome: 'Build production backend services and solve algorithm challenges'
    },
    'Web Development': {
      title: 'Modern Full-Stack React Architecture',
      outcome: 'Architect end-to-end full stack web applications with optimistic UI'
    },
    'Data Science & AI': {
      title: 'Data Science & Machine Learning Engineering',
      outcome: 'Analyze tabular datasets, vectorize calculations, and deploy ML models'
    },
    'AI Engineering': {
      title: 'AI Engineering & Autonomous LLM Systems',
      outcome: 'Build multi-turn RAG agents, cosine vector retrieval, and tool pipelines'
    }
  };

  const handleDomainChange = (d: string) => {
    setDomain(d);
    if (domainPresets[d]) {
      setTitle(domainPresets[d].title);
      setTargetOutcome(domainPresets[d].outcome);
    }
  };

  const handleComplete = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      await api.createGoal({
        title,
        domain,
        target_outcome: targetOutcome,
        experience_level: experienceLevel,
        daily_minutes: dailyMinutes,
        learning_style: learningStyle,
        target_date: targetDate
      });
      await refreshAll();
      showToast('Personal learning profile initialized! Moving to Diagnostic Assessment.', 'success');
      navigate('/diagnostic');
    } catch (err: any) {
      showToast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-10 px-4">
      <div className="bg-white border-3 border-black rounded-2xl p-6 sm:p-10 shadow-neo-lg">
        {/* Header */}
        <div className="mb-8 border-b-2 border-black pb-6">
          <div className="inline-flex items-center gap-2 bg-[#DDD6FE] border-2 border-black rounded-full px-3 py-1 text-xs font-mono font-bold mb-3">
            <Compass className="w-3.5 h-3.5" />
            <span>Learner Setup Wizard • Step 1 of 2</span>
          </div>
          <h1 className="text-3xl font-extrabold text-black">Personalize Your Learning Profile</h1>
          <p className="text-sm text-zinc-600 mt-1">
            Configure your focus domain, time commitment, and goals. SkillForge AI adapts every subsequent task to your verified pacing.
          </p>
        </div>

        {/* Disclaimer Notice */}
        <div className="bg-[#FEF08A] border-2 border-black rounded-xl p-4 mb-8 flex items-start gap-3 shadow-neo-xs">
          <AlertCircle className="w-5 h-5 text-black shrink-0 mt-0.5" />
          <div className="text-xs text-zinc-900 leading-relaxed font-medium">
            <strong>Important Pedagogical Standard:</strong> Self-reported experience levels are treated as initial baseline estimates only. Your personal AI tutor verifies your actual mastery through our objective diagnostic assessment and adjusts your roadmap accordingly.
          </div>
        </div>

        <form onSubmit={handleComplete} className="space-y-6">
          {/* Domain Picker */}
          <div>
            <label className="block text-xs font-bold text-black uppercase tracking-wider mb-2">
              1. What do you want to learn?
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {Object.keys(domainPresets).map((d) => (
                <button
                  key={d}
                  type="button"
                  onClick={() => handleDomainChange(d)}
                  className={`text-left p-3.5 rounded-xl border-2 transition-all font-bold text-sm ${
                    domain === d
                      ? 'bg-black text-[#FEF08A] border-black shadow-neo-sm'
                      : 'bg-zinc-50 hover:bg-[#FAF7F2] border-black text-black'
                  }`}
                >
                  {d}
                </button>
              ))}
            </div>
          </div>

          {/* Goal & Outcome */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-black uppercase tracking-wider mb-1.5">
                Primary Goal Title
              </label>
              <input
                type="text"
                required
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full px-3.5 py-2.5 border-2 border-black rounded-xl text-sm font-semibold bg-white"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-black uppercase tracking-wider mb-1.5">
                Target Outcome / Career Milestone
              </label>
              <input
                type="text"
                required
                value={targetOutcome}
                onChange={(e) => setTargetOutcome(e.target.value)}
                className="w-full px-3.5 py-2.5 border-2 border-black rounded-xl text-sm font-semibold bg-white"
              />
            </div>
          </div>

          {/* Self-Reported Level */}
          <div>
            <label className="block text-xs font-bold text-black uppercase tracking-wider mb-2">
              2. Current Self-Reported Experience Level
            </label>
            <div className="grid grid-cols-3 gap-3">
              {[
                { id: 'beginner', label: 'Beginner', desc: 'Starting from fundamentals' },
                { id: 'intermediate', label: 'Intermediate', desc: 'Know syntax, need depth' },
                { id: 'advanced', label: 'Advanced', desc: 'Ready for architecture' }
              ].map((lvl) => (
                <button
                  key={lvl.id}
                  type="button"
                  onClick={() => setExperienceLevel(lvl.id)}
                  className={`text-left p-3 rounded-xl border-2 transition-all ${
                    experienceLevel === lvl.id
                      ? 'bg-[#DDD6FE] border-black shadow-neo-sm'
                      : 'bg-white hover:bg-zinc-50 border-black'
                  }`}
                >
                  <div className="font-bold text-xs text-black">{lvl.label}</div>
                  <div className="text-[10px] text-zinc-600 mt-0.5">{lvl.desc}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Daily Study Time & Learning Style */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-black uppercase tracking-wider mb-1.5">
                Available Daily Study Time
              </label>
              <select
                value={dailyMinutes}
                onChange={(e) => setDailyMinutes(Number(e.target.value))}
                className="w-full px-3.5 py-2.5 border-2 border-black rounded-xl text-sm font-bold bg-white"
              >
                <option value={20}>20 minutes / day (Micro-learning)</option>
                <option value={30}>30 minutes / day (Steady pace)</option>
                <option value={45}>45 minutes / day (Recommended)</option>
                <option value={60}>60+ minutes / day (Intensive mastery)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-black uppercase tracking-wider mb-1.5">
                Preferred Learning Style
              </label>
              <select
                value={learningStyle}
                onChange={(e) => setLearningStyle(e.target.value)}
                className="w-full px-3.5 py-2.5 border-2 border-black rounded-xl text-sm font-bold bg-white"
              >
                <option value="hands-on">Hands-On Interactive Code</option>
                <option value="conceptual">Conceptual & Analogies</option>
                <option value="project-based">Project & Case-Study Driven</option>
                <option value="visual">Visual & Structured Diagrams</option>
              </select>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#A78BFA] hover:bg-[#906cf8] text-black font-extrabold py-3.5 px-6 rounded-xl border-3 border-black shadow-neo hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-base flex items-center justify-center gap-2 mt-4"
          >
            <span>{loading ? 'Setting Up...' : 'Save & Take Diagnostic Assessment'}</span>
            <ArrowRight className="w-5 h-5" />
          </button>
        </form>
      </div>
    </div>
  );
};
