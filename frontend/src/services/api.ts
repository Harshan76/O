import {
  LearnerProfile, Course, LearningGoal, AssessmentStartResponse,
  AssessmentSubmitResponse, SkillProfileResponse, LearningPathResponse,
  ChatMessage, Flashcard, ChallengeSubmitResponse, MiniProject,
  SubmissionEvaluateResponse, ProgressSummary, ActivityItem, DemoScenario
} from '../types';

const API_BASE = '/api';

class ApiService {
  private learnerId: string = 'demo-learner-1';

  setLearnerId(id: string) {
    this.learnerId = id;
  }

  getLearnerId(): string {
    return this.learnerId;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'x-learner-id': this.learnerId,
      ...(options.headers as Record<string, string> || {})
    };

    const res = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers
    });

    if (!res.ok) {
      let errorMsg = `HTTP Error ${res.status}`;
      try {
        const errorJson = await res.json();
        errorMsg = errorJson.detail || errorMsg;
      } catch {}
      throw new Error(errorMsg);
    }

    return res.json();
  }

  // Profile & Auth
  async getProfile(): Promise<LearnerProfile> {
    return this.request<LearnerProfile>('/profile');
  }

  async updateProfile(data: Partial<LearnerProfile>): Promise<LearnerProfile> {
    return this.request<LearnerProfile>('/profile', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async login(email: string, full_name?: string): Promise<any> {
    const res = await this.request<any>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, full_name })
    });
    if (res.learner?.id) {
      this.setLearnerId(res.learner.id);
    }
    return res;
  }

  // Courses & Goals
  async getCourses(): Promise<Course[]> {
    return this.request<Course[]>('/courses');
  }

  async getGoals(): Promise<LearningGoal[]> {
    return this.request<LearningGoal[]>('/learning-goals');
  }

  async createGoal(data: any): Promise<LearningGoal> {
    return this.request<LearningGoal>('/learning-goals', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  // Diagnostic & Skills
  async startAssessment(courseId: string = 'c-python'): Promise<any> {
    return this.request<any>('/assessments/start', {
      method: 'POST',
      body: JSON.stringify({ course_id: courseId })
    });
  }

  async submitAssessment(assessmentId: string, answers: { question_id: string; answer: string }[]): Promise<AssessmentSubmitResponse> {
    return this.request<AssessmentSubmitResponse>('/assessments/submit', {
      method: 'POST',
      body: JSON.stringify({ assessment_id: assessmentId, answers })
    });
  }

  async getSkillProfile(): Promise<SkillProfileResponse> {
    return this.request<SkillProfileResponse>('/skills/profile');
  }

  // Roadmap & Tasks
  async getCurrentRoadmap(): Promise<LearningPathResponse> {
    return this.request<LearningPathResponse>('/learning-paths/current');
  }

  async generateRoadmap(): Promise<LearningPathResponse> {
    return this.request<LearningPathResponse>('/learning-paths/generate', {
      method: 'POST',
      body: JSON.stringify({})
    });
  }

  async updateTaskStatus(taskId: string, status: string): Promise<any> {
    return this.request<any>(`/tasks/${taskId}/status`, {
      method: 'POST',
      body: JSON.stringify({ status })
    });
  }

  // AI Tutor
  async sendTutorChat(message: string, contextTaskId?: string, courseId?: string, documentId?: string): Promise<any> {
    return this.request<any>('/tutor/chat', {
      method: 'POST',
      body: JSON.stringify({
        message,
        context_task_id: contextTaskId,
        context_course_id: courseId,
        document_id: documentId
      })
    });
  }

  async getTutorHistory(): Promise<ChatMessage[]> {
    return this.request<ChatMessage[]>('/tutor/history');
  }

  // Smart Notes
  async uploadDocument(file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);

    const res = await fetch(`${API_BASE}/documents/upload`, {
      method: 'POST',
      headers: {
        'x-learner-id': this.learnerId
      },
      body: formData
    });

    if (!res.ok) {
      throw new Error(`Failed to upload document: ${res.statusText}`);
    }
    return res.json();
  }

  async getDocuments(): Promise<any[]> {
    return this.request<any[]>('/documents');
  }

  async generateStudyTools(documentId: string): Promise<any> {
    return this.request<any>('/study-tools/generate', {
      method: 'POST',
      body: JSON.stringify({ document_id: documentId })
    });
  }

  async getFlashcards(): Promise<Flashcard[]> {
    return this.request<Flashcard[]>('/flashcards');
  }

  async reviewFlashcard(cardId: string, confidence: string): Promise<any> {
    return this.request<any>(`/flashcards/${cardId}/review`, {
      method: 'POST',
      body: JSON.stringify({ confidence })
    });
  }

  // Challenges
  async getChallenge(challengeId: string): Promise<any> {
    return this.request<any>(`/challenges/${challengeId}`);
  }

  async submitChallenge(challengeId: string, codeOrAnswer: string, language: string = 'python'): Promise<ChallengeSubmitResponse> {
    return this.request<ChallengeSubmitResponse>('/challenges/submit', {
      method: 'POST',
      body: JSON.stringify({
        challenge_id: challengeId,
        code_or_answer: codeOrAnswer,
        language
      })
    });
  }

  // Projects
  async getProjects(): Promise<MiniProject[]> {
    return this.request<MiniProject[]>('/projects');
  }

  async generateProject(domain: string, skillCode: string): Promise<MiniProject> {
    return this.request<MiniProject>('/projects/generate', {
      method: 'POST',
      body: JSON.stringify({ domain, skill_code: skillCode })
    });
  }

  async evaluateProject(projectId: string, submissionText: string, repoLink?: string): Promise<SubmissionEvaluateResponse> {
    return this.request<SubmissionEvaluateResponse>('/submissions/evaluate', {
      method: 'POST',
      body: JSON.stringify({
        project_id: projectId,
        submission_text: submissionText,
        code_repo_link: repoLink
      })
    });
  }

  // Progress & History
  async getProgressSummary(): Promise<ProgressSummary> {
    return this.request<ProgressSummary>('/progress/summary');
  }

  async getActivityHistory(): Promise<ActivityItem[]> {
    return this.request<ActivityItem[]>('/progress/history');
  }

  // Demo Scenarios
  async getDemoScenarios(): Promise<DemoScenario[]> {
    return this.request<DemoScenario[]>('/demo/scenarios');
  }

  async switchScenario(scenarioId: string): Promise<any> {
    const res = await this.request<any>(`/demo/scenarios/${scenarioId}/switch`, {
      method: 'POST'
    });
    if (res.learner_id) {
      this.setLearnerId(res.learner_id);
    }
    return res;
  }
}

export const api = new ApiService();
