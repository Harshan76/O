import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import { useLearner } from '../context/LearnerContext';
import { SubmissionEvaluateResponse } from '../types';
import { CheckCircle2, AlertTriangle, ArrowRight, Sparkles, Award, FileText, Bot } from 'lucide-react';

export const SubmissionFeedbackPage: React.FC = () => {
  const location = useLocation();
  const { activeScenarioId } = useLearner();
  const stateFeedback = location.state?.feedback as SubmissionEvaluateResponse | undefined;

  // Fallback / Seeded Scenario 8 feedback
  const feedback: SubmissionEvaluateResponse = stateFeedback || {
    submission_id: 'sub-demo-8',
    project_id: 'p-react-kanban',
    overall_score: 83,
    passed: true,
    rubric_scores: [
      { criterion: "Architecture & Separation of Concerns", score: 90, feedback: "Clean modular separation between route controllers, validation schemas, and database queries." },
      { criterion: "Input Validation & Type Safety", score: 92, feedback: "Pydantic schemas effectively caught missing fields, malformed emails, and invalid integer boundaries." },
      { criterion: "Error Handling & Status Codes", score: 65, feedback: "Several unhandled database exceptions leaked raw 500 error tracebacks to the client instead of sanitized 400/404 messages." },
      { criterion: "Documentation & Testing", score: 85, feedback: "OpenAPI / Swagger docs were clean; test suite covered happy paths well but lacked negative authorization tests." }
    ],
    strengths: [
      "Clean declarative Pydantic schemas",
      "Proper password hashing with bcrypt salts",
      "Effective token verification middleware"
    ],
    areas_for_improvement: [
      "Implement a centralized exception handler to prevent stack leakages",
      "Add unit tests verifying token expiration and 401 Unauthorized responses",
      "Rate limiter lacked Redis distributed state; currently in-memory only"
    ],
    ai_coaching_notes: "Great submission Liam! Your architectural boundaries are very clean. The main reason this scored 83 instead of 95+ is unhandled internal exceptions leaking tracebacks. In production, this can expose database credentials or internal table structures. Adding a custom FastAPI `@app.exception_handler` will push this into senior-level territory.",
    next_recommended_milestone: "Implement Centralized Exception Handling Middleware"
  };

  return (
    <div className="max-w-5xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Header Banner */}
      <div className={`border-3 border-black rounded-2xl p-6 sm:p-8 shadow-neo-lg ${
        feedback.passed ? 'bg-[#A7F3D0]' : 'bg-[#FECDD3]'
      }`}>
        <div className="flex flex-wrap items-center justify-between gap-4 mb-2">
          <div className="flex items-center gap-2">
            <span className="bg-black text-white text-xs font-mono font-bold px-2.5 py-0.5 rounded">
              Rubric Assessment Report
            </span>
            <span className="text-xs font-mono font-bold text-zinc-700">
              ID: {feedback.submission_id}
            </span>
          </div>
          <div className="text-3xl font-black font-mono bg-white px-4 py-2 border-2 border-black rounded-xl shadow-neo-xs">
            {feedback.overall_score}/100
          </div>
        </div>

        <h1 className="text-3xl font-extrabold text-black">
          {feedback.passed ? 'Project Submission Approved' : 'Project Needs Refinement'}
        </h1>
        <p className="text-sm text-zinc-900 font-medium mt-1">
          Evaluated against 4 explicit criteria pillars with actionable recommendations.
        </p>
      </div>

      {/* Rubric Scorecard Table */}
      <div className="bg-white border-3 border-black rounded-2xl p-6 shadow-neo space-y-4">
        <h2 className="text-xl font-extrabold text-black">Criterion Breakdown</h2>
        <div className="space-y-3">
          {feedback.rubric_scores.map((r, i) => (
            <div key={i} className="bg-zinc-50 border-2 border-black rounded-xl p-4 shadow-neo-xs">
              <div className="flex items-center justify-between mb-1.5">
                <span className="font-extrabold text-sm text-black">{r.criterion}</span>
                <span className={`text-xs font-mono font-bold px-2.5 py-0.5 rounded border border-black ${
                  r.score >= 80 ? 'bg-[#A7F3D0]' : r.score >= 65 ? 'bg-[#FEF08A]' : 'bg-[#FECDD3]'
                }`}>
                  {r.score}/100
                </span>
              </div>
              <p className="text-xs text-zinc-700 font-medium leading-relaxed">{r.feedback}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Strengths & Improvements */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <div className="bg-white border-3 border-black rounded-2xl p-6 shadow-neo space-y-3">
          <div className="flex items-center gap-2 text-emerald-800">
            <CheckCircle2 className="w-5 h-5 text-emerald-600" />
            <h3 className="text-base font-extrabold text-black">Demonstrated Strengths</h3>
          </div>
          <ul className="space-y-2 text-xs font-medium text-zinc-800">
            {feedback.strengths.map((str, i) => (
              <li key={i} className="flex items-start gap-2 bg-emerald-50/60 p-2.5 rounded-lg border border-emerald-300">
                <span className="text-emerald-700 font-bold">✓</span>
                <span>{str}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="bg-white border-3 border-black rounded-2xl p-6 shadow-neo space-y-3">
          <div className="flex items-center gap-2 text-rose-800">
            <AlertTriangle className="w-5 h-5 text-rose-600" />
            <h3 className="text-base font-extrabold text-black">Areas for Improvement</h3>
          </div>
          <ul className="space-y-2 text-xs font-medium text-zinc-800">
            {feedback.areas_for_improvement.map((area, i) => (
              <li key={i} className="flex items-start gap-2 bg-rose-50/60 p-2.5 rounded-lg border border-rose-300">
                <span className="text-rose-700 font-bold">•</span>
                <span>{area}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* AI Coaching Note */}
      <div className="bg-[#FAF7F2] border-3 border-black rounded-2xl p-6 shadow-neo space-y-3">
        <div className="flex items-center gap-2">
          <Bot className="w-5 h-5 text-black" />
          <h3 className="text-base font-extrabold text-black">AI Tutor Coaching Commentary</h3>
        </div>
        <p className="text-xs sm:text-sm text-zinc-800 leading-relaxed font-medium bg-white p-4 rounded-xl border border-black">
          {feedback.ai_coaching_notes}
        </p>

        <div className="bg-[#FEF08A] border border-black rounded-xl p-3 text-xs font-bold text-black flex items-center justify-between">
          <span>Next Recommended Milestone: {feedback.next_recommended_milestone}</span>
          <Link to="/roadmap" className="bg-black text-[#FEF08A] px-3 py-1 rounded text-xs">
            View in Roadmap
          </Link>
        </div>
      </div>
    </div>
  );
};
