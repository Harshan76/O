import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import { useLearner } from '../context/LearnerContext';
import { LearningPathResponse, LearningTask } from '../types';
import { Sparkles, ArrowRight, RefreshCw, CheckCircle2, Clock, Bot, Code, FolderKanban, ChevronRight, X } from 'lucide-react';

export const RoadmapPage: React.FC = () => {
  const { activeScenarioId, showToast, refreshAll } = useLearner();
  const [roadmap, setRoadmap] = useState<LearningPathResponse | null>(null);
  const [selectedTask, setSelectedTask] = useState<LearningTask | null>(null);
  const [loading, setLoading] = useState(true);
  const [regenerating, setRegenerating] = useState(false);

  const fetchRoadmap = async () => {
    try {
      setLoading(true);
      const data = await api.getCurrentRoadmap();
      setRoadmap(data);
    } catch (err: any) {
      showToast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRoadmap();
  }, [activeScenarioId]);

  const handleRegenerate = async () => {
    try {
      setRegenerating(true);
      const updated = await api.generateRoadmap();
      setRoadmap(updated);
      await refreshAll();
      showToast('Learning roadmap dynamically adapted to latest demonstrated performance!', 'success');
    } catch (err: any) {
      showToast(err.message, 'error');
    } finally {
      setRegenerating(false);
    }
  };

  const handleMarkComplete = async (taskId: string) => {
    try {
      await api.updateTaskStatus(taskId, 'completed');
      showToast('Task marked as completed! Updating mastery...', 'success');
      await fetchRoadmap();
      await refreshAll();
      if (selectedTask?.id === taskId) {
        setSelectedTask(prev => prev ? { ...prev, status: 'completed' } : null);
      }
    } catch (err: any) {
      showToast(err.message, 'error');
    }
  };

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-8">
      {/* Header */}
      <div className="bg-white border-3 border-black rounded-2xl p-6 sm:p-8 shadow-neo-lg flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 bg-[#FEF08A] text-black text-xs font-mono font-bold px-3 py-1 rounded-full border border-black mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Deterministic Adaptive Pathway</span>
          </div>
          <h1 className="text-3xl font-extrabold text-black">
            {roadmap?.title || 'Personalized Learning Roadmap'}
          </h1>
          <p className="text-sm text-zinc-600 mt-1 max-w-2xl font-medium">
            {roadmap?.adaptation_reason || 'Customized sequence based on verified skill profile and prerequisite status.'}
          </p>
        </div>

        <button
          onClick={handleRegenerate}
          disabled={regenerating}
          className="bg-[#A78BFA] hover:bg-[#906cf8] text-black font-extrabold px-4 py-2.5 rounded-xl border-2 border-black shadow-neo-xs flex items-center gap-2 text-xs"
        >
          <RefreshCw className={`w-4 h-4 ${regenerating ? 'animate-spin' : ''}`} />
          <span>{regenerating ? 'Re-analyzing Skills...' : 'Regenerate Adaptive Path'}</span>
        </button>
      </div>

      {/* Progress Card */}
      {roadmap && (
        <div className="bg-[#FAF7F2] border-3 border-black rounded-2xl p-6 shadow-neo flex flex-wrap items-center justify-between gap-4">
          <div className="flex-1 min-w-[240px]">
            <div className="flex justify-between text-xs font-mono font-bold mb-1.5">
              <span>Path Progress</span>
              <span>{roadmap.progress_percentage}% Completed</span>
            </div>
            <div className="w-full bg-zinc-200 border-2 border-black rounded-full h-3 overflow-hidden">
              <div className="bg-[#A78BFA] h-full" style={{ width: `${roadmap.progress_percentage}%` }}></div>
            </div>
          </div>
          <div className="text-xs font-mono font-bold bg-white border border-black px-3 py-1.5 rounded-lg shadow-neo-xs">
            {roadmap.tasks?.length || 0} Total Sequential Tasks
          </div>
        </div>
      )}

      {/* Sequential Task Nodes */}
      <div className="space-y-4">
        {roadmap?.tasks?.map((t, idx) => {
          const isCompleted = t.status === 'completed';
          const isInProgress = t.status === 'in_progress';

          return (
            <div
              key={t.id}
              onClick={() => setSelectedTask(t)}
              className={`border-3 border-black rounded-2xl p-6 cursor-pointer transition-all shadow-neo hover:translate-x-1 ${
                isCompleted
                  ? 'bg-zinc-50 opacity-85'
                  : isInProgress
                  ? 'bg-[#DDD6FE]/30 border-black shadow-neo-lg'
                  : 'bg-white'
              }`}
            >
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div className="flex items-center gap-4">
                  <div className={`w-10 h-10 rounded-xl border-2 border-black flex items-center justify-center font-mono font-black text-sm shrink-0 shadow-neo-xs ${
                    isCompleted ? 'bg-[#A7F3D0] text-emerald-950' : isInProgress ? 'bg-[#FEF08A] text-black' : 'bg-black text-white'
                  }`}>
                    {idx + 1}
                  </div>
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-mono text-[10px] font-bold bg-zinc-100 border border-black px-2 py-0.5 rounded">
                        Skill: {t.skill_code}
                      </span>
                      <span className="font-mono text-[10px] font-bold bg-[#FECDD3] text-rose-950 border border-black px-2 py-0.5 rounded">
                        {t.difficulty}
                      </span>
                      <span className="font-mono text-[10px] font-bold bg-[#BAE6FD] text-blue-950 border border-black px-2 py-0.5 rounded">
                        {t.task_type}
                      </span>
                    </div>
                    <h3 className="text-base sm:text-lg font-extrabold text-black">{t.title}</h3>
                    <p className="text-xs text-zinc-600 font-medium mt-0.5 line-clamp-1">{t.learning_objective}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="flex items-center gap-1 text-xs font-mono font-bold text-zinc-600">
                    <Clock className="w-3.5 h-3.5" />
                    <span>{t.estimated_duration}m</span>
                  </div>
                  <span className={`text-xs font-mono font-bold px-2.5 py-1 rounded border border-black uppercase ${
                    isCompleted ? 'bg-[#A7F3D0]' : isInProgress ? 'bg-[#FEF08A]' : 'bg-zinc-100'
                  }`}>
                    {t.status}
                  </span>
                  <ChevronRight className="w-5 h-5 text-zinc-400" />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Task Detail Modal */}
      {selectedTask && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white border-3 border-black rounded-2xl p-6 sm:p-8 max-w-2xl w-full shadow-neo-xl max-h-[90vh] overflow-y-auto space-y-6">
            <div className="flex items-start justify-between border-b-2 border-black pb-4">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-[10px] font-mono font-bold bg-black text-[#FEF08A] px-2 py-0.5 rounded">
                    Task Details
                  </span>
                  <span className="text-[10px] font-mono font-bold bg-[#DDD6FE] px-2 py-0.5 rounded border border-black">
                    {selectedTask.difficulty}
                  </span>
                </div>
                <h2 className="text-2xl font-extrabold text-black">{selectedTask.title}</h2>
              </div>
              <button
                onClick={() => setSelectedTask(null)}
                className="p-1.5 border-2 border-black rounded-lg bg-zinc-100 hover:bg-zinc-200"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-4 text-xs sm:text-sm">
              <div>
                <h4 className="font-extrabold text-black uppercase font-mono text-xs mb-1">Learning Objective</h4>
                <p className="text-zinc-700 bg-zinc-50 p-3 rounded-lg border border-black">{selectedTask.learning_objective}</p>
              </div>

              <div>
                <h4 className="font-extrabold text-black uppercase font-mono text-xs mb-1">Instructions</h4>
                <p className="text-zinc-700 bg-zinc-50 p-3 rounded-lg border border-black whitespace-pre-wrap">{selectedTask.instructions}</p>
              </div>

              {selectedTask.hints && selectedTask.hints.length > 0 && (
                <div>
                  <h4 className="font-extrabold text-black uppercase font-mono text-xs mb-1">Tutor Clues</h4>
                  <ul className="list-disc pl-5 space-y-1 text-zinc-700">
                    {selectedTask.hints.map((h, i) => (
                      <li key={i}>{h}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="bg-[#FEF08A]/30 border border-black rounded-lg p-3 text-xs">
                <strong>Why This Task Was Selected:</strong> {selectedTask.reason_for_recommendation}
              </div>
            </div>

            <div className="flex flex-wrap items-center justify-between gap-3 pt-4 border-t-2 border-black">
              <button
                onClick={() => handleMarkComplete(selectedTask.id)}
                className="bg-white hover:bg-zinc-100 border-2 border-black px-4 py-2 rounded-xl text-xs font-bold shadow-neo-xs flex items-center gap-1.5"
              >
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>Mark Completed</span>
              </button>

              <div className="flex items-center gap-2">
                <Link
                  to="/tutor"
                  className="bg-white hover:bg-zinc-100 border-2 border-black px-4 py-2 rounded-xl text-xs font-bold shadow-neo-xs flex items-center gap-1.5"
                >
                  <Bot className="w-4 h-4" />
                  <span>Discuss with AI Tutor</span>
                </Link>
                <Link
                  to={selectedTask.task_type === 'project' ? '/projects' : '/challenges'}
                  className="bg-[#A78BFA] hover:bg-[#906cf8] text-black font-extrabold px-5 py-2 rounded-xl border-2 border-black shadow-neo-xs flex items-center gap-1.5 text-xs"
                >
                  <span>Launch Task Workspace</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
