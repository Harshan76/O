import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useLearner } from '../context/LearnerContext';
import { SkillProfileResponse, SkillItem } from '../types';
import { MapPin, Sparkles, CheckCircle2, AlertTriangle, HelpCircle, ArrowRight, Layers } from 'lucide-react';

export const SkillGapPage: React.FC = () => {
  const { activeScenarioId, showToast } = useLearner();
  const [profile, setProfile] = useState<SkillProfileResponse | null>(null);
  const [filter, setFilter] = useState<'all' | 'strong' | 'weak' | 'missing_prereq' | 'validating'>('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        setLoading(true);
        const data = await api.getSkillProfile();
        setProfile(data);
      } catch (err: any) {
        showToast(err.message, 'error');
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, [activeScenarioId]);

  const filteredSkills = profile?.skills?.filter(s => {
    if (filter === 'all') return true;
    return s.status === filter;
  }) || [];

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-8">
      {/* Header */}
      <div className="bg-white border-3 border-black rounded-2xl p-6 sm:p-8 shadow-neo-lg">
        <div className="inline-flex items-center gap-2 bg-[#DDD6FE] text-black text-xs font-mono font-bold px-3 py-1 rounded-full border border-black mb-3">
          <MapPin className="w-3.5 h-3.5" />
          <span>Diagnostic Skill Matrix</span>
        </div>
        <h1 className="text-3xl font-extrabold text-black">Visual Skill-Gap Map</h1>
        <p className="text-sm text-zinc-600 mt-1 max-w-2xl font-medium">
          Comprehensive diagnostic visualization mapping verified competencies against missing prerequisites and active growth areas.
        </p>
      </div>

      {/* Overview Stat Counters */}
      {profile && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div className="bg-white border-2 border-black rounded-xl p-4 shadow-neo-sm">
            <div className="text-xs font-mono font-bold text-zinc-500 uppercase">Overall Mastery</div>
            <div className="text-2xl font-extrabold text-black mt-1">{profile.overall_mastery}%</div>
          </div>
          <div className="bg-[#A7F3D0] border-2 border-black rounded-xl p-4 shadow-neo-sm">
            <div className="text-xs font-mono font-bold text-emerald-900 uppercase">Strong Skills</div>
            <div className="text-2xl font-extrabold text-black mt-1">{profile.strong_count}</div>
          </div>
          <div className="bg-[#FECDD3] border-2 border-black rounded-xl p-4 shadow-neo-sm">
            <div className="text-xs font-mono font-bold text-rose-900 uppercase">Weak Skills</div>
            <div className="text-2xl font-extrabold text-black mt-1">{profile.weak_count}</div>
          </div>
          <div className="bg-[#FED7AA] border-2 border-black rounded-xl p-4 shadow-neo-sm">
            <div className="text-xs font-mono font-bold text-amber-900 uppercase">Missing Prereqs</div>
            <div className="text-2xl font-extrabold text-black mt-1">{profile.missing_prereqs_count}</div>
          </div>
          <div className="bg-[#DDD6FE] border-2 border-black rounded-xl p-4 shadow-neo-sm">
            <div className="text-xs font-mono font-bold text-purple-900 uppercase">Validating</div>
            <div className="text-2xl font-extrabold text-black mt-1">{profile.validating_count}</div>
          </div>
        </div>
      )}

      {/* Filter Tabs */}
      <div className="flex flex-wrap items-center gap-2">
        {[
          { id: 'all', label: `All Skills (${profile?.total_skills_mapped || 0})` },
          { id: 'strong', label: `Strong (${profile?.strong_count || 0})` },
          { id: 'weak', label: `Weak (${profile?.weak_count || 0})` },
          { id: 'missing_prereq', label: `Missing Prereqs (${profile?.missing_prereqs_count || 0})` },
          { id: 'validating', label: `Validating (${profile?.validating_count || 0})` },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setFilter(tab.id as any)}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold border-2 transition-all ${
              filter === tab.id
                ? 'bg-black text-[#FEF08A] border-black shadow-neo-xs'
                : 'bg-white hover:bg-zinc-100 border-black text-black'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Skills Matrix Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredSkills.map((s) => {
          const isStrong = s.status === 'strong';
          const isWeak = s.status === 'weak';
          const isPrereqMissing = s.status === 'missing_prereq';

          return (
            <div
              key={s.code}
              className={`border-3 border-black rounded-2xl p-5 shadow-neo transition-all flex flex-col justify-between ${
                isStrong ? 'bg-white' : isWeak ? 'bg-rose-50/50' : isPrereqMissing ? 'bg-amber-50/50' : 'bg-purple-50/40'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="font-mono text-xs font-bold text-zinc-600 bg-white px-2 py-0.5 rounded border border-black">
                    {s.code}
                  </span>
                  <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded border border-black uppercase ${
                    isStrong ? 'bg-[#A7F3D0] text-emerald-900' : isWeak ? 'bg-[#FECDD3] text-rose-900' : isPrereqMissing ? 'bg-[#FED7AA] text-amber-900' : 'bg-[#DDD6FE] text-purple-900'
                  }`}>
                    {s.status.replace('_', ' ')}
                  </span>
                </div>

                <h3 className="text-base font-extrabold text-black mb-1">{s.name}</h3>
                <p className="text-xs text-zinc-600 font-medium mb-3">{s.description}</p>

                {/* Prerequisites list */}
                {s.prerequisites && s.prerequisites.length > 0 && (
                  <div className="text-[11px] font-mono text-zinc-500 mb-2">
                    Prerequisites: <strong>{s.prerequisites.join(', ')}</strong>
                  </div>
                )}
              </div>

              <div className="pt-3 border-t border-black/20 space-y-2">
                <div className="flex items-center justify-between text-xs font-bold font-mono">
                  <span>Score:</span>
                  <span className="text-sm font-extrabold">{s.score}%</span>
                </div>
                <div className="w-full bg-zinc-200 border border-black rounded-full h-2 overflow-hidden">
                  <div
                    className={`h-full ${isStrong ? 'bg-emerald-500' : isWeak ? 'bg-rose-500' : 'bg-amber-500'}`}
                    style={{ width: `${s.score}%` }}
                  ></div>
                </div>
                <div className="bg-white border border-black rounded-lg p-2 text-[11px] text-zinc-800 font-medium">
                  <strong>Action:</strong> {s.recommended_action}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Formula Explainer Card */}
      {profile?.calculation_breakdown && (
        <div className="bg-[#FAF7F2] border-3 border-black rounded-2xl p-6 shadow-neo space-y-2">
          <div className="text-xs font-mono font-bold uppercase text-zinc-500">Deterministic Adaptation Rules & Formula</div>
          <div className="font-mono text-xs bg-white border border-black p-3 rounded-lg text-black font-bold">
            {profile.calculation_breakdown.formula}
          </div>
          <div className="text-xs text-zinc-600 font-medium pt-1">
            <strong>Verification Standard:</strong> {profile.calculation_breakdown.verification_threshold}
          </div>
        </div>
      )}
    </div>
  );
};
