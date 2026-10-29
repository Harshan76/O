export interface LearnerProfile {
  id: string;
  email: string;
  full_name: string;
  avatar_url?: string;
  experience_level: 'beginner' | 'intermediate' | 'advanced';
  daily_minutes: number;
  learning_style: 'hands-on' | 'visual' | 'conceptual' | 'project-based';
  target_completion_date?: string;
  current_streak: number;
  longest_streak: number;
  total_study_hours: number;
  is_simulated: boolean;
}

export interface CourseModule {
  id: string;
  title: string;
  description: string;
  skills_covered: string[];
  estimated_hours: number;
}

export interface Course {
  id: string;
  slug: string;
  title: string;
  description: string;
  domain: string;
  level: string;
  modules: CourseModule[];
}

export interface LearningGoal {
  id: string;
  learner_id: string;
  title: string;
  domain: string;
  target_outcome: string;
  target_date?: string;
  status: 'active' | 'completed' | 'paused';
  progress_percentage: number;
}

export interface QuestionOption {
  id: string;
  text: string;
}

export interface AssessmentQuestion {
  id: string;
  skill_id: string;
  prompt: string;
  question_type: 'mcq' | 'short_answer' | 'code' | 'scenario';
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  options?: QuestionOption[];
  hints: string[];
}

export interface AssessmentStartResponse {
  assessment_id: string;
  title: string;
  course_id: string;
  total_questions: number;
  estimated_minutes: number;
  questions: AssessmentQuestion[];
}

export interface QuestionEvaluationResult {
  question_id: string;
  prompt: string;
  user_answer: string;
  correct_answer: string;
  is_correct: boolean;
  score: number;
  explanation: string;
  skill_code: string;
  difficulty: string;
}

export interface AssessmentSubmitResponse {
  attempt_id: string;
  assessment_id: string;
  score: number;
  max_score: number;
  percentage: number;
  passed: boolean;
  status_summary: string;
  results: QuestionEvaluationResult[];
  skill_gaps_identified: string[];
  strengths_identified: string[];
  adaptation_direction: 'revisit_prerequisites' | 'targeted_practice' | 'advanced_challenge';
  recommended_next_task: {
    title: string;
    learning_objective: string;
    difficulty: string;
    estimated_duration: number;
    reason: string;
  };
}

export interface SkillItem {
  code: string;
  name: string;
  category: string;
  description: string;
  difficulty: string;
  status: 'strong' | 'weak' | 'missing_prereq' | 'validating';
  score: number;
  prerequisites: string[];
  recommended_action: string;
}

export interface SkillProfileResponse {
  learner_id: string;
  overall_mastery: number;
  total_skills_mapped: number;
  strong_count: number;
  weak_count: number;
  missing_prereqs_count: number;
  validating_count: number;
  skills: SkillItem[];
  calculation_breakdown: {
    formula: string;
    verification_threshold: string;
    adaptation_rules: Record<string, string>;
  };
}

export interface LearningTask {
  id: string;
  path_id: string;
  skill_code: string;
  title: string;
  learning_objective: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  instructions: string;
  hints: string[];
  expected_result: string;
  evaluation_criteria: string;
  estimated_duration: number;
  reason_for_recommendation: string;
  task_type: 'quiz' | 'challenge' | 'project' | 'concept' | 'revision';
  status: 'pending' | 'in_progress' | 'completed' | 'skipped';
  order_index: number;
}

export interface LearningPathResponse {
  path_id: string;
  learner_id: string;
  goal_id: string;
  title: string;
  status: string;
  adaptation_reason: string;
  tasks: LearningTask[];
  progress_percentage: number;
}

export interface ChatMessage {
  id: string;
  sender: 'learner' | 'tutor';
  text: string;
  timestamp: string;
  suggested_followups?: string[];
  is_hint?: boolean;
  context_task_id?: string;
}

export interface Flashcard {
  id: string;
  front: string;
  back: string;
  skill_code: string;
  confidence: 'new' | 'learning' | 'mastered';
  review_count: number;
  source_concept?: string;
}

export interface TestCaseResult {
  input: string;
  expected: string;
  actual: string;
  passed: boolean;
}

export interface ChallengeSubmitResponse {
  challenge_id: string;
  passed: boolean;
  score: number;
  test_results: TestCaseResult[];
  stdout: string;
  error_message?: string;
  ai_explanation: string;
  mistake_analysis?: string;
  adaptation_rule_applied: string;
  unlocked_next_task?: any;
}

export interface ProjectMilestone {
  id: string;
  title: string;
  description: string;
  is_completed: boolean;
}

export interface ProjectRubricCriterion {
  criterion: string;
  weight: number;
  description: string;
}

export interface MiniProject {
  id: string;
  title: string;
  domain: string;
  skill_code: string;
  objective: string;
  difficulty: string;
  estimated_hours: number;
  requirements: string[];
  milestones: ProjectMilestone[];
  rubric: ProjectRubricCriterion[];
}

export interface RubricScoreItem {
  criterion: string;
  score: number;
  feedback: string;
}

export interface SubmissionEvaluateResponse {
  submission_id: string;
  project_id: string;
  overall_score: number;
  passed: boolean;
  rubric_scores: RubricScoreItem[];
  strengths: string[];
  areas_for_improvement: string[];
  ai_coaching_notes: string;
  next_recommended_milestone: string;
}

export interface ProgressSummary {
  learner_id: string;
  goal_title: string;
  current_streak: number;
  longest_streak: number;
  total_study_hours: number;
  overall_mastery: number;
  skills_mastered: number;
  skills_in_progress: number;
  projects_completed: number;
  challenges_completed: number;
  mastery_formula_explanation: string;
  is_simulated: boolean;
}

export interface ActivityItem {
  id: string;
  activity_type: string;
  title: string;
  score?: number;
  timestamp: string;
  details: string;
}

export interface DemoScenario {
  id: string;
  title: string;
  learner_name: string;
  email: string;
  goal_title: string;
  domain: string;
  experience_level: string;
  overall_mastery: number;
  description: string;
  is_simulated: boolean;
}
