import React, { useState, useEffect, useRef } from 'react';
import { api } from '../services/api';
import { useLearner } from '../context/LearnerContext';
import { ChatMessage } from '../types';
import { Bot, Send, Sparkles, Lightbulb, HelpCircle, CheckCircle2, User, RefreshCw } from 'lucide-react';

export const TutorChatPage: React.FC = () => {
  const { learner, activeScenarioId, showToast } = useLearner();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const suggestedPills = [
    "Explain this concept simply",
    "Give me a real-world example",
    "Test my understanding",
    "Give me a hint, not the answer",
    "Explain my mistake",
    "Give me a harder challenge"
  ];

  const fetchHistory = async () => {
    try {
      const history = await api.getTutorHistory();
      setMessages(history);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [activeScenarioId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (textToSend?: string) => {
    const text = (textToSend || inputText).trim();
    if (!text || sending) return;

    const userMsg: ChatMessage = {
      id: `usr-${Date.now()}`,
      sender: 'learner',
      text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    setInputText('');
    setSending(true);

    try {
      const res = await api.sendTutorChat(text);
      const botMsg: ChatMessage = {
        id: `bot-${Date.now()}`,
        sender: 'tutor',
        text: res.reply,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        suggested_followups: res.suggested_followups
      };
      setMessages(prev => [...prev, botMsg]);
    } catch (err: any) {
      showToast(err.message, 'error');
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto py-8 px-4 sm:px-6 h-[calc(100vh-140px)] flex flex-col space-y-4">
      {/* Tutor Header */}
      <div className="bg-white border-3 border-black rounded-2xl p-4 sm:p-5 shadow-neo-sm flex items-center justify-between shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-[#DDD6FE] border-2 border-black flex items-center justify-center shadow-neo-xs">
            <Bot className="w-6 h-6 text-black" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-extrabold text-base sm:text-lg text-black">SkillForge AI Personal Tutor</h1>
              <span className="text-[10px] font-mono font-bold bg-[#A7F3D0] text-emerald-950 px-2 py-0.5 rounded border border-black">
                Active & Grounded
              </span>
            </div>
            <p className="text-xs text-zinc-600 font-medium">
              Teaching {learner?.full_name || 'Learner'} ({learner?.experience_level || 'beginner'} tier) • Progressive hints enabled
            </p>
          </div>
        </div>

        <button
          onClick={fetchHistory}
          className="bg-zinc-50 hover:bg-zinc-100 p-2 border-2 border-black rounded-lg shadow-neo-xs"
          title="Reload conversation"
        >
          <RefreshCw className="w-4 h-4 text-black" />
        </button>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 bg-white border-3 border-black rounded-2xl p-4 sm:p-6 shadow-neo overflow-y-auto space-y-4">
        {messages.map((m) => {
          const isTutor = m.sender === 'tutor';
          return (
            <div
              key={m.id}
              className={`flex items-start gap-3 ${isTutor ? 'justify-start' : 'justify-end'}`}
            >
              {isTutor && (
                <div className="w-8 h-8 rounded-lg bg-[#DDD6FE] border-2 border-black flex items-center justify-center shadow-neo-xs shrink-0 mt-1">
                  <Bot className="w-4 h-4 text-black" />
                </div>
              )}

              <div className={`max-w-[85%] sm:max-w-[75%] rounded-2xl p-4 border-2 border-black shadow-neo-xs text-xs sm:text-sm font-medium ${
                isTutor ? 'bg-[#FAF7F2] text-zinc-900' : 'bg-black text-[#FEF08A]'
              }`}>
                <div className="whitespace-pre-wrap leading-relaxed">
                  {m.text}
                </div>

                <div className="mt-2 text-[10px] font-mono opacity-60 text-right">
                  {m.timestamp}
                </div>

                {/* Suggested follow-up buttons if provided */}
                {isTutor && m.suggested_followups && m.suggested_followups.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-zinc-300 flex flex-wrap gap-1.5">
                    {m.suggested_followups.map((pill, i) => (
                      <button
                        key={i}
                        onClick={() => handleSend(pill)}
                        className="bg-white hover:bg-[#FEF08A] text-black text-[11px] font-bold px-2.5 py-1 rounded-md border border-black transition-all shadow-neo-xs"
                      >
                        {pill}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {!isTutor && (
                <div className="w-8 h-8 rounded-lg bg-[#FECDD3] border-2 border-black flex items-center justify-center shadow-neo-xs shrink-0 mt-1 font-bold text-xs">
                  {learner?.full_name ? learner.full_name[0] : 'L'}
                </div>
              )}
            </div>
          );
        })}
        {sending && (
          <div className="flex items-center gap-2 text-xs font-mono font-bold text-zinc-500 bg-zinc-100 p-3 rounded-xl border border-black inline-block">
            <Sparkles className="w-4 h-4 text-purple-600 animate-spin" />
            <span>AI Tutor formulating pedagogical response...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Prompt Pills Bar */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 shrink-0">
        <span className="text-[11px] font-mono font-bold text-zinc-500 shrink-0">Prompts:</span>
        {suggestedPills.map((pill) => (
          <button
            key={pill}
            onClick={() => handleSend(pill)}
            className="bg-white hover:bg-[#FEF08A] text-black text-xs font-bold px-3 py-1.5 rounded-lg border-2 border-black shadow-neo-xs shrink-0 transition-all"
          >
            {pill}
          </button>
        ))}
      </div>

      {/* Input Box */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="flex items-center gap-2 shrink-0"
      >
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Ask your tutor a question, paste an error snippet, or ask for a progressive hint..."
          className="flex-1 px-4 py-3 border-3 border-black rounded-xl text-sm font-semibold bg-white shadow-neo-sm focus:outline-none focus:ring-2 focus:ring-purple-400"
        />
        <button
          type="submit"
          disabled={sending || !inputText.trim()}
          className="bg-[#A78BFA] hover:bg-[#906cf8] text-black font-extrabold px-6 py-3 rounded-xl border-3 border-black shadow-neo hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-sm flex items-center gap-2"
        >
          <span>Send</span>
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
};
