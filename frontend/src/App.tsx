import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { LearnerProvider, useLearner } from './context/LearnerContext';
import { Navbar } from './components/Navbar';
import { LandingPage } from './pages/LandingPage';
import { AuthPage } from './pages/AuthPage';
import { OnboardingPage } from './pages/OnboardingPage';
import { DashboardPage } from './pages/DashboardPage';
import { GoalsCoursesPage } from './pages/GoalsCoursesPage';
import { CourseLearningHubPage } from './pages/CourseLearningHubPage';
import { SmartNotesPage } from './pages/SmartNotesPage';
import { DiagnosticPage } from './pages/DiagnosticPage';
import { SkillGapPage } from './pages/SkillGapPage';
import { RoadmapPage } from './pages/RoadmapPage';
import { TutorChatPage } from './pages/TutorChatPage';
import { ChallengeWorkspacePage } from './pages/ChallengeWorkspacePage';
import { RevisionWorkspacePage } from './pages/RevisionWorkspacePage';
import { MiniProjectPage } from './pages/MiniProjectPage';
import { SubmissionFeedbackPage } from './pages/SubmissionFeedbackPage';
import { MasteryAnalyticsPage } from './pages/MasteryAnalyticsPage';
import { HistoryPage } from './pages/HistoryPage';
import { SettingsPage } from './pages/SettingsPage';

const ToastBanner: React.FC = () => {
  const { toast } = useLearner();
  if (!toast) return null;

  const bg = toast.type === 'success' ? 'bg-[#A7F3D0] text-emerald-950' :
             toast.type === 'error' ? 'bg-[#FECDD3] text-rose-950' :
             toast.type === 'warning' ? 'bg-[#FED7AA] text-amber-950' :
             'bg-[#FEF08A] text-black';

  return (
    <div className="fixed bottom-6 right-6 z-50 animate-bounce">
      <div className={`${bg} border-2 border-black rounded-xl px-4 py-2.5 shadow-neo text-xs sm:text-sm font-extrabold flex items-center gap-2`}>
        <span>{toast.message}</span>
      </div>
    </div>
  );
};

export const AppContent: React.FC = () => {
  return (
    <div className="min-h-screen bg-[#FAF7F2] flex flex-col font-sans selection:bg-[#FEF08A] selection:text-black">
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/auth" element={<AuthPage />} />
          <Route path="/onboarding" element={<OnboardingPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/goals-courses" element={<GoalsCoursesPage />} />
          <Route path="/courses/:courseId/learn" element={<CourseLearningHubPage />} />
          <Route path="/learning-hub" element={<CourseLearningHubPage />} />
          <Route path="/smart-notes" element={<SmartNotesPage />} />
          <Route path="/diagnostic" element={<DiagnosticPage />} />
          <Route path="/skill-gap" element={<SkillGapPage />} />
          <Route path="/roadmap" element={<RoadmapPage />} />
          <Route path="/tutor" element={<TutorChatPage />} />
          <Route path="/challenges" element={<ChallengeWorkspacePage />} />
          <Route path="/revision" element={<RevisionWorkspacePage />} />
          <Route path="/projects" element={<MiniProjectPage />} />
          <Route path="/feedback" element={<SubmissionFeedbackPage />} />
          <Route path="/analytics" element={<MasteryAnalyticsPage />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
      <ToastBanner />
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <Router>
      <LearnerProvider>
        <AppContent />
      </LearnerProvider>
    </Router>
  );
};

export default App;
