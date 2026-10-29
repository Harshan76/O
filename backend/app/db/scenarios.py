import json
import uuid
from datetime import datetime, timezone
from app.db.storage import get_connection

DEMO_SCENARIOS = {
    "1": {
        "id": "1",
        "title": "Beginner with weak prerequisites",
        "learner_name": "Maya Chen",
        "email": "maya@demo.skillforge.ai",
        "goal_title": "Master Python Programming",
        "domain": "Software Development",
        "experience_level": "beginner",
        "daily_minutes": 30,
        "learning_style": "hands-on",
        "overall_mastery": 28.0,
        "current_streak": 2,
        "longest_streak": 4,
        "total_study_hours": 6.5,
        "skills_state": [
            {"code": "PY_VARS", "name": "Variables & Primitive Types", "category": "Fundamentals", "difficulty": "beginner", "status": "weak", "score": 42.0, "prerequisites": [], "recommended_action": "Revisit scalar types and variable reassignment rules"},
            {"code": "PY_EXPR", "name": "Expressions & Boolean Logic", "category": "Fundamentals", "difficulty": "beginner", "status": "missing_prereq", "score": 30.0, "prerequisites": ["PY_VARS"], "recommended_action": "Complete foundational Boolean logic before loops"},
            {"code": "PY_LOOPS", "name": "Loops & Iteration Controls", "category": "Control Flow", "difficulty": "beginner", "status": "missing_prereq", "score": 20.0, "prerequisites": ["PY_EXPR"], "recommended_action": "Prerequisite gate: Pass expressions quiz first"},
            {"code": "PY_FUNCS", "name": "Functions & Scope Isolation", "category": "Modularity", "difficulty": "intermediate", "status": "validating", "score": 15.0, "prerequisites": ["PY_EXPR"], "recommended_action": "Pending prerequisite completion"}
        ],
        "active_task": {
            "id": "task-demo-1",
            "skill_code": "PY_VARS",
            "title": "Step 1: Foundational Variable Mutability & Types",
            "learning_objective": "Distinguish between mutable and immutable Python objects to avoid unintended state bugs.",
            "difficulty": "beginner",
            "instructions": "Declare a list `items = [10, 20]`, append the number 30 to it, and demonstrate that its `id()` remains unchanged.",
            "hints": ["Lists are mutable, so `.append()` modifies in place.", "Check the output of `id(items)` before and after append."],
            "expected_result": "A modified list [10, 20, 30] retaining its initial memory identity.",
            "evaluation_criteria": "Correct mutation syntax without re-instantiating the collection.",
            "estimated_duration": 15,
            "reason_for_recommendation": "Diagnostic score of 42% indicates weak familiarity with mutable references.",
            "task_type": "challenge",
            "status": "in_progress",
            "order_index": 1
        },
        "chat_initial": [
            {"id": "msg-1", "sender": "tutor", "text": "Hi Maya! Welcome to SkillForge AI. I reviewed your diagnostic assessment: you're off to a solid start, but we noticed a gap in Python variable mutability and truthiness expressions. Don't worry—we will take it step-by-step so you master the fundamentals before moving on to loops!", "timestamp": "10:00 AM", "suggested_followups": ["Explain variable mutability simply", "Give me a real-world example", "Why is this a prerequisite for loops?"]}
        ],
        "description": "Simulates a beginner who attempted the diagnostic assessment and struggled with core types. The adaptive engine immediately reroutes the learning path to reinforce prerequisites."
    },
    "2": {
        "id": "2",
        "title": "Intermediate learner with a specific skill gap",
        "learner_name": "Jordan Lee",
        "email": "jordan@demo.skillforge.ai",
        "goal_title": "Modern Full-Stack React Architecture",
        "domain": "Web Development",
        "experience_level": "intermediate",
        "daily_minutes": 45,
        "learning_style": "conceptual",
        "overall_mastery": 72.5,
        "current_streak": 6,
        "longest_streak": 14,
        "total_study_hours": 24.0,
        "skills_state": [
            {"code": "REACT_COMP", "name": "React Component Composition", "category": "Frontend", "difficulty": "beginner", "status": "strong", "score": 92.0, "prerequisites": [], "recommended_action": "Demonstrated mastery verified"},
            {"code": "REACT_JSX", "name": "JSX Syntax & Virtual DOM", "category": "Frontend", "difficulty": "beginner", "status": "strong", "score": 88.0, "prerequisites": ["REACT_COMP"], "recommended_action": "Demonstrated mastery verified"},
            {"code": "REACT_STATE", "name": "State Management & Reactivity", "category": "Frontend", "difficulty": "intermediate", "status": "strong", "score": 84.0, "prerequisites": ["REACT_JSX"], "recommended_action": "Demonstrated mastery verified"},
            {"code": "REACT_HOOKS", "name": "Hooks Lifecycle & useEffect", "category": "Frontend", "difficulty": "intermediate", "status": "weak", "score": 48.0, "prerequisites": ["REACT_STATE"], "recommended_action": "Targeted practice on useEffect dependency arrays and race conditions"},
            {"code": "WEB_API", "name": "Async API Client Integration", "category": "Networking", "difficulty": "intermediate", "status": "validating", "score": 60.0, "prerequisites": ["REACT_HOOKS"], "recommended_action": "Awaiting hook synchronization mastery"}
        ],
        "active_task": {
            "id": "task-demo-2",
            "skill_code": "REACT_HOOKS",
            "title": "Targeted Lab: Fixing Async Race Conditions in useEffect",
            "learning_objective": "Implement an AbortController cleanup pattern inside a React effect to cancel outdated network requests.",
            "difficulty": "intermediate",
            "instructions": "In a component accepting `userId`, construct a `useEffect` that creates an `AbortController`, passes its signal to fetch, and cancels the request on unmount or ID change.",
            "hints": ["Return an arrow function from useEffect to serve as cleanup.", "Call `controller.abort()` inside the cleanup."],
            "expected_result": "No state update attempted after unmount or rapid prop changes.",
            "evaluation_criteria": "Correct lifecycle cleanup without memory leaks or race conditions.",
            "estimated_duration": 25,
            "reason_for_recommendation": "Strong score (88%) on components and state, but diagnostic identified a 48% gap specifically in effect cleanup.",
            "task_type": "challenge",
            "status": "in_progress",
            "order_index": 4
        },
        "chat_initial": [
            {"id": "msg-1", "sender": "tutor", "text": "Hey Jordan! Your component architecture and state management are top notch. However, in the diagnostic, multiple requests overwrote each other due to missing cleanup in useEffect. Let's tackle that specific pattern today so your apps never suffer from stale data!", "timestamp": "11:15 AM", "suggested_followups": ["Explain race conditions with an analogy", "Give me a hint, not the answer", "Show me a test case"]}
        ],
        "description": "Simulates an intermediate developer with strong foundations who has an isolated blind spot in asynchronous React hooks."
    },
    "3": {
        "id": "3",
        "title": "Advanced learner ready for a complex project",
        "learner_name": "Elena Rostova",
        "email": "elena@demo.skillforge.ai",
        "goal_title": "AI Engineering & Autonomous LLM Systems",
        "domain": "Artificial Intelligence",
        "experience_level": "advanced",
        "daily_minutes": 60,
        "learning_style": "project-based",
        "overall_mastery": 91.5,
        "current_streak": 18,
        "longest_streak": 25,
        "total_study_hours": 48.0,
        "skills_state": [
            {"code": "AI_PROMPT", "name": "Structured Prompt Engineering", "category": "AI Systems", "difficulty": "intermediate", "status": "strong", "score": 96.0, "prerequisites": [], "recommended_action": "Mastery confirmed"},
            {"code": "AI_EMBED", "name": "Vector Embeddings & Similarity", "category": "AI Systems", "difficulty": "intermediate", "status": "strong", "score": 92.0, "prerequisites": ["AI_PROMPT"], "recommended_action": "Mastery confirmed"},
            {"code": "AI_RAG", "name": "Retrieval-Augmented Generation", "category": "AI Systems", "difficulty": "advanced", "status": "strong", "score": 89.0, "prerequisites": ["AI_EMBED"], "recommended_action": "Mastery confirmed"},
            {"code": "AI_AGENTS", "name": "Autonomous Agent Tool Calling", "category": "AI Systems", "difficulty": "advanced", "status": "strong", "score": 88.0, "prerequisites": ["AI_RAG"], "recommended_action": "Ready for Capstone Architecture"}
        ],
        "active_task": {
            "id": "task-demo-3",
            "skill_code": "AI_AGENTS",
            "title": "Capstone: Autonomous Course Syllabus RAG Agent",
            "learning_objective": "Architect a multi-turn autonomous agent with dynamic vector retrieval, citation grounding, and tool execution.",
            "difficulty": "advanced",
            "instructions": "Implement the complete 3-tier syllabus agent adhering to the project rubric: chunking overlap, cosine similarity top-3 retrieval, and verified citations.",
            "hints": ["Ensure chunk token overlap is between 15-20% to avoid cut-off definitions.", "Enforce schema validation on tool calling return objects."],
            "expected_result": "A production-grade Python/TypeScript agent module returning verifiable citations.",
            "evaluation_criteria": "Evaluated against explicit 3-pillar rubric: Retrieval Precision, Tool Schemas, Grounding Verification.",
            "estimated_duration": 180,
            "reason_for_recommendation": "Learner has demonstrated >88% across all prerequisite modules. Promoted directly to Capstone Project.",
            "task_type": "project",
            "status": "in_progress",
            "order_index": 5
        },
        "chat_initial": [
            {"id": "msg-1", "sender": "tutor", "text": "Elena, outstanding performance across the board. You have verified mastery in prompt schemas, dense vector search, and RAG pipelines. You're fully primed for the Autonomous Agent Capstone project. Ready to review the rubric?", "timestamp": "09:30 AM", "suggested_followups": ["Review project rubric details", "Give me a harder challenge", "What are common pitfalls in tool schemas?"]}
        ],
        "description": "Simulates an advanced engineer who aced all prerequisite assessments and is recommended a comprehensive practical capstone project."
    },
    "4": {
        "id": "4",
        "title": "Learner who fails a challenge",
        "learner_name": "Devon Taylor",
        "email": "devon@demo.skillforge.ai",
        "goal_title": "Python Programming & System Scripting",
        "domain": "Software Development",
        "experience_level": "beginner",
        "daily_minutes": 30,
        "learning_style": "hands-on",
        "overall_mastery": 38.0,
        "current_streak": 1,
        "longest_streak": 3,
        "total_study_hours": 4.5,
        "skills_state": [
            {"code": "PY_FUNCS", "name": "Functions & Scope Isolation", "category": "Modularity", "difficulty": "intermediate", "status": "strong", "score": 80.0, "prerequisites": ["PY_EXPR"], "recommended_action": "Scope rules understood"},
            {"code": "PY_RECUR", "name": "Recursive Problem Solving", "category": "Algorithms", "difficulty": "intermediate", "status": "weak", "score": 35.0, "prerequisites": ["PY_FUNCS"], "recommended_action": "Rule applied: Score < 50% triggers prerequisite revision"}
        ],
        "failed_challenge_details": {
            "challenge_id": "ch-recur-countdown",
            "submission_code": "def countdown(n):\n    # Missing base case\n    print(n)\n    return countdown(n - 1)",
            "score": 35,
            "passed": False,
            "adaptation_rule_applied": "Score < 50% (35%) -> Deterministic Adaptation Triggered: Revisit Base Case prerequisites and assigned an easier single-step challenge.",
            "test_results": [
                {"input": "countdown(3)", "expected": "3, 2, 1, Done!", "actual": "RecursionError: maximum recursion depth exceeded", "passed": False}
            ],
            "ai_explanation": "Your function called itself repeatedly without ever checking if `n <= 0`. In Python, every recursive call takes a frame on the call stack. Without a base case, the stack fills up and triggers a RecursionError."
        },
        "active_task": {
            "id": "task-demo-4",
            "skill_code": "PY_RECUR",
            "title": "Remedial Lab: Base Cases First — Stop Before You Leap",
            "learning_objective": "Write the termination condition before writing any recursive call.",
            "difficulty": "beginner",
            "instructions": "Write a function `is_zero(n)` that returns `True` when `n == 0` else returns `False`. Then integrate it as the guard clause in a countdown function.",
            "hints": ["The base case MUST return a value without calling the function again.", "Always check `if n <= 0:` at the very top of the function."],
            "expected_result": "Function safely halts at 0 without stack overflow.",
            "evaluation_criteria": "Guaranteed termination on non-positive integers.",
            "estimated_duration": 15,
            "reason_for_recommendation": "Triggered by failing the countdown challenge (35% score). Adapting to simpler base-case focus.",
            "task_type": "challenge",
            "status": "pending",
            "order_index": 2
        },
        "chat_initial": [
            {"id": "msg-1", "sender": "tutor", "text": "Devon, don't be discouraged! Recursion trips up almost every developer at first. The issue was line 3: your function kept calling itself forever because it didn't know when to stop. Let's look at how adding just two lines with a base case fixes it instantly.", "timestamp": "02:20 PM", "suggested_followups": ["Explain my mistake in detail", "Give me a hint, not the answer", "Show an analogy for call stacks"]}
        ],
        "description": "Simulates a learner who submitted recursive code that threw a RecursionError. The deterministic engine drops difficulty, focuses on base cases, and schedules remedial practice."
    },
    "5": {
        "id": "5",
        "title": "Learner who passes a challenge",
        "learner_name": "Sofia Ramos",
        "email": "sofia@demo.skillforge.ai",
        "goal_title": "Modern Full-Stack React Architecture",
        "domain": "Web Development",
        "experience_level": "intermediate",
        "daily_minutes": 45,
        "learning_style": "hands-on",
        "overall_mastery": 85.0,
        "current_streak": 9,
        "longest_streak": 12,
        "total_study_hours": 31.0,
        "skills_state": [
            {"code": "REACT_HOOKS", "name": "Hooks Lifecycle & useEffect", "category": "Frontend", "difficulty": "intermediate", "status": "strong", "score": 90.0, "prerequisites": ["REACT_STATE"], "recommended_action": "Passed challenge with 100% test coverage"},
            {"code": "WEB_API", "name": "Async API Client Integration", "category": "Networking", "difficulty": "intermediate", "status": "strong", "score": 88.0, "prerequisites": ["REACT_HOOKS"], "recommended_action": "Rule applied: Score >= 80% unlocked advanced challenge"}
        ],
        "passed_challenge_details": {
            "challenge_id": "ch-api-resilience",
            "submission_code": "export function useFetchWithAbort(url) {\n  const [data, setData] = useState(null);\n  const [error, setError] = useState(null);\n  useEffect(() => {\n    const controller = new AbortController();\n    fetch(url, { signal: controller.signal })\n      .then(res => res.json())\n      .then(d => setData(d))\n      .catch(err => { if (err.name !== 'AbortError') setError(err); });\n    return () => controller.abort();\n  }, [url]);\n  return { data, error };\n}",
            "score": 100,
            "passed": True,
            "adaptation_rule_applied": "Score >= 80% (100%) -> Deterministic Adaptation Triggered: Mastery upgraded from developing to proficient (90%). Unlocked higher-difficulty task.",
            "test_results": [
                {"input": "Render hook with valid URL", "expected": "data populated", "actual": "data populated", "passed": True},
                {"input": "Rapid URL prop change", "expected": "previous fetch aborted", "actual": "previous fetch aborted", "passed": True},
                {"input": "Component unmount before response", "expected": "no memory leak warning", "actual": "no memory leak warning", "passed": True}
            ],
            "ai_explanation": "Flawless implementation. You handled the AbortController lifecycle correctly and filtered out benign AbortErrors in the catch block."
        },
        "active_task": {
            "id": "task-demo-5",
            "skill_code": "WEB_API",
            "title": "Advanced Challenge: SWR Caching & Revalidation Hook",
            "learning_objective": "Build a stale-while-revalidate client cache to serve instant cached responses while fetching fresh data in the background.",
            "difficulty": "advanced",
            "instructions": "Extend your hook with an in-memory cache map. Return cached data immediately if present, and dispatch an asynchronous revalidation request.",
            "hints": ["Use a module-level Map or useRef for the global cache cache store.", "Expose `isValidating: boolean` in the hook return tuple."],
            "expected_result": "Sub-millisecond render on cached keys, followed by background sync.",
            "evaluation_criteria": "Cache hit efficiency, expiration TTL check, and no render loops.",
            "estimated_duration": 35,
            "reason_for_recommendation": "Passed previous challenge with 100% score. Rule: >= 80% promotes to advanced application.",
            "task_type": "challenge",
            "status": "in_progress",
            "order_index": 5
        },
        "chat_initial": [
            {"id": "msg-1", "sender": "tutor", "text": "Sofia, great job on the AbortController challenge! All 3 test cases passed with zero memory leaks. Because you scored 100%, your mastery increased to 90% and I've unlocked the advanced Stale-While-Revalidate caching challenge. Let's level up!", "timestamp": "04:45 PM", "suggested_followups": ["Give me a harder challenge", "Explain SWR caching simply", "What are cache invalidation strategies?"]}
        ],
        "description": "Simulates a learner who aced a challenge with 100% test coverage. The engine updates mastery to verified and immediately offers an advanced challenge."
    },
    "6": {
        "id": "6",
        "title": "Learner with multiple skill gaps",
        "learner_name": "Marcus Vance",
        "email": "marcus@demo.skillforge.ai",
        "goal_title": "Data Science & Machine Learning Engineering",
        "domain": "Data Science & AI",
        "experience_level": "intermediate",
        "daily_minutes": 50,
        "learning_style": "hands-on",
        "overall_mastery": 44.0,
        "current_streak": 3,
        "longest_streak": 8,
        "total_study_hours": 15.0,
        "skills_state": [
            {"code": "PY_FUNCS", "name": "Functions & Scope", "category": "Fundamentals", "difficulty": "intermediate", "status": "strong", "score": 85.0, "prerequisites": [], "recommended_action": "Python fundamentals solid"},
            {"code": "DS_NUMPY", "name": "NumPy Vectorized Array Ops", "category": "Computation", "difficulty": "intermediate", "status": "weak", "score": 38.0, "prerequisites": ["PY_FUNCS"], "recommended_action": "Gap 1: Replace explicit Python for-loops with broadcasted matrix operations"},
            {"code": "DS_PANDAS", "name": "Pandas Indexing & Aggregations", "category": "Data Analysis", "difficulty": "intermediate", "status": "weak", "score": 42.0, "prerequisites": ["DS_NUMPY"], "recommended_action": "Gap 2: Master .loc/.iloc boolean indexing and multi-index grouping"},
            {"code": "DS_STATS", "name": "Statistical Hypothesis Testing", "category": "Mathematics", "difficulty": "intermediate", "status": "weak", "score": 48.0, "prerequisites": ["DS_PANDAS"], "recommended_action": "Gap 3: P-value interpretation and two-sample t-test assumptions"}
        ],
        "active_task": {
            "id": "task-demo-6",
            "skill_code": "DS_NUMPY",
            "title": "Multi-Gap Resolution 1: Array Broadcasting & Elimination of For-Loops",
            "learning_objective": "Convert slow $O(N^2)$ nested loops into sub-millisecond vectorized NumPy matrix operations.",
            "difficulty": "intermediate",
            "instructions": "Given a 2D array of coordinates `X` (shape: N, 2), compute all pairwise Euclidean distances using NumPy broadcasting without any Python loops.",
            "hints": ["Use `X[:, np.newaxis, :]` to introduce a third dimension for broadcasting.", "Apply `np.sum((diff)**2, axis=-1)`."],
            "expected_result": "A symmetric (N, N) distance matrix computed in < 5ms for N=1000.",
            "evaluation_criteria": "Zero python loops detected in code execution profile.",
            "estimated_duration": 30,
            "reason_for_recommendation": "Multiple gaps detected across NumPy (38%), Pandas (42%), and Stats (48%). Step 1 targets NumPy vectorization.",
            "task_type": "challenge",
            "status": "in_progress",
            "order_index": 2
        },
        "chat_initial": [
            {"id": "msg-1", "sender": "tutor", "text": "Marcus, we've mapped out your skill profile in Data Science. You have strong Python coding skills, but 3 connected gaps in vectorization, Pandas indexing, and hypothesis testing. Rather than tackling them all at once, our adaptive roadmap will systematically eliminate NumPy vectorization first—because Pandas and ML rely heavily on it!", "timestamp": "01:00 PM", "suggested_followups": ["Show my full skill-gap map", "Why start with NumPy broadcasting?", "Give me a real-world example"]}
        ],
        "description": "Simulates a learner with several interconnected skill deficits. Shows how the adaptive engine sequences dependencies to resolve foundational gaps first."
    },
    "7": {
        "id": "7",
        "title": "Learner submitting incorrect code",
        "learner_name": "Kai Tanaka",
        "email": "kai@demo.skillforge.ai",
        "goal_title": "Python Programming & System Scripting",
        "domain": "Software Development",
        "experience_level": "intermediate",
        "daily_minutes": 40,
        "learning_style": "hands-on",
        "overall_mastery": 62.0,
        "current_streak": 4,
        "longest_streak": 10,
        "total_study_hours": 19.5,
        "skills_state": [
            {"code": "PY_VARS", "name": "Variables & Primitive Types", "category": "Fundamentals", "difficulty": "beginner", "status": "strong", "score": 85.0, "prerequisites": [], "recommended_action": "Mastery confirmed"},
            {"code": "PY_EXPR", "name": "Expressions & Boolean Logic", "category": "Fundamentals", "difficulty": "beginner", "status": "strong", "score": 80.0, "prerequisites": ["PY_VARS"], "recommended_action": "Mastery confirmed"},
            {"code": "PY_FUNCS", "name": "Functions & Scope", "category": "Modularity", "difficulty": "intermediate", "status": "validating", "score": 70.0, "prerequisites": ["PY_EXPR"], "recommended_action": "Targeted dictionary optimization practice"},
            {"code": "PY_RECUR", "name": "Recursive Problem Solving", "category": "Algorithms", "difficulty": "intermediate", "status": "weak", "score": 45.0, "prerequisites": ["PY_FUNCS"], "recommended_action": "Revisit recursion bounds"}
        ],
        "submitted_challenge": {
            "title": "Two-Sum with Optimal Space-Time Complexity",
            "code": "def two_sum(nums, target):\n    for i in range(len(nums)):\n        for j in range(i, len(nums)):\n            if nums[i] + nums[j] == target:\n                return [i, j]\n    return []",
            "test_results": [
                {"input": "nums = [2, 7, 11, 15], target = 9", "expected": "[0, 1]", "actual": "[0, 1]", "passed": True},
                {"input": "nums = [3, 2, 4], target = 6", "expected": "[1, 2]", "actual": "[0, 0]", "passed": False},
                {"input": "nums = [3, 3], target = 6", "expected": "[0, 1]", "actual": "[0, 0]", "passed": False}
            ],
            "passed": False,
            "score": 33,
            "mistake_analysis": "Line 3: `range(i, len(nums))` starts at index `i`, allowing an element to add with itself! For target 6 and element 3 at index 0, it returned `[0, 0]`. Furthermore, the nested loop is $O(N^2)$, whereas the requirement specified $O(N)$ with a hash map."
        },
        "chat_initial": [
            {"id": "msg-1", "sender": "tutor", "text": "Kai, take a close look at your inner loop in line 3: `for j in range(i, len(nums)):`. Notice what happens when `i == 0` and `j == 0`—you are checking `nums[0] + nums[0] == 6`, which uses the same number twice! Would you like a hint on how to prevent using the same index, or on how to optimize this to O(N) using a dictionary?", "timestamp": "03:10 PM", "suggested_followups": ["Give me a hint, not the answer", "Explain my mistake", "How does a hash map give O(N)?"]}
        ],
        "description": "Simulates an incorrect code submission with off-by-one and element re-use bugs. Highlights how the AI tutor gives precise line-level feedback and progressive hints without spoiling the solution."
    },
    "8": {
        "id": "8",
        "title": "Learner receiving project feedback",
        "learner_name": "Liam Gallagher",
        "email": "liam@demo.skillforge.ai",
        "goal_title": "Modern Full-Stack Web Architecture",
        "domain": "Web Development",
        "experience_level": "intermediate",
        "daily_minutes": 45,
        "learning_style": "project-based",
        "overall_mastery": 78.0,
        "current_streak": 7,
        "longest_streak": 11,
        "total_study_hours": 28.5,
        "skills_state": [
            {"code": "REACT_COMP", "name": "React Component Composition", "category": "Frontend", "difficulty": "beginner", "status": "strong", "score": 88.0, "prerequisites": [], "recommended_action": "Demonstrated mastery"},
            {"code": "REACT_STATE", "name": "State Management & Reactivity", "category": "Frontend", "difficulty": "intermediate", "status": "strong", "score": 82.0, "prerequisites": ["REACT_COMP"], "recommended_action": "Demonstrated mastery"},
            {"code": "WEB_API", "name": "Async API Client Integration", "category": "Networking", "difficulty": "intermediate", "status": "strong", "score": 85.0, "prerequisites": ["REACT_STATE"], "recommended_action": "Demonstrated mastery"},
            {"code": "WEB_ERR", "name": "Client & Server Error Boundaries", "category": "Reliability", "difficulty": "intermediate", "status": "validating", "score": 65.0, "prerequisites": ["WEB_API"], "recommended_action": "Address unhandled exception leakage"}
        ],
        "project_feedback": {
            "project_title": "RESTful API with Authentication & Rate Limiting",
            "overall_score": 83,
            "passed": True,
            "rubric_scores": [
                {"criterion": "Architecture & Separation of Concerns", "score": 90, "feedback": "Excellent separation between route controllers, validation schemas, and database queries."},
                {"criterion": "Input Validation & Type Safety", "score": 92, "feedback": "Pydantic schemas effectively caught missing fields, malformed emails, and invalid integer boundaries."},
                {"criterion": "Error Handling & Status Codes", "score": 65, "feedback": "Several unhandled database exceptions leaked raw 500 error tracebacks to the client instead of sanitized 400/404 messages."},
                {"criterion": "Documentation & Testing", "score": 85, "feedback": "OpenAPI / Swagger docs were clean; test suite covered happy paths well but lacked negative authorization tests."}
            ],
            "strengths": [
                "Clean declarative Pydantic schemas",
                "Proper password hashing with bcrypt salts",
                "Effective token verification middleware"
            ],
            "areas_for_improvement": [
                "Implement a centralized exception handler to prevent stack leakages",
                "Add unit tests verifying token expiration and 401 Unauthorized responses",
                "Rate limiter lacked Redis distributed state; currently in-memory only"
            ],
            "ai_coaching_notes": "Great submission Liam! Your architectural boundaries are very clean. The main reason this scored 83 instead of 95+ is unhandled internal exceptions leaking tracebacks. In production, this can expose database credentials or internal table structures. Adding a custom FastAPI `@app.exception_handler` will push this into senior-level territory.",
            "next_recommended_milestone": "Implement Centralized Exception Handling Middleware"
        },
        "description": "Simulates project submission evaluation against explicit rubrics, showing detailed scoring per criterion, strengths, areas for improvement, and actionable coaching notes."
    },
    "9": {
        "id": "9",
        "title": "Learner demonstrating improvement over multiple attempts",
        "learner_name": "Priya Patel",
        "email": "priya@demo.skillforge.ai",
        "goal_title": "Python Programming & System Scripting",
        "domain": "Software Development",
        "experience_level": "intermediate",
        "daily_minutes": 45,
        "learning_style": "hands-on",
        "overall_mastery": 88.0,
        "current_streak": 12,
        "longest_streak": 15,
        "total_study_hours": 34.0,
        "skills_state": [
            {"code": "PY_VARS", "name": "Variables & Primitive Types", "category": "Fundamentals", "difficulty": "beginner", "status": "strong", "score": 95.0, "prerequisites": [], "recommended_action": "Demonstrated mastery"},
            {"code": "PY_EXPR", "name": "Expressions & Boolean Logic", "category": "Fundamentals", "difficulty": "beginner", "status": "strong", "score": 92.0, "prerequisites": ["PY_VARS"], "recommended_action": "Demonstrated mastery"},
            {"code": "PY_LOOPS", "name": "Loops & Iteration Controls", "category": "Control Flow", "difficulty": "beginner", "status": "strong", "score": 90.0, "prerequisites": ["PY_EXPR"], "recommended_action": "Demonstrated mastery"},
            {"code": "PY_FUNCS", "name": "Functions & Scope Isolation", "category": "Modularity", "difficulty": "intermediate", "status": "strong", "score": 92.0, "prerequisites": ["PY_EXPR"], "recommended_action": "Demonstrated mastery"},
            {"code": "PY_RECUR", "name": "Recursive Problem Solving", "category": "Algorithms", "difficulty": "intermediate", "status": "strong", "score": 94.0, "prerequisites": ["PY_FUNCS"], "recommended_action": "Verified Mastery with DP & Memoization"}
        ],
        "skill_focus": "Recursive Problem Solving & Memoization (PY_RECUR)",
        "attempt_history": [
            {
                "attempt_number": 1,
                "score": 35,
                "timestamp": "2 days ago",
                "status": "Failed",
                "details": "Naive recursion; hit maximum recursion depth on large test inputs (fibonacci(50)).",
                "mastery_calculated": 35.0,
                "confidence": 30.0
            },
            {
                "attempt_number": 2,
                "score": 70,
                "timestamp": "Yesterday",
                "status": "Partial Pass",
                "details": "Added basic dictionary memoization. Passed 4/5 test cases; edge cases for negative numbers failed.",
                "mastery_calculated": 65.0,
                "confidence": 60.0
            },
            {
                "attempt_number": 3,
                "score": 96,
                "timestamp": "Today",
                "status": "Mastered",
                "details": "Full dynamic programming memoization with `@functools.lru_cache` and negative number input validation. All test cases passed in 0.002s.",
                "mastery_calculated": 94.0,
                "confidence": 95.0
            }
        ],
        "mastery_verification": {
            "skill_code": "PY_RECUR",
            "proficiency_level": "mastered",
            "is_verified": True,
            "formula_explanation": "Mastery is calculated using a decaying exponential moving average (EMA) weighted towards demonstrated practical tests (weight 70%) combined with diagnostic quiz consistency (30%). Mastery status 'Verified' requires >= 80% on at least 2 consecutive attempts."
        },
        "description": "Simulates learner growth across three attempts. Shows the progression from naive failure (35%) to partial fix (70%) to verified mastery (96%) with formula transparency."
    },
    "10": {
        "id": "10",
        "title": "Learner uploading notes and generating quizzes",
        "learner_name": "Samira Khan",
        "email": "samira@demo.skillforge.ai",
        "goal_title": "Data Science & Machine Learning Engineering",
        "domain": "Data Science & AI",
        "experience_level": "intermediate",
        "daily_minutes": 40,
        "learning_style": "visual",
        "overall_mastery": 68.0,
        "current_streak": 5,
        "longest_streak": 9,
        "total_study_hours": 16.0,
        "skills_state": [
            {"code": "PY_FUNCS", "name": "Functions & Scope", "category": "Fundamentals", "difficulty": "intermediate", "status": "strong", "score": 85.0, "prerequisites": [], "recommended_action": "Python fundamentals solid"},
            {"code": "DS_NUMPY", "name": "NumPy Vectorized Array Ops", "category": "Computation", "difficulty": "intermediate", "status": "strong", "score": 78.0, "prerequisites": ["PY_FUNCS"], "recommended_action": "Vectorization demonstrated"},
            {"code": "DS_PANDAS", "name": "Pandas Indexing & Aggregations", "category": "Data Analysis", "difficulty": "intermediate", "status": "validating", "score": 72.0, "prerequisites": ["DS_NUMPY"], "recommended_action": "Targeted practice on aggregations"},
            {"code": "DS_NEURAL", "name": "Neural Network Architecture", "category": "Deep Learning", "difficulty": "advanced", "status": "validating", "score": 68.0, "prerequisites": ["DS_NUMPY"], "recommended_action": "Smart notes generated practice quiz active"}
        ],
        "uploaded_doc": {
            "filename": "Neural_Networks_and_Backpropagation_Notes.txt",
            "file_type": "text/plain",
            "file_size": 4210,
            "char_count": 3840,
            "summary": "Comprehensive overview of artificial neural networks, multilayer perceptron architecture, forward pass activation functions (ReLU, Sigmoid), cross-entropy loss formulation, and gradient computation via the chain rule in backpropagation.",
            "extracted_concepts": [
                {"term": "Backpropagation", "definition": "An algorithm that computes the gradient of the loss function with respect to each weight via the chain rule, propagating errors backward from the output layer.", "importance": "core", "difficulty": "advanced"},
                {"term": "Learning Rate", "definition": "A hyperparameter determining the step size at each iteration while moving toward a minimum of a loss function.", "importance": "core", "difficulty": "intermediate"},
                {"term": "Loss Function", "definition": "A mathematical metric evaluating how well an algorithm models the given dataset (e.g., Mean Squared Error, Cross-Entropy).", "importance": "core", "difficulty": "beginner"},
                {"term": "Vanishing Gradient", "definition": "A phenomenon where gradients become infinitesimally small during backpropagation through deep layers, stalling weight updates in Sigmoid/Tanh networks.", "importance": "important", "difficulty": "advanced"},
                {"term": "ReLU Activation", "definition": "Rectified Linear Unit function defined as f(x) = max(0, x), mitigating vanishing gradients in positive domains.", "importance": "important", "difficulty": "intermediate"}
            ],
            "generated_flashcards": [
                {"front": "What does Backpropagation compute for each weight in a network?", "back": "The partial derivative (gradient) of the loss function with respect to that weight using the mathematical chain rule.", "confidence": "learning"},
                {"front": "Why does the Sigmoid activation function often cause vanishing gradients in deep networks?", "back": "Because the maximum derivative of the Sigmoid function is only 0.25; multiplying these small fractions across many layers diminishes gradients to near zero.", "confidence": "new"},
                {"front": "What is the primary advantage of ReLU over Sigmoid?", "back": "Its derivative is 1 for any positive input, which prevents gradients from decaying during backpropagation.", "confidence": "mastered"}
            ],
            "generated_quiz": [
                {
                    "prompt": "Based on your uploaded notes, which mathematical principle allows backpropagation to compute gradients through multiple composite layers?",
                    "options": [
                        {"id": "A", "text": "The Chain Rule of Calculus"},
                        {"id": "B", "text": "Euler's Formula"},
                        {"id": "C", "text": "The Central Limit Theorem"},
                        {"id": "D", "text": "Bayes' Theorem"}
                    ],
                    "answer_key": "A",
                    "explanation": "Backpropagation is an application of the multivariate chain rule to compute gradients of composite functions in a computational graph."
                },
                {
                    "prompt": "According to the notes, what happens if the learning rate is set too high?",
                    "options": [
                        {"id": "A", "text": "The model will instantly achieve zero loss"},
                        {"id": "B", "text": "The optimizer may oscillate wildly and diverge away from the minimum"},
                        {"id": "C", "text": "The weights are automatically set to zero"},
                        {"id": "D", "text": "The activation function switches from ReLU to Sigmoid"}
                    ],
                    "answer_key": "B",
                    "explanation": "A high learning rate causes steps so large that the optimizer overshoots the minimum and can diverge."
                }
            ]
        },
        "description": "Simulates a learner who uploaded custom lecture notes. Shows automated text extraction, key concept identification, instant flashcards, and grounded quiz generation."
    }
}

def load_scenario(scenario_id: str):
    """Activates and sets up the chosen scenario in the database."""
    if scenario_id not in DEMO_SCENARIOS:
        scenario_id = "1"
    
    scenario = DEMO_SCENARIOS[scenario_id]
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).isoformat()
    
    learner_id = f"demo-learner-{scenario_id}"
    
    # 1. Upsert Learner
    cursor.execute("""
    INSERT INTO learners (id, email, full_name, experience_level, daily_minutes, learning_style, current_streak, longest_streak, total_study_hours, is_simulated, active_scenario, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        email=excluded.email,
        full_name=excluded.full_name,
        experience_level=excluded.experience_level,
        daily_minutes=excluded.daily_minutes,
        learning_style=excluded.learning_style,
        current_streak=excluded.current_streak,
        longest_streak=excluded.longest_streak,
        total_study_hours=excluded.total_study_hours,
        is_simulated=1,
        active_scenario=excluded.active_scenario,
        updated_at=excluded.updated_at
    """, (learner_id, scenario["email"], scenario["learner_name"], scenario["experience_level"], scenario["daily_minutes"], scenario["learning_style"], scenario["current_streak"], scenario["longest_streak"], scenario["total_study_hours"], scenario_id, now, now))
    
    # 2. Upsert Learning Goal
    goal_id = f"goal-demo-{scenario_id}"
    cursor.execute("""
    INSERT INTO learning_goals (id, learner_id, title, domain, target_outcome, status, progress_percentage, created_at)
    VALUES (?, ?, ?, ?, ?, 'active', ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        title=excluded.title,
        domain=excluded.domain,
        progress_percentage=excluded.progress_percentage
    """, (goal_id, learner_id, scenario["goal_title"], scenario["domain"], f"Attain job-ready proficiency in {scenario['domain']}", int(scenario["overall_mastery"]), now))
    
    # 3. Upsert Mastery Records for this scenario
    if "skills_state" in scenario:
        for s in scenario["skills_state"]:
            cursor.execute("""
            INSERT INTO mastery_records (id, learner_id, skill_code, proficiency_level, score, confidence_score, attempts_count, is_verified, last_evaluated_at)
            VALUES (?, ?, ?, ?, ?, 75.0, 3, ?, ?)
            ON CONFLICT(learner_id, skill_code) DO UPDATE SET
                score=excluded.score,
                proficiency_level=excluded.proficiency_level,
                is_verified=excluded.is_verified,
                last_evaluated_at=excluded.last_evaluated_at
            """, (str(uuid.uuid4()), learner_id, s["code"], "mastered" if s["score"] >= 80 else ("developing" if s["score"] >= 50 else "novice"), s["score"], 1 if s["score"] >= 80 else 0, now))

    # 4. Upsert Learning Path and Task
    path_id = f"path-demo-{scenario_id}"
    cursor.execute("""
    INSERT INTO learning_paths (id, learner_id, goal_id, title, status, adaptation_reason, progress_percentage, generated_at, updated_at)
    VALUES (?, ?, ?, ?, 'active', ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        title=excluded.title,
        adaptation_reason=excluded.adaptation_reason,
        progress_percentage=excluded.progress_percentage,
        updated_at=excluded.updated_at
    """, (path_id, learner_id, goal_id, f"Adaptive Path: {scenario['goal_title']}", f"Configured for Scenario {scenario_id}: {scenario['title']}", int(scenario["overall_mastery"]), now, now))

    if "active_task" in scenario:
        t = scenario["active_task"]
        cursor.execute("""
        INSERT INTO learning_tasks (id, path_id, skill_code, title, learning_objective, difficulty, instructions, hints_json, expected_result, evaluation_criteria, estimated_duration, reason_for_recommendation, task_type, status, order_index, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            title=excluded.title,
            learning_objective=excluded.learning_objective,
            instructions=excluded.instructions,
            status=excluded.status
        """, (t["id"], path_id, t["skill_code"], t["title"], t["learning_objective"], t["difficulty"], t["instructions"], json.dumps(t.get("hints", [])), t.get("expected_result", ""), t.get("evaluation_criteria", ""), t.get("estimated_duration", 20), t.get("reason_for_recommendation", ""), t.get("task_type", "challenge"), t.get("status", "pending"), t.get("order_index", 1), now))

    # 5. Upsert Chat
    if "chat_initial" in scenario:
        conv_id = f"conv-demo-{scenario_id}"
        cursor.execute("""
        INSERT INTO tutor_conversations (id, learner_id, messages_json, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            messages_json=excluded.messages_json,
            updated_at=excluded.updated_at
        """, (conv_id, learner_id, json.dumps(scenario["chat_initial"]), now, now))

    # 6. Upsert Uploaded Document & Flashcards if Scenario 10
    if scenario_id == "10" and "uploaded_doc" in scenario:
        doc = scenario["uploaded_doc"]
        doc_id = "doc-demo-10"
        cursor.execute("""
        INSERT INTO uploaded_documents (id, learner_id, filename, file_type, file_size, char_count, summary, concepts_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            summary=excluded.summary,
            concepts_json=excluded.concepts_json
        """, (doc_id, learner_id, doc["filename"], doc["file_type"], doc["file_size"], doc["char_count"], doc["summary"], json.dumps(doc["extracted_concepts"]), now))

        for idx, fc in enumerate(doc["generated_flashcards"]):
            fc_id = f"fc-demo-10-{idx}"
            cursor.execute("""
            INSERT INTO flashcards (id, learner_id, document_id, skill_code, front, back, confidence, review_count, created_at)
            VALUES (?, ?, ?, 'DS_NEURAL', ?, ?, ?, 1, ?)
            ON CONFLICT(id) DO UPDATE SET front=excluded.front, back=excluded.back
            """, (fc_id, learner_id, doc_id, fc["front"], fc["back"], fc["confidence"], now))

    conn.commit()
    conn.close()
    return scenario
