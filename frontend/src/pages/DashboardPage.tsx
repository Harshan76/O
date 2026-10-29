import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useLearner } from '../context/LearnerContext';
import { api } from '../services/api';
import { LearningPathResponse, SkillProfileResponse } from '../types';
import { 
  Sparkles, Flame, Clock, Brain, ArrowRight, 
  CheckCircle2, Bot, Layers, Code, Award, Target, AlertTriangle
} from 'lucide-react';

export const DashboardPage: React.FC = () => {
  const { learner, progress, activeScenarioId, scenarios } = useLearner();
  const [roadmap, setRoadmap] = useState<LearningPathResponse | null>(null);
  const [skillProfile, setSkillProfile] = useState<SkillProfileResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [rm, sp] = await Promise.all([
          api.getCurrentRoadmap().catch(() => null),
          api.getSkillProfile().catch(() => null)
        ]);
        setRoadmap(rm);
        setSkillProfile(sp);
      } catch (err) {
        console.error('Failed to load dashboard data:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [activeScenarioId]);

  const activeTask = roadmap?.tasks?.find(t => t.status === 'in_progress') || roadmap?.tasks?.[0];
  const currentScenario = scenarios.find(s => s.id === activeScenarioId);

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-8">
      {/* Welcome & Streak Banner */}
      <div className="bg-white border-3 border-black rounded-2xl p-6 sm:p-8 shadow-neo-lg flex flex-wrap items-center justify-between gap-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="bg-[#DDD6FE] text-black text-xs font-mono font-bold px-2.5 py-0.5 rounded-full border border-black">
              Learner Dashboard
            </span>
            <span className="text-xs font-mono text-zinc-500 font-bold">
              ID: {learner?.id}
            </span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-black">
            Welcome, {learner?.full_name || 'Learner'}!
          </h1>
          <p className="text-sm text-zinc-600 mt-1 font-medium">
            Goal: <strong className="text-black">{progress?.goal_title || 'Software Engineering'}</strong> • Pacing: {learner?.daily_minutes || 45} mins/day
          </p>
        </div>

        {/* Stats Row */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="bg-[#FEF08A] border-2 border-black rounded-xl p-3 shadow-neo-xs flex items-center gap-2.5">
            <Flame className="w-6 h-6 text-orange-600 fill-orange-500" />
            <div>
              <div className="text-xs font-mono text-zinc-700 font-bold uppercase">Streak</div>
              <div className="text-xl font-extrabold text-black">{progress?.current_streak || 1} Days</div>
            </div>
          </div>

          <div className="bg-[#BAE6FD] border-2 border-black rounded-xl p-3 shadow-neo-xs flex items-center gap-2.5">
            <Clock className="w-6 h-6 text-blue-700" />
            <div>
              <div className="text-xs font-mono text-zinc-700 font-bold uppercase">Total Hours</div>
              <div className="text-xl font-extrabold text-black">{progress?.total_study_hours || 12.5} hrs</div>
            </div>
          </div>

          <div className="bg-[#A7F3D0] border-2 border-black rounded-xl p-3 shadow-neo-xs flex items-center gap-2.5">
            <Award className="w-6 h-6 text-emerald-800" />
            <div>
              <div className="text-xs font-mono text-zinc-700 font-bold uppercase">Mastery</div>
              <div className="text-xl font-extrabold text-black">{progress?.overall_mastery || 0}%</div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Focus: Next Recommended Action Hero */}
      <div className="bg-[#FAF7F2] border-3 border-black rounded-2xl p-6 sm:p-8 shadow-neo relative overflow-hidden">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
          <div className="inline-flex items-center gap-2 bg-[#FEF08A] text-black text-xs font-mono font-bold px-3 py-1 rounded-full border border-black">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI TUTOR NEXT RECOMMENDED ACTION</span>
          </div>
          <span className="text-xs font-mono bg-black text-white px-2 py-0.5 rounded font-bold">
            Priority Task
          </span>
        </div>

        {activeTask ? (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-center">
            <div className="lg:col-span-2 space-y-2">
              <h2 className="text-2xl font-extrabold text-black">{activeTask.title}</h2>
              <p className="text-sm text-zinc-700 font-medium leading-relaxed">
                {activeTask.learning_objective}
              </p>
              <div className="flex flex-wrap items-center gap-3 pt-2 text-xs font-mono font-bold">
                <span className="bg-white border border-black px-2.5 py-1 rounded">
                  Difficulty: {activeTask.difficulty}
                </span>
                <span className="bg-white border border-black px-2.5 py-1 rounded">
                  Est. {activeTask.estimated_duration} mins
                </span>
                <span className="bg-[#DDD6FE] text-black border border-black px-2.5 py-1 rounded">
                  Skill: {activeTask.skill_code}
                </span>
              </div>
              <div className="bg-white/80 border border-black rounded-lg p-3 text-xs text-zinc-700 mt-2">
                <strong>Why Recommended:</strong> {activeTask.reason_for_recommendation}
              </div>
            </div>

            <div className="flex flex-col gap-3">
              <Link
                to={activeTask.task_type === 'project' ? '/projects' : '/challenges'}
                className="bg-[#A78BFA] hover:bg-[#906cf8] text-black font-extrabold py-3.5 px-6 rounded-xl border-3 border-black shadow-neo hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-center flex items-center justify-center gap-2"
              >
                <span>Start Recommended Challenge</span>
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link
                to="/tutor"
                className="bg-white hover:bg-zinc-100 text-black font-bold py-2.5 px-4 rounded-xl border-2 border-black text-xs text-center flex items-center justify-center gap-1.5 shadow-neo-xs"
              >
                <Bot className="w-4 h-4" />
                <span>Ask AI Tutor for a Concept Hint</span>
              </Link>
            </div>
          </div>
        ) : (
          <div className="text-center py-6">
            <p className="text-sm text-zinc-600 font-medium">No active tasks in queue. Take the diagnostic to initialize your roadmap.</p>
            <Link to="/diagnostic" className="mt-3 inline-block bg-[#FEF08A] border-2 border-black font-bold text-xs px-4 py-2 rounded shadow-neo-xs">
              Take Diagnostic Assessment
            </Link>
          </div>
        )}
      </div>

      {/* Quick Launchpad & Skill Gaps Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Link
          to="/tutor"
          className="bg-white border-2 border-black rounded-xl p-4 shadow-neo-sm hover:shadow-neo hover:bg-[#DDD6FE]/30 transition-all flex flex-col justify-between"
        >
          <div className="flex items-center justify-between mb-2">
            <Bot className="w-6 h-6 text-black" />
            <span className="text-[10px] font-mono font-bold bg-[#DDD6FE] px-2 py-0.5 rounded border border-black">Always Active</span>
          </div>
          <div>
            <h3 className="font-extrabold text-sm text-black">AI Tutor Chat</h3>
            <p className="text-xs text-zinc-600 mt-1">Get progressive hints, concept breakdowns, and check questions.</p>
          </div>
        </Link>

        <Link
          to="/diagnostic"
          className="bg-white border-2 border-black rounded-xl p-4 shadow-neo-sm hover:shadow-neo hover:bg-[#FEF08A]/30 transition-all flex flex-col justify-between"
        >
          <div className="flex items-center justify-between mb-2">
            <Brain className="w-6 h-6 text-black" />
            <span className="text-[10px] font-mono font-bold bg-[#FEF08A] px-2 py-0.5 rounded border border-black">Baseline</span>
          </div>
          <div>
            <h3 className="font-extrabold text-sm text-black">Diagnostic Quiz</h3>
            <p className="text-xs text-zinc-600 mt-1">Objective assessment testing skills and missing prerequisites.</p>
          </div>
        </Link>

        <Link
          to="/challenges"
          className="bg-white border-2 border-black rounded-xl p-4 shadow-neo-sm hover:shadow-neo hover:bg-[#FECDD3]/30 transition-all flex flex-col justify-between"
        >
          <div className="flex items-center justify-between mb-2">
            <Code className="w-6 h-6 text-black" />
            <span className="text-[10px] font-mono font-bold bg-[#FECDD3] px-2 py-0.5 rounded border border-black">Sandboxed</span>
          </div>
          <div>
            <h3 className="font-extrabold text-sm text-black">Code Challenges</h3>
            <p className="text-xs text-zinc-600 mt-1">Safe deterministic code runner with mistake diagnostics.</p>
          </div>
        </Link>

        <Link
          to="/smart-notes"
          className="bg-white border-2 border-black rounded-xl p-4 shadow-neo-sm hover:shadow-neo hover:bg-[#A7F3D0]/30 transition-all flex flex-col justify-between"
        >
          <div className="flex items-center justify-between mb-2">
            <Layers className="w-6 h-6 text-black" />
            <span className="text-[10px] font-mono font-bold bg-[#A7F3D0] px-2 py-0.5 rounded border border-black">Upload</span>
          </div>
          <div>
            <h3 className="font-extrabold text-sm text-black">Smart Notes & Revision</h3>
            <p className="text-xs text-zinc-600 mt-1">Extract key concepts from PDF/TXT and generate flashcards.</p>
          </div>
        </Link>
      </div>

      {/* Active Roadmap Path Overview */}
      <div className="bg-white border-3 border-black rounded-2xl p-6 sm:p-8 shadow-neo-lg">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-6 pb-4 border-b-2 border-black">
          <div>
            <h2 className="text-xl font-extrabold text-black">Adaptive Learning Roadmap</h2>
            <p className="text-xs text-zinc-600">Tasks dynamically ordered based on demonstrated weaknesses and prerequisite status.</p>
          </div>
          <Link
            to="/roadmap"
            className="text-xs font-bold bg-[#FEF08A] hover:bg-[#fde047] text-black px-3.5 py-1.5 rounded-lg border-2 border-black shadow-neo-xs flex items-center gap-1.5"
          >
            <span>View Full Roadmap</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="space-y-3">
          {roadmap?.tasks?.map((t, idx) => (
            <div
              key={t.id}
              className={`p-4 rounded-xl border-2 border-black transition-all flex flex-wrap items-center justify-between gap-4 ${
                t.status === 'in_progress'
                  ? 'bg-[#DDD6FE]/30 shadow-neo-xs'
                  : t.status === 'completed'
                  ? 'bg-zinc-50 opacity-80'
                  : 'bg-white'
              }`}
            >
              <div className="flex items-center gap-3">
                <span className="w-7 h-7 rounded-full bg-black text-[#FEF08A] font-mono font-bold text-xs flex items-center justify-center shrink-0">
                  {idx + 1}
                </span>
                <div>
                  <div className="font-bold text-sm text-black">{t.title}</div>
                  <div className="text-xs text-zinc-600">{t.learning_objective}</div>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded border border-black bg-white">
                  {t.difficulty}
                </span>
                <span className={`text-[10px] font-mono font-bold px-2.5 py-0.5 rounded border border-black ${
                  t.status === 'completed' ? 'bg-[#A7F3D0]' : t.status === 'in_progress' ? 'bg-[#FEF08A]' : 'bg-zinc-100'
                }`}>
                  {t.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
