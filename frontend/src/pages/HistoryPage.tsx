import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useLearner } from '../context/LearnerContext';
import { ActivityItem } from '../types';
import { History, Sparkles, Brain, Code, FolderKanban, Layers, Bot, Calendar } from 'lucide-react';

export const HistoryPage: React.FC = () => {
  const { activeScenarioId, showToast } = useLearner();
  const [history, setHistory] = useState<ActivityItem[]>([]);
  const [filter, setFilter] = useState<string>('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        setLoading(true);
        const data = await api.getActivityHistory();
        setHistory(data);
      } catch (err: any) {
        showToast(err.message, 'error');
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, [activeScenarioId]);

  const filteredHistory = history.filter(item => {
    if (filter === 'all') return true;
    return item.activity_type === filter;
  });

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'assessment': return <Brain className="w-5 h-5 text-purple-700" />;
      case 'challenge': return <Code className="w-5 h-5 text-emerald-700" />;
      case 'project': return <FolderKanban className="w-5 h-5 text-blue-700" />;
      case 'smart_notes': return <Layers className="w-5 h-5 text-amber-700" />;
      default: return <Bot className="w-5 h-5 text-zinc-700" />;
    }
  };

  return (
    <div className="max-w-5xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="bg-white border-3 border-black rounded-2xl p-6 sm:p-8 shadow-neo-lg">
        <div className="inline-flex items-center gap-2 bg-[#DDD6FE] text-black text-xs font-mono font-bold px-3 py-1 rounded-full border border-black mb-3">
          <History className="w-3.5 h-3.5" />
          <span>Audit Trail & Activity Log</span>
        </div>
        <h1 className="text-3xl font-extrabold text-black">Learner Activity Timeline</h1>
        <p className="text-sm text-zinc-600 mt-1 max-w-2xl font-medium">
          Comprehensive chronological record of all evaluated assessments, coding submissions, capstone milestones, and study sessions.
        </p>
      </div>

      {/* Filter Tabs */}
      <div className="flex flex-wrap items-center gap-2">
        {['all', 'assessment', 'challenge', 'project'].map((tab) => (
          <button
            key={tab}
            onClick={() => setFilter(tab)}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold font-mono uppercase border-2 transition-all ${
              filter === tab
                ? 'bg-black text-[#FEF08A] border-black shadow-neo-xs'
                : 'bg-white hover:bg-zinc-100 border-black text-black'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Activity Timeline List */}
      <div className="space-y-4">
        {filteredHistory.length > 0 ? (
          filteredHistory.map((item) => (
            <div
              key={item.id}
              className="bg-white border-3 border-black rounded-2xl p-5 shadow-neo transition-all flex flex-wrap items-center justify-between gap-4"
            >
              <div className="flex items-center gap-3.5">
                <div className="w-10 h-10 rounded-xl bg-zinc-100 border-2 border-black flex items-center justify-center shadow-neo-xs shrink-0">
                  {getActivityIcon(item.activity_type)}
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-0.5">
                    <span className="text-[10px] font-mono font-bold bg-[#FEF08A] px-2 py-0.5 rounded border border-black uppercase">
                      {item.activity_type}
                    </span>
                    <span className="text-[11px] font-mono text-zinc-500">
                      {new Date(item.timestamp).toLocaleDateString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                  <h3 className="font-extrabold text-sm sm:text-base text-black">{item.title}</h3>
                  <p className="text-xs text-zinc-600 font-medium">{item.details}</p>
                </div>
              </div>

              {item.score !== undefined && item.score !== null && (
                <div className="text-xs font-mono font-black bg-zinc-50 border-2 border-black px-3 py-1.5 rounded-lg shadow-neo-xs">
                  Score: {item.score}%
                </div>
              )}
            </div>
          ))
        ) : (
          <div className="bg-white border-3 border-black rounded-2xl p-12 text-center shadow-neo">
            <History className="w-12 h-12 text-zinc-400 mx-auto mb-3" />
            <h3 className="text-lg font-extrabold text-black">No Activity Logged Yet</h3>
            <p className="text-xs text-zinc-600 mt-1">Complete a challenge or diagnostic assessment to start building your verified learning history.</p>
          </div>
        )}
      </div>
    </div>
  );
};
