import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useLearner } from '../context/LearnerContext';
import { MiniProject } from '../types';
import { FolderKanban, Sparkles, CheckCircle2, Clock, ArrowRight, ShieldCheck, FileCode } from 'lucide-react';

export const MiniProjectPage: React.FC = () => {
  const navigate = useNavigate();
  const { activeScenarioId, showToast } = useLearner();
  const [projects, setProjects] = useState<MiniProject[]>([]);
  const [selectedProject, setSelectedProject] = useState<MiniProject | null>(null);
  const [submissionText, setSubmissionText] = useState('');
  const [repoLink, setRepoLink] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        setLoading(true);
        const data = await api.getProjects();
        setProjects(data);
        if (data.length > 0) {
          // If Scenario 3 (Elena), select Capstone
          if (activeScenarioId === '3') {
            const p3 = data.find(p => p.id === 'p-ai-rag-agent');
            setSelectedProject(p3 || data[0]);
          } else {
            setSelectedProject(data[0]);
          }
        }
      } catch (err: any) {
        showToast(err.message, 'error');
      } finally {
        setLoading(false);
      }
    };
    fetchProjects();
  }, [activeScenarioId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedProject) return;
    if (!submissionText.trim()) {
      showToast('Please provide your project architecture / code description.', 'error');
      return;
    }

    try {
      setSubmitting(true);
      const res = await api.evaluateProject(selectedProject.id, submissionText, repoLink);
      showToast(`Project evaluated! Overall score: ${res.overall_score}%`, 'success');
      // Pass evaluation response via navigation state to feedback page
      navigate('/feedback', { state: { feedback: res, project: selectedProject } });
    } catch (err: any) {
      showToast(err.message, 'error');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-8">
      {/* Header */}
      <div className="bg-white border-3 border-black rounded-2xl p-6 sm:p-8 shadow-neo-lg flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 bg-[#FECDD3] text-black text-xs font-mono font-bold px-3 py-1 rounded-full border border-black mb-3">
            <FolderKanban className="w-3.5 h-3.5" />
            <span>Practical Capstone Mini-Projects</span>
          </div>
          <h1 className="text-3xl font-extrabold text-black">Practical Mini-Project Workspace</h1>
          <p className="text-sm text-zinc-600 mt-1 max-w-2xl font-medium">
            Integrate mastered concepts into deployable software artifacts. Evaluated against transparent, structured rubrics.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Project Selector List */}
        <div className="lg:col-span-4 space-y-3">
          <div className="text-xs font-mono font-bold text-zinc-500 uppercase tracking-wider mb-1">
            Available Mini-Projects ({projects.length})
          </div>
          {projects.map((p) => (
            <button
              key={p.id}
              onClick={() => setSelectedProject(p)}
              className={`w-full text-left p-4 rounded-xl border-3 transition-all ${
                selectedProject?.id === p.id
                  ? 'bg-[#DDD6FE] border-black shadow-neo font-bold'
                  : 'bg-white hover:bg-zinc-50 border-black shadow-neo-xs'
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-[10px] font-mono font-bold bg-black text-[#FEF08A] px-2 py-0.5 rounded">
                  {p.domain}
                </span>
                <span className="text-[10px] font-mono font-bold text-zinc-600">
                  {p.difficulty}
                </span>
              </div>
              <h3 className="font-extrabold text-sm text-black mb-1">{p.title}</h3>
              <div className="text-[11px] text-zinc-600 line-clamp-2">{p.objective}</div>
            </button>
          ))}
        </div>

        {/* Selected Project Brief & Submission Form */}
        <div className="lg:col-span-8 space-y-6">
          {selectedProject && (
            <div className="bg-white border-3 border-black rounded-2xl p-6 sm:p-8 shadow-neo space-y-6">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xs font-mono font-bold bg-[#A7F3D0] text-emerald-950 px-2.5 py-0.5 rounded border border-black">
                    Assessing: {selectedProject.skill_code}
                  </span>
                  <span className="text-xs font-mono font-bold text-zinc-600">
                    Est. {selectedProject.estimated_hours} Hours
                  </span>
                </div>
                <h2 className="text-2xl font-extrabold text-black">{selectedProject.title}</h2>
                <p className="text-xs sm:text-sm text-zinc-700 font-medium mt-1 leading-relaxed">
                  {selectedProject.objective}
                </p>
              </div>

              {/* Requirements Checklist */}
              <div className="bg-[#FAF7F2] border-2 border-black rounded-xl p-4 space-y-2">
                <div className="text-xs font-mono font-bold text-zinc-500 uppercase">
                  Project Requirements Checklist
                </div>
                <div className="space-y-1.5">
                  {selectedProject.requirements?.map((req, i) => (
                    <div key={i} className="flex items-start gap-2 text-xs font-bold text-zinc-800">
                      <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                      <span>{req}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Explicit Evaluation Rubric */}
              <div>
                <div className="text-xs font-mono font-bold text-zinc-500 uppercase mb-2">
                  Transparent Evaluation Rubric
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  {selectedProject.rubric?.map((rub, i) => (
                    <div key={i} className="bg-zinc-50 border-2 border-black rounded-xl p-3 shadow-neo-xs">
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-extrabold text-xs text-black">{rub.criterion}</span>
                        <span className="text-[10px] font-mono font-bold bg-[#FEF08A] px-1.5 py-0.5 rounded border border-black">
                          {rub.weight}%
                        </span>
                      </div>
                      <p className="text-[11px] text-zinc-600">{rub.description}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Submission Box */}
              <form onSubmit={handleSubmit} className="border-t-2 border-black pt-6 space-y-4">
                <div>
                  <label className="block text-xs font-bold text-black uppercase tracking-wider mb-1">
                    Repository Link / Live URL (Optional)
                  </label>
                  <input
                    type="url"
                    value={repoLink}
                    onChange={(e) => setRepoLink(e.target.value)}
                    placeholder="https://github.com/learner/skillforge-capstone"
                    className="w-full px-3.5 py-2 border-2 border-black rounded-xl text-xs sm:text-sm font-semibold bg-white"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-black uppercase tracking-wider mb-1">
                    Project Architecture, Schema & Code Implementation (Markdown or Code)
                  </label>
                  <textarea
                    rows={8}
                    required
                    value={submissionText}
                    onChange={(e) => setSubmissionText(e.target.value)}
                    placeholder={`# Architecture Overview\nImplemented modular controller separation...\n\n# Code Excerpt\nfrom pydantic import BaseModel\n...`}
                    className="w-full p-4 border-2 border-black rounded-xl text-xs sm:text-sm font-mono bg-zinc-50 focus:bg-white focus:outline-none"
                  />
                </div>

                <button
                  type="submit"
                  disabled={submitting}
                  className="w-full bg-[#A78BFA] hover:bg-[#906cf8] text-black font-extrabold py-3.5 px-6 rounded-xl border-3 border-black shadow-neo hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-sm flex items-center justify-center gap-2"
                >
                  <span>{submitting ? 'Evaluating Against Rubric...' : 'Submit Project for Rubric Evaluation'}</span>
                  <ArrowRight className="w-5 h-5" />
                </button>
              </form>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
