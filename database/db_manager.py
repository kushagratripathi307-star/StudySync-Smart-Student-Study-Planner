"""
StudySync - Smart Student Study Planner
Database Manager - SQLite3 Connection & CRUD Operations
"""

import os
import sqlite3
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
from database.schema import CREATE_TABLES_SQL
from utils.date_utils import calculate_days_left, calculate_duration_hours, get_current_week_dates


class DatabaseManager:
    """Encapsulates all SQLite database operations for StudySync."""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            self.db_path = os.path.join(base_dir, "studysync.db")
        else:
            self.db_path = db_path
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        """Returns a database connection with foreign key support and dict-like row access."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_db(self):
        """Initializes database tables if they do not exist."""
        with self.get_connection() as conn:
            conn.executescript(CREATE_TABLES_SQL)
            conn.commit()

    # =========================================================================
    # USER OPERATIONS
    # =========================================================================

    def create_user(self, username: str, email: str, password_hash: str, salt: str,
                    full_name: str, theme: str = "Dark") -> int:
        query = """
        INSERT INTO users (username, email, password_hash, salt, full_name, theme)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, (username.strip(), email.strip().lower(),
                                         password_hash, salt, full_name.strip(), theme))
            conn.commit()
            return cursor.lastrowid

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM users WHERE id = ?;"
        with self.get_connection() as conn:
            row = conn.execute(query, (user_id,)).fetchone()
            return dict(row) if row else None

    def get_user_by_identifier(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Finds user by username or email (case-insensitive)."""
        clean_id = identifier.strip().lower()
        query = "SELECT * FROM users WHERE LOWER(username) = ? OR LOWER(email) = ?;"
        with self.get_connection() as conn:
            row = conn.execute(query, (clean_id, clean_id)).fetchone()
            return dict(row) if row else None

    def update_user_profile(self, user_id: int, full_name: str, email: str) -> bool:
        query = "UPDATE users SET full_name = ?, email = ? WHERE id = ?;"
        with self.get_connection() as conn:
            cursor = conn.execute(query, (full_name.strip(), email.strip().lower(), user_id))
            conn.commit()
            return cursor.rowcount > 0

    def update_user_password(self, user_id: int, new_hash: str, new_salt: str) -> bool:
        query = "UPDATE users SET password_hash = ?, salt = ? WHERE id = ?;"
        with self.get_connection() as conn:
            cursor = conn.execute(query, (new_hash, new_salt, user_id))
            conn.commit()
            return cursor.rowcount > 0

    def update_user_theme(self, user_id: int, theme: str) -> bool:
        query = "UPDATE users SET theme = ? WHERE id = ?;"
        with self.get_connection() as conn:
            cursor = conn.execute(query, (theme, user_id))
            conn.commit()
            return cursor.rowcount > 0

    # =========================================================================
    # SUBJECT OPERATIONS
    # =========================================================================

    def add_subject(self, user_id: int, name: str, code: str, description: str,
                    target_hours: float, syllabus_progress: float = 0.0,
                    semester: str = "Semester 4", color: str = "#7667F8") -> int:
        query = """
        INSERT INTO subjects (user_id, name, code, description, target_hours, syllabus_progress, semester, color)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, (user_id, name.strip(), code.strip(), description.strip(),
                                         target_hours, syllabus_progress, semester.strip(), color))
            conn.commit()
            return cursor.lastrowid

    def get_subjects(self, user_id: int, search_term: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieves subjects for a user with dynamically calculated logged hours."""
        if search_term and search_term.strip():
            term = f"%{search_term.strip().lower()}%"
            query = """
            SELECT s.*, 
                   COALESCE((SELECT SUM(duration_hours) FROM study_sessions 
                             WHERE subject_id = s.id AND is_completed = 1), 0.0) as logged_hours
            FROM subjects s
            WHERE s.user_id = ? AND (LOWER(s.name) LIKE ? OR LOWER(s.code) LIKE ?)
            ORDER BY s.name ASC;
            """
            params = (user_id, term, term)
        else:
            query = """
            SELECT s.*, 
                   COALESCE((SELECT SUM(duration_hours) FROM study_sessions 
                             WHERE subject_id = s.id AND is_completed = 1), 0.0) as logged_hours
            FROM subjects s
            WHERE s.user_id = ?
            ORDER BY s.name ASC;
            """
            params = (user_id,)

        with self.get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [dict(r) for r in rows]

    def get_subject_by_id(self, subject_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        query = """
        SELECT s.*, 
               COALESCE((SELECT SUM(duration_hours) FROM study_sessions 
                         WHERE subject_id = s.id AND is_completed = 1), 0.0) as logged_hours
        FROM subjects s
        WHERE s.id = ? AND s.user_id = ?;
        """
        with self.get_connection() as conn:
            row = conn.execute(query, (subject_id, user_id)).fetchone()
            return dict(row) if row else None

    def get_subject_by_code(self, user_id: int, code: str) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM subjects WHERE user_id = ? AND LOWER(code) = ?;"
        with self.get_connection() as conn:
            row = conn.execute(query, (user_id, code.strip().lower())).fetchone()
            return dict(row) if row else None

    def update_subject(self, subject_id: int, user_id: int, name: str, code: str,
                       description: str, target_hours: float, syllabus_progress: float,
                       semester: str, color: str) -> bool:
        query = """
        UPDATE subjects 
        SET name = ?, code = ?, description = ?, target_hours = ?, 
            syllabus_progress = ?, semester = ?, color = ?
        WHERE id = ? AND user_id = ?;
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, (name.strip(), code.strip(), description.strip(),
                                         target_hours, syllabus_progress, semester.strip(),
                                         color, subject_id, user_id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_subject(self, subject_id: int, user_id: int) -> bool:
        query = "DELETE FROM subjects WHERE id = ? AND user_id = ?;"
        with self.get_connection() as conn:
            cursor = conn.execute(query, (subject_id, user_id))
            conn.commit()
            return cursor.rowcount > 0

    # =========================================================================
    # STUDY SESSION OPERATIONS (PLANNER & PRODUCTIVITY)
    # =========================================================================

    def add_session(self, user_id: int, subject_id: Optional[int], title: str,
                    study_date: str, start_time: str, end_time: str,
                    duration_hours: float, priority: str = "Medium",
                    description: str = "", is_completed: int = 0) -> int:
        query = """
        INSERT INTO study_sessions (user_id, subject_id, title, study_date, start_time, end_time,
                                   duration_hours, priority, description, is_completed)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, (user_id, subject_id, title.strip(), study_date,
                                         start_time, end_time, duration_hours,
                                         priority, description.strip(), is_completed))
            conn.commit()
            return cursor.lastrowid

    def get_sessions(self, user_id: int, date_filter: Optional[str] = None,
                     subject_id: Optional[int] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        conditions = ["ss.user_id = ?"]
        params: List[Any] = [user_id]

        if date_filter:
            today_str = date.today().strftime("%Y-%m-%d")
            if date_filter == "today":
                conditions.append("ss.study_date = ?")
                params.append(today_str)
            elif date_filter == "this_week":
                week_dates = get_current_week_dates()
                start_w = week_dates[0].strftime("%Y-%m-%d")
                end_w = week_dates[-1].strftime("%Y-%m-%d")
                conditions.append("ss.study_date >= ? AND ss.study_date <= ?")
                params.extend([start_w, end_w])
            elif date_filter == "upcoming":
                conditions.append("ss.study_date >= ?")
                params.append(today_str)
            elif date_filter == "past":
                conditions.append("ss.study_date < ?")
                params.append(today_str)

        if subject_id:
            conditions.append("ss.subject_id = ?")
            params.append(subject_id)

        if status:
            if status.lower() == "completed":
                conditions.append("ss.is_completed = 1")
            elif status.lower() == "pending":
                conditions.append("ss.is_completed = 0")

        query = f"""
        SELECT ss.*, s.name as subject_name, s.code as subject_code, s.color as subject_color
        FROM study_sessions ss
        LEFT JOIN subjects s ON ss.subject_id = s.id
        WHERE {" AND ".join(conditions)}
        ORDER BY ss.study_date DESC, ss.start_time ASC;
        """
        with self.get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [dict(r) for r in rows]

    def get_today_sessions(self, user_id: int) -> List[Dict[str, Any]]:
        today_str = date.today().strftime("%Y-%m-%d")
        return self.get_sessions(user_id, date_filter="today")

    def update_session(self, session_id: int, user_id: int, subject_id: Optional[int],
                       title: str, study_date: str, start_time: str, end_time: str,
                       duration_hours: float, priority: str, description: str,
                       is_completed: int) -> bool:
        query = """
        UPDATE study_sessions
        SET subject_id = ?, title = ?, study_date = ?, start_time = ?, end_time = ?,
            duration_hours = ?, priority = ?, description = ?, is_completed = ?
        WHERE id = ? AND user_id = ?;
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, (subject_id, title.strip(), study_date, start_time,
                                         end_time, duration_hours, priority, description.strip(),
                                         is_completed, session_id, user_id))
            conn.commit()
            return cursor.rowcount > 0

    def toggle_session_completed(self, session_id: int, user_id: int) -> bool:
        query = """
        UPDATE study_sessions
        SET is_completed = CASE WHEN is_completed = 1 THEN 0 ELSE 1 END
        WHERE id = ? AND user_id = ?;
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, (session_id, user_id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_session(self, session_id: int, user_id: int) -> bool:
        query = "DELETE FROM study_sessions WHERE id = ? AND user_id = ?;"
        with self.get_connection() as conn:
            cursor = conn.execute(query, (session_id, user_id))
            conn.commit()
            return cursor.rowcount > 0

    def get_weekly_study_hours(self, user_id: int) -> Dict[str, float]:
        """Returns Monday-Sunday study hours for the current week."""
        week_dates = get_current_week_dates()
        days_map = {d.strftime("%Y-%m-%d"): d.strftime("%a") for d in week_dates}
        # Initialize with 0.0 for all 7 days
        result = {d.strftime("%a"): 0.0 for d in week_dates}

        start_date = week_dates[0].strftime("%Y-%m-%d")
        end_date = week_dates[-1].strftime("%Y-%m-%d")

        query = """
        SELECT study_date, SUM(duration_hours) as daily_total
        FROM study_sessions
        WHERE user_id = ? AND is_completed = 1 AND study_date >= ? AND study_date <= ?
        GROUP BY study_date;
        """
        with self.get_connection() as conn:
            rows = conn.execute(query, (user_id, start_date, end_date)).fetchall()
            for r in rows:
                d_str = r["study_date"]
                if d_str in days_map:
                    day_name = days_map[d_str]
                    result[day_name] = round(r["daily_total"], 2)

        return result

    def get_total_hours_this_week(self, user_id: int) -> float:
        weekly = self.get_weekly_study_hours(user_id)
        return round(sum(weekly.values()), 1)

    def get_total_study_hours_all_time(self, user_id: int) -> float:
        query = """
        SELECT COALESCE(SUM(duration_hours), 0.0) as total
        FROM study_sessions
        WHERE user_id = ? AND is_completed = 1;
        """
        with self.get_connection() as conn:
            row = conn.execute(query, (user_id,)).fetchone()
            return round(row["total"], 1) if row else 0.0

    def get_subject_distribution(self, user_id: int) -> List[Dict[str, Any]]:
        """Returns subject distribution for analytics pie/donut chart."""
        query = """
        SELECT s.name as subject_name, s.color as subject_color, 
               COALESCE(SUM(ss.duration_hours), 0.0) as total_hours
        FROM subjects s
        LEFT JOIN study_sessions ss ON s.id = ss.subject_id AND ss.is_completed = 1
        WHERE s.user_id = ?
        GROUP BY s.id, s.name, s.color
        HAVING total_hours > 0
        ORDER BY total_hours DESC;
        """
        with self.get_connection() as conn:
            rows = conn.execute(query, (user_id,)).fetchall()
            return [dict(r) for r in rows]

    def get_monthly_study_trend(self, user_id: int) -> List[Dict[str, Any]]:
        """Returns study hours aggregated across the last 4 weeks."""
        today = date.today()
        trend = []
        for i in range(3, -1, -1):
            w_start = today - timedelta(days=(i * 7) + 6)
            w_end = today - timedelta(days=i * 7)
            query = """
            SELECT COALESCE(SUM(duration_hours), 0.0) as total
            FROM study_sessions
            WHERE user_id = ? AND is_completed = 1 AND study_date >= ? AND study_date <= ?;
            """
            with self.get_connection() as conn:
                row = conn.execute(query, (user_id, w_start.strftime("%Y-%m-%d"),
                                            w_end.strftime("%Y-%m-%d"))).fetchone()
                total = round(row["total"], 1) if row else 0.0
                label = f"Wk {4 - i}" if i > 0 else "This Wk"
                trend.append({"week": label, "hours": total})
        return trend

    # =========================================================================
    # TASK OPERATIONS
    # =========================================================================

    def add_task(self, user_id: int, subject_id: Optional[int], title: str,
                 description: str, due_date: str, priority: str = "Medium",
                 status: str = "Pending") -> int:
        query = """
        INSERT INTO tasks (user_id, subject_id, title, description, due_date, priority, status)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, (user_id, subject_id, title.strip(),
                                         description.strip(), due_date, priority, status))
            conn.commit()
            return cursor.lastrowid

    def get_tasks(self, user_id: int, status_filter: Optional[str] = None,
                  subject_id: Optional[int] = None, priority_filter: Optional[str] = None,
                  search: Optional[str] = None, sort_by: str = "due_date") -> List[Dict[str, Any]]:
        conditions = ["t.user_id = ?"]
        params: List[Any] = [user_id]
        today_str = date.today().strftime("%Y-%m-%d")

        if status_filter:
            if status_filter.lower() == "overdue":
                conditions.append("t.status != 'Completed' AND t.due_date < ?")
                params.append(today_str)
            else:
                conditions.append("t.status = ?")
                params.append(status_filter)

        if subject_id:
            conditions.append("t.subject_id = ?")
            params.append(subject_id)

        if priority_filter and priority_filter.lower() != "all":
            conditions.append("t.priority = ?")
            params.append(priority_filter)

        if search and search.strip():
            term = f"%{search.strip().lower()}%"
            conditions.append("(LOWER(t.title) LIKE ? OR LOWER(t.description) LIKE ?)")
            params.extend([term, term])

        # Sorting
        order_clause = "t.due_date ASC"
        if sort_by == "priority":
            order_clause = """
            CASE t.priority 
                WHEN 'High' THEN 1 
                WHEN 'Medium' THEN 2 
                WHEN 'Low' THEN 3 
                ELSE 4 
            END ASC, t.due_date ASC
            """
        elif sort_by == "created":
            order_clause = "t.created_at DESC"

        query = f"""
        SELECT t.*, s.name as subject_name, s.code as subject_code, s.color as subject_color
        FROM tasks t
        LEFT JOIN subjects s ON t.subject_id = s.id
        WHERE {" AND ".join(conditions)}
        ORDER BY {order_clause};
        """
        with self.get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [dict(r) for r in rows]

    def get_task_by_id(self, task_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM tasks WHERE id = ? AND user_id = ?;"
        with self.get_connection() as conn:
            row = conn.execute(query, (task_id, user_id)).fetchone()
            return dict(row) if row else None

    def update_task(self, task_id: int, user_id: int, subject_id: Optional[int],
                    title: str, description: str, due_date: str, priority: str,
                    status: str) -> bool:
        query = """
        UPDATE tasks
        SET subject_id = ?, title = ?, description = ?, due_date = ?,
            priority = ?, status = ?
        WHERE id = ? AND user_id = ?;
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, (subject_id, title.strip(), description.strip(),
                                         due_date, priority, status, task_id, user_id))
            conn.commit()
            return cursor.rowcount > 0

    def update_task_status(self, task_id: int, user_id: int, status: str) -> bool:
        query = "UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?;"
        with self.get_connection() as conn:
            cursor = conn.execute(query, (status, task_id, user_id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_task(self, task_id: int, user_id: int) -> bool:
        query = "DELETE FROM tasks WHERE id = ? AND user_id = ?;"
        with self.get_connection() as conn:
            cursor = conn.execute(query, (task_id, user_id))
            conn.commit()
            return cursor.rowcount > 0

    def get_task_stats(self, user_id: int) -> Dict[str, int]:
        today_str = date.today().strftime("%Y-%m-%d")
        query = """
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed,
            SUM(CASE WHEN status = 'Pending' AND due_date >= ? THEN 1 ELSE 0 END) as pending,
            SUM(CASE WHEN status = 'In Progress' AND due_date >= ? THEN 1 ELSE 0 END) as in_progress,
            SUM(CASE WHEN status != 'Completed' AND due_date < ? THEN 1 ELSE 0 END) as overdue
        FROM tasks
        WHERE user_id = ?;
        """
        with self.get_connection() as conn:
            row = conn.execute(query, (today_str, today_str, today_str, user_id)).fetchone()
            if not row:
                return {"total": 0, "completed": 0, "pending": 0, "in_progress": 0, "overdue": 0}
            return {
                "total": row["total"] or 0,
                "completed": row["completed"] or 0,
                "pending": row["pending"] or 0,
                "in_progress": row["in_progress"] or 0,
                "overdue": row["overdue"] or 0
            }

    def get_upcoming_deadlines(self, user_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Returns non-completed tasks sorted by due date for dashboard widget."""
        query = """
        SELECT t.*, s.name as subject_name, s.code as subject_code, s.color as subject_color
        FROM tasks t
        LEFT JOIN subjects s ON t.subject_id = s.id
        WHERE t.user_id = ? AND t.status != 'Completed'
        ORDER BY t.due_date ASC
        LIMIT ?;
        """
        with self.get_connection() as conn:
            rows = conn.execute(query, (user_id, limit)).fetchall()
            return [dict(r) for r in rows]

    # =========================================================================
    # EXAM OPERATIONS
    # =========================================================================

    def add_exam(self, user_id: int, subject_id: Optional[int], name: str,
                 exam_date: str, exam_time: str = "10:00",
                 exam_type: str = "Internal Exam", notes: str = "") -> int:
        query = """
        INSERT INTO exams (user_id, subject_id, name, exam_date, exam_time, exam_type, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, (user_id, subject_id, name.strip(),
                                         exam_date, exam_time, exam_type, notes.strip()))
            conn.commit()
            return cursor.lastrowid

    def get_exams(self, user_id: int, filter_type: Optional[str] = None) -> List[Dict[str, Any]]:
        today_str = date.today().strftime("%Y-%m-%d")
        conditions = ["e.user_id = ?"]
        params: List[Any] = [user_id]

        if filter_type == "upcoming":
            conditions.append("e.exam_date >= ?")
            params.append(today_str)
        elif filter_type == "past":
            conditions.append("e.exam_date < ?")
            params.append(today_str)

        query = f"""
        SELECT e.*, s.name as subject_name, s.code as subject_code, s.color as subject_color
        FROM exams e
        LEFT JOIN subjects s ON e.subject_id = s.id
        WHERE {" AND ".join(conditions)}
        ORDER BY e.exam_date ASC, e.exam_time ASC;
        """
        with self.get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [dict(r) for r in rows]

    def get_exam_by_id(self, exam_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM exams WHERE id = ? AND user_id = ?;"
        with self.get_connection() as conn:
            row = conn.execute(query, (exam_id, user_id)).fetchone()
            return dict(row) if row else None

    def update_exam(self, exam_id: int, user_id: int, subject_id: Optional[int],
                    name: str, exam_date: str, exam_time: str, exam_type: str,
                    notes: str) -> bool:
        query = """
        UPDATE exams
        SET subject_id = ?, name = ?, exam_date = ?, exam_time = ?,
            exam_type = ?, notes = ?
        WHERE id = ? AND user_id = ?;
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, (subject_id, name.strip(), exam_date,
                                         exam_time, exam_type, notes.strip(),
                                         exam_id, user_id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_exam(self, exam_id: int, user_id: int) -> bool:
        query = "DELETE FROM exams WHERE id = ? AND user_id = ?;"
        with self.get_connection() as conn:
            cursor = conn.execute(query, (exam_id, user_id))
            conn.commit()
            return cursor.rowcount > 0

    def get_upcoming_exams_count(self, user_id: int) -> int:
        today_str = date.today().strftime("%Y-%m-%d")
        query = "SELECT COUNT(*) as count FROM exams WHERE user_id = ? AND exam_date >= ?;"
        with self.get_connection() as conn:
            row = conn.execute(query, (user_id, today_str)).fetchone()
            return row["count"] if row else 0

    # =========================================================================
    # SAMPLE DATA GENERATOR & RESET
    # =========================================================================

    def has_sample_data(self, user_id: int) -> bool:
        """Checks if sample subjects already exist for this user."""
        query = "SELECT COUNT(*) as count FROM subjects WHERE user_id = ? AND code IN ('CS201', 'CS202', 'CS203', 'CS204', 'CS205');"
        with self.get_connection() as conn:
            row = conn.execute(query, (user_id,)).fetchone()
            return (row["count"] or 0) > 0

    def seed_sample_data(self, user_id: int):
        """Populates rich, realistic sample records for a 2nd year B.Tech student."""
        # 1. Subjects
        subjects_data = [
            ("Data Structures & Algorithms", "CS201", "Core algorithmic design, sorting, trees, and graphs", 45.0, 75.0, "Semester 4", "#7667F8"),
            ("Operating Systems", "CS202", "Concurrency, process scheduling, memory virtualization and file systems", 40.0, 60.0, "Semester 4", "#38C98B"),
            ("Database Management Systems", "CS203", "Relational algebra, SQL, normalization, and ACID properties", 35.0, 80.0, "Semester 4", "#3B82F6"),
            ("Object-Oriented Programming", "CS204", "Classes, inheritance, polymorphism, design patterns in Java", 30.0, 90.0, "Semester 4", "#F5B84B"),
            ("Computer Organization", "CS205", "Instruction set architectures, ALU design, pipelining and caches", 35.0, 50.0, "Semester 4", "#EC4899"),
        ]

        sub_ids = {}
        for name, code, desc, tgt, syl, sem, color in subjects_data:
            sid = self.add_subject(user_id, name, code, desc, tgt, syl, sem, color)
            sub_ids[code] = sid

        today = date.today()
        today_str = today.strftime("%Y-%m-%d")

        # 2. Study Sessions
        # Past few days sessions for weekly graph & analytics
        sessions_to_add = [
            (sub_ids["CS201"], "Binary Search Tree Traversals", (today - timedelta(days=2)).strftime("%Y-%m-%d"), "10:00", "12:30", 2.5, "High", "Implemented recursive and iterative inorder traversals", 1),
            (sub_ids["CS202"], "Round Robin Process Scheduling", (today - timedelta(days=1)).strftime("%Y-%m-%d"), "14:00", "16:00", 2.0, "High", "Calculated turnaround and waiting times", 1),
            (sub_ids["CS203"], "BCNF & Normalization Forms", (today - timedelta(days=1)).strftime("%Y-%m-%d"), "17:00", "18:30", 1.5, "Medium", "Practiced 3NF to BCNF decomposition questions", 1),
            (sub_ids["CS201"], "Dynamic Programming: Knapsack", today_str, "09:30", "11:30", 2.0, "High", "Solved 0/1 knapsack subproblems", 1),
            (sub_ids["CS204"], "Design Patterns: Factory & Observer", today_str, "15:00", "16:45", 1.75, "Medium", "Reviewed SOLID principles and code examples", 0),
            (sub_ids["CS205"], "Pipeline Hazard Resolutions", (today + timedelta(days=1)).strftime("%Y-%m-%d"), "11:00", "13:00", 2.0, "Medium", "Structural and data forward branch hazards", 0),
        ]

        for sid, title, s_date, start, end, dur, prio, desc, comp in sessions_to_add:
            self.add_session(user_id, sid, title, s_date, start, end, dur, prio, desc, comp)

        # 3. Tasks & Assignments
        tasks_to_add = [
            (sub_ids["CS202"], "Complete Process Synchronization Lab Report", "Write up Dining Philosophers with semaphores", (today + timedelta(days=2)).strftime("%Y-%m-%d"), "High", "In Progress"),
            (sub_ids["CS203"], "Submit DBMS Mini Project ER Schema", "Normalize database tables to 3NF and build DDL scripts", (today + timedelta(days=4)).strftime("%Y-%m-%d"), "High", "Pending"),
            (sub_ids["CS201"], "Graph Algorithm Problem Set 4", "Solve Dijkstra and Kruskal MST problems on HackerRank", (today + timedelta(days=6)).strftime("%Y-%m-%d"), "Medium", "Pending"),
            (sub_ids["CS204"], "Java Multi-threaded Client-Server App", "Build socket connection with thread pool executor", (today + timedelta(days=9)).strftime("%Y-%m-%d"), "Medium", "Pending"),
            (sub_ids["CS205"], "Cache Memory Simulation Assignment", "Analyze hit/miss rates in direct and associative caches", (today - timedelta(days=1)).strftime("%Y-%m-%d"), "High", "Completed"),
        ]

        for sid, title, desc, due, prio, status in tasks_to_add:
            self.add_task(user_id, sid, title, desc, due, prio, status)

        # 4. Upcoming Exams
        exams_to_add = [
            (sub_ids["CS202"], "Operating Systems Midterm Exam", (today + timedelta(days=5)).strftime("%Y-%m-%d"), "10:30", "Midterm", "Covers Unit 1 & 2: Process Management, Threads, Deadlocks"),
            (sub_ids["CS201"], "DSA Practical Lab Evaluation", (today + timedelta(days=11)).strftime("%Y-%m-%d"), "14:00", "Practical", "Coding test on Trees, Heaps and Graph algorithms"),
            (sub_ids["CS203"], "DBMS Assessment & SQL Test", (today + timedelta(days=18)).strftime("%Y-%m-%d"), "09:30", "Internal Exam", "SQL queries, relational algebra, and recovery techniques"),
            (sub_ids["CS204"], "OOP Final Semester Exam", (today + timedelta(days=32)).strftime("%Y-%m-%d"), "10:00", "End Semester", "Comprehensive theory and OOP design paper"),
        ]

        for sid, name, e_date, e_time, e_type, notes in exams_to_add:
            self.add_exam(user_id, sid, name, e_date, e_time, e_type, notes)

    def clear_user_data(self, user_id: int):
        """Clears all records for the user, retaining the user account."""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM exams WHERE user_id = ?;", (user_id,))
            conn.execute("DELETE FROM tasks WHERE user_id = ?;", (user_id,))
            conn.execute("DELETE FROM study_sessions WHERE user_id = ?;", (user_id,))
            conn.execute("DELETE FROM subjects WHERE user_id = ?;", (user_id,))
            conn.commit()
