import unittest
import os
import sys

# Ensure backend directory is in sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.main import root, health_check
from app.db.storage import init_db, seed_initial_catalog
from app.db.scenarios import DEMO_SCENARIOS, load_scenario
from app.api.profile_routes import get_learner_profile, update_learner_profile, login_learner, register_learner
from app.api.course_goal_routes import list_courses, get_learning_goals, create_learning_goal
from app.api.assessment_routes import start_assessment, submit_assessment, get_skill_profile
from app.api.roadmap_routes import get_current_learning_path, generate_learning_path
from app.api.tutor_routes import chat_with_tutor, get_tutor_history
from app.api.study_routes import get_flashcards, review_flashcard
from app.api.challenge_routes import get_challenge_detail, submit_challenge
from app.api.project_routes import list_mini_projects, generate_mini_project, evaluate_project_submission
from app.api.progress_routes import get_progress_summary, get_progress_history
from app.api.demo_routes import list_demo_scenarios, switch_active_scenario
from app.api.course_learning_routes import (
    get_course_learning_resources,
    list_student_notes,
    create_student_note,
    update_student_note,
    delete_student_note
)
from app.models.schemas import (
    LearnerProfileUpdate, LearningGoalCreate,
    AssessmentSubmitRequest, QuestionAnswer,
    TutorChatRequest, ChallengeSubmitRequest, SubmissionEvaluateRequest,
    StudentNoteCreate, StudentNoteUpdate
)
from app.services.notes_service import process_document_and_extract, generate_study_tools_from_notes

class TestSkillForgeBackend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        seed_initial_catalog()

    def test_01_root_and_health(self):
        r = root()
        self.assertEqual(r["platform"], "SkillForge AI")
        self.assertEqual(r["status"], "operational")

        h = health_check()
        self.assertEqual(h["status"], "healthy")
        self.assertTrue(h["tutor_ready"])

    def test_02_all_10_demo_scenarios_switch(self):
        scenarios = list_demo_scenarios()
        self.assertEqual(len(scenarios), 10)

        for s in scenarios:
            sid = s["id"]
            res = switch_active_scenario(sid)
            self.assertEqual(res["status"], "success")
            self.assertEqual(res["learner_id"], f"demo-learner-{sid}")
            self.assertIn("title", res["scenario"])

    def test_03_learner_profile_and_goals(self):
        # Switch to Scenario 1: Maya Chen (Beginner)
        switch_active_scenario("1")
        prof = get_learner_profile(x_learner_id="demo-learner-1")
        self.assertEqual(prof.email, "maya@demo.skillforge.ai")
        self.assertEqual(prof.experience_level, "beginner")

        # Update profile
        updated = update_learner_profile(
            update_data=LearnerProfileUpdate(daily_minutes=50, learning_style="hands-on"),
            x_learner_id="demo-learner-1"
        )
        self.assertEqual(updated.daily_minutes, 50)

        # Courses Catalog
        courses = list_courses()
        self.assertGreaterEqual(len(courses), 4)
        slugs = [c.slug for c in courses]
        self.assertIn("python-programming", slugs)
        self.assertIn("full-stack-web", slugs)

        # Learning Goals
        goals = get_learning_goals(x_learner_id="demo-learner-1")
        self.assertGreaterEqual(len(goals), 1)

    def test_04_diagnostic_and_deterministic_adaptation(self):
        # Switch to scenario 1
        switch_active_scenario("1")
        learner_id = "demo-learner-1"

        # Start diagnostic
        start_res = start_assessment(payload={"course_id": "c-python"}, x_learner_id=learner_id)
        self.assertEqual(start_res.course_id, "c-python")
        self.assertGreater(len(start_res.questions), 0)

        # Submit all wrong answers (< 50% rule)
        wrong_answers = [QuestionAnswer(question_id=q.id, answer="WRONG") for q in start_res.questions]
        eval_res = submit_assessment(
            submission=AssessmentSubmitRequest(assessment_id=start_res.assessment_id, answers=wrong_answers),
            x_learner_id=learner_id
        )
        self.assertEqual(eval_res.score, 0)
        self.assertEqual(eval_res.adaptation_direction, "revisit_prerequisites")
        self.assertIn("revisiting prerequisites", eval_res.recommended_next_task["reason"])

        # Check skill gap map calculation
        gap_map = get_skill_profile(x_learner_id=learner_id)
        self.assertGreater(gap_map.total_skills_mapped, 0)
        self.assertIn("formula", gap_map.calculation_breakdown)

    def test_05_roadmap_generation(self):
        learner_id = "demo-learner-1"
        path = get_current_learning_path(x_learner_id=learner_id)
        self.assertIsNotNone(path.path_id)
        self.assertGreater(len(path.tasks), 0)

        # Generate / re-order path based on skills
        gen_path = generate_learning_path(payload={}, x_learner_id=learner_id)
        self.assertGreater(len(gen_path.tasks), 0)

    def test_06_ai_tutor_pedagogy(self):
        learner_id = "demo-learner-1"

        # Test Hint request
        hint_reply = chat_with_tutor(
            req=TutorChatRequest(message="Give me a hint, not the answer", context_task_id="task-demo-1"),
            x_learner_id=learner_id
        )
        self.assertIn("Hint", hint_reply.reply)
        self.assertIsNotNone(hint_reply.check_question)

        # Test Analogy request
        analogy_reply = chat_with_tutor(
            req=TutorChatRequest(message="Explain this concept simply with an analogy"),
            x_learner_id=learner_id
        )
        self.assertTrue(analogy_reply.analogies_used)

        # Test Conversation History
        history = get_tutor_history(x_learner_id=learner_id)
        self.assertGreaterEqual(len(history), 2)

    def test_07_safe_code_evaluator(self):
        learner_id = "demo-learner-7"
        
        # 1. Unmodified starter code must return score 0 and unevaluated/failed tests
        starter_code = "def two_sum(nums, target):\n    # Write your solution here\n    pass"
        starter_res = submit_challenge(
            req=ChallengeSubmitRequest(challenge_id="ch-two-sum", code_or_answer=starter_code, language="python"),
            x_learner_id=learner_id
        )
        self.assertFalse(starter_res.passed)
        self.assertEqual(starter_res.score, 0)
        self.assertTrue(all(not tr.passed for tr in starter_res.test_results))

        # 2. Submitting buggy code (element reuse bug: range(i, len(nums)))
        buggy_code = "def two_sum(nums, target):\n    for i in range(len(nums)):\n        for j in range(i, len(nums)):\n            if nums[i] + nums[j] == target:\n                return [i, j]\n    return []"
        eval_res = submit_challenge(
            req=ChallengeSubmitRequest(challenge_id="ch-two-sum", code_or_answer=buggy_code, language="python"),
            x_learner_id=learner_id
        )
        self.assertFalse(eval_res.passed)
        self.assertIn("Score < 50%", eval_res.adaptation_rule_applied)
        self.assertIsNotNone(eval_res.mistake_analysis)
        self.assertEqual(eval_res.score, 33)

        # 3. Submitting optimal hashmap solution: must pass 100%
        optimal_code = "def two_sum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        diff = target - n\n        if diff in seen:\n            return [seen[diff], i]\n        seen[n] = i\n    return []"
        opt_res = submit_challenge(
            req=ChallengeSubmitRequest(challenge_id="ch-two-sum", code_or_answer=optimal_code, language="python"),
            x_learner_id=learner_id
        )
        self.assertTrue(opt_res.passed)
        self.assertEqual(opt_res.score, 100)
        self.assertTrue(all(tr.passed for tr in opt_res.test_results))

    def test_08_mini_projects_and_rubric_evaluation(self):
        projects = list_mini_projects()
        self.assertGreaterEqual(len(projects), 3)

        # Evaluate project submission
        sub_text = """
from pydantic import BaseModel
class UserModel(BaseModel):
    id: int
    name: str

def safe_handler(data):
    try:
        user = UserModel(**data)
        return {"status": "ok", "user": user.dict()}
    except Exception as e:
        return {"status": "error", "message": "Invalid schema"}
"""
        eval_resp = evaluate_project_submission(
            req=SubmissionEvaluateRequest(project_id="p-py-cli", submission_text=sub_text),
            x_learner_id="demo-learner-8"
        )
        self.assertTrue(eval_resp.passed)
        self.assertGreaterEqual(eval_resp.overall_score, 70)
        self.assertGreater(len(eval_resp.rubric_scores), 0)

    def test_09_smart_notes_extraction_and_study_tools(self):
        learner_id = "demo-learner-10"
        sample_doc = b"Neural Networks: Interconnected computational layers.\nBackpropagation: Gradient calculation via chain rule.\nLearning Rate: Step size hyperparameter."
        doc_result = process_document_and_extract(
            learner_id=learner_id,
            filename="Machine_Learning_Intro.txt",
            file_bytes=sample_doc
        )
        self.assertIn("Machine_Learning_Intro.txt", doc_result["filename"])
        self.assertGreaterEqual(len(doc_result["key_concepts"]), 2)

        # Generate study tools from extracted notes
        tools = generate_study_tools_from_notes(document_id=doc_result["id"], learner_id=learner_id)
        self.assertGreaterEqual(len(tools["flashcards"]), 2)
        self.assertGreaterEqual(len(tools["generated_quizzes"]), 1)

    def test_10_progress_analytics_and_history(self):
        switch_active_scenario("9")
        learner_id = "demo-learner-9"
        summary = get_progress_summary(x_learner_id=learner_id)
        self.assertGreater(summary.overall_mastery, 0)
        self.assertIn("Exponential Moving Average", summary.mastery_formula_explanation)

        history = get_progress_history(x_learner_id=learner_id)
        self.assertIsInstance(history, list)

    def test_11_course_learning_hub_and_smart_notes(self):
        learner_id = "test-learner-hub"
        course_id = "c-python"

        # 1. Fetch course learning hub resources
        resources = get_course_learning_resources(course_id=course_id)
        self.assertEqual(resources.course_id, "c-python")
        self.assertGreaterEqual(len(resources.topics), 3)

        first_topic = resources.topics[0]
        self.assertIsNotNone(first_topic.study_notes.introduction)
        self.assertGreaterEqual(len(first_topic.study_notes.concepts), 2)
        self.assertGreaterEqual(len(first_topic.videos), 1)
        self.assertIn("embed", first_topic.videos[0].embed_url)

        # 2. Create student personal note
        create_payload = StudentNoteCreate(
            title="Reference Semantics Note",
            content="Variables point to memory addresses. Shallow copy doesn't duplicate nested objects.",
            topic_id=first_topic.id,
            topic_title=first_topic.title
        )
        created_note = create_student_note(
            course_id=course_id,
            payload=create_payload,
            x_learner_id=learner_id
        )
        self.assertEqual(created_note.title, "Reference Semantics Note")
        self.assertEqual(created_note.course_id, course_id)
        self.assertEqual(created_note.learner_id, learner_id)

        # 3. List notes for this student and course
        notes_list = list_student_notes(course_id=course_id, x_learner_id=learner_id)
        self.assertTrue(any(n.id == created_note.id for n in notes_list))

        # 4. Note isolation: another student should NOT see this note
        other_notes = list_student_notes(course_id=course_id, x_learner_id="other-student-99")
        self.assertFalse(any(n.id == created_note.id for n in other_notes))

        # 5. Update note
        update_payload = StudentNoteUpdate(
            title="Updated Reference Semantics",
            content="Updated: Immutable objects cannot be altered in-place."
        )
        updated_note = update_student_note(
            course_id=course_id,
            note_id=created_note.id,
            payload=update_payload,
            x_learner_id=learner_id
        )
        self.assertEqual(updated_note.title, "Updated Reference Semantics")

        # 6. Delete note
        del_resp = delete_student_note(
            course_id=course_id,
            note_id=created_note.id,
            x_learner_id=learner_id
        )
        self.assertEqual(del_resp["status"], "success")

        # Verify deletion
        notes_after_del = list_student_notes(course_id=course_id, x_learner_id=learner_id)
        self.assertFalse(any(n.id == created_note.id for n in notes_after_del))

if __name__ == "__main__":
    unittest.main()
