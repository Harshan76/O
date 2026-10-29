from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --- Learner Profile Models ---
class LearnerProfile(BaseModel):
    id: str = "demo-learner-1"
    email: str = "learner@skillforge.ai"
    full_name: str = "Alex Mercer"
    avatar_url: Optional[str] = None
    experience_level: str = "beginner" # beginner, intermediate, advanced
    daily_minutes: int = 45
    learning_style: str = "hands-on" # hands-on, visual, conceptual, project-based
    target_completion_date: Optional[str] = "2026-12-31"
    current_streak: int = 4
    longest_streak: int = 12
    total_study_hours: float = 18.5
    is_simulated: bool = False

class LearnerProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    experience_level: Optional[str] = None
    daily_minutes: Optional[int] = None
    learning_style: Optional[str] = None
    target_completion_date: Optional[str] = None

# --- Learning Goals ---
class LearningGoal(BaseModel):
    id: str
    learner_id: str
    title: str
    domain: str
    target_outcome: str
    target_date: Optional[str] = None
    status: str = "active" # active, completed, paused
    progress_percentage: int = 0

class LearningGoalCreate(BaseModel):
    title: str
    domain: str
    target_outcome: str
    experience_level: str
    daily_minutes: int
    learning_style: str
    target_date: Optional[str] = None

# --- Courses & Curriculum ---
class CourseModule(BaseModel):
    id: str
    title: str
    description: str
    skills_covered: List[str]
    estimated_hours: int

class Course(BaseModel):
    id: str
    slug: str
    title: str
    description: str
    domain: str
    level: str
    modules: List[CourseModule] = []

# --- Documents & Notes Extraction ---
class ExtractedConcept(BaseModel):
    term: str
    definition: str
    importance: str # core, important, reference
    difficulty: str # beginner, intermediate, advanced

class DocumentUploadResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    file_size: int
    char_count: int
    summary: str
    key_concepts: List[ExtractedConcept]
    preview_snippet: str

# --- Skills & Skill-Gap Map ---
class SkillItem(BaseModel):
    code: str
    name: str
    category: str
    description: str
    difficulty: str
    status: str # "strong", "weak", "missing_prereq", "validating"
    score: float # 0 - 100
    prerequisites: List[str] = []
    recommended_action: str

class SkillProfileResponse(BaseModel):
    learner_id: str
    overall_mastery: float
    total_skills_mapped: int
    strong_count: int
    weak_count: int
    missing_prereqs_count: int
    validating_count: int
    skills: List[SkillItem]
    calculation_breakdown: Dict[str, Any]

# --- Assessments ---
class QuestionOption(BaseModel):
    id: str
    text: str

class AssessmentQuestion(BaseModel):
    id: str
    skill_id: str
    prompt: str
    question_type: str # mcq, short_answer, code, scenario
    difficulty: str # beginner, intermediate, advanced
    options: Optional[List[QuestionOption]] = None
    hints: List[str] = []

class AssessmentStartResponse(BaseModel):
    assessment_id: str
    title: str
    course_id: str
    total_questions: int
    estimated_minutes: int
    questions: List[AssessmentQuestion]

class QuestionAnswer(BaseModel):
    question_id: str
    answer: str

class AssessmentSubmitRequest(BaseModel):
    assessment_id: str
    answers: List[QuestionAnswer]

class QuestionEvaluationResult(BaseModel):
    question_id: str
    prompt: str
    user_answer: str
    correct_answer: str
    is_correct: bool
    score: float
    explanation: str
    skill_code: str
    difficulty: str

class AssessmentSubmitResponse(BaseModel):
    attempt_id: str
    assessment_id: str
    score: int
    max_score: int
    percentage: float
    passed: bool
    status_summary: str
    results: List[QuestionEvaluationResult]
    skill_gaps_identified: List[str]
    strengths_identified: List[str]
    adaptation_direction: str # "revisit_prerequisites", "targeted_practice", "advanced_challenge"
    recommended_next_task: Dict[str, Any]

# --- Learning Path & Tasks ---
class LearningTask(BaseModel):
    id: str
    path_id: str
    skill_code: str
    title: str
    learning_objective: str
    difficulty: str # beginner, intermediate, advanced
    instructions: str
    hints: List[str] = []
    expected_result: str
    evaluation_criteria: str
    estimated_duration: int # minutes
    reason_for_recommendation: str
    task_type: str # quiz, challenge, project, concept, revision
    status: str # pending, in_progress, completed, skipped
    order_index: int

class LearningPathResponse(BaseModel):
    path_id: str
    learner_id: str
    goal_id: str
    title: str
    status: str
    adaptation_reason: str
    tasks: List[LearningTask]
    progress_percentage: int

# --- AI Tutor Chat ---
class ChatMessage(BaseModel):
    id: str
    sender: str # "learner" or "tutor"
    text: str
    timestamp: str
    suggested_followups: Optional[List[str]] = None
    is_hint: bool = False
    context_task_id: Optional[str] = None

class TutorChatRequest(BaseModel):
    message: str
    context_task_id: Optional[str] = None
    context_course_id: Optional[str] = None
    document_id: Optional[str] = None
    conversation_id: Optional[str] = None

class TutorChatResponse(BaseModel):
    reply: str
    suggested_followups: List[str]
    analogies_used: bool = False
    check_question: Optional[str] = None
    hints_remaining: int = 3
    is_grounded_in_notes: bool = False

# --- Flashcards & Study Tools ---
class Flashcard(BaseModel):
    id: str
    front: str
    back: str
    skill_code: str
    confidence: str # "new", "learning", "mastered"
    review_count: int = 0
    source_concept: Optional[str] = None

class StudyToolsResponse(BaseModel):
    flashcards: List[Flashcard]
    generated_quizzes: List[AssessmentQuestion]

# --- Coding & Quiz Challenges ---
class TestCaseResult(BaseModel):
    input: str
    expected: str
    actual: str
    passed: bool

class ChallengeSubmitRequest(BaseModel):
    challenge_id: str
    code_or_answer: str
    language: str = "python"

class ChallengeSubmitResponse(BaseModel):
    challenge_id: str
    passed: bool
    score: int # 0 - 100
    test_results: List[TestCaseResult] = []
    stdout: str = ""
    error_message: Optional[str] = None
    ai_explanation: str
    mistake_analysis: Optional[str] = None
    adaptation_rule_applied: str
    unlocked_next_task: Optional[Dict[str, Any]] = None

# --- Mini-Projects ---
class ProjectMilestone(BaseModel):
    id: str
    title: str
    description: str
    is_completed: bool = False

class ProjectRubricCriterion(BaseModel):
    criterion: str
    weight: int # percentage
    description: str

class MiniProject(BaseModel):
    id: str
    title: str
    domain: str
    skill_code: str
    objective: str
    difficulty: str
    estimated_hours: int
    requirements: List[str]
    milestones: List[ProjectMilestone]
    rubric: List[ProjectRubricCriterion]

class SubmissionEvaluateRequest(BaseModel):
    project_id: str
    submission_text: str
    code_repo_link: Optional[str] = None

class RubricScoreItem(BaseModel):
    criterion: str
    score: int # 0-100
    feedback: str

class SubmissionEvaluateResponse(BaseModel):
    submission_id: str
    project_id: str
    overall_score: int
    passed: bool
    rubric_scores: List[RubricScoreItem]
    strengths: List[str]
    areas_for_improvement: List[str]
    ai_coaching_notes: str
    next_recommended_milestone: str

# --- Progress & History ---
class ProgressSummary(BaseModel):
    learner_id: str
    goal_title: str
    current_streak: int
    longest_streak: int
    total_study_hours: float
    overall_mastery: float
    skills_mastered: int
    skills_in_progress: int
    projects_completed: int
    challenges_completed: int
    mastery_formula_explanation: str
    is_simulated: bool = False

class ActivityItem(BaseModel):
    id: str
    activity_type: str # "assessment", "challenge", "project", "quiz", "tutor"
    title: str
    score: Optional[float] = None
    timestamp: str
    details: str

# --- Course Learning Hub & Personal Smart Notes ---
class StudentNoteCreate(BaseModel):
    title: str
    content: str
    topic_id: Optional[str] = None
    topic_title: Optional[str] = None

class StudentNoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    topic_id: Optional[str] = None
    topic_title: Optional[str] = None

class StudentNote(BaseModel):
    id: str
    learner_id: str
    course_id: str
    topic_id: Optional[str] = None
    topic_title: Optional[str] = None
    title: str
    content: str
    created_at: str
    updated_at: str

class TopicConceptItem(BaseModel):
    term: str
    definition: str

class TopicStepItem(BaseModel):
    step: str
    title: str
    description: str

class TopicCodeExample(BaseModel):
    language: str
    code: str
    explanation: str

class TopicPracticeQuestion(BaseModel):
    question: str
    answer: str
    explanation: str

class TopicStudyNotesSchema(BaseModel):
    introduction: str
    concepts: List[TopicConceptItem]
    step_by_step: List[TopicStepItem]
    code_example: Optional[TopicCodeExample] = None
    key_takeaways: List[str]
    practice_questions: List[TopicPracticeQuestion]

class TopicVideoSchema(BaseModel):
    id: str
    title: str
    channel: str
    embed_url: str
    watch_url: str
    search_url: str
    duration: str
    summary: str

class CourseTopicResourceSchema(BaseModel):
    id: str
    title: str
    description: str
    estimated_minutes: int
    study_notes: TopicStudyNotesSchema
    videos: List[TopicVideoSchema]

class CourseLearningHubResponse(BaseModel):
    course_id: str
    course_title: str
    domain: str
    level: str
    description: str
    diagnostic_assessment_id: Optional[str] = None
    topics: List[CourseTopicResourceSchema]
