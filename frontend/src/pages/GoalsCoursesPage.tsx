import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import { Course, LearningGoal } from '../types';
import { useLearner } from '../context/LearnerContext';
import { 
  BookOpen, Target, Sparkles, CheckCircle2, Clock, 
  ArrowRight, Play, FileText, ExternalLink, Video 
} from 'lucide-react';

// Verified educational video mappings for each curriculum module
const MODULE_LEARNING_LINKS: Record<string, { videoUrl: string; channel: string }> = {
  // Python Programming & System Scripting
  'm-py-1': { videoUrl: 'https://www.youtube.com/watch?v=rfscVS0vtbw', channel: 'freeCodeCamp' },
  'm-py-2': { videoUrl: 'https://www.youtube.com/watch?v=6iF8Xb7Z3wQ', channel: 'Corey Schafer' },
  'm-py-3': { videoUrl: 'https://www.youtube.com/watch?v=9Os0o3wzS_I', channel: 'Corey Schafer' },
  'm-py-4': { videoUrl: 'https://www.youtube.com/watch?v=NIWwJbo-9_8', channel: 'Corey Schafer' },

  // Modern Full-Stack Web Architecture
  'm-fs-1': { videoUrl: 'https://www.youtube.com/watch?v=bMknfKXIFA8', channel: 'freeCodeCamp' },
  'm-fs-2': { videoUrl: 'https://www.youtube.com/watch?v=0ZJgIjIuY7U', channel: 'Web Dev Simplified' },
  'm-fs-3': { videoUrl: 'https://www.youtube.com/watch?v=gL3xep_J_jI', channel: 'Web Dev Simplified' },
  'm-fs-4': { videoUrl: 'https://www.youtube.com/watch?v=mbsmsi7l3r4', channel: 'Web Dev Simplified' },

  // Data Science & Machine Learning Engineering
  'm-ds-1': { videoUrl: 'https://www.youtube.com/watch?v=QUT1VHiLmmI', channel: 'freeCodeCamp' },
  'm-ds-2': { videoUrl: 'https://www.youtube.com/watch?v=vmEHCJofslg', channel: 'freeCodeCamp' },
  'm-ds-3': { videoUrl: 'https://www.youtube.com/watch?v=tTeMYuS87oU', channel: 'StatQuest' },
  'm-ds-4': { videoUrl: 'https://www.youtube.com/watch?v=aircAruvnKk', channel: '3Blue1Brown' },

  // AI Engineering & Autonomous LLM Systems
  'm-ai-1': { videoUrl: 'https://www.youtube.com/watch?v=jC4v5AS4RIM', channel: 'DeepLearning.AI' },
  'm-ai-2': { videoUrl: 'https://www.youtube.com/watch?v=ySus5ZS0b94', channel: 'StatQuest' },
  'm-ai-3': { videoUrl: 'https://www.youtube.com/watch?v=T-D1OfcDW1M', channel: 'freeCodeCamp' },
  'm-ai-4': { videoUrl: 'https://www.youtube.com/watch?v=bZQun8Y4L2A', channel: 'IBM Technology' }
};

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
          Choose a foundational track or specialized curriculum. Click on any module to watch its educational video or open its structured study notes & PDF guide.
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
                <div className="mt-3 pt-2 border-t border-zinc-200 flex justify-end">
                  <Link
                    to={`/courses/${g.title.toLowerCase().includes('react') || g.title.toLowerCase().includes('web') ? 'c-fullstack' : g.title.toLowerCase().includes('data') ? 'c-datasci' : g.title.toLowerCase().includes('ai') ? 'c-ai-eng' : 'c-python'}/learn`}
                    className="text-xs font-bold text-black hover:text-emerald-800 flex items-center gap-1 font-mono"
                  >
                    <span>Open Learning Hub</span>
                    <ArrowRight className="w-3 h-3" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Courses Catalog */}
      <div className="space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h2 className="text-2xl font-extrabold text-black">Available Courses</h2>
          <span className="text-xs font-mono font-bold text-zinc-500 bg-zinc-100 px-2.5 py-1 rounded-lg border border-black">
            💡 Click any module card to watch the video or study notes
          </span>
        </div>

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
                <div className="border-t-2 border-dashed border-zinc-300 pt-4 mb-6 space-y-2.5">
                  <div className="flex items-center justify-between">
                    <div className="text-xs font-mono font-bold text-zinc-500 uppercase tracking-wider">
                      Curriculum Modules ({c.modules?.length || 0})
                    </div>
                    <span className="text-[10px] font-mono text-zinc-500">
                      Click to Learn
                    </span>
                  </div>

                  {c.modules?.map((m) => {
                    const videoInfo = MODULE_LEARNING_LINKS[m.id];
                    return (
                      <div
                        key={m.id}
                        className="bg-zinc-50 hover:bg-[#FEF08A]/30 border-2 border-black rounded-xl p-3 text-xs transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 shadow-neo-xs hover:translate-x-0.5 group"
                      >
                        {/* Title & Description Click Area */}
                        <Link
                          to={`/courses/${c.id}/learn?topic=${m.id}&tab=videos`}
                          className="flex-1 cursor-pointer"
                        >
                          <div className="font-extrabold text-sm text-black group-hover:text-amber-950 flex items-center gap-1.5">
                            <span>{m.title}</span>
                            <ArrowRight className="w-3.5 h-3.5 opacity-0 group-hover:opacity-100 transition-opacity text-black" />
                          </div>
                          <div className="text-[11px] text-zinc-600 font-medium mt-0.5">{m.description}</div>
                        </Link>

                        {/* Interactive Learning Actions */}
                        <div className="flex items-center gap-1.5 shrink-0 pt-1 sm:pt-0 border-t sm:border-t-0 border-zinc-200">
                          <span className="flex items-center gap-1 font-mono text-[10px] text-zinc-500 font-bold mr-1">
                            <Clock className="w-3 h-3" />
                            {m.estimated_hours}h
                          </span>

                          {/* 1. Direct Video in Hub */}
                          <Link
                            to={`/courses/${c.id}/learn?topic=${m.id}&tab=videos`}
                            title="Watch Video Lesson in Learning Hub"
                            className="bg-[#FEF08A] hover:bg-[#fde047] text-black font-extrabold px-2.5 py-1 rounded-lg border border-black shadow-neo-xs text-[11px] flex items-center gap-1 transition-all"
                          >
                            <Play className="w-3 h-3 fill-black text-black" />
                            <span>Video</span>
                          </Link>

                          {/* 2. Direct Watch on YouTube */}
                          {videoInfo && (
                            <a
                              href={videoInfo.videoUrl}
                              target="_blank"
                              rel="noopener noreferrer"
                              title={`Watch directly on YouTube (${videoInfo.channel})`}
                              className="bg-white hover:bg-zinc-100 text-zinc-800 font-bold p-1 rounded-lg border border-black shadow-neo-xs text-[10px] flex items-center transition-all"
                            >
                              <ExternalLink className="w-3 h-3 text-black" />
                            </a>
                          )}

                          {/* 3. Direct Study Notes & PDF Guide */}
                          <Link
                            to={`/courses/${c.id}/learn?topic=${m.id}&tab=pdf`}
                            title="Open Printable Study Guide & Notes"
                            className="bg-[#A7F3D0] hover:bg-[#86efac] text-emerald-950 font-extrabold px-2.5 py-1 rounded-lg border border-black shadow-neo-xs text-[11px] flex items-center gap-1 transition-all"
                          >
                            <FileText className="w-3 h-3 text-emerald-900" />
                            <span>PDF/Notes</span>
                          </Link>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Course Bottom Action Bar */}
              <div className="flex flex-col sm:flex-row items-center gap-2.5">
                <Link
                  to={`/courses/${c.id}/learn`}
                  className="w-full sm:flex-1 bg-[#A7F3D0] hover:bg-[#86efac] text-emerald-950 font-extrabold py-3 px-3 rounded-xl border-2 border-black shadow-neo-sm hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-xs sm:text-sm flex items-center justify-center gap-1.5"
                >
                  <BookOpen className="w-4 h-4 text-emerald-950" />
                  <span>Open Learning Hub</span>
                </Link>

                <button
                  onClick={() => handleEnroll(c)}
                  disabled={enrolling === c.id}
                  className="w-full sm:flex-1 bg-[#FEF08A] hover:bg-[#fde047] text-black font-extrabold py-3 px-3 rounded-xl border-2 border-black shadow-neo-sm hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-xs sm:text-sm flex items-center justify-center gap-1.5"
                >
                  <span>{enrolling === c.id ? 'Enrolling...' : 'Set Active Goal'}</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
