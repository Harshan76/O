-- ====================================================================
-- SKILLFORGE AI: SUPABASE POSTGRESQL SCHEMA WITH ROW-LEVEL SECURITY
-- Strict Learner-First Architecture (No teacher roles or classrooms)
-- ====================================================================

-- Enable necessary extensions
create extension if not exists "uuid-ossp";

-- 1. Learners Profile
create table if not exists public.learners (
    id uuid primary key default uuid_generate_v4(),
    auth_user_id uuid references auth.users(id) on delete cascade,
    email text not null,
    full_name text not null,
    avatar_url text,
    experience_level text default 'beginner', -- beginner, intermediate, advanced
    daily_minutes integer default 45,
    learning_style text default 'hands-on', -- visual, hands-on, conceptual, project-based
    target_completion_date date,
    current_streak integer default 1,
    longest_streak integer default 1,
    total_study_hours numeric(5, 2) default 0.0,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 2. Learning Goals
create table if not exists public.learning_goals (
    id uuid primary key default uuid_generate_v4(),
    learner_id uuid not null references public.learners(id) on delete cascade,
    title text not null,
    domain text not null,
    target_outcome text not null,
    target_date date,
    status text default 'active', -- active, completed, paused
    progress_percentage integer default 0,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 3. Courses (Public Catalog)
create table if not exists public.courses (
    id uuid primary key default uuid_generate_v4(),
    slug text unique not null,
    title text not null,
    description text not null,
    domain text not null,
    level text default 'all-levels',
    modules_json jsonb default '[]'::jsonb,
    is_active boolean default true,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 4. Skills & Taxonomies
create table if not exists public.skills (
    id uuid primary key default uuid_generate_v4(),
    course_id uuid references public.courses(id) on delete cascade,
    code text unique not null,
    name text not null,
    category text not null,
    description text,
    difficulty text default 'beginner',
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 5. Skill Prerequisites
create table if not exists public.skill_prerequisites (
    id uuid primary key default uuid_generate_v4(),
    skill_id uuid not null references public.skills(id) on delete cascade,
    prerequisite_skill_id uuid not null references public.skills(id) on delete cascade,
    unique(skill_id, prerequisite_skill_id)
);

-- 6. Uploaded Documents
create table if not exists public.uploaded_documents (
    id uuid primary key default uuid_generate_v4(),
    learner_id uuid not null references public.learners(id) on delete cascade,
    filename text not null,
    file_type text not null,
    file_size integer not null,
    extracted_text text,
    summary text,
    concepts_json jsonb default '[]'::jsonb,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 7. Extracted Concepts
create table if not exists public.extracted_concepts (
    id uuid primary key default uuid_generate_v4(),
    document_id uuid not null references public.uploaded_documents(id) on delete cascade,
    term text not null,
    definition text not null,
    importance text default 'medium',
    difficulty text default 'medium',
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 8. Assessments
create table if not exists public.assessments (
    id uuid primary key default uuid_generate_v4(),
    course_id uuid references public.courses(id) on delete cascade,
    title text not null,
    type text default 'diagnostic', -- diagnostic, practice, milestone, final
    description text,
    total_questions integer default 10,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 9. Assessment Questions
create table if not exists public.questions (
    id uuid primary key default uuid_generate_v4(),
    assessment_id uuid not null references public.assessments(id) on delete cascade,
    skill_id uuid references public.skills(id) on delete set null,
    prompt text not null,
    question_type text default 'mcq', -- mcq, short_answer, code, scenario
    difficulty text default 'medium', -- beginner, intermediate, advanced
    options_json jsonb default '[]'::jsonb,
    answer_key text not null,
    rubric_json jsonb default '{}'::jsonb,
    hints_json jsonb default '[]'::jsonb,
    explanation text,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 10. Assessment Attempts
create table if not exists public.assessment_attempts (
    id uuid primary key default uuid_generate_v4(),
    assessment_id uuid not null references public.assessments(id) on delete cascade,
    learner_id uuid not null references public.learners(id) on delete cascade,
    score integer default 0,
    max_score integer default 100,
    percentage numeric(5, 2) default 0.0,
    results_json jsonb default '[]'::jsonb,
    mistakes_json jsonb default '[]'::jsonb,
    status text default 'completed',
    completed_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 11. Learning Paths
create table if not exists public.learning_paths (
    id uuid primary key default uuid_generate_v4(),
    learner_id uuid not null references public.learners(id) on delete cascade,
    goal_id uuid references public.learning_goals(id) on delete cascade,
    title text not null,
    status text default 'active',
    generated_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 12. Learning Tasks (Adaptive Sequence)
create table if not exists public.learning_tasks (
    id uuid primary key default uuid_generate_v4(),
    path_id uuid not null references public.learning_paths(id) on delete cascade,
    skill_id uuid references public.skills(id) on delete set null,
    title text not null,
    learning_objective text not null,
    difficulty text default 'intermediate', -- beginner, intermediate, advanced
    instructions text not null,
    hints_json jsonb default '[]'::jsonb,
    expected_result text,
    evaluation_criteria text,
    estimated_duration integer default 20, -- minutes
    reason_for_recommendation text not null,
    task_type text default 'challenge', -- concept, quiz, challenge, project, revision
    status text default 'pending', -- pending, in_progress, completed, skipped
    order_index integer default 0,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 13. Tutor Conversations
create table if not exists public.tutor_conversations (
    id uuid primary key default uuid_generate_v4(),
    learner_id uuid not null references public.learners(id) on delete cascade,
    course_id uuid references public.courses(id) on delete set null,
    context_task_id uuid references public.learning_tasks(id) on delete set null,
    messages_json jsonb default '[]'::jsonb,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 14. Flashcards
create table if not exists public.flashcards (
    id uuid primary key default uuid_generate_v4(),
    learner_id uuid not null references public.learners(id) on delete cascade,
    document_id uuid references public.uploaded_documents(id) on delete set null,
    skill_id uuid references public.skills(id) on delete set null,
    front text not null,
    back text not null,
    confidence_level text default 'learning', -- new, learning, mastered
    review_count integer default 0,
    last_reviewed_at timestamp with time zone,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 15. Mini-Projects
create table if not exists public.mini_projects (
    id uuid primary key default uuid_generate_v4(),
    course_id uuid references public.courses(id) on delete cascade,
    skill_id uuid references public.skills(id) on delete set null,
    title text not null,
    objective text not null,
    requirements_json jsonb default '[]'::jsonb,
    milestones_json jsonb default '[]'::jsonb,
    rubric_json jsonb default '{}'::jsonb,
    difficulty text default 'intermediate',
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 16. Project Submissions & Feedback
create table if not exists public.project_submissions (
    id uuid primary key default uuid_generate_v4(),
    project_id uuid not null references public.mini_projects(id) on delete cascade,
    learner_id uuid not null references public.learners(id) on delete cascade,
    submission_text text not null,
    code_repo_link text,
    feedback_json jsonb default '{}'::jsonb,
    score integer default 0,
    status text default 'evaluated', -- pending, evaluated
    submitted_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 17. Mastery Records
create table if not exists public.mastery_records (
    id uuid primary key default uuid_generate_v4(),
    learner_id uuid not null references public.learners(id) on delete cascade,
    skill_id uuid not null references public.skills(id) on delete cascade,
    proficiency_level text default 'developing', -- novice, developing, proficient, mastered
    score numeric(5, 2) default 0.0,
    confidence_score numeric(5, 2) default 50.0,
    attempts_count integer default 0,
    is_verified boolean default false,
    last_evaluated_at timestamp with time zone default timezone('utc'::text, now()) not null,
    unique(learner_id, skill_id)
);

-- 18. Learning Activity History
create table if not exists public.learning_activity_history (
    id uuid primary key default uuid_generate_v4(),
    learner_id uuid not null references public.learners(id) on delete cascade,
    activity_type text not null, -- assessment, quiz, coding, project, flashcard, tutor
    title text not null,
    metadata_json jsonb default '{}'::jsonb,
    score numeric(5, 2),
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- ====================================================================
-- ROW-LEVEL SECURITY (RLS) POLICIES
-- ====================================================================

alter table public.learners enable row level security;
alter table public.learning_goals enable row level security;
alter table public.courses enable row level security;
alter table public.skills enable row level security;
alter table public.skill_prerequisites enable row level security;
alter table public.uploaded_documents enable row level security;
alter table public.extracted_concepts enable row level security;
alter table public.assessments enable row level security;
alter table public.questions enable row level security;
alter table public.assessment_attempts enable row level security;
alter table public.learning_paths enable row level security;
alter table public.learning_tasks enable row level security;
alter table public.tutor_conversations enable row level security;
alter table public.flashcards enable row level security;
alter table public.mini_projects enable row level security;
alter table public.project_submissions enable row level security;
alter table public.mastery_records enable row level security;
alter table public.learning_activity_history enable row level security;

-- Public catalog read access
create policy "Anyone can read courses" on public.courses for select using (true);
create policy "Anyone can read skills" on public.skills for select using (true);
create policy "Anyone can read skill prerequisites" on public.skill_prerequisites for select using (true);
create policy "Anyone can read public assessments" on public.assessments for select using (true);
create policy "Anyone can read public questions" on public.questions for select using (true);
create policy "Anyone can read mini projects" on public.mini_projects for select using (true);

-- Learner-specific isolation policies
create policy "Learners manage own profile" on public.learners
    for all using (auth.uid() = auth_user_id or auth.uid() = id);

create policy "Learners manage own goals" on public.learning_goals
    for all using (auth.uid() = learner_id);

create policy "Learners manage own documents" on public.uploaded_documents
    for all using (auth.uid() = learner_id);

create policy "Learners read own extracted concepts" on public.extracted_concepts
    for all using (exists (
        select 1 from public.uploaded_documents
        where public.uploaded_documents.id = public.extracted_concepts.document_id
        and public.uploaded_documents.learner_id = auth.uid()
    ));

create policy "Learners manage own assessment attempts" on public.assessment_attempts
    for all using (auth.uid() = learner_id);

create policy "Learners manage own learning paths" on public.learning_paths
    for all using (auth.uid() = learner_id);

create policy "Learners manage own learning tasks" on public.learning_tasks
    for all using (exists (
        select 1 from public.learning_paths
        where public.learning_paths.id = public.learning_tasks.path_id
        and public.learning_paths.learner_id = auth.uid()
    ));

create policy "Learners manage own tutor conversations" on public.tutor_conversations
    for all using (auth.uid() = learner_id);

create policy "Learners manage own flashcards" on public.flashcards
    for all using (auth.uid() = learner_id);

create policy "Learners manage own project submissions" on public.project_submissions
    for all using (auth.uid() = learner_id);

create policy "Learners manage own mastery records" on public.mastery_records
    for all using (auth.uid() = learner_id);

create policy "Learners manage own activity history" on public.learning_activity_history
    for all using (auth.uid() = learner_id);
