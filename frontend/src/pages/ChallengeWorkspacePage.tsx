import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useLearner } from '../context/LearnerContext';
import { ChallengeSubmitResponse } from '../types';
import { Code, Play, Sparkles, Lightbulb, CheckCircle2, XCircle, ArrowRight, Bot, AlertTriangle, RefreshCw } from 'lucide-react';

export const ChallengeWorkspacePage: React.FC = () => {
  const { activeScenarioId, showToast, refreshAll } = useLearner();
  const [challengeId, setChallengeId] = useState('ch-two-sum');
  const [challenge, setChallenge] = useState<any>(null);
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<ChallengeSubmitResponse | null>(null);
  const [tutorHint, setTutorHint] = useState<string | null>(null);
  const [validationWarning, setValidationWarning] = useState<string | null>(null);

  const fetchChallenge = async (id: string) => {
    try {
      setResult(null);
      setValidationWarning(null);
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
    const trimmedCode = code.trim();
    const starterTrimmed = challenge?.starter_code?.trim() || '';

    // 1. Validate that the code editor is not empty
    if (!trimmedCode) {
      const msg = 'Write your solution and click Run to evaluate your code.';
      setValidationWarning(msg);
      showToast(msg, 'warning');
      return;
    }

    // 2. Validate that the code is not still the unchanged starter placeholder
    const isStarterCode = trimmedCode === starterTrimmed;
    const isOnlyPass = language === 'python' && (
      trimmedCode.split('\n')
        .map(line => line.split('#')[0].trim())
        .filter(Boolean)
        .every(line => line.startsWith('def ') || line === 'pass')
    );

    if (isStarterCode || isOnlyPass) {
      const msg = 'Your code editor still contains only the starter placeholder. Write your solution before running tests.';
      setValidationWarning(msg);
      showToast(msg, 'warning');
      return;
    }

    setValidationWarning(null);

    try {
      setRunning(true);
      const res = await api.submitChallenge(challengeId, code, language);
      setResult(res);
      await refreshAll();

      const totalTests = res.test_results?.length || 0;
      const passedTests = res.test_results?.filter(t => t.passed).length || 0;
      const isAllPassed = res.passed && totalTests > 0 && passedTests === totalTests && res.score === 100;

      if (isAllPassed) {
        showToast('All test cases passed! Mastery upgraded.', 'success');
      } else {
        showToast(`Test execution complete: ${passedTests}/${totalTests} passed (${res.score}%). Review feedback.`, 'warning');
      }
    } catch (err: any) {
      showToast(err.message || 'Execution error during test evaluation', 'error');
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

  const handleResetToStarter = () => {
    if (challenge?.starter_code) {
      setCode(challenge.starter_code);
      setResult(null);
      setValidationWarning(null);
      showToast('Code reset to starter template.', 'info');
    }
  };

  // Derive stats strictly from actual test results
  const totalTests = result?.test_results?.length || 0;
  const passedTests = result?.test_results?.filter(t => t.passed).length || 0;
  const isAllPassed = Boolean(result?.passed && totalTests > 0 && passedTests === totalTests && result?.score === 100);

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
          {/* Editor Container */}
          <div className="bg-zinc-900 border-3 border-black rounded-2xl p-5 shadow-neo text-white space-y-4">
            <div className="flex items-center justify-between border-b border-zinc-700 pb-3">
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-rose-500 border border-black"></span>
                <span className="w-3 h-3 rounded-full bg-amber-400 border border-black"></span>
                <span className="w-3 h-3 rounded-full bg-emerald-500 border border-black"></span>
                <span className="text-xs font-mono font-bold ml-2 text-zinc-400">solution.{language === 'python' ? 'py' : 'ts'}</span>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={handleResetToStarter}
                  title="Reset to starter code"
                  className="text-zinc-400 hover:text-white transition-colors p-1"
                >
                  <RefreshCw className="w-3.5 h-3.5" />
                </button>
                <select
                  value={language}
                  onChange={(e) => {
                    setLanguage(e.target.value);
                    setResult(null);
                    setValidationWarning(null);
                  }}
                  className="bg-zinc-800 text-xs font-mono font-bold text-white px-2 py-1 rounded border border-zinc-700 focus:outline-none"
                >
                  <option value="python">Python 3.12</option>
                  <option value="javascript">JavaScript / TypeScript</option>
                </select>
              </div>
            </div>

            <textarea
              value={code}
              onChange={(e) => {
                setCode(e.target.value);
                if (result) setResult(null);
                if (validationWarning) setValidationWarning(null);
              }}
              rows={12}
              className="w-full bg-zinc-950 text-emerald-400 font-mono text-xs sm:text-sm p-4 rounded-xl border border-zinc-800 focus:outline-none focus:ring-1 focus:ring-purple-400 resize-y leading-relaxed"
              spellCheck={false}
              placeholder="# Write your solution here"
            />

            <div className="flex items-center justify-between pt-2">
              <span className="text-[11px] font-mono text-zinc-400">
                Sandboxed evaluation • AST syntax validation
              </span>
              <button
                onClick={handleRunCode}
                disabled={running}
                className="bg-[#FEF08A] hover:bg-[#fde047] disabled:opacity-50 disabled:cursor-not-allowed text-black font-extrabold px-6 py-2.5 rounded-xl border-2 border-black shadow-neo-sm hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-xs flex items-center gap-2"
              >
                <Play className="w-4 h-4 fill-black" />
                <span>{running ? 'Executing Tests...' : 'Run in Isolated Runner'}</span>
              </button>
            </div>
          </div>

          {/* Validation Warning Alert */}
          {validationWarning && (
            <div className="bg-[#FEF08A] border-3 border-black rounded-2xl p-4 shadow-neo flex items-start gap-3">
              <AlertTriangle className="w-5 h-5 text-black shrink-0 mt-0.5" />
              <div>
                <h4 className="text-xs font-bold font-mono uppercase text-black">Action Required</h4>
                <p className="text-xs text-zinc-900 font-medium mt-0.5">{validationWarning}</p>
              </div>
            </div>
          )}

          {/* Loading State */}
          {running && (
            <div className="bg-white border-3 border-black rounded-2xl p-8 shadow-neo text-center space-y-3">
              <div className="w-12 h-12 rounded-xl bg-[#DDD6FE] border-2 border-black flex items-center justify-center mx-auto animate-pulse">
                <Play className="w-6 h-6 fill-black text-black ml-0.5" />
              </div>
              <h3 className="text-base font-extrabold text-black">Executing Tests in Isolated Runner...</h3>
              <p className="text-xs sm:text-sm text-zinc-600 font-medium">
                Running AST syntax analysis and testing assertions against your code.
              </p>
            </div>
          )}

          {/* Neutral Empty State: Before code execution */}
          {!running && !result && !validationWarning && (
            <div className="bg-white border-3 border-black rounded-2xl p-8 shadow-neo text-center space-y-3">
              <div className="w-12 h-12 rounded-xl bg-zinc-100 border-2 border-black flex items-center justify-center mx-auto text-zinc-700">
                <Code className="w-6 h-6" />
              </div>
              <h3 className="text-base font-extrabold text-black">Awaiting Code Execution</h3>
              <p className="text-xs sm:text-sm text-zinc-600 font-medium max-w-sm mx-auto">
                Write your solution and click Run to evaluate your code.
              </p>
              <div className="pt-2">
                <span className="text-[11px] font-mono font-bold bg-zinc-100 text-zinc-600 px-3 py-1 rounded-lg border border-zinc-300">
                  Runner Status: Ready
                </span>
              </div>
            </div>
          )}

          {/* Execution & Adaptation Results: Only rendered after actual evaluation */}
          {!running && result && (
            <div className={`border-3 border-black rounded-2xl p-6 shadow-neo ${
              isAllPassed ? 'bg-[#A7F3D0]' : (passedTests > 0 ? 'bg-[#FEF08A]' : 'bg-[#FECDD3]')
            }`}>
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  {isAllPassed ? (
                    <CheckCircle2 className="w-6 h-6 text-emerald-950" />
                  ) : (
                    <XCircle className="w-6 h-6 text-rose-950" />
                  )}
                  <h3 className="text-xl font-extrabold text-black">
                    {isAllPassed
                      ? 'All Tests Passed (100%)'
                      : (passedTests > 0
                        ? `Tests Incomplete (${passedTests}/${totalTests} Passed - ${result.score}%)`
                        : `Assertion Failure (0/${totalTests} Passed - ${result.score}%)`)}
                  </h3>
                </div>
                <span className="text-xs font-mono font-bold bg-black text-white px-2.5 py-1 rounded">
                  Score: {result.score}/100
                </span>
              </div>

              {/* Mistake analysis (only when tests fail or errors occur) */}
              {result.mistake_analysis && (
                <div className="bg-white/90 border border-black rounded-xl p-3.5 mb-3 text-xs font-medium text-rose-950">
                  <strong>Mistake Breakdown:</strong> {result.mistake_analysis}
                </div>
              )}

              {/* AI Explanation */}
              {result.ai_explanation && (
                <div className="bg-white/90 border border-black rounded-xl p-3.5 mb-3 text-xs font-medium text-zinc-900 leading-relaxed">
                  <strong>Tutor Explanation:</strong> {result.ai_explanation}
                </div>
              )}

              {/* Adaptation Rule Applied */}
              {result.adaptation_rule_applied && (
                <div className="bg-black text-[#FEF08A] font-mono text-xs p-3 rounded-xl border border-black mb-3">
                  <strong>Adaptation Rule:</strong> {result.adaptation_rule_applied}
                </div>
              )}

              {/* Test Cases Results Table */}
              <div className="space-y-1.5">
                <div className="text-[11px] font-mono font-bold uppercase text-zinc-800">
                  Test Case Execution Log ({passedTests}/{totalTests} passed):
                </div>
                {result.test_results?.map((tr, idx) => (
                  <div key={idx} className="bg-white border border-black rounded-lg p-2.5 text-xs flex flex-col gap-1 font-mono">
                    <div className="flex items-center justify-between">
                      <span className="truncate pr-2 font-bold text-black">{tr.input}</span>
                      <span className={`px-2 py-0.5 rounded font-bold text-[10px] ${
                        tr.passed ? 'bg-emerald-200 text-emerald-900' : 'bg-rose-200 text-rose-900'
                      }`}>
                        {tr.passed ? 'PASSED' : 'FAILED'}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-[11px] text-zinc-500">
                      <span>Expected: <span className="text-emerald-700 font-bold">{tr.expected}</span></span>
                      {tr.actual && <span>Actual: <span className={tr.passed ? "text-emerald-700" : "text-rose-700 font-bold"}>{tr.actual}</span></span>}
                    </div>
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
