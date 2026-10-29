"""
Course Learning Hub Resources Catalog
Contains structured topic-wise study notes and verified educational videos
for all 4 curriculum modules across all 4 courses (16 modules total).
"""

from typing import Dict, Any, List

COURSE_LEARNING_RESOURCES: Dict[str, Dict[str, Any]] = {
    "c-python": {
        "course_id": "c-python",
        "course_title": "Python Programming & System Scripting",
        "domain": "Software Development",
        "level": "Beginner to Advanced",
        "description": "Master Python syntax, data structures, functional patterns, object-oriented design, and asynchronous programming.",
        "diagnostic_assessment_id": "a-python-diag",
        "topics": [
            {
                "id": "m-py-1",
                "title": "Variables, Expressions & Types",
                "description": "Core data types, variable scope, operations, and memory reference semantics.",
                "estimated_minutes": 20,
                "study_notes": {
                    "introduction": "In Python, variables are names (references) pointing to objects stored in heap memory. Understanding primitive scalar types, relational expressions, and the distinction between mutable and immutable objects is fundamental to writing defect-free code.",
                    "concepts": [
                        {
                            "term": "Reference Semantics",
                            "definition": "Variables act as pointers/labels referencing objects in heap memory. Assigning `b = a` points `b` to the same memory address as `a`."
                        },
                        {
                            "term": "Mutability vs Immutability",
                            "definition": "Mutable objects (lists, dicts, sets) can be altered in-place. Immutable objects (integers, floats, strings, tuples) cannot be altered once created."
                        },
                        {
                            "term": "Truthiness & Short-Circuiting",
                            "definition": "Objects evaluated in boolean contexts resolve to False if empty (`[]`, `''`, `{}`, `0`, `None`). Python logical operators (`and`, `or`) short-circuit evaluation from left to right."
                        }
                    ],
                    "step_by_step": [
                        {
                            "step": "1",
                            "title": "Variable Binding",
                            "description": "Bind descriptive variable names using `=`: `learner_score = 95.5`."
                        },
                        {
                            "step": "2",
                            "title": "Inspecting Memory Address",
                            "description": "Use `id(obj)` to view memory locations and `is` to check object identity: `a is b`."
                        },
                        {
                            "step": "3",
                            "title": "Defensive Copying",
                            "description": "Avoid shared reference mutations by creating shallow copies (`list(my_list)`) or deep copies (`copy.deepcopy()`)."
                        }
                    ],
                    "code_example": {
                        "language": "python",
                        "code": "# Demonstration of Reference Semantics & Mutability\noriginal = [1, 2, 3]\nalias_ref = original\nindependent_copy = list(original)\n\nalias_ref.append(4)\nprint(f'Original: {original}')          # [1, 2, 3, 4]\nprint(f'Alias:    {alias_ref}')         # [1, 2, 3, 4]\nprint(f'Copy:     {independent_copy}')  # [1, 2, 3]\nprint(f'Are original & alias identical: {alias_ref is original}') # True",
                        "explanation": "Because lists are mutable, modifying `alias_ref` updates the shared underlying memory buffer referenced by `original`."
                    },
                    "key_takeaways": [
                        "Integers, floats, strings, and tuples are immutable; lists, dictionaries, and sets are mutable.",
                        "Use `==` to test equality of values and `is` to test memory identity.",
                        "`bool('0')` evaluates to True because it is a non-empty string."
                    ],
                    "practice_questions": [
                        {
                            "question": "What is the output of `x = (1, 2); x += (3,); print(x)`?",
                            "answer": "(1, 2, 3)",
                            "explanation": "Because tuples are immutable, `+=` creates a brand-new tuple object and rebinds `x` to the new memory address."
                        }
                    ]
                },
                "videos": [
                    {
                        "id": "v-py-1",
                        "title": "Python Tutorial for Beginners: Variables & Data Types",
                        "channel": "freeCodeCamp.org",
                        "embed_url": "https://www.youtube-nocookie.com/embed/rfscVS0vtbw",
                        "watch_url": "https://www.youtube.com/watch?v=rfscVS0vtbw",
                        "search_url": "https://www.youtube.com/results?search_query=freecodecamp+python+variables+and+data+types",
                        "duration": "18 mins",
                        "summary": "Covers Python variable assignments, memory pointers, type conversions, and scalar primitives."
                    }
                ]
            },
            {
                "id": "m-py-2",
                "title": "Control Flow & Iteration",
                "description": "Branching, loops, comprehensions, and iteration protocols.",
                "estimated_minutes": 25,
                "study_notes": {
                    "introduction": "Control flow structures govern logical branching and repetition. Python emphasizes clean iterable loops (`for item in iterable`) and comprehension syntax rather than manual C-style index counters.",
                    "concepts": [
                        {
                            "term": "for/while Iteration",
                            "definition": "Repeats execution across an iterable sequence until exhausted or when a conditional boolean check turns false."
                        },
                        {
                            "term": "break vs continue",
                            "definition": "`break` terminates the enclosing loop immediately. `continue` skips the remainder of the current iteration and jumps to the next cycle."
                        },
                        {
                            "term": "List Comprehensions",
                            "definition": "Concise, performant syntax for creating new sequences by applying expressions and predicate filters to an iterable: `[expr for item in list if condition]`."
                        }
                    ],
                    "step_by_step": [
                        {
                            "step": "1",
                            "title": "Iterating Over Sequences",
                            "description": "Iterate directly over elements or use `enumerate(items, start=1)` when index tracking is needed."
                        },
                        {
                            "step": "2",
                            "title": "Filtering with Guards",
                            "description": "Use `continue` to bypass invalid records and `break` to halt early upon finding target matches."
                        },
                        {
                            "step": "3",
                            "title": "Transforming Data with Comprehensions",
                            "description": "Replace imperative `.append()` loops with declarative list or dictionary comprehensions."
                        }
                    ],
                    "code_example": {
                        "language": "python",
                        "code": "# Pythonic iteration with enumerate & list comprehension\nnumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n\n# Filter even numbers and square them\neven_squares = [n**2 for n in numbers if n % 2 == 0]\nprint('Even squares:', even_squares) # [4, 16, 36, 64, 100]\n\n# Summing odd numbers with continue\nodd_sum = 0\nfor n in numbers:\n    if n % 2 == 0:\n        continue\n    odd_sum += n\nprint('Odd sum:', odd_sum) # 25",
                        "explanation": "Demonstrates `continue` skipping even numbers and a clean list comprehension generating transformed lists."
                    },
                    "key_takeaways": [
                        "Use `enumerate()` instead of maintaining manual index variables (`i += 1`).",
                        "`range(start, stop, step)` generates values lazily in O(1) memory.",
                        "List comprehensions execute faster in Python bytecode than manual `list.append()` loops."
                    ],
                    "practice_questions": [
                        {
                            "question": "What does `[x for x in range(10) if x % 3 == 0]` evaluate to?",
                            "answer": "[0, 3, 6, 9]",
                            "explanation": "Generates numbers 0 through 9 and filters for values where `x % 3 == 0`."
                        }
                    ]
                },
                "videos": [
                    {
                        "id": "v-py-2",
                        "title": "Python Loops and Iterations: For/While Loops Tutorial",
                        "channel": "Corey Schafer",
                        "embed_url": "https://www.youtube-nocookie.com/embed/6iF8Xb7Z3wQ",
                        "watch_url": "https://www.youtube.com/watch?v=6iF8Xb7Z3wQ",
                        "search_url": "https://www.youtube.com/results?search_query=corey+schafer+python+loops+and+iterations",
                        "duration": "16 mins",
                        "summary": "Walkthrough of for loops, while loops, break, continue, range, and nested iterations."
                    }
                ]
            },
            {
                "id": "m-py-3",
                "title": "Functions & Modular Architecture",
                "description": "Parameters, recursion, closures, generators, and LEGB scope isolation.",
                "estimated_minutes": 25,
                "study_notes": {
                    "introduction": "Functions modularize code into testable, isolated units. In Python, functions are first-class citizens: they can be assigned to variables, passed as arguments, decorated, and returned from other functions.",
                    "concepts": [
                        {
                            "term": "LEGB Scope",
                            "definition": "Name resolution sequence: Local -> Enclosing -> Global -> Built-in. Inner scopes can read outer variables but cannot rebind them without `nonlocal` or `global`."
                        },
                        {
                            "term": "Default Argument Trap",
                            "definition": "Default parameters are evaluated once at function definition time. Never use mutable objects (`[]`, `{}`) as default parameters."
                        },
                        {
                            "term": "Recursion & Call Stack",
                            "definition": "Functions that call themselves to solve divide-and-conquer subproblems. Must always include a base case stopping guard."
                        }
                    ],
                    "step_by_step": [
                        {
                            "step": "1",
                            "title": "Function Signature",
                            "description": "Define clear parameter names and type hints: `def two_sum(nums: list[int], target: int) -> list[int]:`."
                        },
                        {
                            "step": "2",
                            "title": "Safe Default Parameter",
                            "description": "Use `None` as default for mutable containers: `def register(tags=None): if tags is None: tags = []`."
                        },
                        {
                            "step": "3",
                            "title": "Base Case Guard",
                            "description": "When using recursion, place base case conditions first: `if n <= 0: return [0]`."
                        }
                    ],
                    "code_example": {
                        "language": "python",
                        "code": "# Safe default parameters and pure function design\ndef create_session(user_id: str, tags: list = None) -> dict:\n    if tags is None:\n        tags = [] # Instantiated fresh per invocation\n    tags.append('active')\n    return {'user_id': user_id, 'tags': tags}\n\ns1 = create_session('alice')\ns2 = create_session('bob')\nprint(s1) # {'user_id': 'alice', 'tags': ['active']}\nprint(s2) # {'user_id': 'bob', 'tags': ['active']} (Containers are isolated)",
                        "explanation": "Avoids the mutable default argument bug where default lists retain appended items across calls."
                    },
                    "key_takeaways": [
                        "Always use `None` as default for mutable parameters (lists, dictionaries).",
                        "Recursive algorithms require base cases to prevent stack overflow (`RecursionError`).",
                        "Pure functions avoid side-effects, making code predictable and easily testable."
                    ],
                    "practice_questions": [
                        {
                            "question": "What happens if a recursive function lacks a base case?",
                            "answer": "It triggers infinite recursion and raises `RecursionError: maximum recursion depth exceeded`.",
                            "explanation": "Python limits the call stack to protect against C-level memory corruption."
                        }
                    ]
                },
                "videos": [
                    {
                        "id": "v-py-3",
                        "title": "Python Functions: Defining, Arguments, and Return Values",
                        "channel": "Corey Schafer",
                        "embed_url": "https://www.youtube-nocookie.com/embed/9Os0o3wzS_I",
                        "watch_url": "https://www.youtube.com/watch?v=9Os0o3wzS_I",
                        "search_url": "https://www.youtube.com/results?search_query=corey+schafer+python+functions",
                        "duration": "22 mins",
                        "summary": "Comprehensive tutorial covering positional arguments, keyword arguments, *args, **kwargs, and return statements."
                    }
                ]
            },
            {
                "id": "m-py-4",
                "title": "Error Handling & Robust I/O",
                "description": "Exceptions, context managers, file streams, and defensive engineering.",
                "estimated_minutes": 20,
                "study_notes": {
                    "introduction": "Defensive error handling and deterministic resource management ensure system reliability. Python uses `try...except...finally` blocks and the `with` statement (context managers) to guarantee file handles and network sockets are closed cleanly.",
                    "concepts": [
                        {
                            "term": "EAFP Principle",
                            "definition": "'Easier to Ask for Forgiveness than Permission.' Idiomatic Python prefers attempting operations inside `try` blocks rather than defensive condition checks."
                        },
                        {
                            "term": "Context Managers (`with`)",
                            "definition": "Objects implementing `__enter__()` and `__exit__()` protocol that automatically acquire and release resources even if an exception occurs."
                        },
                        {
                            "term": "Specific Exception Trapping",
                            "definition": "Always catch concrete exception types (`FileNotFoundError`, `KeyError`) rather than a bare `except:`, which masks unexpected errors."
                        }
                    ],
                    "step_by_step": [
                        {
                            "step": "1",
                            "title": "Guarded Execution",
                            "description": "Wrap risky I/O or parsing logic in `try:` blocks."
                        },
                        {
                            "step": "2",
                            "title": "Trapping Domain Exceptions",
                            "description": "Catch specific error types and provide informative error logging."
                        },
                        {
                            "step": "3",
                            "title": "Automatic Resource Cleanup",
                            "description": "Use `with open('file.txt', 'r') as f:` to ensure file descriptors close automatically."
                        }
                    ],
                    "code_example": {
                        "language": "python",
                        "code": "# Deterministic resource cleanup with context manager\nimport json\n\ndef safe_load_config(filepath: str) -> dict:\n    try:\n        with open(filepath, 'r') as f:\n            return json.load(f)\n    except FileNotFoundError:\n        print(f'Warning: {filepath} not found. Loading defaults.')\n        return {'status': 'default', 'retries': 3}\n    except json.JSONDecodeError as e:\n        print(f'Error parsing config JSON: {e}')\n        raise",
                        "explanation": "Guarantees file closure and provides graceful fallback handling for missing configuration files."
                    },
                    "key_takeaways": [
                        "Always use `with` statements when handling files, locks, or database connections.",
                        "Never write bare `except:`; catch specific exceptions like `ValueError` or `KeyError`.",
                        "The `finally:` block executes regardless of whether an exception occurred."
                    ],
                    "practice_questions": [
                        {
                            "question": "Why is `with open('data.txt') as f:` safer than `f = open('data.txt')`?",
                            "answer": "The context manager automatically calls `f.close()` even if an exception is raised inside the block.",
                            "explanation": "Prevents file descriptor leaks and lock collisions in long-running processes."
                        }
                    ]
                },
                "videos": [
                    {
                        "id": "v-py-4",
                        "title": "Python Exception Handling: Try/Except/Finally Blocks",
                        "channel": "Corey Schafer",
                        "embed_url": "https://www.youtube-nocookie.com/embed/NIWwJbo-9_8",
                        "watch_url": "https://www.youtube.com/watch?v=NIWwJbo-9_8",
                        "search_url": "https://www.youtube.com/results?search_query=corey+schafer+python+exceptions+try+except",
                        "duration": "17 mins",
                        "summary": "Covers try/except/else/finally blocks, catching specific exceptions, and raising custom errors."
                    }
                ]
            }
        ]
    },
    "c-fullstack": {
        "course_id": "c-fullstack",
        "course_title": "Modern Full-Stack Web Architecture",
        "domain": "Web Development",
        "level": "Intermediate",
        "description": "Build high-performance web applications using React, TypeScript, state machines, REST/GraphQL APIs, and server patterns.",
        "diagnostic_assessment_id": "a-react-diag",
        "topics": [
            {
                "id": "m-fs-1",
                "title": "React Components & JSX",
                "description": "Pure components, JSX parsing, rendering trees, props, and Virtual DOM reconciliation.",
                "estimated_minutes": 20,
                "study_notes": {
                    "introduction": "React expresses user interfaces as functional component trees. Using JSX syntactic sugar and an in-memory Virtual DOM, React batches state updates and computes the minimal set of real DOM mutations through reconciliation.",
                    "concepts": [
                        {
                            "term": "Virtual DOM Reconciliation",
                            "definition": "The diffing algorithm comparing previous and next Virtual DOM fiber trees to compute minimal real DOM mutations."
                        },
                        {
                            "term": "Component Purity",
                            "definition": "Components should behave as pure functions with respect to props: identical props must always render identical JSX."
                        },
                        {
                            "term": "Keys in Lists",
                            "definition": "Persistent string/number identifiers giving React stable tracking of elements across reorders, insertions, and deletions."
                        }
                    ],
                    "step_by_step": [
                        {
                            "step": "1",
                            "title": "Component Decomposition",
                            "description": "Break complex UIs into focused, single-responsibility presentational and container components."
                        },
                        {
                            "step": "2",
                            "title": "Defining Typed Props",
                            "description": "Use TypeScript interfaces to define rigid prop contracts: `interface CardProps { title: string; isActive?: boolean; }`."
                        },
                        {
                            "step": "3",
                            "title": "Using Stable Keys",
                            "description": "When mapping arrays, pass stable unique IDs (`key={user.id}`) rather than array indices."
                        }
                    ],
                    "code_example": {
                        "language": "tsx",
                        "code": "interface ModuleCardProps {\n  title: string;\n  hours: number;\n  onSelect: () => void;\n}\n\nexport const ModuleCard: React.FC<ModuleCardProps> = ({ title, hours, onSelect }) => (\n  <div onClick={onSelect} className=\"p-3 bg-white border-2 border-black rounded-xl shadow-neo cursor-pointer hover:bg-yellow-100\">\n    <h4 className=\"font-bold text-sm text-black\">{title}</h4>\n    <span className=\"text-xs font-mono text-zinc-600\">{hours} hours study time</span>\n  </div>\n);",
                        "explanation": "A clean, pure functional component with typed props and Neo-Brutalist styling."
                    },
                    "key_takeaways": [
                        "JSX is compiled into nested `React.createElement()` JavaScript calls.",
                        "Never mutate props directly inside child components.",
                        "Stable keys prevent UI state desynchronization when rendering lists."
                    ],
                    "practice_questions": [
                        {
                            "question": "Why should array indices not be used as keys when list items can be re-ordered or filtered?",
                            "answer": "Indices change when items shift, causing React to associate old DOM nodes and state with the wrong item.",
                            "explanation": "Persistent unique IDs allow React to accurately identify moving vs removed elements."
                        }
                    ]
                },
                "videos": [
                    {
                        "id": "v-fs-1",
                        "title": "React JS Full Course 2024: Components & JSX",
                        "channel": "freeCodeCamp.org",
                        "embed_url": "https://www.youtube-nocookie.com/embed/bMknfKXIFA8",
                        "watch_url": "https://www.youtube.com/watch?v=bMknfKXIFA8",
                        "search_url": "https://www.youtube.com/results?search_query=freecodecamp+react+components+and+jsx",
                        "duration": "25 mins",
                        "summary": "Explains functional components, JSX syntax compilation, props, and rendering trees."
                    }
                ]
            },
            {
                "id": "m-fs-2",
                "title": "Hooks & Async State Lifecycle",
                "description": "useEffect, custom hooks, race conditions, caching, and state synchronization.",
                "estimated_minutes": 25,
                "study_notes": {
                    "introduction": "Hooks allow functional components to manage local state and synchronize with external systems. Mastering `useEffect` dependency hygiene and cleanup logic prevents stale closures and memory leaks in production apps.",
                    "concepts": [
                        {
                            "term": "Dependency Array",
                            "definition": "The array passed as the 2nd argument to `useEffect`. React only re-executes the effect when at least one dependency changes reference identity."
                        },
                        {
                            "term": "Effect Teardown Callback",
                            "definition": "The cleanup function returned by `useEffect`, executed prior to re-running the effect and upon component unmount."
                        },
                        {
                            "term": "Stale Closures",
                            "definition": "A bug occurring when an asynchronous callback captures outdated state or prop values from an earlier render pass."
                        }
                    ],
                    "step_by_step": [
                        {
                            "step": "1",
                            "title": "Declare Reactive State",
                            "description": "Use `useState` for local state and `useReducer` for complex state transitions."
                        },
                        {
                            "step": "2",
                            "title": "Synchronize Side Effects",
                            "description": "Trigger network fetches or subscriptions inside `useEffect`."
                        },
                        {
                            "step": "3",
                            "title": "Return Teardown Cleanup",
                            "description": "Always unsubscribe event listeners or abort pending network requests in the return function."
                        }
                    ],
                    "code_example": {
                        "language": "tsx",
                        "code": "import { useState, useEffect } from 'react';\n\nexport function useWindowWidth() {\n  const [width, setWidth] = useState(window.innerWidth);\n\n  useEffect(() => {\n    const handleResize = () => setWidth(window.innerWidth);\n    window.addEventListener('resize', handleResize);\n    // Teardown cleanup function on unmount\n    return () => window.removeEventListener('resize', handleResize);\n  }, []); // Empty array: runs once on mount\n\n  return width;\n}",
                        "explanation": "Custom hook encapsulating resize listener lifecycle with guaranteed unmount cleanup."
                    },
                    "key_takeaways": [
                        "Always list all reactive values read inside `useEffect` in its dependency array.",
                        "Empty dependency array `[]` runs once on mount and cleans up on unmount.",
                        "Custom hooks must begin with the `use` prefix to adhere to React Hook rules."
                    ],
                    "practice_questions": [
                        {
                            "question": "What is the consequence of omitting a state variable from a `useEffect` dependency array?",
                            "answer": "The effect will capture a stale closure of that variable and fail to re-execute when the state changes.",
                            "explanation": "React checks dependency array equality to decide whether to re-invoke the effect."
                        }
                    ]
                },
                "videos": [
                    {
                        "id": "v-fs-2",
                        "title": "Learn useEffect in 13 Minutes",
                        "channel": "Web Dev Simplified",
                        "embed_url": "https://www.youtube-nocookie.com/embed/0ZJgIjIuY7U",
                        "watch_url": "https://www.youtube.com/watch?v=0ZJgIjIuY7U",
                        "search_url": "https://www.youtube.com/results?search_query=web+dev+simplified+useeffect",
                        "duration": "13 mins",
                        "summary": "Covers dependency arrays, when effects run, and why cleanup functions prevent memory leaks."
                    }
                ]
            },
            {
                "id": "m-fs-3",
                "title": "API Integration & Resilient Data Fetching",
                "description": "Axios/Fetch, query caching, AbortController cancellation, and error boundaries.",
                "estimated_minutes": 25,
                "study_notes": {
                    "introduction": "Production web clients must handle network latency, transient failures, and component unmounts defensively. Using `AbortController` eliminates race conditions when users rapidly switch views or update search queries.",
                    "concepts": [
                        {
                            "term": "AbortController",
                            "definition": "Web API that can abort active `fetch` requests via an `AbortSignal`, canceling in-flight HTTP requests cleanly."
                        },
                        {
                            "term": "Network Race Conditions",
                            "definition": "A bug where a slow earlier request resolves AFTER a faster newer request, overwriting current UI state with stale data."
                        },
                        {
                            "term": "Error Boundaries",
                            "definition": "Class components that catch JavaScript runtime errors anywhere in their child component tree, rendering fallback UI."
                        }
                    ],
                    "step_by_step": [
                        {
                            "step": "1",
                            "title": "Instantiate Controller",
                            "description": "Create `const controller = new AbortController()` inside your fetch effect."
                        },
                        {
                            "step": "2",
                            "title": "Attach Signal",
                            "description": "Pass `{ signal: controller.signal }` to your `fetch()` or Axios call."
                        },
                        {
                            "step": "3",
                            "title": "Abort on Teardown",
                            "description": "Return `() => controller.abort()` in the effect cleanup callback."
                        }
                    ],
                    "code_example": {
                        "language": "tsx",
                        "code": "useEffect(() => {\n  const controller = new AbortController();\n  \n  fetch(`/api/courses/${courseId}/resources`, { signal: controller.signal })\n    .then(res => res.json())\n    .then(data => setResources(data))\n    .catch(err => {\n      if (err.name !== 'AbortError') {\n        setError(err.message);\n      }\n    });\n\n  return () => controller.abort(); // Cancel pending fetch on unmount or course change\n}, [courseId]);",
                        "explanation": "Guarantees that pending fetches are canceled if the user switches courses, preventing race conditions."
                    },
                    "key_takeaways": [
                        "Always catch `AbortError` separately so user-canceled fetches don't show error banners.",
                        "Use AbortController to prevent race conditions during rapid typing in search bars.",
                        "Error boundaries prevent an unhandled rendering error from crashing the entire application."
                    ],
                    "practice_questions": [
                        {
                            "question": "Why is `err.name === 'AbortError'` checked in fetch catch blocks?",
                            "answer": "To ignore intentional cancellations without displaying false network failure alerts to the user.",
                            "explanation": "When `controller.abort()` is called, the fetch promise rejects with an DOMException named 'AbortError'."
                        }
                    ]
                },
                "videos": [
                    {
                        "id": "v-fs-3",
                        "title": "How to Cancel API Requests with AbortController",
                        "channel": "Web Dev Simplified",
                        "embed_url": "https://www.youtube-nocookie.com/embed/gL3xep_J_jI",
                        "watch_url": "https://www.youtube.com/watch?v=gL3xep_J_jI",
                        "search_url": "https://www.youtube.com/results?search_query=web+dev+simplified+abortcontroller",
                        "duration": "10 mins",
                        "summary": "Demonstrates connecting AbortController to fetch requests inside useEffect for memory leak prevention."
                    }
                ]
            },
            {
                "id": "m-fs-4",
                "title": "Full-Stack Security & Authentication",
                "description": "JWT, HTTP-only cookies, CORS, Row-Level Security (RLS), and API protection.",
                "estimated_minutes": 25,
                "study_notes": {
                    "introduction": "Web security protects learner identities and platform data against unauthorized access. Modern architectures combine cryptographic tokens (JWTs), HTTP-only cookies to prevent XSS theft, strict CORS headers, and database Row-Level Security (RLS).",
                    "concepts": [
                        {
                            "term": "HTTP-Only Cookies",
                            "definition": "Cookies with the `HttpOnly` flag cannot be accessed via client-side JavaScript (`document.cookie`), shielding session tokens from XSS attacks."
                        },
                        {
                            "term": "Cross-Origin Resource Sharing (CORS)",
                            "definition": "Browser security mechanism that restricts cross-origin HTTP requests unless the server explicitly grants access via `Access-Control-Allow-Origin`."
                        },
                        {
                            "term": "Row-Level Security (RLS)",
                            "definition": "Database-level policy ensuring that SQL queries can only access rows matching the authenticated user's ID."
                        }
                    ],
                    "step_by_step": [
                        {
                            "step": "1",
                            "title": "Issue Cryptographic Tokens",
                            "description": "Issue signed JWT tokens containing user ID, role, and expiration timestamp."
                        },
                        {
                            "step": "2",
                            "title": "Configure CORS Allowlist",
                            "description": "Configure FastAPI `CORSMiddleware` with explicit allowed origins rather than wildcard `*` when credentials are used."
                        },
                        {
                            "step": "3",
                            "title": "Enforce Tenant Isolation",
                            "description": "Filter all database queries with `WHERE learner_id = ?` to prevent cross-learner data leakage."
                        }
                    ],
                    "code_example": {
                        "language": "python",
                        "code": "# FastAPI CORS Configuration with explicit origin validation\nfrom fastapi.middleware.cors import CORSMiddleware\n\norigins = ['https://skillforge.vercel.app', 'http://localhost:5173']\n\napp.add_middleware(\n    CORSMiddleware,\n    allow_origins=origins,\n    allow_credentials=True,\n    allow_methods=['*'],\n    allow_headers=['*'],\n)",
                        "explanation": "Guarantees that only authorized frontend origins can transmit credentials and access API endpoints."
                    },
                    "key_takeaways": [
                        "Never store sensitive session JWTs in unencrypted `localStorage` if vulnerable to XSS.",
                        "When using `allow_credentials=True`, CORS prohibits `allow_origins=['*']`.",
                        "Always validate user identity on the backend; never trust client-provided IDs blindly."
                    ],
                    "practice_questions": [
                        {
                            "question": "What is the primary advantage of storing session tokens in HTTP-only cookies rather than localStorage?",
                            "answer": "HTTP-only cookies are inaccessible to malicious JavaScript scripts injected via XSS vulnerabilities.",
                            "explanation": "Browsers restrict JavaScript access to HTTP-only cookies, transmitting them automatically only in HTTP headers."
                        }
                    ]
                },
                "videos": [
                    {
                        "id": "v-fs-4",
                        "title": "JWT Authentication Tutorial: Cookies vs LocalStorage",
                        "channel": "Web Dev Simplified",
                        "embed_url": "https://www.youtube-nocookie.com/embed/mbsmsi7l3r4",
                        "watch_url": "https://www.youtube.com/watch?v=mbsmsi7l3r4",
                        "search_url": "https://www.youtube.com/results?search_query=web+dev+simplified+jwt+authentication",
                        "duration": "15 mins",
                        "summary": "Compares JWT storage in cookies vs localStorage and explains access vs refresh token architecture."
                    }
                ]
            }
        ]
    },
    "c-datasci": {
        "course_id": "c-datasci",
        "course_title": "Data Science & Machine Learning Engineering",
        "domain": "Data Science & AI",
        "level": "Intermediate to Advanced",
        "description": "Data analysis, vectorization, statistical modeling, feature engineering, and neural network pipelines.",
        "diagnostic_assessment_id": "a-datasci-diag",
        "topics": [
            {
                "id": "m-ds-1",
                "title": "Vectorized Operations with NumPy",
                "description": "Broadcasting, linear algebra operations, slicing, and high-performance array computation.",
                "estimated_minutes": 20,
                "study_notes": {
                    "introduction": "NumPy replaces slow Python iteration loops with compiled, contiguous C-level `ndarray` structures, enabling vectorized arithmetic operations at hardware memory speeds.",
                    "concepts": [
                        {
                            "term": "Vectorization",
                            "definition": "Executing mathematical operations across entire arrays simultaneously without explicit Python for-loops."
                        },
                        {
                            "term": "Broadcasting Semantics",
                            "definition": "Rules that expand dimensions of size 1 across larger dimensions during arithmetic operations."
                        },
                        {
                            "term": "Memory Strides",
                            "definition": "Fixed byte step sizes used to navigate contiguous memory buffers, enabling instantaneous slicing and transposing."
                        }
                    ],
                    "step_by_step": [
                        {
                            "step": "1",
                            "title": "Array Allocation",
                            "description": "Create ndarrays using `np.array()`, `np.zeros()`, `np.ones()`, or `np.arange()`."
                        },
                        {
                            "step": "2",
                            "title": "Broadcasting Operations",
                            "description": "Add vectors to matrices: `matrix + bias` without manual looping."
                        },
                        {
                            "step": "3",
                            "title": "Boolean Masking",
                            "description": "Filter data conditionally: `filtered = arr[arr > threshold]`."
                        }
                    ],
                    "code_example": {
                        "language": "python",
                        "code": "import numpy as np\n\n# 3 learners across 4 test attempts\nscores = np.array([\n    [85, 90, 78, 92],\n    [60, 65, 58, 70],\n    [95, 98, 92, 100]\n])\n\n# Calculate mean per learner across columns (axis 1)\naverag = scores.mean(axis=1)\nprint('Averages:', averag) # [86.25, 63.25, 96.25]\n\n# Identify learners with average >= 80\nhonor_roll = scores[averag >= 80]\nprint('Honors:', len(honor_roll)) # 2",
                        "explanation": "Shows axis reduction and boolean array masking executed at compiled C speed."
                    },
                    "key_takeaways": [
                        "Always prefer NumPy vectorized universal functions (ufuncs) over Python `for` loops.",
                        "Broadcasting aligns trailing dimensions from right to left.",
                        "Array slicing returns views; use `.copy()` if an independent clone is required."
                    ],
                    "practice_questions": [
                        {
                            "question": "Can an array of shape (3, 1) be added to an array of shape (3, 5)?",
                            "answer": "Yes. The dimension of size 1 automatically expands across all 5 columns.",
                            "explanation": "Trailing dimensions are compatible when they match or one of them is 1."
                        }
                    ]
                },
                "videos": [
                    {
                        "id": "v-ds-1",
                        "title": "Python NumPy Tutorial for Beginners",
                        "channel": "freeCodeCamp.org",
                        "embed_url": "https://www.youtube-nocookie.com/embed/QUT1VHiLmmI",
                        "watch_url": "https://www.youtube.com/watch?v=QUT1VHiLmmI",
                        "search_url": "https://www.youtube.com/results?search_query=freecodecamp+numpy+tutorial",
                        "duration": "24 mins",
                        "summary": "Covers multi-dimensional arrays, slicing, broadcasting, and linear algebra operations."
                    }
                ]
            },
            {
                "id": "m-ds-2",
                "title": "Data Wrangling with Pandas",
                "description": "DataFrames, multi-indexing, groupby, joins, and data cleansing.",
                "estimated_minutes": 25,
                "study_notes": {
                    "introduction": "Pandas provides two-dimensional tabular `DataFrame` structures for data cleaning, reshaping, aggregation, and merging. Mastering label-based `.loc` and position-based `.iloc` indexing prevents subtle indexing errors.",
                    "concepts": [
                        {
                            "term": ".loc vs .iloc",
                            "definition": "`.loc` indexes by index labels and column names. `.iloc` indexes strictly by integer positions (0, 1, 2...)."
                        },
                        {
                            "term": "Split-Apply-Combine",
                            "definition": "The GroupBy design pattern: dividing data into groups, applying an aggregate function, and combining outputs."
                        },
                        {
                            "term": "Handling Missing Data",
                            "definition": "Detecting NaNs with `.isna()`, dropping with `.dropna()`, or imputing with `.fillna()`."
                        }
                    ],
                    "step_by_step": [
                        {
                            "step": "1",
                            "title": "Loading Data",
                            "description": "Inspect structure with `df.head()`, `df.info()`, and `df.describe()`."
                        },
                        {
                            "step": "2",
                            "title": "Filtering Records",
                            "description": "Filter rows with conditions: `df[df['score'] >= 80]`."
                        },
                        {
                            "step": "3",
                            "title": "Grouping and Aggregating",
                            "description": "Group by category: `df.groupby('domain')['score'].mean()`."
                        }
                    ],
                    "code_example": {
                        "language": "python",
                        "code": "import pandas as pd\n\ndf = pd.DataFrame({\n    'learner': ['Alice', 'Bob', 'Charlie', 'Dana'],\n    'track': ['Python', 'Web', 'Python', 'AI'],\n    'score': [92, 85, 74, 96]\n})\n\n# Compute average score per track\navgs = df.groupby('track')['score'].mean().reset_index()\nprint(avgs)\n#     track  score\n# 0      AI   96.0\n# 1  Python   83.0\n# 2     Web   85.0",
                        "explanation": "Demonstrates group-by aggregation to summarize performance metrics per educational domain."
                    },
                    "key_takeaways": [
                        "`.loc` is label-based (inclusive of start and end).",
                        "`.iloc` is integer position-based (stop index is exclusive).",
                        "Method chaining creates expressive, readable data transformation pipelines."
                    ],
                    "practice_questions": [
                        {
                            "question": "What is the difference between `df['col']` and `df[['col']]`?",
                            "answer": "`df['col']` returns a 1D Pandas Series; `df[['col']]` returns a 2D DataFrame.",
                            "explanation": "Passing a single string returns a Series; passing a list returns a DataFrame."
                        }
                    ]
                },
                "videos": [
                    {
                        "id": "v-ds-2",
                        "title": "Pandas Full Tutorial: Learn Data Analysis with Python",
                        "channel": "freeCodeCamp.org",
                        "embed_url": "https://www.youtube-nocookie.com/embed/vmEHCJofslg",
                        "watch_url": "https://www.youtube.com/watch?v=vmEHCJofslg",
                        "search_url": "https://www.youtube.com/results?search_query=freecodecamp+pandas+data+analysis",
                        "duration": "28 mins",
                        "summary": "Covers DataFrames, reading CSVs, filtering rows, handling NaNs, and groupby operations."
                    }
                ]
            },
            {
                "id": "m-ds-3",
                "title": "Statistical Testing & Modeling",
                "description": "Hypothesis testing, p-values, regression, and distribution analysis.",
                "estimated_minutes": 25,
                "study_notes": {
                    "introduction": "Statistical inference allows data scientists to draw conclusions about populations from sample observations. Hypothesis testing provides formal frameworks (t-tests, ANOVA, chi-square) to evaluate whether observed differences are statistically significant.",
                    "concepts": [
                        {
                            "term": "Null Hypothesis (H0)",
                            "definition": "The default assumption that there is no true difference or effect. We seek evidence to reject H0."
                        },
                        {
                            "term": "p-value",
                            "definition": "The probability of observing results at least as extreme as the sample data, assuming the null hypothesis is true."
                        },
                        {
                            "term": "Significance Level (Alpha)",
                            "definition": "The probability threshold (typically 0.05) below which we reject the null hypothesis in favor of the alternative."
                        }
                    ],
                    "step_by_step": [
                        {
                            "step": "1",
                            "title": "State Hypotheses",
                            "description": "Define H0 (no effect) and H1 (significant difference)."
                        },
                        {
                            "step": "2",
                            "title": "Select Significance Threshold",
                            "description": "Establish alpha (typically alpha = 0.05)."
                        },
                        {
                            "step": "3",
                            "title": "Calculate Test Statistic & p-value",
                            "description": "If p-value < alpha, reject H0 and conclude statistical significance."
                        }
                    ],
                    "code_example": {
                        "language": "python",
                        "code": "# Two-sample t-test using scipy.stats\nfrom scipy import stats\n\ngroup_a = [88, 92, 95, 89, 94]\ngroup_b = [72, 75, 78, 71, 74]\n\nt_stat, p_val = stats.ttest_ind(group_a, group_b)\nprint(f'p-value: {p_val:.4f}') # e.g. p < 0.001\n\nif p_val < 0.05:\n    print('Statistically significant difference detected: Reject H0.')",
                        "explanation": "Computes two-sample t-statistic and evaluates p-value against the alpha = 0.05 threshold."
                    },
                    "key_takeaways": [
                        "p < 0.05 means the observed result is unlikely under the null hypothesis alone.",
                        "Statistical significance does not automatically guarantee practical importance.",
                        "Always inspect data distributions for normality before applying parametric tests."
                    ],
                    "practice_questions": [
                        {
                            "question": "If a test yields p = 0.03 at alpha = 0.05, what is the conclusion?",
                            "answer": "Reject the null hypothesis; the result is statistically significant at the 5% level.",
                            "explanation": "Because 0.03 < 0.05, we reject H0."
                        }
                    ]
                },
                "videos": [
                    {
                        "id": "v-ds-3",
                        "title": "Hypothesis Testing and p-values Explained Clearly",
                        "channel": "StatQuest with Josh Starmer",
                        "embed_url": "https://www.youtube-nocookie.com/embed/tTeMYuS87oU",
                        "watch_url": "https://www.youtube.com/watch?v=tTeMYuS87oU",
                        "search_url": "https://www.youtube.com/results?search_query=statquest+hypothesis+testing+p+values",
                        "duration": "14 mins",
                        "summary": "Visual, intuitive explanation of null hypotheses, distributions, and p-value calculations."
                    }
                ]
            },
            {
                "id": "m-ds-4",
                "title": "Neural Networks & Deep Learning",
                "description": "Perceptrons, backpropagation, activation functions, optimizers, and loss surfaces.",
                "estimated_minutes": 25,
                "study_notes": {
                    "introduction": "Neural networks learn complex non-linear representations from high-dimensional data. Forward propagation computes predictions through layered linear transformations and activation functions, while backpropagation computes analytical gradients via the calculus chain rule.",
                    "concepts": [
                        {
                            "term": "Activation Functions",
                            "definition": "Non-linear functions (ReLU, Sigmoid, GELU) that enable networks to approximate non-linear functions."
                        },
                        {
                            "term": "Backpropagation",
                            "definition": "Algorithm calculating partial derivatives of the loss function with respect to weights using the chain rule."
                        },
                        {
                            "term": "Gradient Descent Optimizer",
                            "definition": "Iterative optimization algorithm (SGD, Adam) that adjusts weights in the negative gradient direction to minimize loss."
                        }
                    ],
                    "step_by_step": [
                        {
                            "step": "1",
                            "title": "Forward Pass",
                            "description": "Multiply inputs by weight matrices, add bias, and apply activation functions: `z = Wx + b`, `a = relu(z)`."
                        },
                        {
                            "step": "2",
                            "title": "Calculate Loss",
                            "description": "Compute discrepancy between prediction and ground-truth using MSE or Cross-Entropy loss."
                        },
                        {
                            "step": "3",
                            "title": "Backward Pass & Update",
                            "description": "Propagate gradients backward and update weights: `W = W - learning_rate * grad`."
                        }
                    ],
                    "code_example": {
                        "language": "python",
                        "code": "# Simple Perceptron forward pass with ReLU\nimport numpy as np\n\ndef relu(x):\n    return np.maximum(0, x)\n\nX = np.array([0.5, 0.8]) # 2 input features\nW = np.array([[0.2, 0.4], [0.1, -0.3]]) # 2x2 weight matrix\nb = np.array([0.1, 0.05]) # bias\n\n# Forward pass\nz = np.dot(X, W) + b\nactivations = relu(z)\nprint('Layer activations:', activations)",
                        "explanation": "Calculates matrix dot product and applies ReLU activation non-linearity."
                    },
                    "key_takeaways": [
                        "ReLU mitigates the vanishing gradient problem for positive inputs compared to Sigmoid.",
                        "Learning rate controls step size along the loss gradient surface.",
                        "Backpropagation efficiently computes analytical gradients using the chain rule."
                    ],
                    "practice_questions": [
                        {
                            "question": "What happens if the learning rate is set too large?",
                            "answer": "Weights diverge or oscillate wildly across the loss surface, failing to converge.",
                            "explanation": "A high learning rate overshoots the minimum point on the loss gradient."
                        }
                    ]
                },
                "videos": [
                    {
                        "id": "v-ds-4",
                        "title": "Neural Networks: But what is a neural network? (Deep Learning Chapter 1)",
                        "channel": "3Blue1Brown",
                        "embed_url": "https://www.youtube-nocookie.com/embed/aircAruvnKk",
                        "watch_url": "https://www.youtube.com/watch?v=aircAruvnKk",
                        "search_url": "https://www.youtube.com/results?search_query=3blue1brown+neural+networks+chapter+1",
                        "duration": "19 mins",
                        "summary": "World-class visual animations breaking down neurons, weights, biases, and activation layers."
                    }
                ]
            }
        ]
    },
    "c-ai-eng": {
        "course_id": "c-ai-eng",
        "course_title": "AI Engineering & Autonomous LLM Systems",
        "domain": "Artificial Intelligence",
        "level": "Advanced",
        "description": "Design production RAG systems, tool-calling agents, vector database indexing, and structured evaluation.",
        "diagnostic_assessment_id": "a-ai-diag",
        "topics": [
            {
                "id": "m-ai-1",
                "title": "Prompt Engineering & Structured Outputs",
                "description": "Few-shot prompting, JSON schema constraints, system delimiters, and deterministic token steering.",
                "estimated_minutes": 20,
                "study_notes": {
                    "introduction": "Prompt engineering transforms probabilistic LLMs into deterministic software components. In enterprise AI applications, prompts enforce rigid JSON Schema contracts, few-shot patterns, and strict behavioral boundaries.",
                    "concepts": [
                        {
                            "term": "System Instructions",
                            "definition": "The foundational behavioral directive defining role, tone, output boundaries, and execution constraints."
                        },
                        {
                            "term": "Few-Shot Demonstrations",
                            "definition": "Providing 2-5 explicit (Input -> Output) examples in-context to guide the model's output formatting and reasoning pattern."
                        },
                        {
                            "term": "JSON Schema Enforcement",
                            "definition": "Constraining token decoding to ensure responses parse directly into typed Pydantic or TypeScript models."
                        }
                    ],
                    "step_by_step": [
                        {
                            "step": "1",
                            "title": "Use Structured Delimiters",
                            "description": "Separate context, user inputs, and guidelines using markdown headers or triple quotes (`\"\"\"`)."
                        },
                        {
                            "step": "2",
                            "title": "Provide Realistic Demonstrations",
                            "description": "Show the exact target schema with realistic input-output pairs."
                        },
                        {
                            "step": "3",
                            "title": "Constrain Response Schema",
                            "description": "Instruct the model: 'Respond strictly in valid JSON matching this schema: {\"score\": int, \"notes\": str}'."
                        }
                    ],
                    "code_example": {
                        "language": "python",
                        "code": "from pydantic import BaseModel\n\nclass TutorFeedback(BaseModel):\n    score: int\n    passed: bool\n    key_finding: str\n\nprompt = \"\"\"\nYou are an automated coding evaluator.\nReturn strictly valid JSON matching the TutorFeedback schema.\n\nInput:\ndef two_sum(nums, target): return []\n\nOutput JSON:\n{\"score\": 33, \"passed\": false, \"key_finding\": \"Returns empty list without computing target\"}\n\"\"\"",
                        "explanation": "Combines explicit role prompting with concrete schema examples to achieve reliable structured JSON output."
                    },
                    "key_takeaways": [
                        "Delimiters prevent prompt injection by isolating user inputs from system instructions.",
                        "Few-shot examples significantly improve schema compliance over zero-shot instructions.",
                        "Always validate model outputs against backend Pydantic models before returning to clients."
                    ],
                    "practice_questions": [
                        {
                            "question": "Why is concatenating raw user input directly into system prompts dangerous?",
                            "answer": "It enables prompt injection, allowing attackers to override system instructions and extract internal secrets.",
                            "explanation": "Separating user input using delimiters or structured API parameters prevents injection."
                        }
                    ]
                },
                "videos": [
                    {
                        "id": "v-ai-1",
                        "title": "ChatGPT Prompt Engineering for Developers",
                        "channel": "DeepLearning.AI",
                        "embed_url": "https://www.youtube-nocookie.com/embed/jC4v5AS4RIM",
                        "watch_url": "https://www.youtube.com/watch?v=jC4v5AS4RIM",
                        "search_url": "https://www.youtube.com/results?search_query=deeplearning+ai+prompt+engineering+andrew+ng",
                        "duration": "20 mins",
                        "summary": "Andrew Ng and Isa Fulford explain principles of clear prompting, delimiters, few-shot prompting, and structured outputs."
                    }
                ]
            },
            {
                "id": "m-ai-2",
                "title": "Vector Embeddings & Semantic Search",
                "description": "Dense vectors, cosine similarity, hybrid search, and vector database indexing.",
                "estimated_minutes": 25,
                "study_notes": {
                    "introduction": "Vector embeddings represent text passages as high-dimensional coordinates in semantic space. By calculating distance metrics (Cosine Similarity or Dot Product), vector databases retrieve semantically related content even without exact keyword overlap.",
                    "concepts": [
                        {
                            "term": "Vector Embedding",
                            "definition": "A dense numerical vector (e.g. 768, 1536 dimensions) capturing the semantic meaning of a word, sentence, or document passage."
                        },
                        {
                            "term": "Cosine Similarity",
                            "definition": "Metric measuring the cosine of the angle between two vectors: `cos(theta) = (A . B) / (||A|| * ||B||)`. Ranges from -1 to 1."
                        },
                        {
                            "term": "Approximate Nearest Neighbors (ANN)",
                            "definition": "Indexing algorithms (HNSW, IVF) that search billions of vectors in sub-millisecond latency by approximating closest neighbors."
                        }
                    ],
                    "step_by_step": [
                        {
                            "step": "1",
                            "title": "Generate Passage Embeddings",
                            "description": "Pass document chunks to an embedding model: `vec = embed('Python mutability')`."
                        },
                        {
                            "step": "2",
                            "title": "Index in Vector Store",
                            "description": "Store vectors alongside metadata (chunk ID, course ID, document title)."
                        },
                        {
                            "step": "3",
                            "title": "Perform Similarity Search",
                            "description": "Embed learner queries and search for top-k closest vectors using cosine similarity."
                        }
                    ],
                    "code_example": {
                        "language": "python",
                        "code": "import numpy as np\n\ndef cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:\n    # Normalized dot product\n    norm_v1 = np.linalg.norm(v1)\n    norm_v2 = np.linalg.norm(v2)\n    if norm_v1 == 0 or norm_v2 == 0:\n        return 0.0\n    return float(np.dot(v1, v2) / (norm_v1 * norm_v2))\n\n# Compare query vector with candidate chunk\nq_vec = np.array([0.2, 0.8, -0.1])\nchunk_vec = np.array([0.25, 0.75, -0.05])\nsim = cosine_similarity(q_vec, chunk_vec)\nprint(f'Cosine Similarity: {sim:.4f}') # ~ 0.99 (High semantic similarity)",
                        "explanation": "Calculates cosine similarity to measure semantic proximity between query and document vectors."
                    },
                    "key_takeaways": [
                        "For unit-normalized vectors, cosine similarity equals the dot product.",
                        "Vector embeddings capture conceptual meaning, not just exact keyword matches.",
                        "Hybrid search combines vector search (synonyms) with BM25 keyword search (acronyms)."
                    ],
                    "practice_questions": [
                        {
                            "question": "What is the cosine similarity between two identical vectors?",
                            "answer": "1.0",
                            "explanation": "The angle between identical vectors is 0 degrees; `cos(0) = 1`."
                        }
                    ]
                },
                "videos": [
                    {
                        "id": "v-ai-2",
                        "title": "Word and Sentence Embeddings Explained Clearly",
                        "channel": "StatQuest with Josh Starmer",
                        "embed_url": "https://www.youtube-nocookie.com/embed/ySus5ZS0b94",
                        "watch_url": "https://www.youtube.com/watch?v=ySus5ZS0b94",
                        "search_url": "https://www.youtube.com/results?search_query=statquest+neural+network+embeddings",
                        "duration": "16 mins",
                        "summary": "Visual step-by-step explanation of high-dimensional vectors, semantic distance, and word embedding spaces."
                    }
                ]
            },
            {
                "id": "m-ai-3",
                "title": "RAG Pipelines & Chunking Strategies",
                "description": "Document chunking, re-ranking, context injection, and citation grounding.",
                "estimated_minutes": 25,
                "study_notes": {
                    "introduction": "Retrieval-Augmented Generation (RAG) grounds LLM responses in verified external knowledge. By chunking documents with overlap, indexing into vector databases, and injecting retrieved passages into system prompts, RAG eliminates hallucinations.",
                    "concepts": [
                        {
                            "term": "Chunk Overlap",
                            "definition": "Retaining 50-100 tokens of overlap across adjacent chunks to prevent sentences and context from being severed."
                        },
                        {
                            "term": "Context Window Injection",
                            "definition": "Formatting retrieved document excerpts into the LLM system prompt as explicit source material."
                        },
                        {
                            "term": "Re-ranking",
                            "definition": "Using a cross-encoder model to re-score top retrieved chunks, prioritizing high-precision relevance."
                        }
                    ],
                    "step_by_step": [
                        {
                            "step": "1",
                            "title": "Document Parsing & Chunking",
                            "description": "Split documents into semantic passages (e.g. 500 characters with 100 character overlap)."
                        },
                        {
                            "step": "2",
                            "title": "Retrieval by Similarity",
                            "description": "Embed learner query and retrieve top-k chunks from the vector database."
                        },
                        {
                            "step": "3",
                            "title": "Grounded Generation",
                            "description": "Inject retrieved excerpts into prompt: 'Answer using only the provided notes. Cite source chunks.'."
                        }
                    ],
                    "code_example": {
                        "language": "python",
                        "code": "# Grounded RAG prompt template\ndef build_rag_prompt(query: str, retrieved_chunks: list[str]) -> str:\n    joined_context = '\\n---\\n'.join(retrieved_chunks)\n    return f\"\"\"\n    You are an AI Tutor. Answer the question using ONLY the provided study notes.\n    If the answer is not in the excerpts, say 'I cannot find that in the notes.'\n\n    Notes Excerpts:\n    {joined_context}\n\n    Learner Question: {query}\n    \"\"\"",
                        "explanation": "Constrains LLM generation strictly to retrieved document excerpts to prevent hallucination."
                    },
                    "key_takeaways": [
                        "Chunk overlap preserves semantic relationships across boundaries.",
                        "Always instruct RAG models to admit when context is insufficient rather than guessing.",
                        "Re-ranking retrieved passages improves answer accuracy by up to 30%."
                    ],
                    "practice_questions": [
                        {
                            "question": "What is the danger of chunks that are too small (e.g. 20 words)?",
                            "answer": "They lack sufficient semantic context to be accurately matched during retrieval and answer synthesis.",
                            "explanation": "Micro-chunks lose sentence continuity and core conceptual relationships."
                        }
                    ]
                },
                "videos": [
                    {
                        "id": "v-ai-3",
                        "title": "Retrieval Augmented Generation (RAG) Explained",
                        "channel": "freeCodeCamp.org",
                        "embed_url": "https://www.youtube-nocookie.com/embed/T-D1OfcDW1M",
                        "watch_url": "https://www.youtube.com/watch?v=T-D1OfcDW1M",
                        "search_url": "https://www.youtube.com/results?search_query=freecodecamp+rag+explained",
                        "duration": "22 mins",
                        "summary": "Deep dive into vector embeddings, document chunking, similarity indexing, and context-injected generation."
                    }
                ]
            },
            {
                "id": "m-ai-4",
                "title": "Autonomous Agents & Tool Calling",
                "description": "ReAct loops, function calling, stateful memory, and agent orchestration.",
                "estimated_minutes": 25,
                "study_notes": {
                    "introduction": "Autonomous AI agents combine LLM reasoning with tool execution. Using the ReAct (Reasoning + Acting) cycle, agents iteratively inspect user goals, decide which tools to call with JSON schemas, observe tool outputs, and adjust their strategy until the objective is accomplished.",
                    "concepts": [
                        {
                            "term": "ReAct Cycle",
                            "definition": "Thought -> Action -> Observation loop where the agent reflects, invokes a tool, observes the output, and iterates."
                        },
                        {
                            "term": "Tool Calling Protocol",
                            "definition": "Standardized JSON Schema definitions describing available functions, argument types, and constraints to the LLM."
                        },
                        {
                            "term": "Agent Guardrails",
                            "definition": "Execution limits on maximum iterations, recursion depth, and tool timeouts to prevent infinite loops."
                        }
                    ],
                    "step_by_step": [
                        {
                            "step": "1",
                            "title": "Define Tool Schemas",
                            "description": "Declare available tools using JSON Schema: `search_docs(query: str)`, `calculate(expr: str)`."
                        },
                        {
                            "step": "2",
                            "title": "Run ReAct Agent Loop",
                            "description": "LLM inspects task, generates tool call payload, backend executes tool, and returns observation."
                        },
                        {
                            "step": "3",
                            "title": "Synthesize Final Response",
                            "description": "When the agent determines all requirements are satisfied, it returns the final solution."
                        }
                    ],
                    "code_example": {
                        "language": "python",
                        "code": "# Conceptual ReAct execution loop\ndef run_agent_turn(user_goal: str, tools: dict):\n    messages = [{'role': 'user', 'content': user_goal}]\n    for iteration in range(5): # Guardrail: max 5 turns\n        decision = llm_decide_next_step(messages, tools)\n        if decision.is_final:\n            return decision.final_answer\n        \n        # Execute chosen tool\n        observation = tools[decision.tool_name](**decision.tool_args)\n        messages.append({'role': 'tool', 'name': decision.tool_name, 'content': observation})\n    return 'Agent reached maximum iteration limit.'",
                        "explanation": "Demonstrates the iterative ReAct loop with guardrails against runaway execution."
                    },
                    "key_takeaways": [
                        "ReAct combines explicit reasoning traces with deterministic tool execution.",
                        "Always set max-iteration guardrails to prevent infinite tool-calling loops.",
                        "Validate all tool inputs against schemas before execution."
                    ],
                    "practice_questions": [
                        {
                            "question": "What is the purpose of the 'Observation' step in a ReAct agent loop?",
                            "answer": "It provides the real-world output of the executed tool back to the LLM for subsequent reasoning.",
                            "explanation": "Without the observation, the agent cannot verify whether the tool succeeded or adapt its plan."
                        }
                    ]
                },
                "videos": [
                    {
                        "id": "v-ai-4",
                        "title": "What are AI Agents? Autonomous LLM Tool Calling",
                        "channel": "IBM Technology",
                        "embed_url": "https://www.youtube-nocookie.com/embed/bZQun8Y4L2A",
                        "watch_url": "https://www.youtube.com/watch?v=bZQun8Y4L2A",
                        "search_url": "https://www.youtube.com/results?search_query=ibm+technology+what+are+ai+agents",
                        "duration": "12 mins",
                        "summary": "Explains the ReAct loop, tool calling protocols, stateful memory, and multi-step autonomous problem solving."
                    }
                ]
            }
        ]
    }
}
