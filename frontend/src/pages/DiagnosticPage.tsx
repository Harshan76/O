import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useLearner } from '../context/LearnerContext';
import { AssessmentQuestion, AssessmentSubmitResponse } from '../types';
import { Brain, Sparkles, CheckCircle2, AlertTriangle, ArrowRight, Lightbulb, RefreshCw } from 'lucide-react';

export const DiagnosticPage: React.FC = () => {
  const { showToast, refreshAll } = useLearner();
  const [assessmentId, setAssessmentId] = useState<string>('');
  const [title, setTitle] = useState<string>('Diagnostic Assessment');
  const [questions, setQuestions] = useState<AssessmentQuestion[]>([]);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [results, setResults] = useState<AssessmentSubmitResponse | null>(null);
  const [hintsRevealed, setHintsRevealed] = useState<Record<string, boolean>>({});

  const startTest = async () => {
    try {
      setLoading(true);
      setResults(null);
      setAnswers({});
      const data = await api.startAssessment('c-python');
      setAssessmentId(data.assessment_id);
      setTitle(data.title);
      setQuestions(data.questions);
    } catch (err: any) {
      showToast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    startTest();
  }, []);

  const handleSelectOption = (qId: string, optionId: string) => {
    setAnswers(prev => ({ ...prev, [qId]: optionId }));
  };

  const toggleHint = (qId: string) => {
    setHintsRevealed(prev => ({ ...prev, [qId]: !prev[qId] }));
  };

  const handleSubmit = async () => {
    if (Object.keys(answers).length < questions.length) {
      if (!confirm('You have unanswered questions. Submit anyway?')) return;
    }

    try {
      setSubmitting(true);
      const payloadAnswers = questions.map(q => ({
        question_id: q.id,
        answer: answers[q.id] || ''
      }));

      const res = await api.submitAssessment(assessmentId, payloadAnswers);
      setResults(res);
      await refreshAll();
      showToast(`Diagnostic submitted! Score: ${res.score}% — Rule: ${res.adaptation_direction}`, 'success');
    } catch (err: any) {
      showToast(err.message, 'error');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="bg-white border-3 border-black rounded-2xl p-6 sm:p-8 shadow-neo-lg flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 bg-[#FEF08A] text-black text-xs font-mono font-bold px-3 py-1 rounded-full border border-black mb-2">
            <Brain className="w-3.5 h-3.5" />
            <span>AI Diagnostic Engine</span>
          </div>
          <h1 className="text-3xl font-extrabold text-black">{title}</h1>
          <p className="text-xs sm:text-sm text-zinc-600 font-medium">
            Predefined answer keys & explicit rubrics establish your verified baseline.
          </p>
        </div>
        <button
          onClick={startTest}
          className="bg-white hover:bg-zinc-50 border-2 border-black px-3.5 py-1.5 rounded-lg text-xs font-bold shadow-neo-xs flex items-center gap-1.5"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Restart Assessment</span>
        </button>
      </div>

      {/* Results Card if submitted */}
      {results && (
        <div className={`border-3 border-black rounded-2xl p-6 sm:p-8 shadow-neo-lg ${
          results.percentage >= 80 ? 'bg-[#A7F3D0]' : results.percentage >= 50 ? 'bg-[#FEF08A]' : 'bg-[#FECDD3]'
        }`}>
          <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
            <div>
              <span className="text-xs font-mono font-bold uppercase bg-black text-white px-2 py-0.5 rounded">
                Evaluation Complete
              </span>
              <h2 className="text-2xl font-extrabold text-black mt-1">
                Diagnostic Result: {results.score}% ({results.passed ? 'Demonstrated Mastery' : 'Prerequisite Gaps Detected'})
              </h2>
            </div>
            <div className="text-3xl font-black font-mono bg-white px-4 py-2 border-2 border-black rounded-xl shadow-neo-xs">
              {results.score}/100
            </div>
          </div>

          <p className="text-sm text-zinc-900 font-bold mb-4">
            {results.status_summary}
          </p>

          <div className="bg-white/90 border-2 border-black rounded-xl p-4 space-y-2 mb-6">
            <div className="text-xs font-mono font-bold uppercase text-zinc-500">Deterministic Adaptation Triggered</div>
            <div className="text-sm font-extrabold text-black">
              Direction: <span className="underline">{results.adaptation_direction.replace('_', ' ').toUpperCase()}</span>
            </div>
            <div className="text-xs text-zinc-700">
              <strong>Next Task Assigned:</strong> {results.recommended_next_task?.title} ({results.recommended_next_task?.difficulty} tier)
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <a
              href="/skill-gap"
              className="bg-black text-[#FEF08A] font-extrabold px-6 py-2.5 rounded-xl border-2 border-black shadow-neo-xs text-xs flex items-center gap-2"
            >
              <span>View Skill-Gap Map</span>
              <ArrowRight className="w-4 h-4" />
            </a>
            <a
              href="/roadmap"
              className="bg-white hover:bg-zinc-100 text-black font-extrabold px-5 py-2.5 rounded-xl border-2 border-black shadow-neo-xs text-xs"
            >
              Go to Adapted Roadmap
            </a>
          </div>
        </div>
      )}

      {/* Questions List */}
      <div className="space-y-6">
        {questions.map((q, idx) => {
          const isAnswered = !!answers[q.id];
          const showHint = hintsRevealed[q.id];
          const resultDetail = results?.results?.find(r => r.question_id === q.id);

          return (
            <div
              key={q.id}
              className={`bg-white border-3 border-black rounded-2xl p-6 shadow-neo ${
                resultDetail
                  ? resultDetail.is_correct ? 'border-emerald-700 bg-emerald-50/20' : 'border-rose-600 bg-rose-50/20'
                  : ''
              }`}
            >
              {/* Question Meta */}
              <div className="flex items-center justify-between mb-3">
                <span className="bg-black text-[#FEF08A] font-mono font-bold text-xs px-2.5 py-0.5 rounded">
                  Question #{idx + 1}
                </span>
                <div className="flex items-center gap-2">
                  <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded border border-black bg-zinc-100">
                    Skill: {q.skill_id}
                  </span>
                  <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded border border-black bg-[#DDD6FE]">
                    {q.difficulty}
                  </span>
                </div>
              </div>

              {/* Prompt */}
              <div className="text-sm sm:text-base font-extrabold text-black mb-4 whitespace-pre-wrap leading-relaxed">
                {q.prompt}
              </div>

              {/* Options */}
              {q.options && q.options.length > 0 && (
                <div className="space-y-2 mb-4">
                  {q.options.map((opt) => {
                    const isSelected = answers[q.id] === opt.id;
                    return (
                      <button
                        key={opt.id}
                        type="button"
                        onClick={() => handleSelectOption(q.id, opt.id)}
                        className={`w-full text-left p-3 rounded-xl border-2 transition-all flex items-center justify-between text-xs sm:text-sm font-bold ${
                          isSelected
                            ? 'bg-black text-[#FEF08A] border-black shadow-neo-xs'
                            : 'bg-zinc-50 hover:bg-[#FEF08A]/30 border-black text-black'
                        }`}
                      >
                        <div className="flex items-center gap-3">
                          <span className={`w-6 h-6 rounded border border-black flex items-center justify-center font-mono font-bold text-xs ${
                            isSelected ? 'bg-[#FEF08A] text-black' : 'bg-white text-black'
                          }`}>
                            {opt.id}
                          </span>
                          <span>{opt.text}</span>
                        </div>
                      </button>
                    );
                  })}
                </div>
              )}

              {/* Progressive Hints Accordion */}
              {q.hints && q.hints.length > 0 && (
                <div className="mt-3">
                  <button
                    type="button"
                    onClick={() => toggleHint(q.id)}
                    className="text-xs font-bold text-zinc-700 hover:text-black flex items-center gap-1.5 underline"
                  >
                    <Lightbulb className="w-3.5 h-3.5 text-amber-500" />
                    <span>{showHint ? 'Hide Tutor Hint' : 'Request Progressive Hint'}</span>
                  </button>
                  {showHint && (
                    <div className="bg-[#FEF08A]/40 border border-black rounded-lg p-3 text-xs text-zinc-900 mt-2 font-medium">
                      💡 <strong>Tutor Clue:</strong> {q.hints[0]}
                    </div>
                  )}
                </div>
              )}

              {/* Post-submission result explanation */}
              {resultDetail && (
                <div className={`mt-4 p-3 rounded-xl border-2 text-xs font-medium ${
                  resultDetail.is_correct ? 'bg-emerald-50 border-emerald-600 text-emerald-900' : 'bg-rose-50 border-rose-600 text-rose-900'
                }`}>
                  <div className="font-bold mb-1">
                    {resultDetail.is_correct ? '✓ Correct Answer' : `✗ Incorrect (Correct was ${resultDetail.correct_answer})`}
                  </div>
                  <div>{resultDetail.explanation}</div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Submission CTA */}
      {!results && (
        <div className="bg-white border-3 border-black rounded-2xl p-6 shadow-neo-lg text-center">
          <button
            onClick={handleSubmit}
            disabled={submitting}
            className="bg-[#A78BFA] hover:bg-[#906cf8] text-black font-extrabold py-3.5 px-8 rounded-xl border-3 border-black shadow-neo hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-base inline-flex items-center gap-2"
          >
            <span>{submitting ? 'Evaluating Diagnostic...' : 'Submit Diagnostic Assessment'}</span>
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      )}
    </div>
  );
};
