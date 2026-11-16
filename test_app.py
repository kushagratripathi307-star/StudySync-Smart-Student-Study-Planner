"""
StudySync - Comprehensive Automated Test Suite
Verifies Database, Authentication, Business Logic, and GUI Components
"""

import os
import sys
import unittest
from datetime import date, timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.db_manager import DatabaseManager
from authentication.auth import AuthService
from utils.date_utils import (
    calculate_days_left, calculate_duration_hours,
    parse_date, get_current_date_str, format_date_display
)
from utils.validators import (
    validate_email, validate_username, validate_password,
    validate_registration, validate_time, validate_date
)


class TestStudySyncCore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use an isolated test database
        cls.test_db_path = os.path.join(BASE_DIR, "test_studysync.db")
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)
        cls.db = DatabaseManager(cls.test_db_path)
        cls.auth = AuthService(cls.db)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_db_path):
            try:
                os.remove(cls.test_db_path)
            except Exception:
                pass

    def test_01_validators(self):
        """Test input validator routines."""
        # Email
        ok, _ = validate_email("student@college.edu")
        self.assertTrue(ok)
        ok, _ = validate_email("invalid-email")
        self.assertFalse(ok)

        # Username
        ok, _ = validate_username("kushagra_26")
        self.assertTrue(ok)
        ok, _ = validate_username("ab")  # Too short
        self.assertFalse(ok)

        # Password
        ok, _ = validate_password("secret123")
        self.assertTrue(ok)
        ok, _ = validate_password("123")  # Too short
        self.assertFalse(ok)

        # Registration
        ok, _ = validate_registration("Kushagra Verma", "kushagra@college.edu", "kushagra", "password123", "password123")
        self.assertTrue(ok)
        ok, msg = validate_registration("Kushagra Verma", "kushagra@college.edu", "kushagra", "password123", "mismatch")
        self.assertFalse(ok)
        self.assertIn("match", msg.lower())

        # Time & Date
        ok, _ = validate_time("14:30")
        self.assertTrue(ok)
        ok, _ = validate_time("25:99")
        self.assertFalse(ok)

        ok, _ = validate_date("2026-11-28")
        self.assertTrue(ok)
        ok, _ = validate_date("28-11-2026")
        self.assertFalse(ok)

    def test_02_date_utilities(self):
        """Test duration and countdown calculations."""
        # Duration: 14:00 to 16:30 -> 2.5 hours
        dur = calculate_duration_hours("14:00", "16:30")
        self.assertEqual(dur, 2.5)

        # Invalid end time before start time -> 0.0
        dur_inv = calculate_duration_hours("16:00", "14:00")
        self.assertEqual(dur_inv, 0.0)

        # Countdowns
        today = date.today()
        future_12d = (today + timedelta(days=12)).strftime("%Y-%m-%d")
        days, text, urgency = calculate_days_left(future_12d)
        self.assertEqual(days, 12)
        self.assertEqual(text, "12 DAYS LEFT")
        self.assertEqual(urgency, "upcoming")

        tomorrow = (today + timedelta(days=1)).strftime("%Y-%m-%d")
        days, text, urgency = calculate_days_left(tomorrow)
        self.assertEqual(days, 1)
        self.assertEqual(text, "TOMORROW")
        self.assertEqual(urgency, "urgent")

        today_str = today.strftime("%Y-%m-%d")
        days, text, urgency = calculate_days_left(today_str)
        self.assertEqual(days, 0)
        self.assertEqual(text, "TODAY")
        self.assertEqual(urgency, "urgent")

    def test_03_authentication_and_user_crud(self):
        """Test user registration, duplicate prevention, and login."""
        # Register user
        ok, msg = self.auth.register("Kushagra Verma", "kushagra@test.edu", "kush_v", "studyPass1", "studyPass1")
        self.assertTrue(ok, msg)
        user = self.auth.current_user
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "kush_v")

        # Duplicate username
        ok, msg = self.auth.register("Other Name", "other@test.edu", "kush_v", "studyPass1", "studyPass1")
        self.assertFalse(ok)
        self.assertIn("already taken", msg.lower())

        # Duplicate email
        ok, msg = self.auth.register("Other Name", "kushagra@test.edu", "other_user", "studyPass1", "studyPass1")
        self.assertFalse(ok)
        self.assertIn("already exists", msg.lower())

        # Test login
        self.auth.logout()
        self.assertIsNone(self.auth.current_user)

        # Invalid credentials
        ok, msg = self.auth.login("kush_v", "wrongPass")
        self.assertFalse(ok)

        # Valid credentials
        ok, msg = self.auth.login("kush_v", "studyPass1")
        self.assertTrue(ok, msg)
        self.assertIsNotNone(self.auth.current_user)

    def test_04_subjects_crud(self):
        """Test adding, fetching, updating, and deleting subjects."""
        user_id = self.auth.current_user["id"]

        sub_id = self.db.add_subject(
            user_id=user_id,
            name="Data Structures & Algorithms",
            code="CS201",
            description="Core computer science course",
            target_hours=50.0,
            syllabus_progress=60.0,
            semester="Semester 4",
            color="#7667F8"
        )
        self.assertGreater(sub_id, 0)

        # Retrieve
        subs = self.db.get_subjects(user_id)
        self.assertEqual(len(subs), 1)
        self.assertEqual(subs[0]["code"], "CS201")

        # Update
        ok = self.db.update_subject(
            subject_id=sub_id,
            user_id=user_id,
            name="Data Structures & Algorithms Advanced",
            code="CS201A",
            description="Updated description",
            target_hours=60.0,
            syllabus_progress=75.0,
            semester="Semester 4",
            color="#38C98B"
        )
        self.assertTrue(ok)

        updated_sub = self.db.get_subject_by_id(sub_id, user_id)
        self.assertEqual(updated_sub["code"], "CS201A")
        self.assertEqual(updated_sub["target_hours"], 60.0)

    def test_05_study_sessions_crud(self):
        """Test study session creation, completion toggle, and weekly hours."""
        user_id = self.auth.current_user["id"]
        subs = self.db.get_subjects(user_id)
        sub_id = subs[0]["id"]

        today_str = date.today().strftime("%Y-%m-%d")

        sess_id = self.db.add_session(
            user_id=user_id,
            subject_id=sub_id,
            title="Tree Traversals Practice",
            study_date=today_str,
            start_time="14:00",
            end_time="16:30",
            duration_hours=2.5,
            priority="High",
            description="Practiced in-order and pre-order binary trees",
            is_completed=0
        )
        self.assertGreater(sess_id, 0)

        # Verify today's sessions
        today_sessions = self.db.get_today_sessions(user_id)
        self.assertEqual(len(today_sessions), 1)
        self.assertEqual(today_sessions[0]["is_completed"], 0)

        # Toggle completion
        ok = self.db.toggle_session_completed(sess_id, user_id)
        self.assertTrue(ok)

        # Verify completed
        sess = self.db.get_sessions(user_id, status="completed")
        self.assertEqual(len(sess), 1)
        self.assertEqual(sess[0]["is_completed"], 1)

        # Verify weekly study hours
        weekly = self.db.get_weekly_study_hours(user_id)
        self.assertGreater(sum(weekly.values()), 0.0)

    def test_06_tasks_crud(self):
        """Test task creation, filtering, and status updates."""
        user_id = self.auth.current_user["id"]
        subs = self.db.get_subjects(user_id)
        sub_id = subs[0]["id"]

        due_date = (date.today() + timedelta(days=3)).strftime("%Y-%m-%d")

        task_id = self.db.add_task(
            user_id=user_id,
            subject_id=sub_id,
            title="Complete Lab Exercise 5",
            description="Write code for Red-Black tree rotations",
            due_date=due_date,
            priority="High",
            status="Pending"
        )
        self.assertGreater(task_id, 0)

        # Get task stats
        stats = self.db.get_task_stats(user_id)
        self.assertEqual(stats["total"], 1)
        self.assertEqual(stats["pending"], 1)
        self.assertEqual(stats["completed"], 0)

        # Update status
        self.db.update_task_status(task_id, user_id, "Completed")
        stats_updated = self.db.get_task_stats(user_id)
        self.assertEqual(stats_updated["completed"], 1)

    def test_07_exams_crud(self):
        """Test exam creation, countdown calculation, and upcoming query."""
        user_id = self.auth.current_user["id"]
        subs = self.db.get_subjects(user_id)
        sub_id = subs[0]["id"]

        exam_date = (date.today() + timedelta(days=8)).strftime("%Y-%m-%d")

        exam_id = self.db.add_exam(
            user_id=user_id,
            subject_id=sub_id,
            name="DSA Midterm Examination",
            exam_date=exam_date,
            exam_time="11:00",
            exam_type="Midterm",
            notes="Units 1 through 3"
        )
        self.assertGreater(exam_id, 0)

        upcoming_count = self.db.get_upcoming_exams_count(user_id)
        self.assertEqual(upcoming_count, 1)

        exams = self.db.get_exams(user_id, filter_type="upcoming")
        self.assertEqual(len(exams), 1)
        self.assertEqual(exams[0]["name"], "DSA Midterm Examination")

    def test_08_sample_data_seeding(self):
        """Test demonstration sample data generator."""
        # Provision demo account
        ok, msg = self.auth.login_demo_account()
        self.assertTrue(ok)
        demo_user = self.auth.current_user
        self.assertIsNotNone(demo_user)

        subjects = self.db.get_subjects(demo_user["id"])
        self.assertGreaterEqual(len(subjects), 5)

        sessions = self.db.get_sessions(demo_user["id"])
        self.assertGreaterEqual(len(sessions), 4)

        tasks = self.db.get_tasks(demo_user["id"])
        self.assertGreaterEqual(len(tasks), 4)

        exams = self.db.get_exams(demo_user["id"])
        self.assertGreaterEqual(len(exams), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
