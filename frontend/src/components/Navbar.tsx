import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useLearner } from '../context/LearnerContext';
import { 
  Sparkles, Compass, BookOpen, Brain, 
  MapPin, Bot, Code, Layers, FolderKanban, 
  BarChart3, History, Settings, Menu, X, ChevronDown, CheckCircle, GraduationCap
} from 'lucide-react';

export const Navbar: React.FC = () => {
  const { learner, activeScenarioId, scenarios, switchScenario, progress } = useLearner();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [scenarioDropdownOpen, setScenarioDropdownOpen] = useState(false);

  const navLinks = [
    { to: '/dashboard', label: 'Dashboard', icon: Compass },
    { to: '/goals-courses', label: 'Goals & Courses', icon: BookOpen },
    { to: '/courses/c-python/learn', label: 'Learning Hub', icon: GraduationCap },
    { to: '/smart-notes', label: 'Smart Notes', icon: Layers },
    { to: '/diagnostic', label: 'Diagnostic', icon: Brain },
    { to: '/skill-gap', label: 'Skill Gap', icon: MapPin },
    { to: '/roadmap', label: 'Roadmap', icon: Sparkles },
    { to: '/tutor', label: 'AI Tutor', icon: Bot },
    { to: '/challenges', label: 'Challenges', icon: Code },
    { to: '/revision', label: 'Revision', icon: Layers },
    { to: '/projects', label: 'Projects', icon: FolderKanban },
    { to: '/analytics', label: 'Mastery', icon: BarChart3 },
    { to: '/history', label: 'History', icon: History },
    { to: '/settings', label: 'Settings', icon: Settings },
  ];

  const currentScenario = scenarios.find(s => s.id === activeScenarioId);

  return (
    <header className="sticky top-0 z-50 bg-[#FAF7F2] border-b-2 border-black">
      {/* Top Banner for Simulated Demo Scenarios */}
      <div className="bg-[#FEF08A] border-b-2 border-black px-4 py-1.5 text-xs font-mono font-bold flex flex-wrap items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="bg-black text-[#FEF08A] px-1.5 py-0.5 rounded border border-black uppercase tracking-wider text-[10px]">
            Simulated Demo
          </span>
          <span className="text-zinc-800 truncate">
            {currentScenario ? `Scenario ${currentScenario.id}: ${currentScenario.title} (${currentScenario.learner_name})` : 'SkillForge AI Demo Mode'}
          </span>
        </div>
        <div className="flex items-center gap-2 relative">
          <button
            onClick={() => setScenarioDropdownOpen(!scenarioDropdownOpen)}
            className="bg-white hover:bg-zinc-100 text-black px-2 py-0.5 border-2 border-black rounded shadow-neo-xs flex items-center gap-1 font-bold transition-all text-xs"
          >
            <span>Switch Scenario ({activeScenarioId}/10)</span>
            <ChevronDown className="w-3 h-3" />
          </button>

          {scenarioDropdownOpen && (
            <div className="absolute right-0 top-7 w-80 max-h-96 overflow-y-auto bg-white border-2 border-black shadow-neo-lg rounded p-2 z-50 text-left">
              <div className="text-[11px] font-bold text-zinc-500 uppercase tracking-wider mb-1 px-1">
                10 Seeded Demonstration Scenarios
              </div>
              {scenarios.map((s) => (
                <button
                  key={s.id}
                  onClick={() => {
                    switchScenario(s.id);
                    setScenarioDropdownOpen(false);
                  }}
                  className={`w-full text-left p-2 rounded border border-black mb-1.5 transition-all flex items-start gap-2 ${
                    s.id === activeScenarioId
                      ? 'bg-[#DDD6FE] text-black font-bold'
                      : 'bg-zinc-50 hover:bg-[#FEF08A] text-zinc-900'
                  }`}
                >
                  <span className="bg-black text-white text-[10px] px-1.5 py-0.5 rounded font-mono shrink-0">
                    #{s.id}
                  </span>
                  <div className="flex-1 min-w-0">
                    <div className="text-xs font-bold truncate">{s.title}</div>
                    <div className="text-[10px] text-zinc-600 truncate">
                      {s.learner_name} • {s.goal_title} ({s.overall_mastery}% mastery)
                    </div>
                  </div>
                  {s.id === activeScenarioId && <CheckCircle className="w-3.5 h-3.5 text-black shrink-0 mt-0.5" />}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Main Navigation Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo */}
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-10 h-10 bg-[#A78BFA] border-2 border-black rounded-lg shadow-neo-sm flex items-center justify-center group-hover:translate-x-0.5 group-hover:translate-y-0.5 group-hover:shadow-neo-xs transition-all">
              <Sparkles className="w-6 h-6 text-black fill-yellow-300" />
            </div>
            <div>
              <span className="text-xl font-extrabold tracking-tight text-black font-sans">SkillForge</span>
              <span className="ml-1 text-xs font-black bg-black text-[#FEF08A] px-1.5 py-0.5 rounded border border-black uppercase">AI</span>
              <div className="text-[10px] font-mono text-zinc-600 -mt-1">Learner-First AI Tutor</div>
            </div>
          </Link>

          {/* Desktop Nav Links */}
          <nav className="hidden xl:flex items-center gap-1">
            {navLinks.slice(0, 9).map((link) => {
              const Icon = link.icon;
              const isActive = location.pathname === link.to || (link.to.includes('/learn') && location.pathname.includes('/learn'));
              return (
                <Link
                  key={link.to}
                  to={link.to}
                  className={`px-2.5 py-1.5 rounded-md text-xs font-bold border-2 transition-all flex items-center gap-1.5 ${
                    isActive
                      ? 'bg-black text-[#FEF08A] border-black shadow-neo-xs'
                      : 'border-transparent text-zinc-800 hover:border-black hover:bg-white'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{link.label}</span>
                </Link>
              );
            })}

            {/* More Links Dropdown */}
            <div className="relative group">
              <button className="px-2.5 py-1.5 rounded-md text-xs font-bold border-2 border-transparent hover:border-black hover:bg-white text-zinc-800 flex items-center gap-1">
                <span>More</span>
                <ChevronDown className="w-3 h-3" />
              </button>
              <div className="absolute right-0 top-8 hidden group-hover:block w-48 bg-white border-2 border-black rounded shadow-neo-lg p-1.5 z-50">
                {navLinks.slice(9).map((link) => {
                  const Icon = link.icon;
                  return (
                    <Link
                      key={link.to}
                      to={link.to}
                      className="flex items-center gap-2 px-3 py-1.5 rounded text-xs font-bold hover:bg-[#FEF08A] text-zinc-800 mb-0.5"
                    >
                      <Icon className="w-3.5 h-3.5" />
                      <span>{link.label}</span>
                    </Link>
                  );
                })}
              </div>
            </div>
          </nav>

          {/* User Profile Chip */}
          <div className="hidden sm:flex items-center gap-3">
            <Link
              to="/dashboard"
              className="flex items-center gap-2 bg-white border-2 border-black px-3 py-1.5 rounded-lg shadow-neo-sm hover:translate-x-0.5 hover:translate-y-0.5 hover:shadow-neo-xs transition-all"
            >
              <div className="w-7 h-7 rounded-full bg-[#FECDD3] border-2 border-black flex items-center justify-center font-black text-xs">
                {learner?.full_name ? learner.full_name[0] : 'L'}
              </div>
              <div className="text-left text-xs">
                <div className="font-bold text-black leading-tight truncate max-w-[110px]">
                  {learner?.full_name || 'Active Learner'}
                </div>
                <div className="text-[10px] text-zinc-500 font-mono">
                  {learner?.experience_level || 'beginner'}
                </div>
              </div>
            </Link>
          </div>

          {/* Mobile Menu Toggle Button */}
          <div className="xl:hidden flex items-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 border-2 border-black rounded-lg bg-white shadow-neo-xs"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Drawer */}
      {mobileMenuOpen && (
        <div className="xl:hidden border-t-2 border-black bg-white p-4 space-y-1.5 max-h-[80vh] overflow-y-auto">
          {navLinks.map((link) => {
            const Icon = link.icon;
            const isActive = location.pathname === link.to || (link.to.includes('/learn') && location.pathname.includes('/learn'));
            return (
              <Link
                key={link.to}
                to={link.to}
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-bold border-2 ${
                  isActive
                    ? 'bg-black text-[#FEF08A] border-black shadow-neo-xs'
                    : 'border-black bg-zinc-50 hover:bg-[#FEF08A] text-zinc-900'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{link.label}</span>
              </Link>
            );
          })}
        </div>
      )}
    </header>
  );
};
