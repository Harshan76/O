import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Course, LearningGoal } from '../types';
import { useLearner } from '../context/LearnerContext';
import { BookOpen, Target, Sparkles, CheckCircle2, Clock, ArrowRight } from 'lucide-react';

export const GoalsCoursesPage: React.FC = () => {
  const { refreshAll, showToast } = useLearner();
  const [courses, setCourses] = useState<Course[]>([]);
  const [goals, setGoals] = useState<LearningGoal[]>([]);
  const [loading, setLoading] = useState(true);
  const [enrolling, setEnrolling] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [cList, gList] = await Promise.all([
          api.getCourses(),
          api.getGoals()
        ]);
        setCourses(cList);
        setGoals(gList);
      } catch (err: any) {
        showToast(err.message, 'error');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleEnroll = async (c: Course) => {
    try {
      setEnrolling(c.id);
      await api.createGoal({
        title: c.title,
        domain: c.domain,
        target_outcome: `Attain job-ready proficiency in ${c.title}`,
        experience_level: 'intermediate',
        daily_minutes: 45,
        learning_style: 'hands-on',
        target_date: '2026-12-31'
      });
      await refreshAll();
      showToast(`Enrolled in ${c.title}! Goal active.`, 'success');
      const updatedGoals = await api.getGoals();
      setGoals(updatedGoals);
    } catch (err: any) {
      showToast(err.message, 'error');
    } finally {
      setEnrolling(null);
    }
  };

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-8">
      {/* Header */}
      <div className="bg-white border-3 border-black rounded-2xl p-6 sm:p-8 shadow-neo-lg">
        <div className="inline-flex items-center gap-2 bg-[#DDD6FE] text-black text-xs font-mono font-bold px-3 py-1 rounded-full border border-black mb-3">
          <BookOpen className="w-3.5 h-3.5" />
          <span>Curriculum Catalog & Active Goals</span>
        </div>
        <h1 className="text-3xl font-extrabold text-black">Learning Goals & Course Catalog</h1>
        <p className="text-sm text-zinc-600 mt-1 max-w-2xl font-medium">
          Choose a foundational track or specialized curriculum. Your AI tutor personalizes the pace, prerequisite checkpoints, and project milestones to your demonstrated skill level.
        </p>
      </div>

      {/* Active Goals Section */}
      {goals.length > 0 && (
        <div className="bg-[#FAF7F2] border-3 border-black rounded-2xl p-6 shadow-neo">
          <h2 className="text-lg font-extrabold text-black mb-4 flex items-center gap-2">
            <Target className="w-5 h-5 text-black" />
            <span>Active Learning Goals ({goals.length})</span>
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {goals.map((g) => (
              <div key={g.id} className="bg-white border-2 border-black rounded-xl p-4 shadow-neo-sm">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-mono font-bold bg-[#FEF08A] px-2 py-0.5 rounded border border-black">
                    {g.domain}
                  </span>
                  <span className="text-xs font-mono font-bold text-emerald-700 bg-[#A7F3D0] px-2 py-0.5 rounded border border-black">
                    {g.status}
                  </span>
                </div>
                <h3 className="font-extrabold text-base text-black mb-1">{g.title}</h3>
                <p className="text-xs text-zinc-600 font-medium mb-3">{g.target_outcome}</p>
                <div className="w-full bg-zinc-200 border border-black rounded-full h-2.5 overflow-hidden">
                  <div className="bg-[#A78BFA] h-full" style={{ width: `${g.progress_percentage}%` }}></div>
                </div>
                <div className="text-[10px] font-mono text-zinc-600 mt-1.5 flex justify-between">
                  <span>Progress</span>
                  <span>{g.progress_percentage}% Mastered</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Courses Catalog */}
      <div className="space-y-6">
        <h2 className="text-2xl font-extrabold text-black">Available Courses</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {courses.map((c) => (
            <div
              key={c.id}
              className="bg-white border-3 border-black rounded-2xl p-6 shadow-neo flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-mono font-bold bg-[#DDD6FE] px-2.5 py-0.5 rounded border border-black">
                    {c.domain}
                  </span>
                  <span className="text-xs font-mono font-bold text-zinc-600">
                    {c.level}
                  </span>
                </div>
                <h3 className="text-xl font-extrabold text-black mb-2">{c.title}</h3>
                <p className="text-sm text-zinc-700 font-medium mb-4 leading-relaxed">
                  {c.description}
                </p>

                {/* Modules breakdown */}
                <div className="border-t-2 border-dashed border-zinc-300 pt-4 mb-6 space-y-2">
                  <div className="text-xs font-mono font-bold text-zinc-500 uppercase tracking-wider">
                    Curriculum Modules ({c.modules?.length || 0})
                  </div>
                  {c.modules?.map((m) => (
                    <div key={m.id} className="bg-zinc-50 border border-black rounded-lg p-2.5 text-xs flex items-center justify-between">
                      <div>
                        <div className="font-bold text-black">{m.title}</div>
                        <div className="text-[11px] text-zinc-600">{m.description}</div>
                      </div>
                      <div className="flex items-center gap-1 font-mono text-[10px] text-zinc-500 shrink-0 ml-2">
                        <Clock className="w-3 h-3" />
                        <span>{m.estimated_hours}h</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <button
                onClick={() => handleEnroll(c)}
                disabled={enrolling === c.id}
                className="w-full bg-[#FEF08A] hover:bg-[#fde047] text-black font-extrabold py-3 px-4 rounded-xl border-2 border-black shadow-neo-sm hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-sm flex items-center justify-center gap-2"
              >
                <span>{enrolling === c.id ? 'Enrolling...' : 'Set as Active Learning Goal'}</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
