import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLearner } from '../context/LearnerContext';
import { api } from '../services/api';
import { Sparkles, ArrowRight, Lock, Mail, User, ShieldCheck } from 'lucide-react';

export const AuthPage: React.FC = () => {
  const navigate = useNavigate();
  const { refreshAll, showToast } = useLearner();
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) {
      showToast('Please enter your email', 'error');
      return;
    }

    try {
      setLoading(true);
      await api.login(email, fullName || 'Learner');
      await refreshAll();
      showToast(isRegister ? 'Learner account created!' : 'Logged in successfully!', 'success');
      navigate(isRegister ? '/onboarding' : '/dashboard');
    } catch (err: any) {
      showToast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickDemo = async (demoEmail: string, demoName: string) => {
    try {
      setLoading(true);
      await api.login(demoEmail, demoName);
      await refreshAll();
      showToast(`Logged in as simulated learner: ${demoName}`, 'success');
      navigate('/dashboard');
    } catch (err: any) {
      showToast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto py-12 px-4">
      <div className="bg-white border-3 border-black rounded-2xl p-6 sm:p-8 shadow-neo-lg">
        {/* Header */}
        <div className="text-center mb-6">
          <div className="w-12 h-12 bg-[#DDD6FE] border-2 border-black rounded-xl shadow-neo-sm mx-auto flex items-center justify-center mb-3">
            <Sparkles className="w-6 h-6 text-black fill-yellow-300" />
          </div>
          <h1 className="text-2xl font-extrabold text-black">
            {isRegister ? 'Create Learner Account' : 'Welcome Back, Learner'}
          </h1>
          <p className="text-xs text-zinc-600 mt-1 font-medium">
            Strict learner-only platform. No teachers, no classrooms.
          </p>
        </div>

        {/* Tab Toggle */}
        <div className="grid grid-cols-2 gap-2 p-1 bg-[#FAF7F2] border-2 border-black rounded-lg mb-6">
          <button
            type="button"
            onClick={() => setIsRegister(false)}
            className={`py-1.5 text-xs font-bold rounded ${
              !isRegister ? 'bg-black text-[#FEF08A] shadow-neo-xs' : 'text-zinc-600 hover:text-black'
            }`}
          >
            Learner Login
          </button>
          <button
            type="button"
            onClick={() => setIsRegister(true)}
            className={`py-1.5 text-xs font-bold rounded ${
              isRegister ? 'bg-black text-[#FEF08A] shadow-neo-xs' : 'text-zinc-600 hover:text-black'
            }`}
          >
            Register
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {isRegister && (
            <div>
              <label className="block text-xs font-bold text-black mb-1">Full Name</label>
              <div className="relative">
                <User className="w-4 h-4 text-zinc-400 absolute left-3 top-3" />
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="Alex Mercer"
                  className="w-full pl-9 pr-3 py-2 border-2 border-black rounded-lg text-sm bg-white focus:outline-none focus:bg-[#FEF08A]/20"
                />
              </div>
            </div>
          )}

          <div>
            <label className="block text-xs font-bold text-black mb-1">Learner Email</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-zinc-400 absolute left-3 top-3" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="learner@skillforge.ai"
                className="w-full pl-9 pr-3 py-2 border-2 border-black rounded-lg text-sm bg-white focus:outline-none focus:bg-[#FEF08A]/20"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-black mb-1">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-zinc-400 absolute left-3 top-3" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••••••"
                className="w-full pl-9 pr-3 py-2 border-2 border-black rounded-lg text-sm bg-white focus:outline-none focus:bg-[#FEF08A]/20"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#FEF08A] hover:bg-[#fde047] text-black font-extrabold py-2.5 px-4 rounded-lg border-2 border-black shadow-neo hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-sm flex items-center justify-center gap-2 mt-2"
          >
            <span>{loading ? 'Processing...' : (isRegister ? 'Complete Registration' : 'Log In as Learner')}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        {/* Quick Demo Logins for Judges */}
        <div className="mt-8 pt-6 border-t-2 border-dashed border-zinc-300">
          <div className="text-[11px] font-mono font-bold text-zinc-500 uppercase tracking-wider mb-2 text-center">
            One-Click Simulated Learner Logins
          </div>
          <div className="space-y-1.5">
            <button
              onClick={() => handleQuickDemo('maya@demo.skillforge.ai', 'Maya Chen')}
              className="w-full text-left p-2 rounded border border-black bg-zinc-50 hover:bg-[#DDD6FE] text-xs font-bold flex items-center justify-between transition-all"
            >
              <span>Maya Chen (Beginner • Python)</span>
              <span className="text-[10px] font-mono bg-black text-white px-1.5 py-0.5 rounded">Scenario #1</span>
            </button>
            <button
              onClick={() => handleQuickDemo('jordan@demo.skillforge.ai', 'Jordan Lee')}
              className="w-full text-left p-2 rounded border border-black bg-zinc-50 hover:bg-[#FECDD3] text-xs font-bold flex items-center justify-between transition-all"
            >
              <span>Jordan Lee (Intermediate • React)</span>
              <span className="text-[10px] font-mono bg-black text-white px-1.5 py-0.5 rounded">Scenario #2</span>
            </button>
            <button
              onClick={() => handleQuickDemo('elena@demo.skillforge.ai', 'Elena Rostova')}
              className="w-full text-left p-2 rounded border border-black bg-zinc-50 hover:bg-[#A7F3D0] text-xs font-bold flex items-center justify-between transition-all"
            >
              <span>Elena Rostova (Advanced • AI Capstone)</span>
              <span className="text-[10px] font-mono bg-black text-white px-1.5 py-0.5 rounded">Scenario #3</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
