import React, { createContext, useContext, useState, useEffect } from 'react';
import { LearnerProfile, DemoScenario, ProgressSummary } from '../types';
import { api } from '../services/api';

interface LearnerContextType {
  learner: LearnerProfile | null;
  activeScenarioId: string;
  scenarios: DemoScenario[];
  progress: ProgressSummary | null;
  loading: boolean;
  switchScenario: (id: string) => Promise<void>;
  refreshAll: () => Promise<void>;
  toast: { message: string; type: 'success' | 'info' | 'warning' | 'error' } | null;
  showToast: (message: string, type?: 'success' | 'info' | 'warning' | 'error') => void;
}

const LearnerContext = createContext<LearnerContextType | undefined>(undefined);

export const LearnerProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [learner, setLearner] = useState<LearnerProfile | null>(null);
  const [activeScenarioId, setActiveScenarioId] = useState<string>('1');
  const [scenarios, setScenarios] = useState<DemoScenario[]>([]);
  const [progress, setProgress] = useState<ProgressSummary | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'info' | 'warning' | 'error' } | null>(null);

  const showToast = (message: string, type: 'success' | 'info' | 'warning' | 'error' = 'info') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 4000);
  };

  const refreshAll = async () => {
    try {
      setLoading(true);
      const [scList, pSummary, prof] = await Promise.all([
        api.getDemoScenarios().catch(() => []),
        api.getProgressSummary().catch(() => null),
        api.getProfile().catch(() => null)
      ]);
      setScenarios(scList);
      setProgress(pSummary);
      setLearner(prof);
    } catch (err: any) {
      console.error('Failed to load initial learner data:', err);
    } finally {
      setLoading(false);
    }
  };

  const switchScenario = async (id: string) => {
    try {
      setLoading(true);
      const res = await api.switchScenario(id);
      setActiveScenarioId(id);
      showToast(`Activated Demo Scenario ${id}: ${res.scenario?.title || ''}`, 'success');
      await refreshAll();
    } catch (err: any) {
      showToast(`Failed to switch scenario: ${err.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshAll();
  }, []);

  return (
    <LearnerContext.Provider
      value={{
        learner,
        activeScenarioId,
        scenarios,
        progress,
        loading,
        switchScenario,
        refreshAll,
        toast,
        showToast
      }}
    >
      {children}
    </LearnerContext.Provider>
  );
};

export const useLearner = () => {
  const context = useContext(LearnerContext);
  if (!context) {
    throw new Error('useLearner must be used within a LearnerProvider');
  }
  return context;
};
