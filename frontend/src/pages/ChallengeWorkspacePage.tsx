import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useLearner } from '../context/LearnerContext';
import { ChallengeSubmitResponse } from '../types';
import { Code, Play, Sparkles, Lightbulb, CheckCircle2, XCircle, ArrowRight, Bot, AlertTriangle } from 'lucide-react';

export const ChallengeWorkspacePage: React.FC = () => {
  const { activeScenarioId, showToast, refreshAll } = useLearner();
  const [challengeId, setChallengeId] = useState('ch-two-sum');
  const [challenge, setChallenge] = useState<any>(null);
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<ChallengeSubmitResponse | null>(null);
  const [tutorHint, setTutorHint] = useState<string | null>(null);

  const fetchChallenge = async (id: string) => {
    try {
      setResult(null);
      setTutorHint(null);
      const data = await api.getChallenge(id);
      setChallenge(data);
      setCode(data.starter_code || 'def solution():\n    pass');
    } catch (err: any) {
      showToast(err.message, 'error');
    }
  };

  useEffect(() => {
    // If active scenario is 4 or 7, default to their challenge
    if (activeScenarioId === '4') {
      setChallengeId('ch-recur-countdown');
      fetchChallenge('ch-recur-countdown');
    } else if (activeScenarioId === '5') {
      setChallengeId('ch-api-resilience');
      fetchChallenge('ch-api-resilience');
    } else {
      setChallengeId('ch-two-sum');
      fetchChallenge('ch-two-sum');
    }
  }, [activeScenarioId]);

  const handleRunCode = async () => {
    try {
      setRunning(true);
      const res = await api.submitChallenge(challengeId, code, language);
      setResult(res);
      await refreshAll();
      showToast(res.passed ? 'All test cases passed! Mastery upgraded.' : 'Test failed — review mistake analysis.', res.passed ? 'success' : 'warning');
    } catch (err: any) {
      showToast(err.message, 'error');
    } finally {
      setRunning(false);
    }
  };

  const handleAskTutorHint = async () => {
    try {
      const chat = await api.sendTutorChat(`Give me a hint, not the answer for challenge: ${challenge?.title}`);
      setTutorHint(chat.reply);
      showToast('AI Tutor provided a targeted hint!', 'info');
    } catch (err: any) {
      showToast(err.message, 'error');
    }
  };

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-6">
      {/* Workspace Header */}
      <div className="bg-white border-3 border-black rounded-2xl p-6 shadow-neo flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs font-mono font-bold bg-black text-[#FEF08A] px-2.5 py-0.5 rounded">
              Safe Sandboxed Runner
            </span>
            <span className="text-xs font-mono font-bold bg-[#DDD6FE] px-2 py-0.5 rounded border border-black">
              {challenge?.difficulty || 'intermediate'}
            </span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-black">
            {challenge?.title || 'Interactive Challenge Workspace'}
          </h1>
        </div>

        {/* Challenge Switcher Selector */}
        <div className="flex items-center gap-2">
          {['ch-two-sum', 'ch-recur-countdown', 'ch-api-resilience'].map((cid) => (
            <button
              key={cid}
              onClick={() => {
                setChallengeId(cid);
                fetchChallenge(cid);
              }}
              className={`text-xs font-bold font-mono px-3 py-1.5 rounded-lg border-2 transition-all ${
                challengeId === cid
                  ? 'bg-[#FEF08A] border-black shadow-neo-xs text-black'
                  : 'bg-zinc-50 border-black hover:bg-zinc-100 text-zinc-700'
              }`}
            >
              {cid.replace('ch-', '')}
            </button>
          ))}
        </div>
      </div>

      {/* Split Workspace */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Challenge Brief & Test Cases */}
        <div className="lg:col-span-5 space-y-6">
          <div className="bg-white border-3 border-black rounded-2xl p-6 shadow-neo space-y-4">
            <h2 className="text-lg font-extrabold text-black">Problem Brief</h2>
            <p className="text-xs sm:text-sm text-zinc-700 font-medium leading-relaxed">
              {challenge?.description}
            </p>

            <div className="border-t-2 border-black pt-4">
              <h3 className="text-xs font-mono font-bold text-zinc-500 uppercase mb-2">Expected Test Assertions</h3>
              <div className="space-y-2">
                {challenge?.test_cases?.map((tc: any, i: number) => (
                  <div key={i} className="bg-zinc-50 border border-black rounded-lg p-2.5 text-xs font-mono">
                    <div className="text-zinc-600">Input: <strong className="text-black">{tc.input}</strong></div>
                    <div className="text-zinc-600">Expected: <strong className="text-emerald-700">{tc.expected}</strong></div>
                  </div>
                ))}
              </div>
            </div>

            <button
              onClick={handleAskTutorHint}
              className="w-full bg-white hover:bg-[#FEF08A] border-2 border-black rounded-xl p-2.5 text-xs font-bold shadow-neo-xs flex items-center justify-center gap-2 transition-all"
            >
              <Lightbulb className="w-4 h-4 text-amber-500" />
              <span>Ask AI Tutor for a Clue</span>
            </button>

            {tutorHint && (
              <div className="bg-[#FAF7F2] border-2 border-black rounded-xl p-3 text-xs text-zinc-900 leading-relaxed font-medium">
                {tutorHint}
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Code Editor & Execution Output */}
        <div className="lg:col-span-7 space-y-6">
          <div className="bg-zinc-900 border-3 border-black rounded-2xl p-5 shadow-neo text-white space-y-4">
            <div className="flex items-center justify-between border-b border-zinc-700 pb-3">
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-rose-500 border border-black"></span>
                <span className="w-3 h-3 rounded-full bg-amber-400 border border-black"></span>
                <span className="w-3 h-3 rounded-full bg-emerald-500 border border-black"></span>
                <span className="text-xs font-mono font-bold ml-2 text-zinc-400">solution.py</span>
              </div>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="bg-zinc-800 text-xs font-mono font-bold text-white px-2 py-1 rounded border border-zinc-700 focus:outline-none"
              >
                <option value="python">Python 3.12</option>
                <option value="javascript">JavaScript / TypeScript</option>
              </select>
            </div>

            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              rows={12}
              className="w-full bg-zinc-950 text-emerald-400 font-mono text-xs sm:text-sm p-4 rounded-xl border border-zinc-800 focus:outline-none focus:ring-1 focus:ring-purple-400 resize-y leading-relaxed"
              spellCheck={false}
            />

            <div className="flex items-center justify-between pt-2">
              <span className="text-[11px] font-mono text-zinc-400">
                Sandboxed evaluation • AST syntax validation
              </span>
              <button
                onClick={handleRunCode}
                disabled={running}
                className="bg-[#FEF08A] hover:bg-[#fde047] text-black font-extrabold px-6 py-2.5 rounded-xl border-2 border-black shadow-neo-sm hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-xs flex items-center gap-2"
              >
                <Play className="w-4 h-4 fill-black" />
                <span>{running ? 'Executing Tests...' : 'Run in Isolated Runner'}</span>
              </button>
            </div>
          </div>

          {/* Execution & Adaptation Results */}
          {result && (
            <div className={`border-3 border-black rounded-2xl p-6 shadow-neo ${
              result.passed ? 'bg-[#A7F3D0]' : 'bg-[#FECDD3]'
            }`}>
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  {result.passed ? (
                    <CheckCircle2 className="w-6 h-6 text-emerald-950" />
                  ) : (
                    <XCircle className="w-6 h-6 text-rose-950" />
                  )}
                  <h3 className="text-xl font-extrabold text-black">
                    {result.passed ? `All Tests Passed (${result.score}%)` : `Assertion Failure (${result.score}%)`}
                  </h3>
                </div>
                <span className="text-xs font-mono font-bold bg-black text-white px-2.5 py-1 rounded">
                  Score: {result.score}/100
                </span>
              </div>

              {/* Mistake analysis */}
              {result.mistake_analysis && (
                <div className="bg-white/90 border border-black rounded-xl p-3.5 mb-3 text-xs font-medium text-rose-950">
                  <strong>Mistake Breakdown:</strong> {result.mistake_analysis}
                </div>
              )}

              {/* AI Explanation */}
              <div className="bg-white/90 border border-black rounded-xl p-3.5 mb-3 text-xs font-medium text-zinc-900 leading-relaxed">
                <strong>Tutor Explanation:</strong> {result.ai_explanation}
              </div>

              {/* Adaptation Rule Applied */}
              <div className="bg-black text-[#FEF08A] font-mono text-xs p-3 rounded-xl border border-black mb-3">
                <strong>Adaptation Rule:</strong> {result.adaptation_rule_applied}
              </div>

              {/* Test Cases Results Table */}
              <div className="space-y-1.5">
                <div className="text-[11px] font-mono font-bold uppercase text-zinc-800">Test Case Execution Log:</div>
                {result.test_results?.map((tr, idx) => (
                  <div key={idx} className="bg-white border border-black rounded-lg p-2 text-xs flex items-center justify-between font-mono">
                    <span className="truncate pr-2">{tr.input}</span>
                    <span className={`px-2 py-0.5 rounded font-bold text-[10px] ${
                      tr.passed ? 'bg-emerald-200 text-emerald-900' : 'bg-rose-200 text-rose-900'
                    }`}>
                      {tr.passed ? 'PASSED' : 'FAILED'}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
