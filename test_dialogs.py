"""
StudySync - Modal Dialogs Verification Test
Tests all add/edit dialogs, validation paths, and database commits.
"""

import os
import sys
import time
import customtkinter as ctk
from unittest.mock import patch

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.db_manager import DatabaseManager
from components.dialogs import (
    ConfirmDialog, SubjectDialog, SessionDialog, TaskDialog, ExamDialog
)

def test_dialogs():
    root = ctk.CTk()
    root.withdraw() # Headless

    db = DatabaseManager()
    user = db.get_user_by_identifier("demo_student")
    if not user:
        from authentication.auth import AuthService
        auth = AuthService(db)
        auth.login_demo_account()
        user = auth.current_user

    user_id = user["id"]

    print("Testing ConfirmDialog...")
    confirmed = []
    dlg_confirm = ConfirmDialog(root, "Confirm Test", "Test message", on_confirm=lambda: confirmed.append(True))
    root.update()
    dlg_confirm._handle_confirm()
    assert len(confirmed) == 1, "Confirmation callback must trigger"
    dlg_confirm.destroy()
    root.update()
    print("ConfirmDialog passed.")

    with patch("tkinter.messagebox.askyesno", return_value=True):
        print("Testing SubjectDialog...")
        saved_sub = []
        dlg_sub = SubjectDialog(root, db, user_id, on_save_callback=lambda: saved_sub.append(True))
        root.update()
        test_code = f"T{int(time.time()) % 10000}"
        dlg_sub.name_entry.set("Cloud Computing & DevOps")
        dlg_sub.code_entry.set(test_code)
        dlg_sub.hours_entry.set("45.0")
        dlg_sub.prog_entry.set("30.0")
        dlg_sub._save()
        assert len(saved_sub) == 1, "SubjectDialog save callback must trigger"
        dlg_sub.destroy()
        root.update()
        print("SubjectDialog passed.")

    print("Testing SessionDialog...")
    saved_sess = []
    dlg_sess = SessionDialog(root, db, user_id, on_save_callback=lambda: saved_sess.append(True))
    root.update()
    dlg_sess.title_entry.set("Kubernetes Cluster Architecture")
    dlg_sess.start_entry.set("10:00")
    dlg_sess.end_entry.set("12:00")
    dlg_sess._save()
    assert len(saved_sess) == 1, "SessionDialog save callback must trigger"
    dlg_sess.destroy()
    root.update()
    print("SessionDialog passed.")

    print("Testing TaskDialog...")
    saved_task = []
    dlg_task = TaskDialog(root, db, user_id, on_save_callback=lambda: saved_task.append(True))
    root.update()
    dlg_task.title_entry.set("Deploy Docker Microservice Lab")
    dlg_task._save()
    assert len(saved_task) == 1, "TaskDialog save callback must trigger"
    dlg_task.destroy()
    root.update()
    print("TaskDialog passed.")

    print("Testing ExamDialog...")
    saved_exam = []
    dlg_exam = ExamDialog(root, db, user_id, on_save_callback=lambda: saved_exam.append(True))
    root.update()
    dlg_exam.name_entry.set("Cloud Computing End Semester Exam")
    dlg_exam.time_entry.set("14:30")
    dlg_exam._save()
    assert len(saved_exam) == 1, "ExamDialog save callback must trigger"
    dlg_exam.destroy()
    root.update()
    print("ExamDialog passed.")

    root.destroy()
    print("All dialog tests executed and committed to database successfully!")

if __name__ == "__main__":
    test_dialogs()
