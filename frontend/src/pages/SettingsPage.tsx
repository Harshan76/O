import React, { useState } from 'react';
import { api } from '../services/api';
import { useLearner } from '../context/LearnerContext';
import { Settings, User, Clock, Brain, Save, ShieldCheck, Key, RefreshCw } from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const { learner, refreshAll, showToast, activeScenarioId, switchScenario } = useLearner();
  const [fullName, setFullName] = useState(learner?.full_name || '');
  const [dailyMinutes, setDailyMinutes] = useState(learner?.daily_minutes || 45);
  const [learningStyle, setLearningStyle] = useState(learner?.learning_style || 'hands-on');
  const [saving, setSaving] = useState(false);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSaving(true);
      await api.updateProfile({
        full_name: fullName,
        daily_minutes: dailyMinutes,
        learning_style: learningStyle as any
      });
      await refreshAll();
      showToast('Learner preferences saved!', 'success');
    } catch (err: any) {
      showToast(err.message, 'error');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="bg-white border-3 border-black rounded-2xl p-6 sm:p-8 shadow-neo-lg">
        <div className="inline-flex items-center gap-2 bg-[#DDD6FE] text-black text-xs font-mono font-bold px-3 py-1 rounded-full border border-black mb-3">
          <Settings className="w-3.5 h-3.5" />
          <span>Learner Configuration</span>
        </div>
        <h1 className="text-3xl font-extrabold text-black">Settings & Learning Preferences</h1>
        <p className="text-sm text-zinc-600 mt-1 max-w-2xl font-medium">
          Customize your daily study cadence, pedagogy preferences, and inspect backend operational configuration.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Profile Settings Form */}
        <div className="md:col-span-2">
          <form onSubmit={handleSave} className="bg-white border-3 border-black rounded-2xl p-6 sm:p-8 shadow-neo space-y-5">
            <h2 className="text-xl font-extrabold text-black border-b-2 border-black pb-3">
              Personal Profile
            </h2>

            <div>
              <label className="block text-xs font-bold text-black uppercase tracking-wider mb-1.5">
                Learner Full Name
              </label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="w-full px-3.5 py-2.5 border-2 border-black rounded-xl text-sm font-semibold bg-white"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-black uppercase tracking-wider mb-1.5">
                Daily Study Pacing
              </label>
              <select
                value={dailyMinutes}
                onChange={(e) => setDailyMinutes(Number(e.target.value))}
                className="w-full px-3.5 py-2.5 border-2 border-black rounded-xl text-sm font-bold bg-white"
              >
                <option value={20}>20 minutes / day (Bite-sized practice)</option>
                <option value={30}>30 minutes / day (Steady progress)</option>
                <option value={45}>45 minutes / day (Standard pace)</option>
                <option value={60}>60+ minutes / day (Accelerated track)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-black uppercase tracking-wider mb-1.5">
                Preferred Pedagogical Style
              </label>
              <select
                value={learningStyle}
                onChange={(e) => setLearningStyle(e.target.value as any)}
                className="w-full px-3.5 py-2.5 border-2 border-black rounded-xl text-sm font-bold bg-white"
              >
                <option value="hands-on">Hands-on interactive exercises</option>
                <option value="conceptual">Conceptual & analogies first</option>
                <option value="project-based">Project & capstone oriented</option>
                <option value="visual">Visual structures & diagrams</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={saving}
              className="bg-[#FEF08A] hover:bg-[#fde047] text-black font-extrabold py-3 px-6 rounded-xl border-2 border-black shadow-neo-sm hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-xs sm:text-sm flex items-center gap-2"
            >
              <Save className="w-4 h-4" />
              <span>{saving ? 'Saving...' : 'Save Preferences'}</span>
            </button>
          </form>
        </div>

        {/* Backend & Environment Diagnostics */}
        <div className="space-y-6">
          <div className="bg-[#FAF7F2] border-3 border-black rounded-2xl p-6 shadow-neo space-y-4">
            <h3 className="font-extrabold text-sm text-black uppercase font-mono">
              System Environment
            </h3>

            <div className="space-y-2 text-xs font-mono font-medium">
              <div className="flex justify-between border-b border-zinc-300 pb-1.5">
                <span className="text-zinc-600">Backend API:</span>
                <span className="text-emerald-700 font-bold">FastAPI 0.110+</span>
              </div>
              <div className="flex justify-between border-b border-zinc-300 pb-1.5">
                <span className="text-zinc-600">Database Engine:</span>
                <span className="text-black font-bold">SQLite / Supabase RLS</span>
              </div>
              <div className="flex justify-between border-b border-zinc-300 pb-1.5">
                <span className="text-zinc-600">AI Tutor Mode:</span>
                <span className="text-purple-700 font-bold">Pedagogical Engine</span>
              </div>
              <div className="flex justify-between border-b border-zinc-300 pb-1.5">
                <span className="text-zinc-600">Active Scenario:</span>
                <span className="bg-black text-[#FEF08A] px-1.5 py-0.5 rounded text-[10px]">
                  #{activeScenarioId}
                </span>
              </div>
            </div>

            <div className="pt-2">
              <div className="text-[11px] font-bold text-zinc-700 mb-1 flex items-center gap-1">
                <Key className="w-3.5 h-3.5" />
                <span>Live LLM Integration:</span>
              </div>
              <p className="text-[11px] text-zinc-600 leading-normal">
                To connect Gemini API directly, set <code>GEMINI_API_KEY</code> in <code>.env</code>. When omitted, the platform uses its deterministic pedagogical engine with zero external dependencies.
              </p>
            </div>

            <button
              onClick={() => switchScenario('1')}
              className="w-full bg-white hover:bg-zinc-100 border-2 border-black rounded-xl p-2.5 text-xs font-bold shadow-neo-xs flex items-center justify-center gap-1.5 mt-2"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Reset to Scenario #1</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
