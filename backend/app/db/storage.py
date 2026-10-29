import json
import sqlite3
import os
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from app.config import settings

def resolve_db_path() -> str:
    path = settings.SQLITE_DB_PATH
    if os.path.isabs(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return path
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_dir, path)

DB_FILE = resolve_db_path()

def get_connection():
    conn = sqlite3.connect(DB_FILE, timeout=30.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=10000;")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Learners
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS learners (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        avatar_url TEXT,
        experience_level TEXT DEFAULT 'beginner',
        daily_minutes INTEGER DEFAULT 45,
        learning_style TEXT DEFAULT 'hands-on',
        target_completion_date TEXT,
        current_streak INTEGER DEFAULT 3,
        longest_streak INTEGER DEFAULT 7,
        total_study_hours REAL DEFAULT 12.5,
        is_simulated INTEGER DEFAULT 0,
        active_scenario TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """)

    # 2. Learning Goals
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS learning_goals (
        id TEXT PRIMARY KEY,
        learner_id TEXT NOT NULL,
        title TEXT NOT NULL,
        domain TEXT NOT NULL,
        target_outcome TEXT NOT NULL,
        target_date TEXT,
        status TEXT DEFAULT 'active',
        progress_percentage INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    );
    """)

    # 3. Courses
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id TEXT PRIMARY KEY,
        slug TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        domain TEXT NOT NULL,
        level TEXT DEFAULT 'all-levels',
        modules_json TEXT DEFAULT '[]',
        is_active INTEGER DEFAULT 1,
        created_at TEXT NOT NULL
    );
    """)

    # 4. Skills
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        id TEXT PRIMARY KEY,
        course_id TEXT,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        difficulty TEXT DEFAULT 'beginner',
        created_at TEXT NOT NULL
    );
    """)

    # 5. Skill Prerequisites
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skill_prerequisites (
        id TEXT PRIMARY KEY,
        skill_id TEXT NOT NULL,
        prerequisite_code TEXT NOT NULL
    );
    """)

    # 6. Uploaded Documents
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS uploaded_documents (
        id TEXT PRIMARY KEY,
        learner_id TEXT NOT NULL,
        filename TEXT NOT NULL,
        file_type TEXT NOT NULL,
        file_size INTEGER NOT NULL,
        char_count INTEGER DEFAULT 0,
        summary TEXT,
        extracted_text TEXT,
        concepts_json TEXT DEFAULT '[]',
        created_at TEXT NOT NULL
    );
    """)

    # 7. Assessments
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assessments (
        id TEXT PRIMARY KEY,
        course_id TEXT,
        title TEXT NOT NULL,
        type TEXT DEFAULT 'diagnostic',
        description TEXT,
        total_questions INTEGER DEFAULT 5,
        created_at TEXT NOT NULL
    );
    """)

    # 8. Questions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id TEXT PRIMARY KEY,
        assessment_id TEXT NOT NULL,
        skill_code TEXT NOT NULL,
        prompt TEXT NOT NULL,
        question_type TEXT DEFAULT 'mcq',
        difficulty TEXT DEFAULT 'medium',
        options_json TEXT DEFAULT '[]',
        answer_key TEXT NOT NULL,
        rubric_json TEXT DEFAULT '{}',
        hints_json TEXT DEFAULT '[]',
        explanation TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)

    # 9. Assessment Attempts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assessment_attempts (
        id TEXT PRIMARY KEY,
        assessment_id TEXT NOT NULL,
        learner_id TEXT NOT NULL,
        score INTEGER DEFAULT 0,
        max_score INTEGER DEFAULT 100,
        percentage REAL DEFAULT 0.0,
        results_json TEXT DEFAULT '[]',
        mistakes_json TEXT DEFAULT '[]',
        status TEXT DEFAULT 'completed',
        completed_at TEXT NOT NULL
    );
    """)

    # 10. Learning Paths
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS learning_paths (
        id TEXT PRIMARY KEY,
        learner_id TEXT NOT NULL,
        goal_id TEXT,
        title TEXT NOT NULL,
        status TEXT DEFAULT 'active',
        adaptation_reason TEXT,
        progress_percentage INTEGER DEFAULT 0,
        generated_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """)

    # 11. Learning Tasks
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS learning_tasks (
        id TEXT PRIMARY KEY,
        path_id TEXT NOT NULL,
        skill_code TEXT NOT NULL,
        title TEXT NOT NULL,
        learning_objective TEXT NOT NULL,
        difficulty TEXT DEFAULT 'intermediate',
        instructions TEXT NOT NULL,
        hints_json TEXT DEFAULT '[]',
        expected_result TEXT,
        evaluation_criteria TEXT,
        estimated_duration INTEGER DEFAULT 20,
        reason_for_recommendation TEXT NOT NULL,
        task_type TEXT DEFAULT 'challenge',
        status TEXT DEFAULT 'pending',
        order_index INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    );
    """)

    # 12. Tutor Conversations & Messages
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tutor_conversations (
        id TEXT PRIMARY KEY,
        learner_id TEXT NOT NULL,
        course_id TEXT,
        context_task_id TEXT,
        messages_json TEXT DEFAULT '[]',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """)

    # 13. Flashcards
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flashcards (
        id TEXT PRIMARY KEY,
        learner_id TEXT NOT NULL,
        document_id TEXT,
        skill_code TEXT,
        front TEXT NOT NULL,
        back TEXT NOT NULL,
        confidence TEXT DEFAULT 'learning',
        review_count INTEGER DEFAULT 0,
        source_concept TEXT,
        created_at TEXT NOT NULL
    );
    """)

    # 14. Mini-Projects
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mini_projects (
        id TEXT PRIMARY KEY,
        course_id TEXT,
        skill_code TEXT NOT NULL,
        title TEXT NOT NULL,
        domain TEXT NOT NULL,
        objective TEXT NOT NULL,
        difficulty TEXT DEFAULT 'intermediate',
        estimated_hours INTEGER DEFAULT 6,
        requirements_json TEXT DEFAULT '[]',
        milestones_json TEXT DEFAULT '[]',
        rubric_json TEXT DEFAULT '[]',
        created_at TEXT NOT NULL
    );
    """)

    # 15. Project Submissions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS project_submissions (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        learner_id TEXT NOT NULL,
        submission_text TEXT NOT NULL,
        code_repo_link TEXT,
        overall_score INTEGER DEFAULT 0,
        passed INTEGER DEFAULT 0,
        rubric_scores_json TEXT DEFAULT '[]',
        feedback_json TEXT DEFAULT '{}',
        submitted_at TEXT NOT NULL
    );
    """)

    # 16. Mastery Records
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mastery_records (
        id TEXT PRIMARY KEY,
        learner_id TEXT NOT NULL,
        skill_code TEXT NOT NULL,
        proficiency_level TEXT DEFAULT 'developing',
        score REAL DEFAULT 0.0,
        confidence_score REAL DEFAULT 50.0,
        attempts_count INTEGER DEFAULT 0,
        is_verified INTEGER DEFAULT 0,
        last_evaluated_at TEXT NOT NULL,
        UNIQUE(learner_id, skill_code)
    );
    """)

    # 17. Learning Activity History
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS learning_activity_history (
        id TEXT PRIMARY KEY,
        learner_id TEXT NOT NULL,
        activity_type TEXT NOT NULL,
        title TEXT NOT NULL,
        score REAL,
        details TEXT,
        created_at TEXT NOT NULL
    );
    """)

    # 18. Student Personal Smart Notes (Course & Topic scoped)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_notes (
        id TEXT PRIMARY KEY,
        learner_id TEXT NOT NULL,
        course_id TEXT NOT NULL,
        topic_id TEXT,
        topic_title TEXT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (learner_id) REFERENCES learners(id),
        FOREIGN KEY (course_id) REFERENCES courses(id)
    );
    """)

    conn.commit()
    conn.close()

# Data seeding logic for default catalogs and 10 scenarios
def seed_initial_catalog():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if courses already exist
    cursor.execute("SELECT COUNT(*) FROM courses")
    has_courses = cursor.fetchone()[0] > 0
    cursor.execute("SELECT COUNT(*) FROM questions WHERE assessment_id = 'a-datasci-diag'")
    has_all_questions = cursor.fetchone()[0] > 0

    if has_courses and has_all_questions:
        conn.close()
        return

    now = datetime.now(timezone.utc).isoformat()

    # 1. Seed Courses
    courses = [
        {
            "id": "c-python",
            "slug": "python-programming",
            "title": "Python Programming & System Scripting",
            "description": "Master Python syntax, data structures, functional patterns, object-oriented design, and asynchronous programming.",
            "domain": "Software Development",
            "level": "Beginner to Advanced",
            "modules": [
                {"id": "m-py-1", "title": "Variables, Expressions & Types", "description": "Core data types, variable scope, operations", "skills_covered": ["PY_VARS", "PY_EXPR"], "estimated_hours": 3},
                {"id": "m-py-2", "title": "Control Flow & Iteration", "description": "Branching, loops, comprehensions", "skills_covered": ["PY_LOOPS", "PY_COMP"], "estimated_hours": 4},
                {"id": "m-py-3", "title": "Functions & Modular Architecture", "description": "Parameters, recursion, closures, generators", "skills_covered": ["PY_FUNCS", "PY_RECUR"], "estimated_hours": 5},
                {"id": "m-py-4", "title": "Error Handling & Robust I/O", "description": "Exceptions, context managers, file streams", "skills_covered": ["PY_EXCP", "PY_IO"], "estimated_hours": 4}
            ]
        },
        {
            "id": "c-fullstack",
            "slug": "full-stack-web",
            "title": "Modern Full-Stack Web Architecture",
            "description": "Build high-performance web applications using React, TypeScript, state machines, REST/GraphQL APIs, and server patterns.",
            "domain": "Web Development",
            "level": "Intermediate",
            "modules": [
                {"id": "m-fs-1", "title": "React Components & JSX", "description": "Pure components, JSX parsing, rendering trees", "skills_covered": ["REACT_COMP", "REACT_JSX"], "estimated_hours": 4},
                {"id": "m-fs-2", "title": "Hooks & Async State Lifecycle", "description": "useEffect, custom hooks, race conditions, caching", "skills_covered": ["REACT_HOOKS", "REACT_STATE"], "estimated_hours": 6},
                {"id": "m-fs-3", "title": "API Integration & Resilient Data Fetching", "description": "Axios/Fetch, query caching, error boundaries", "skills_covered": ["WEB_API", "WEB_ERR"], "estimated_hours": 5},
                {"id": "m-fs-4", "title": "Full-Stack Security & Authentication", "description": "JWT, HTTP-only cookies, CORS, RLS", "skills_covered": ["WEB_AUTH", "WEB_SEC"], "estimated_hours": 6}
            ]
        },
        {
            "id": "c-datasci",
            "slug": "data-science-ml",
            "title": "Data Science & Machine Learning Engineering",
            "description": "Data analysis, vectorization, statistical modeling, feature engineering, and neural network pipelines.",
            "domain": "Data Science & AI",
            "level": "Intermediate to Advanced",
            "modules": [
                {"id": "m-ds-1", "title": "Vectorized Operations with NumPy", "description": "Broadcasting, linear algebra operations, slicing", "skills_covered": ["DS_NUMPY", "DS_LINALG"], "estimated_hours": 5},
                {"id": "m-ds-2", "title": "Data Wrangling with Pandas", "description": "DataFrames, multi-indexing, groupby, joins", "skills_covered": ["DS_PANDAS", "DS_TRANS"], "estimated_hours": 5},
                {"id": "m-ds-3", "title": "Statistical Testing & Modeling", "description": "Hypothesis testing, p-values, regression", "skills_covered": ["DS_STATS", "DS_REGR"], "estimated_hours": 6},
                {"id": "m-ds-4", "title": "Neural Networks & Deep Learning", "description": "Perceptrons, backprop, optimizers, PyTorch", "skills_covered": ["DS_NEURAL", "DS_BACKPROP"], "estimated_hours": 8}
            ]
        },
        {
            "id": "c-ai-eng",
            "slug": "ai-engineering-llms",
            "title": "AI Engineering & Autonomous LLM Systems",
            "description": "Design production RAG systems, tool-calling agents, vector database indexing, and structured evaluation.",
            "domain": "Artificial Intelligence",
            "level": "Advanced",
            "modules": [
                {"id": "m-ai-1", "title": "Prompt Engineering & Structured Outputs", "description": "Few-shot prompting, JSON schema constraints", "skills_covered": ["AI_PROMPT", "AI_SCHEMA"], "estimated_hours": 4},
                {"id": "m-ai-2", "title": "Vector Embeddings & Semantic Search", "description": "Dense vectors, cosine similarity, hybrid search", "skills_covered": ["AI_EMBED", "AI_SEARCH"], "estimated_hours": 6},
                {"id": "m-ai-3", "title": "RAG Pipelines & Chunking Strategies", "description": "Document chunking, re-ranking, context injection", "skills_covered": ["AI_RAG", "AI_RETRIEVAL"], "estimated_hours": 7},
                {"id": "m-ai-4", "title": "Autonomous Agents & Tool Calling", "description": "ReAct loops, function calling, stateful memory", "skills_covered": ["AI_AGENTS", "AI_TOOLS"], "estimated_hours": 8}
            ]
        }
    ]

    for c in courses:
        cursor.execute("""
        INSERT OR IGNORE INTO courses (id, slug, title, description, domain, level, modules_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (c["id"], c["slug"], c["title"], c["description"], c["domain"], c["level"], json.dumps(c["modules"]), now))

    # 2. Seed Skills
    skills_data = [
        # Python
        ("PY_VARS", "Variables & Primitive Types", "Fundamentals", "Understanding variable assignment, mutability, and primitive scalar types.", "beginner", "c-python", []),
        ("PY_EXPR", "Expressions & Boolean Logic", "Fundamentals", "Evaluating relational operators, truthiness, and boolean expressions.", "beginner", "c-python", ["PY_VARS"]),
        ("PY_LOOPS", "Loops & Iteration Controls", "Control Flow", "Writing for/while loops, break/continue statements, and iterators.", "beginner", "c-python", ["PY_EXPR"]),
        ("PY_COMP", "List Comprehensions & Generators", "Control Flow", "Transforming sequences with idiomatic comprehension syntax.", "intermediate", "c-python", ["PY_LOOPS"]),
        ("PY_FUNCS", "Functions & Scope Isolation", "Modularity", "Defining pure functions, default parameters, and LEGB variable scope.", "intermediate", "c-python", ["PY_EXPR"]),
        ("PY_RECUR", "Recursive Problem Solving", "Algorithms", "Solving divide-and-conquer problems using base and recursive cases.", "intermediate", "c-python", ["PY_FUNCS"]),
        ("PY_EXCP", "Exception Handling & Cleanup", "Reliability", "Using try/except/finally and custom domain exceptions.", "intermediate", "c-python", ["PY_FUNCS"]),
        
        # React & Web
        ("REACT_COMP", "React Component Composition", "Frontend", "Building reusable presentational and container components with props.", "beginner", "c-fullstack", []),
        ("REACT_JSX", "JSX Syntax & Virtual DOM", "Frontend", "Understanding JSX compilation, key reconciliation, and virtual DOM diffing.", "beginner", "c-fullstack", ["REACT_COMP"]),
        ("REACT_STATE", "State Management & Reactivity", "Frontend", "Managing local state using useState and useReducer correctly.", "intermediate", "c-fullstack", ["REACT_JSX"]),
        ("REACT_HOOKS", "Hooks Lifecycle & useEffect", "Frontend", "Synchronizing side effects, managing dependency arrays, and preventing race conditions.", "intermediate", "c-fullstack", ["REACT_STATE"]),
        ("WEB_API", "Async API Client Integration", "Networking", "Fetching remote data with cancellation, status management, and caching.", "intermediate", "c-fullstack", ["REACT_HOOKS"]),
        ("WEB_ERR", "Client-Side Error Boundaries", "Reliability", "Gracefully capturing UI runtime faults without unmounting the whole tree.", "intermediate", "c-fullstack", ["REACT_COMP"]),

        # Data Science
        ("DS_NUMPY", "NumPy Vectorized Array Ops", "Computation", "Performing element-wise operations without explicit python loops.", "intermediate", "c-datasci", ["PY_FUNCS"]),
        ("DS_PANDAS", "Pandas Indexing & Aggregations", "Data Analysis", "Querying, masking, and aggregating structured tabular datasets.", "intermediate", "c-datasci", ["DS_NUMPY"]),
        ("DS_STATS", "Statistical Hypothesis Testing", "Mathematics", "Applying null hypothesis testing, z-tests, t-tests, and p-value calculation.", "intermediate", "c-datasci", ["DS_PANDAS"]),
        ("DS_NEURAL", "Neural Network Architecture", "Deep Learning", "Constructing forward pass math with weights, biases, and activation layers.", "advanced", "c-datasci", ["DS_NUMPY"]),

        # AI Engineering
        ("AI_PROMPT", "Structured Prompt Engineering", "AI Systems", "Crafting system instructions, dynamic few-shot exemplars, and delimiters.", "intermediate", "c-ai-eng", []),
        ("AI_EMBED", "Vector Embeddings & Similarity", "AI Systems", "Generating embeddings, distance metrics (cosine/dot), and vector indexing.", "intermediate", "c-ai-eng", ["AI_PROMPT"]),
        ("AI_RAG", "Retrieval-Augmented Generation", "AI Systems", "Grounding LLM reasoning with external document chunks and re-ranking.", "advanced", "c-ai-eng", ["AI_EMBED"]),
        ("AI_AGENTS", "Autonomous Agent Tool Calling", "AI Systems", "Building deterministic agent loops with ReAct patterns and function calling.", "advanced", "c-ai-eng", ["AI_RAG"])
    ]

    for code, name, cat, desc, diff, cid, prereqs in skills_data:
        sid = f"skill-{code.lower()}"
        cursor.execute("""
        INSERT OR IGNORE INTO skills (id, course_id, code, name, category, description, difficulty, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (sid, cid, code, name, cat, desc, diff, now))
        for p in prereqs:
            cursor.execute("""
            INSERT OR IGNORE INTO skill_prerequisites (id, skill_id, prerequisite_code)
            VALUES (?, ?, ?)
            """, (str(uuid.uuid4()), sid, p))

    # 3. Seed Diagnostic Assessments & Questions
    assessments_info = [
        {"id": "a-python-diag", "course_id": "c-python", "title": "Python Core Diagnostic Assessment", "description": "Evaluate understanding of Python syntax, loops, functions, and recursion."},
        {"id": "a-react-diag", "course_id": "c-fullstack", "title": "React & Web Architecture Diagnostic", "description": "Measure proficiency with JSX, hooks, state synchronization, and async data."},
        {"id": "a-datasci-diag", "course_id": "c-datasci", "title": "Data Science & Numerical Diagnostic", "description": "Assess matrix math, vectorized logic, slicing, and statistical foundations."},
        {"id": "a-ai-diag", "course_id": "c-ai-eng", "title": "AI Engineering Diagnostic Assessment", "description": "Verify embeddings, retrieval architectures, context windows, and tool schemas."}
    ]

    for a in assessments_info:
        cursor.execute("""
        INSERT OR IGNORE INTO assessments (id, course_id, title, type, description, total_questions, created_at)
        VALUES (?, ?, ?, 'diagnostic', ?, 5, ?)
        """, (a["id"], a["course_id"], a["title"], a["description"], now))

    # Diagnostic Questions with Predefined Answer Keys and Detailed Rubrics
    diagnostic_questions = [
        # Python Diagnostic Questions
        {
            "id": "q-py-1",
            "assessment_id": "a-python-diag",
            "skill_code": "PY_VARS",
            "prompt": "In Python, which of the following variables will hold a mutable object?",
            "question_type": "mcq",
            "difficulty": "beginner",
            "options": [
                {"id": "A", "text": "x = (1, 2, 3)"},
                {"id": "B", "text": "x = 'skillforge'"},
                {"id": "C", "text": "x = [1, 2, 3]"},
                {"id": "D", "text": "x = 42"}
            ],
            "answer_key": "C",
            "hints": ["Tuples, strings, and integers are immutable in Python.", "Look for brackets indicating a list."],
            "explanation": "Lists are mutable in Python; items can be appended or modified in-place. Tuples, strings, and integers are strictly immutable."
        },
        {
            "id": "q-py-2",
            "assessment_id": "a-python-diag",
            "skill_code": "PY_EXPR",
            "prompt": "What does the expression `bool([] or None or '0')` evaluate to in Python?",
            "question_type": "mcq",
            "difficulty": "beginner",
            "options": [
                {"id": "A", "text": "False"},
                {"id": "B", "text": "True"},
                {"id": "C", "text": "None"},
                {"id": "D", "text": "Raises a TypeError"}
            ],
            "answer_key": "B",
            "hints": ["Evaluate short-circuiting from left to right.", "An empty list is falsy, None is falsy, but a non-empty string is truthy."],
            "explanation": "`[]` and `None` are falsy. `'0'` is a non-empty string, which is truthy. Hence `or` evaluates to `'0'`, and `bool('0')` is `True`."
        },
        {
            "id": "q-py-3",
            "assessment_id": "a-python-diag",
            "skill_code": "PY_LOOPS",
            "prompt": "What is the output of:\n```python\ntotal = 0\nfor i in range(1, 5):\n    if i % 2 == 0:\n        continue\n    total += i\nprint(total)\n```",
            "question_type": "mcq",
            "difficulty": "beginner",
            "options": [
                {"id": "A", "text": "4"},
                {"id": "B", "text": "10"},
                {"id": "C", "text": "6"},
                {"id": "D", "text": "15"}
            ],
            "answer_key": "A",
            "hints": ["range(1, 5) generates 1, 2, 3, 4.", "Even numbers are skipped due to continue."],
            "explanation": "Numbers 2 and 4 are skipped by `continue`. The loop sums 1 + 3 = 4."
        },
        {
            "id": "q-py-4",
            "assessment_id": "a-python-diag",
            "skill_code": "PY_FUNCS",
            "prompt": "What will calling `foo()` output?\n```python\nx = 10\ndef foo():\n    x = 20\n    return x\nprint(foo(), x)\n```",
            "question_type": "mcq",
            "difficulty": "intermediate",
            "options": [
                {"id": "A", "text": "20 20"},
                {"id": "B", "text": "20 10"},
                {"id": "C", "text": "10 10"},
                {"id": "D", "text": "UnboundLocalError"}
            ],
            "answer_key": "B",
            "hints": ["Inside `foo()`, `x = 20` creates a local variable in the function's scope.", "The global `x` remains unchanged."],
            "explanation": "`foo()` defines a local variable `x` without the `global` keyword. It returns 20, while the outer global variable `x` remains 10."
        },
        {
            "id": "q-py-5",
            "assessment_id": "a-python-diag",
            "skill_code": "PY_RECUR",
            "prompt": "What is the critical requirement of every valid recursive function to prevent a stack overflow?",
            "question_type": "mcq",
            "difficulty": "intermediate",
            "options": [
                {"id": "A", "text": "A while loop wrapping the recursive call"},
                {"id": "B", "text": "A base case condition that returns without recursing"},
                {"id": "C", "text": "A global variable tracking memory addresses"},
                {"id": "D", "text": "Type hints on all arguments"}
            ],
            "answer_key": "B",
            "hints": ["Recursion needs a stopping point.", "Without this termination condition, Python hits `RecursionError`."],
            "explanation": "A base case is mandatory to terminate recursion when a minimal condition is satisfied, preventing unbounded call stack growth."
        },

        # React Diagnostic Questions
        {
            "id": "q-react-1",
            "assessment_id": "a-react-diag",
            "skill_code": "REACT_COMP",
            "prompt": "In React, why must components remain pure with respect to their props?",
            "question_type": "mcq",
            "difficulty": "beginner",
            "options": [
                {"id": "A", "text": "So that React can safely re-render components with predictable UI output for the same input props"},
                {"id": "B", "text": "Because JavaScript does not allow modifying objects in memory"},
                {"id": "C", "text": "To enforce asynchronous rendering in single-threaded environments"},
                {"id": "D", "text": "Because Tailwind CSS requires immutable class names"}
            ],
            "answer_key": "A",
            "hints": ["Think about predictable rendering and avoiding hidden side effects."],
            "explanation": "React components must behave like pure functions with respect to their props so renders are idempotent and deterministic."
        },
        {
            "id": "q-react-2",
            "assessment_id": "a-react-diag",
            "skill_code": "REACT_STATE",
            "prompt": "What is wrong with the following snippet?\n```javascript\nconst [count, setCount] = useState(0);\nconst handleClick = () => {\n  setCount(count + 1);\n  setCount(count + 1);\n};\n```",
            "question_type": "mcq",
            "difficulty": "intermediate",
            "options": [
                {"id": "A", "text": "It throws a syntax error"},
                {"id": "B", "text": "Both calls use the same stale `count` in the current render closure, incrementing count only once by 1"},
                {"id": "C", "text": "It triggers infinite re-renders immediately"},
                {"id": "D", "text": "State can only be updated inside useEffect"}
            ],
            "answer_key": "B",
            "hints": ["Consider how closure values work during an event handler execution.", "Use functional update `c => c + 1` if you need sequential increments."],
            "explanation": "Because `count` is captured in the event handler's closure, both `setCount(0 + 1)` set the next state to 1. Using `setCount(prev => prev + 1)` avoids stale state."
        },
        {
            "id": "q-react-3",
            "assessment_id": "a-react-diag",
            "skill_code": "REACT_HOOKS",
            "prompt": "In a `useEffect` hook that fetches data based on a `userId` prop, what is the best practice to prevent setting state on an unmounted component or handling race conditions?",
            "question_type": "mcq",
            "difficulty": "intermediate",
            "options": [
                {"id": "A", "text": "Omit userId from the dependency array"},
                {"id": "B", "text": "Use an `isMounted` flag or AbortController inside the effect cleanup function"},
                {"id": "C", "text": "Wrap the fetch call in a setTimeout of 1000ms"},
                {"id": "D", "text": "Call `forceUpdate()` on the window object"}
            ],
            "answer_key": "B",
            "hints": ["Effects can return a cleanup function.", "AbortController can cancel in-flight HTTP requests."],
            "explanation": "Returning a cleanup function with an active cancellation token or AbortController ensures previous network responses are discarded when dependencies change."
        },
        {
            "id": "q-react-4",
            "assessment_id": "a-react-diag",
            "skill_code": "WEB_API",
            "prompt": "Which HTTP status code should your backend return when a learner submits invalid form data violating schema validation?",
            "question_type": "mcq",
            "difficulty": "beginner",
            "options": [
                {"id": "A", "text": "500 Internal Server Error"},
                {"id": "B", "text": "404 Not Found"},
                {"id": "C", "text": "422 Unprocessable Content (or 400 Bad Request)"},
                {"id": "D", "text": "301 Moved Permanently"}
            ],
            "answer_key": "C",
            "hints": ["4xx represents client errors, while 5xx represents unhandled server errors."],
            "explanation": "422 (or 400) indicates that the server understands the request entity syntax but cannot process the contained instructions due to validation errors."
        },
        {
            "id": "q-react-5",
            "assessment_id": "a-react-diag",
            "skill_code": "WEB_ERR",
            "prompt": "Which lifecycle method or React construct is required to catch JavaScript rendering errors in child component trees?",
            "question_type": "mcq",
            "difficulty": "intermediate",
            "options": [
                {"id": "A", "text": "A Class component implementing `componentDidCatch` or `static getDerivedStateFromError`"},
                {"id": "B", "text": "A standard try/catch block inside JSX tags"},
                {"id": "C", "text": "The `window.onerror` event listener in index.html"},
                {"id": "D", "text": "A React.memo wrapper"}
            ],
            "answer_key": "A",
            "hints": ["Functional components cannot currently define error boundaries directly without class methods or a helper library."],
            "explanation": "Error boundaries must be implemented using class components with `static getDerivedStateFromError` and/or `componentDidCatch` to trap render-phase errors."
        },
        # Data Science Diagnostic Questions
        {
            "id": "q-ds-1",
            "assessment_id": "a-datasci-diag",
            "skill_code": "DS_NUMPY",
            "prompt": "When can two NumPy arrays be broadcast together according to NumPy broadcasting rules?",
            "question_type": "mcq",
            "difficulty": "intermediate",
            "options": [
                {"id": "A", "text": "Only when both arrays have the exact same shape in every dimension"},
                {"id": "B", "text": "When their trailing dimensions are equal or one of them is 1"},
                {"id": "C", "text": "Whenever the total number of elements in both arrays is identical"},
                {"id": "D", "text": "Broadcasting only works between 1D vectors and scalar constants"}
            ],
            "answer_key": "B",
            "hints": ["NumPy compares dimensions element-wise starting from trailing (rightmost) dimensions.", "A dimension of size 1 can stretch to match the other array."],
            "explanation": "Two dimensions are compatible when they are equal or one of them is 1. Dimensions are compared starting from the rightmost dimension."
        },
        {
            "id": "q-ds-2",
            "assessment_id": "a-datasci-diag",
            "skill_code": "DS_PANDAS",
            "prompt": "What is the primary difference between `.loc` and `.iloc` indexing in a Pandas DataFrame?",
            "question_type": "mcq",
            "difficulty": "beginner",
            "options": [
                {"id": "A", "text": "`.loc` is label-based while `.iloc` is integer position-based"},
                {"id": "B", "text": "`.loc` modifies data in place while `.iloc` creates a deep copy"},
                {"id": "C", "text": "`.loc` only works on columns while `.iloc` only works on rows"},
                {"id": "D", "text": "There is no difference; they are interchangeable aliases"}
            ],
            "answer_key": "A",
            "hints": ["Think about labels/names vs zero-based integer offsets."],
            "explanation": "`.loc` accesses data by row/column index labels, while `.iloc` accesses data strictly by integer ordinal positions (0, 1, 2...)."
        },
        {
            "id": "q-ds-3",
            "assessment_id": "a-datasci-diag",
            "skill_code": "DS_STATS",
            "prompt": "In hypothesis testing with a significance threshold of alpha = 0.05, what does a p-value of 0.02 indicate?",
            "question_type": "mcq",
            "difficulty": "intermediate",
            "options": [
                {"id": "A", "text": "The null hypothesis has a 98% probability of being true"},
                {"id": "B", "text": "Reject the null hypothesis because the observed result is statistically significant at the 5% level"},
                {"id": "C", "text": "Fail to reject the null hypothesis because p < alpha"},
                {"id": "D", "text": "The statistical test was inconclusive and must be discarded"}
            ],
            "answer_key": "B",
            "hints": ["When p-value < alpha, the data is unlikely to have arisen solely under the null hypothesis."],
            "explanation": "Since the p-value (0.02) is less than alpha (0.05), we reject the null hypothesis in favor of the alternative hypothesis."
        },
        {
            "id": "q-ds-4",
            "assessment_id": "a-datasci-diag",
            "skill_code": "DS_NEURAL",
            "prompt": "Why is the ReLU (Rectified Linear Unit) activation function commonly preferred over Sigmoid in deep hidden layers?",
            "question_type": "mcq",
            "difficulty": "advanced",
            "options": [
                {"id": "A", "text": "ReLU mitigates the vanishing gradient problem for positive activations and is computationally efficient"},
                {"id": "B", "text": "ReLU bounds all outputs strictly between 0 and 1"},
                {"id": "C", "text": "ReLU is always smooth and infinitely differentiable at 0"},
                {"id": "D", "text": "ReLU eliminates the need for backpropagation entirely"}
            ],
            "answer_key": "A",
            "hints": ["Consider what happens to the derivative of Sigmoid for very large inputs."],
            "explanation": "Sigmoid saturates at 0 and 1, causing gradients to vanish during backpropagation. ReLU has a constant derivative of 1 for positive inputs, mitigating vanishing gradients."
        },
        {
            "id": "q-ds-5",
            "assessment_id": "a-datasci-diag",
            "skill_code": "DS_NUMPY",
            "prompt": "What does `np.dot(A, B)` compute when `A` has shape (3, 4) and `B` has shape (4, 2)?",
            "question_type": "mcq",
            "difficulty": "intermediate",
            "options": [
                {"id": "A", "text": "A matrix with shape (3, 2)"},
                {"id": "B", "text": "A matrix with shape (4, 4)"},
                {"id": "C", "text": "A scalar sum of element-wise products"},
                {"id": "D", "text": "Raises a ValueError because dimensions do not match exactly"}
            ],
            "answer_key": "A",
            "hints": ["Inner dimensions must match: (3, 4) x (4, 2) results in the outer dimensions."],
            "explanation": "Matrix multiplication of (M, K) with (K, N) produces a matrix of shape (M, N). Here, (3, 4) x (4, 2) yields shape (3, 2)."
        },
        # AI Engineering Diagnostic Questions
        {
            "id": "q-ai-1",
            "assessment_id": "a-ai-diag",
            "skill_code": "AI_PROMPT",
            "prompt": "What is the primary benefit of Few-Shot Prompting compared to Zero-Shot Prompting for LLMs?",
            "question_type": "mcq",
            "difficulty": "intermediate",
            "options": [
                {"id": "A", "text": "It permanently fine-tunes the underlying neural network model weights"},
                {"id": "B", "text": "It grounds the model's pattern recognition using explicit input-output demonstration examples"},
                {"id": "C", "text": "It reduces token consumption and context window usage"},
                {"id": "D", "text": "It bypasses the need for system instructions and temperature settings"}
            ],
            "answer_key": "B",
            "hints": ["Few-shot gives the model examples inside the context window before asking for the actual target response."],
            "explanation": "Few-shot prompting provides contextual demonstration exemplars that steer format, reasoning structure, and output consistency without weight updates."
        },
        {
            "id": "q-ai-2",
            "assessment_id": "a-ai-diag",
            "skill_code": "AI_EMBED",
            "prompt": "When comparing two unit-normalized vector embeddings in a vector database, why is Cosine Similarity equivalent to Dot Product?",
            "question_type": "mcq",
            "difficulty": "intermediate",
            "options": [
                {"id": "A", "text": "Because the product of their norms (magnitudes) is exactly 1"},
                {"id": "B", "text": "Because high-dimensional spaces ignore vector direction"},
                {"id": "C", "text": "Because dot product only works on orthogonal matrices"},
                {"id": "D", "text": "Because cosine similarity cannot be calculated in Euclidean spaces"}
            ],
            "answer_key": "A",
            "hints": ["Cosine similarity = (A . B) / (||A|| * ||B||). What is ||A|| * ||B|| when vectors have unit length?"],
            "explanation": "Since both vectors have unit length (norm = 1), the denominator `||A|| * ||B||` is 1, making `cos(theta) = A . B`."
        },
        {
            "id": "q-ai-3",
            "assessment_id": "a-ai-diag",
            "skill_code": "AI_RAG",
            "prompt": "In a Retrieval-Augmented Generation (RAG) pipeline, why is chunk overlap (e.g. 50-100 tokens) recommended when splitting documents?",
            "question_type": "mcq",
            "difficulty": "advanced",
            "options": [
                {"id": "A", "text": "To double the storage efficiency of the vector index"},
                {"id": "B", "text": "To ensure semantic context at sentence boundaries is preserved across neighboring chunks"},
                {"id": "C", "text": "To speed up approximate nearest neighbor (ANN) retrieval latency"},
                {"id": "D", "text": "To allow the embedding model to skip stop words"}
            ],
            "answer_key": "B",
            "hints": ["If an important concept or sentence is split cleanly across two chunks, context can be lost."],
            "explanation": "Chunk overlap prevents critical semantic context, relationships, or sentences from being severed at hard chunk boundaries."
        },
        {
            "id": "q-ai-4",
            "assessment_id": "a-ai-diag",
            "skill_code": "AI_AGENTS",
            "prompt": "What core execution cycle characterizes the ReAct (Reasoning + Acting) agent pattern?",
            "question_type": "mcq",
            "difficulty": "advanced",
            "options": [
                {"id": "A", "text": "Thought -> Action -> Observation loop until the final objective is accomplished"},
                {"id": "B", "text": "Pre-training -> Fine-tuning -> RLHF evaluation"},
                {"id": "C", "text": "Prompt -> Static Response without tool interaction"},
                {"id": "D", "text": "Embedding generation -> Cosine ranking -> Direct response"}
            ],
            "answer_key": "A",
            "hints": ["ReAct alternates between generating reasoning thoughts and executing tool actions with environmental observations."],
            "explanation": "The ReAct loop interleaves explicit reasoning traces ('Thought'), tool invocation ('Action'), and tool response processing ('Observation')."
        },
        {
            "id": "q-ai-5",
            "assessment_id": "a-ai-diag",
            "skill_code": "AI_PROMPT",
            "prompt": "Which open standard is used by LLM function calling frameworks (such as Gemini and OpenAI) to define structured tool arguments?",
            "question_type": "mcq",
            "difficulty": "intermediate",
            "options": [
                {"id": "A", "text": "JSON Schema"},
                {"id": "B", "text": "XML DTD"},
                {"id": "C", "text": "YAML 1.2 Syntax"},
                {"id": "D", "text": "GraphQL Type Definition"}
            ],
            "answer_key": "A",
            "hints": ["It defines properties, types ('string', 'number', 'object'), required arrays, and descriptions in JSON."],
            "explanation": "Tool schemas and function definitions use JSON Schema specifications to enforce parameter names, types, descriptions, and required constraints."
        }
    ]

    for q in diagnostic_questions:
        cursor.execute("""
        INSERT OR REPLACE INTO questions (id, assessment_id, skill_code, prompt, question_type, difficulty, options_json, answer_key, hints_json, explanation, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (q["id"], q["assessment_id"], q["skill_code"], q["prompt"], q["question_type"], q["difficulty"], json.dumps(q["options"]), q["answer_key"], json.dumps(q["hints"]), q["explanation"], now))

    # 4. Seed Mini-Projects Catalog
    projects = [
        {
            "id": "p-py-cli",
            "course_id": "c-python",
            "skill_code": "PY_FUNCS",
            "title": "Interactive CLI Task & Study Tracker",
            "domain": "Python Programming",
            "objective": "Build a modular command-line application that manages learner study sessions with persistent JSON storage, input validation, and clean functional architecture.",
            "difficulty": "beginner",
            "estimated_hours": 4,
            "requirements": [
                "Implement robust command parsing with arguments",
                "Store tasks and time logs in structured JSON files",
                "Handle invalid inputs with informative domain errors",
                "Write pure utility functions with type hints"
            ],
            "milestones": [
                {"id": "m1", "title": "Architecture & Schema Setup", "description": "Define data structures and file read/write helpers", "is_completed": False},
                {"id": "m2", "title": "Core CLI Operations", "description": "Implement add, complete, list, and filter commands", "is_completed": False},
                {"id": "m3", "title": "Error Handling & Logging", "description": "Trap missing file errors and corrupt data gracefully", "is_completed": False}
            ],
            "rubric": [
                {"criterion": "Code Modularity & Purity", "weight": 35, "description": "Separation of concerns between CLI UI, file I/O, and business logic"},
                {"criterion": "Error Handling & Resilience", "weight": 35, "description": "Graceful handling of edge cases without stack crashes"},
                {"criterion": "Documentation & Types", "weight": 30, "description": "Clear docstrings, PEP 8 compliance, and type annotations"}
            ]
        },
        {
            "id": "p-react-kanban",
            "course_id": "c-fullstack",
            "skill_code": "REACT_HOOKS",
            "title": "Adaptive Kanban Task Board with Optimistic UI",
            "domain": "Full-Stack Web",
            "objective": "Design an interactive Kanban board with column swimlanes, drag-and-drop state transitions, optimistic local updates, and persistent localStorage sync.",
            "difficulty": "intermediate",
            "estimated_hours": 6,
            "requirements": [
                "Custom hook `useKanban` managing state transitions",
                "Optimistic UI updates with rollback on network errors",
                "Accessible keyboard navigation and drag indicators",
                "Clean component hierarchy and memoization where needed"
            ],
            "milestones": [
                {"id": "mk1", "title": "Board Layout & Columns", "description": "Design responsive Neo-Brutalist cards and columns", "is_completed": False},
                {"id": "mk2", "title": "State Transitions & Custom Hooks", "description": "Implement task move, edit, and status updates", "is_completed": False},
                {"id": "mk3", "title": "Optimistic Synchronization", "description": "Add localStorage fallback and simulate server sync", "is_completed": False}
            ],
            "rubric": [
                {"criterion": "Hook Architecture & State Safety", "weight": 40, "description": "Clean separation of state logic avoiding race conditions"},
                {"criterion": "UI Polish & Accessibility", "weight": 30, "description": "Keyboard accessible, clear states, high contrast layout"},
                {"criterion": "Error Handling & Edge Cases", "weight": 30, "description": "No broken states when manipulating empty columns or duplicate IDs"}
            ]
        },
        {
            "id": "p-ai-rag-agent",
            "course_id": "c-ai-eng",
            "skill_code": "AI_AGENTS",
            "title": "Autonomous Course Syllabus RAG Agent",
            "domain": "AI Engineering",
            "objective": "Construct an end-to-end question-answering agent that chunks syllabus documents, indexes vector embeddings, retrieves relevant context, and executes tool calls.",
            "difficulty": "advanced",
            "estimated_hours": 8,
            "requirements": [
                "Document chunking pipeline with configurable token overlap",
                "Cosine similarity vector index calculation",
                "Structured prompt template with citation grounding",
                "Tool-calling router to execute diagnostic queries"
            ],
            "milestones": [
                {"id": "ma1", "title": "Chunking & Vector Indexing", "description": "Process documents into chunk embeddings", "is_completed": False},
                {"id": "ma2", "title": "Semantic Retrieval Pipeline", "description": "Return top-k relevant chunks with similarity scores", "is_completed": False},
                {"id": "ma3", "title": "ReAct Tool Execution", "description": "Agent loop calling search and calculator tools", "is_completed": False}
            ],
            "rubric": [
                {"criterion": "Retrieval Precision & Chunking", "weight": 35, "description": "Effective chunk overlap avoiding hallucinated boundaries"},
                {"criterion": "Tool Calling Protocol & Schemas", "weight": 35, "description": "Robust argument parsing and defensive error handling"},
                {"criterion": "Evaluation & Grounding Verification", "weight": 30, "description": "Verifiable citations referencing source document excerpts"}
            ]
        }
    ]

    for p in projects:
        cursor.execute("""
        INSERT OR IGNORE INTO mini_projects (id, course_id, skill_code, title, domain, objective, difficulty, estimated_hours, requirements_json, milestones_json, rubric_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["course_id"], p["skill_code"], p["title"], p["domain"], p["objective"], p["difficulty"], p["estimated_hours"], json.dumps(p["requirements"]), json.dumps(p["milestones"]), json.dumps(p["rubric"]), now))

    conn.commit()
    conn.close()

seed_initial_catalog()
