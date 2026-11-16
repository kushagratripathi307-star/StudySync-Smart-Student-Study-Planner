"""
StudySync - Smart Student Study Planner
Modal Dialogs for Adding/Editing Records and Confirmation Prompts
Engineered with fixed bottom action bars so Save and Cancel buttons are never clipped.
"""

from typing import Any, Optional, Callable, Dict, List
import customtkinter as ctk
from tkinter import messagebox
from datetime import date
from utils.theme import (
    COLOR_BG, COLOR_CARD, COLOR_CARD_SECONDARY, COLOR_BORDER,
    COLOR_PRIMARY, COLOR_PRIMARY_HOVER, COLOR_SECONDARY,
    COLOR_DANGER, COLOR_DANGER_HOVER, COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED, FONT_HEADING_MD,
    FONT_SUBHEADING, FONT_BODY, FONT_BODY_BOLD, FONT_BODY_SM,
    FONT_CAPTION, CARD_RADIUS, BUTTON_RADIUS, SUBJECT_PALETTE
)
from components.buttons import PrimaryButton, SecondaryButton, DangerButton
from components.forms import FormEntry, FormDropdown, FormDateEntry, FormTextBox
from utils.date_utils import calculate_duration_hours, parse_date
from utils.validators import validate_time, validate_date, validate_number


def center_window(window: ctk.CTkToplevel, width: int, height: int, parent: Any = None):
    """
    Centers a modal window safely within the visible display bounds.
    Guarantees the dialog is never placed partially off-screen on 1366x768 or 1440x900.
    """
    window.update_idletasks()
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()

    # Clamp dimensions to available desktop space
    target_w = min(width, screen_w - 40)
    target_h = min(height, screen_h - 80)

    if parent and parent.winfo_viewable():
        parent.update_idletasks()
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        x = px + (pw - target_w) // 2
        y = py + (ph - target_h) // 2
    else:
        x = (screen_w - target_w) // 2
        y = (screen_h - target_h) // 2

    # Safety bounds to prevent window headers or footers from going off-screen
    x = max(15, min(x, screen_w - target_w - 20))
    y = max(20, min(y, screen_h - target_h - 50))
    window.geometry(f"{target_w}x{target_h}+{x}+{y}")


class ConfirmDialog(ctk.CTkToplevel):
    """Clean confirmation dialog for destructive or important actions."""
    def __init__(self, parent: Any, title: str, message: str,
                 confirm_text: str = "Confirm", is_danger: bool = False,
                 on_confirm: Optional[Callable] = None):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.on_confirm = on_confirm
        self.result = False

        self.configure(fg_color=COLOR_BG)
        center_window(self, 440, 220, parent)

        card = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=CARD_RADIUS,
                            border_width=1, border_color=COLOR_BORDER)
        card.pack(fill="both", expand=True, padx=14, pady=14)

        # Header
        lbl_title = ctk.CTkLabel(card, text=title, font=FONT_HEADING_MD,
                                 text_color=COLOR_TEXT_PRIMARY, anchor="w")
        lbl_title.pack(fill="x", padx=20, pady=(16, 6))

        # Message body
        lbl_msg = ctk.CTkLabel(card, text=message, font=FONT_BODY,
                               text_color=COLOR_TEXT_SECONDARY, wraplength=380,
                               justify="left", anchor="w")
        lbl_msg.pack(fill="x", padx=20, pady=(0, 16))

        # Bottom Action Bar
        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(side="bottom", fill="x", padx=20, pady=(0, 16))

        cancel_btn = SecondaryButton(btn_row, text="Cancel", width=100, height=38,
                                     command=self.destroy)
        cancel_btn.pack(side="right", padx=(10, 0))

        if is_danger:
            confirm_btn = DangerButton(btn_row, text=confirm_text, width=130, height=38,
                                       command=self._handle_confirm)
        else:
            confirm_btn = PrimaryButton(btn_row, text=confirm_text, width=130, height=38,
                                        command=self._handle_confirm)
        confirm_btn.pack(side="right")

    def _handle_confirm(self):
        self.result = True
        if self.on_confirm:
            self.on_confirm()
        self.destroy()


class SubjectDialog(ctk.CTkToplevel):
    """
    Add / Edit Subject Modal Dialog.
    Features:
    - Fixed Top Header
    - Scrollable Form Content (prevents any field crowding)
    - Fixed Bottom Action Bar with prominent Save and Cancel buttons
    """
    def __init__(self, parent: Any, db: Any, user_id: int,
                 subject: Optional[Dict] = None, on_save_callback: Optional[Callable] = None):
        super().__init__(parent)
        self.db = db
        self.user_id = user_id
        self.subject = subject
        self.on_save = on_save_callback

        title_text = "Edit Subject" if subject else "Add New Subject"
        self.title(title_text)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.configure(fg_color=COLOR_BG)

        center_window(self, 520, 580, parent)

        # Outer Card Frame
        card = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=CARD_RADIUS,
                            border_width=1, border_color=COLOR_BORDER)
        card.pack(fill="both", expand=True, padx=14, pady=14)

        # 1. FIXED TOP HEADER
        top_header = ctk.CTkFrame(card, fg_color="transparent")
        top_header.pack(side="top", fill="x", padx=22, pady=(16, 8))

        ctk.CTkLabel(top_header, text=title_text, font=FONT_HEADING_MD,
                     text_color=COLOR_TEXT_PRIMARY, anchor="w").pack(side="left")

        # 2. FIXED BOTTOM ACTION BAR (Packed first with side="bottom" so it's NEVER clipped)
        ctk.CTkFrame(card, height=1, fg_color=COLOR_BORDER).pack(side="bottom", fill="x", padx=16, pady=(0, 0))

        btn_bar = ctk.CTkFrame(card, fg_color="transparent")
        btn_bar.pack(side="bottom", fill="x", padx=22, pady=14)

        SecondaryButton(btn_bar, text="Cancel", width=110, height=38,
                        command=self.destroy).pack(side="right", padx=(10, 0))

        action_label = "Update Subject" if subject else "Save Subject"
        self.save_btn = PrimaryButton(btn_bar, text=action_label, width=140, height=38,
                                      command=self._save)
        self.save_btn.pack(side="right")

        # 3. SCROLLABLE FORM BODY (Fills the space between Header and Action Bar)
        form_scroll = ctk.CTkScrollableFrame(card, fg_color="transparent")
        form_scroll.pack(side="top", fill="both", expand=True, padx=16, pady=(0, 6))

        # Subject Name
        self.name_entry = FormEntry(form_scroll, label="Subject Name", placeholder="e.g. Data Structures & Algorithms",
                                    initial_value=subject.get("name", "") if subject else "")
        self.name_entry.pack(fill="x", pady=4)

        # Subject Code
        code_val = subject.get("code", "") if subject else ""
        self.code_entry = FormEntry(form_scroll, label="Subject Code", placeholder="e.g. CS201",
                                    initial_value=code_val)
        self.code_entry.pack(fill="x", pady=4)

        # Row with Target Hours & Syllabus Percentage side-by-side
        row_stats = ctk.CTkFrame(form_scroll, fg_color="transparent")
        row_stats.pack(fill="x", pady=4)
        row_stats.columnconfigure((0, 1), weight=1)

        hours_val = str(subject.get("target_hours", 40.0)) if subject else "40.0"
        self.hours_entry = FormEntry(row_stats, label="Target Study Hours", placeholder="40.0",
                                     initial_value=hours_val, width=180)
        self.hours_entry.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        prog_val = str(subject.get("syllabus_progress", 0.0)) if subject else "0.0"
        self.prog_entry = FormEntry(row_stats, label="Completed Syllabus (%)", placeholder="0 to 100",
                                    initial_value=prog_val, width=180)
        self.prog_entry.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        # Semester Dropdown
        sem_val = subject.get("semester", "Semester 4") if subject else "Semester 4"
        self.sem_dropdown = FormDropdown(form_scroll, label="Academic Semester",
                                         values=["Semester 1", "Semester 2", "Semester 3", "Semester 4",
                                                 "Semester 5", "Semester 6", "Semester 7", "Semester 8"],
                                         default_value=sem_val)
        self.sem_dropdown.pack(fill="x", pady=4)

        # Color Selector for subject badge
        cur_color = subject.get("color", "#7667F8") if subject else "#7667F8"
        self.color_map = {
            "Purple (#7667F8)": "#7667F8",
            "Emerald Green (#38C98B)": "#38C98B",
            "Ocean Blue (#3B82F6)": "#3B82F6",
            "Amber Gold (#F5B84B)": "#F5B84B",
            "Rose Pink (#EC4899)": "#EC4899",
            "Cyan Sky (#06B6D4)": "#06B6D4",
        }
        color_names = list(self.color_map.keys())
        default_color_name = color_names[0]
        for name_label, hex_code in self.color_map.items():
            if hex_code == cur_color:
                default_color_name = name_label
                break

        self.color_dropdown = FormDropdown(form_scroll, label="Course Accent Color",
                                           values=color_names, default_value=default_color_name)
        self.color_dropdown.pack(fill="x", pady=4)

        # Description / Topics
        self.desc_entry = FormTextBox(form_scroll, label="Description / Key Syllabus Topics",
                                      initial_text=subject.get("description", "") if subject else "",
                                      height=75)
        self.desc_entry.pack(fill="x", pady=4)

    def _save(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Validation Error", "Subject Name is required.", parent=self)
            return

        code = self.code_entry.get().strip() or name[:4].upper()

        # Check duplicate code if adding new subject
        if not self.subject:
            existing = self.db.get_subject_by_code(self.user_id, code) if hasattr(self.db, "get_subject_by_code") else None
            if existing:
                msg = f"A subject with code '{code}' already exists ({existing['name']}). Do you want to use this code anyway?"
                if not messagebox.askyesno("Duplicate Subject Code", msg, parent=self):
                    return
        
        ok_h, msg_h, tgt_hours = validate_number(self.hours_entry.get(), min_val=0.5, max_val=1000, field_name="Target Hours")
        if not ok_h:
            messagebox.showerror("Validation Error", msg_h, parent=self)
            return

        ok_p, msg_p, syl_prog = validate_number(self.prog_entry.get(), min_val=0, max_val=100, field_name="Syllabus %")
        if not ok_p:
            messagebox.showerror("Validation Error", msg_p, parent=self)
            return

        semester = self.sem_dropdown.get()
        description = self.desc_entry.get()
        color = self.color_map.get(self.color_dropdown.get(), "#7667F8")

        try:
            if self.subject:
                self.db.update_subject(
                    subject_id=self.subject["id"],
                    user_id=self.user_id,
                    name=name,
                    code=code,
                    description=description,
                    target_hours=tgt_hours,
                    syllabus_progress=syl_prog,
                    semester=semester,
                    color=color
                )
            else:
                self.db.add_subject(
                    user_id=self.user_id,
                    name=name,
                    code=code,
                    description=description,
                    target_hours=tgt_hours,
                    syllabus_progress=syl_prog,
                    semester=semester,
                    color=color
                )
            if self.on_save:
                self.on_save()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save subject: {e}", parent=self)


class SessionDialog(ctk.CTkToplevel):
    """
    Add / Edit Study Session Modal Dialog.
    Features:
    - Fixed Top Header
    - Dynamic duration calculation preview
    - Fixed Bottom Action Bar with clearly visible Save Session and Cancel buttons
    """
    def __init__(self, parent: Any, db: Any, user_id: int,
                 session: Optional[Dict] = None, on_save_callback: Optional[Callable] = None):
        super().__init__(parent)
        self.db = db
        self.user_id = user_id
        self.session = session
        self.on_save = on_save_callback

        title_text = "Edit Study Session" if session else "Plan New Study Session"
        self.title(title_text)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.configure(fg_color=COLOR_BG)

        center_window(self, 520, 600, parent)

        card = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=CARD_RADIUS,
                            border_width=1, border_color=COLOR_BORDER)
        card.pack(fill="both", expand=True, padx=14, pady=14)

        # 1. FIXED TOP HEADER
        top_header = ctk.CTkFrame(card, fg_color="transparent")
        top_header.pack(side="top", fill="x", padx=22, pady=(16, 8))

        ctk.CTkLabel(top_header, text=title_text, font=FONT_HEADING_MD,
                     text_color=COLOR_TEXT_PRIMARY, anchor="w").pack(side="left")

        # 2. FIXED BOTTOM ACTION BAR
        ctk.CTkFrame(card, height=1, fg_color=COLOR_BORDER).pack(side="bottom", fill="x", padx=16, pady=(0, 0))

        btn_bar = ctk.CTkFrame(card, fg_color="transparent")
        btn_bar.pack(side="bottom", fill="x", padx=22, pady=14)

        SecondaryButton(btn_bar, text="Cancel", width=110, height=38,
                        command=self.destroy).pack(side="right", padx=(10, 0))

        action_label = "Update Session" if session else "Save Session"
        self.save_btn = PrimaryButton(btn_bar, text=action_label, width=140, height=38,
                                      command=self._save)
        self.save_btn.pack(side="right")

        # 3. SCROLLABLE FORM BODY
        form_scroll = ctk.CTkScrollableFrame(card, fg_color="transparent")
        form_scroll.pack(side="top", fill="both", expand=True, padx=16, pady=(0, 6))

        # Session Title
        self.title_entry = FormEntry(form_scroll, label="Session Title / Goal",
                                     placeholder="e.g. Revise Binary Search Trees",
                                     initial_value=session.get("title", "") if session else "")
        self.title_entry.pack(fill="x", pady=4)

        # Subject Selection
        subjects = self.db.get_subjects(user_id)
        self.subject_map = {f"{s['code']} - {s['name']}": s['id'] for s in subjects}
        sub_names = list(self.subject_map.keys())
        if not sub_names:
            sub_names = ["General (No Subject)"]

        default_sub = None
        if session and session.get("subject_id"):
            for s_label, sid in self.subject_map.items():
                if sid == session["subject_id"]:
                    default_sub = s_label
                    break

        self.sub_dropdown = FormDropdown(form_scroll, label="Select Subject",
                                         values=sub_names, default_value=default_sub)
        self.sub_dropdown.pack(fill="x", pady=4)

        # Study Date
        date_val = session.get("study_date", date.today().strftime("%Y-%m-%d")) if session else date.today().strftime("%Y-%m-%d")
        self.date_entry = FormDateEntry(form_scroll, label="Study Date", default_date=date_val)
        self.date_entry.pack(fill="x", pady=4)

        # Time row: Start Time and End Time side-by-side
        time_frame = ctk.CTkFrame(form_scroll, fg_color="transparent")
        time_frame.pack(fill="x", pady=4)
        time_frame.columnconfigure((0, 1), weight=1)

        st_val = session.get("start_time", "14:00") if session else "14:00"
        et_val = session.get("end_time", "16:00") if session else "16:00"

        self.start_entry = FormEntry(time_frame, label="Start Time (HH:MM)", placeholder="14:00",
                                     initial_value=st_val, width=180)
        self.start_entry.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.end_entry = FormEntry(time_frame, label="End Time (HH:MM)", placeholder="16:00",
                                   initial_value=et_val, width=180)
        self.end_entry.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        # Priority & Completion row
        meta_frame = ctk.CTkFrame(form_scroll, fg_color="transparent")
        meta_frame.pack(fill="x", pady=4)
        meta_frame.columnconfigure((0, 1), weight=1)

        prio_val = session.get("priority", "Medium") if session else "Medium"
        self.prio_dropdown = FormDropdown(meta_frame, label="Priority",
                                          values=["High", "Medium", "Low"], default_value=prio_val,
                                          width=180)
        self.prio_dropdown.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.is_completed_var = ctk.BooleanVar(value=bool(session.get("is_completed", 0)) if session else False)
        chk_frame = ctk.CTkFrame(meta_frame, fg_color="transparent")
        chk_frame.grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=(20, 0))
        self.completed_chk = ctk.CTkCheckBox(chk_frame, text="Mark as Completed",
                                            variable=self.is_completed_var,
                                            font=FONT_BODY_SM,
                                            fg_color=COLOR_PRIMARY,
                                            text_color=COLOR_TEXT_PRIMARY)
        self.completed_chk.pack(anchor="w")

        # Notes / Topics description
        self.desc_entry = FormTextBox(form_scroll, label="Session Notes / Chapter References",
                                      initial_text=session.get("description", "") if session else "",
                                      height=70)
        self.desc_entry.pack(fill="x", pady=4)

    def _save(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Validation Error", "Session Title cannot be empty.", parent=self)
            return

        selected_sub = self.sub_dropdown.get()
        subject_id = self.subject_map.get(selected_sub, None)

        s_date = self.date_entry.get().strip()
        ok_d, msg_d = validate_date(s_date)
        if not ok_d:
            messagebox.showerror("Validation Error", msg_d, parent=self)
            return

        st_time = self.start_entry.get().strip()
        ok_st, msg_st = validate_time(st_time)
        if not ok_st:
            messagebox.showerror("Validation Error", f"Start Time: {msg_st}", parent=self)
            return

        et_time = self.end_entry.get().strip()
        ok_et, msg_et = validate_time(et_time)
        if not ok_et:
            messagebox.showerror("Validation Error", f"End Time: {msg_et}", parent=self)
            return

        duration = calculate_duration_hours(st_time, et_time)
        if duration <= 0:
            messagebox.showerror("Validation Error", "End Time must be later than Start Time.", parent=self)
            return

        priority = self.prio_dropdown.get()
        is_comp = 1 if self.is_completed_var.get() else 0
        desc = self.desc_entry.get().strip()

        try:
            if self.session:
                self.db.update_session(
                    session_id=self.session["id"],
                    user_id=self.user_id,
                    subject_id=subject_id,
                    title=title,
                    study_date=s_date,
                    start_time=st_time,
                    end_time=et_time,
                    duration_hours=duration,
                    priority=priority,
                    description=desc,
                    is_completed=is_comp
                )
            else:
                self.db.add_session(
                    user_id=self.user_id,
                    subject_id=subject_id,
                    title=title,
                    study_date=s_date,
                    start_time=st_time,
                    end_time=et_time,
                    duration_hours=duration,
                    priority=priority,
                    description=desc,
                    is_completed=is_comp
                )
            if self.on_save:
                self.on_save()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save session: {e}", parent=self)


class TaskDialog(ctk.CTkToplevel):
    """
    Add / Edit Task & Assignment Modal Dialog.
    Features:
    - Fixed Top Header
    - Fixed Bottom Action Bar with prominent Save Task and Cancel buttons
    """
    def __init__(self, parent: Any, db: Any, user_id: int,
                 task: Optional[Dict] = None, on_save_callback: Optional[Callable] = None):
        super().__init__(parent)
        self.db = db
        self.user_id = user_id
        self.task = task
        self.on_save = on_save_callback

        title_text = "Edit Assignment" if task else "Create New Assignment"
        self.title(title_text)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.configure(fg_color=COLOR_BG)

        center_window(self, 520, 560, parent)

        card = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=CARD_RADIUS,
                            border_width=1, border_color=COLOR_BORDER)
        card.pack(fill="both", expand=True, padx=14, pady=14)

        # 1. FIXED TOP HEADER
        top_header = ctk.CTkFrame(card, fg_color="transparent")
        top_header.pack(side="top", fill="x", padx=22, pady=(16, 8))

        ctk.CTkLabel(top_header, text=title_text, font=FONT_HEADING_MD,
                     text_color=COLOR_TEXT_PRIMARY, anchor="w").pack(side="left")

        # 2. FIXED BOTTOM ACTION BAR
        ctk.CTkFrame(card, height=1, fg_color=COLOR_BORDER).pack(side="bottom", fill="x", padx=16, pady=(0, 0))

        btn_bar = ctk.CTkFrame(card, fg_color="transparent")
        btn_bar.pack(side="bottom", fill="x", padx=22, pady=14)

        SecondaryButton(btn_bar, text="Cancel", width=110, height=38,
                        command=self.destroy).pack(side="right", padx=(10, 0))

        action_label = "Update Task" if task else "Save Task"
        self.save_btn = PrimaryButton(btn_bar, text=action_label, width=140, height=38,
                                      command=self._save)
        self.save_btn.pack(side="right")

        # 3. SCROLLABLE FORM BODY
        form_scroll = ctk.CTkScrollableFrame(card, fg_color="transparent")
        form_scroll.pack(side="top", fill="both", expand=True, padx=16, pady=(0, 6))

        # Title
        self.title_entry = FormEntry(form_scroll, label="Assignment Title",
                                     placeholder="e.g. Complete Process Scheduling Lab",
                                     initial_value=task.get("title", "") if task else "")
        self.title_entry.pack(fill="x", pady=4)

        # Subject
        subjects = self.db.get_subjects(user_id)
        self.subject_map = {f"{s['code']} - {s['name']}": s['id'] for s in subjects}
        sub_names = list(self.subject_map.keys())
        if not sub_names:
            sub_names = ["General (No Subject)"]

        default_sub = None
        if task and task.get("subject_id"):
            for s_label, sid in self.subject_map.items():
                if sid == task["subject_id"]:
                    default_sub = s_label
                    break

        self.sub_dropdown = FormDropdown(form_scroll, label="Associated Subject",
                                         values=sub_names, default_value=default_sub)
        self.sub_dropdown.pack(fill="x", pady=4)

        # Due Date
        due_val = task.get("due_date", date.today().strftime("%Y-%m-%d")) if task else date.today().strftime("%Y-%m-%d")
        self.due_entry = FormDateEntry(form_scroll, label="Due Date", default_date=due_val)
        self.due_entry.pack(fill="x", pady=4)

        # Priority & Status row
        meta_frame = ctk.CTkFrame(form_scroll, fg_color="transparent")
        meta_frame.pack(fill="x", pady=4)
        meta_frame.columnconfigure((0, 1), weight=1)

        prio_val = task.get("priority", "Medium") if task else "Medium"
        self.prio_dropdown = FormDropdown(meta_frame, label="Priority",
                                          values=["High", "Medium", "Low"], default_value=prio_val,
                                          width=180)
        self.prio_dropdown.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        status_val = task.get("status", "Pending") if task else "Pending"
        self.status_dropdown = FormDropdown(meta_frame, label="Status",
                                            values=["Pending", "In Progress", "Completed"],
                                            default_value=status_val, width=180)
        self.status_dropdown.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        # Description
        self.desc_entry = FormTextBox(form_scroll, label="Description & Requirements",
                                      initial_text=task.get("description", "") if task else "",
                                      height=75)
        self.desc_entry.pack(fill="x", pady=4)

    def _save(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Validation Error", "Assignment Title is required.", parent=self)
            return

        selected_sub = self.sub_dropdown.get()
        subject_id = self.subject_map.get(selected_sub, None)

        due_date = self.due_entry.get().strip()
        ok_d, msg_d = validate_date(due_date)
        if not ok_d:
            messagebox.showerror("Validation Error", msg_d, parent=self)
            return

        priority = self.prio_dropdown.get()
        status = self.status_dropdown.get()
        desc = self.desc_entry.get().strip()

        try:
            if self.task:
                self.db.update_task(
                    task_id=self.task["id"],
                    user_id=self.user_id,
                    subject_id=subject_id,
                    title=title,
                    description=desc,
                    due_date=due_date,
                    priority=priority,
                    status=status
                )
            else:
                self.db.add_task(
                    user_id=self.user_id,
                    subject_id=subject_id,
                    title=title,
                    description=desc,
                    due_date=due_date,
                    priority=priority,
                    status=status
                )
            if self.on_save:
                self.on_save()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save assignment: {e}", parent=self)


class ExamDialog(ctk.CTkToplevel):
    """
    Add / Edit Examination Modal Dialog.
    Features:
    - Fixed Top Header
    - Prominently sized Save Exam (140x38) and Cancel (110x38) buttons
    - Fixed Bottom Action Bar: Never clipped, fits any screen resolution
    """
    def __init__(self, parent: Any, db: Any, user_id: int,
                 exam: Optional[Dict] = None, on_save_callback: Optional[Callable] = None):
        super().__init__(parent)
        self.db = db
        self.user_id = user_id
        self.exam = exam
        self.on_save = on_save_callback

        title_text = "Edit Examination" if exam else "Schedule Upcoming Examination"
        self.title(title_text)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.configure(fg_color=COLOR_BG)

        center_window(self, 520, 560, parent)

        card = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=CARD_RADIUS,
                            border_width=1, border_color=COLOR_BORDER)
        card.pack(fill="both", expand=True, padx=14, pady=14)

        # 1. FIXED TOP HEADER
        top_header = ctk.CTkFrame(card, fg_color="transparent")
        top_header.pack(side="top", fill="x", padx=22, pady=(16, 8))

        ctk.CTkLabel(top_header, text=title_text, font=FONT_HEADING_MD,
                     text_color=COLOR_TEXT_PRIMARY, anchor="w").pack(side="left")

        # 2. FIXED BOTTOM ACTION BAR
        ctk.CTkFrame(card, height=1, fg_color=COLOR_BORDER).pack(side="bottom", fill="x", padx=16, pady=(0, 0))

        btn_bar = ctk.CTkFrame(card, fg_color="transparent")
        btn_bar.pack(side="bottom", fill="x", padx=22, pady=14)

        SecondaryButton(btn_bar, text="Cancel", width=110, height=38,
                        command=self.destroy).pack(side="right", padx=(10, 0))

        action_label = "Update Exam" if exam else "Save Exam"
        self.save_btn = PrimaryButton(btn_bar, text=action_label, width=140, height=38,
                                      command=self._save)
        self.save_btn.pack(side="right")

        # 3. SCROLLABLE FORM BODY
        form_scroll = ctk.CTkScrollableFrame(card, fg_color="transparent")
        form_scroll.pack(side="top", fill="both", expand=True, padx=16, pady=(0, 6))

        # Exam Name
        self.name_entry = FormEntry(form_scroll, label="Examination Name",
                                    placeholder="e.g. Operating Systems Midterm",
                                    initial_value=exam.get("name", "") if exam else "")
        self.name_entry.pack(fill="x", pady=4)

        # Associated Subject
        subjects = self.db.get_subjects(user_id)
        self.subject_map = {f"{s['code']} - {s['name']}": s['id'] for s in subjects}
        sub_names = list(self.subject_map.keys())
        if not sub_names:
            sub_names = ["General (No Subject)"]

        default_sub = None
        if exam and exam.get("subject_id"):
            for s_label, sid in self.subject_map.items():
                if sid == exam["subject_id"]:
                    default_sub = s_label
                    break

        self.sub_dropdown = FormDropdown(form_scroll, label="Associated Course",
                                         values=sub_names, default_value=default_sub)
        self.sub_dropdown.pack(fill="x", pady=4)

        # Exam Date
        date_val = exam.get("exam_date", date.today().strftime("%Y-%m-%d")) if exam else date.today().strftime("%Y-%m-%d")
        self.date_entry = FormDateEntry(form_scroll, label="Examination Date", default_date=date_val)
        self.date_entry.pack(fill="x", pady=4)

        # Time & Type row
        meta_frame = ctk.CTkFrame(form_scroll, fg_color="transparent")
        meta_frame.pack(fill="x", pady=4)
        meta_frame.columnconfigure((0, 1), weight=1)

        time_val = exam.get("exam_time", "10:00") if exam else "10:00"
        self.time_entry = FormEntry(meta_frame, label="Exam Time (HH:MM)", placeholder="10:00",
                                    initial_value=time_val, width=180)
        self.time_entry.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        type_val = exam.get("exam_type", "Internal Exam") if exam else "Internal Exam"
        self.type_dropdown = FormDropdown(meta_frame, label="Exam Type",
                                          values=["Internal Exam", "Midterm", "End Semester", "Practical", "Quiz"],
                                          default_value=type_val, width=180)
        self.type_dropdown.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        # Syllabus Notes
        self.notes_entry = FormTextBox(form_scroll, label="Syllabus Scope & Preparation Notes",
                                       initial_text=exam.get("notes", "") if exam else "",
                                       height=75)
        self.notes_entry.pack(fill="x", pady=4)

    def _save(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Validation Error", "Examination Name is required.", parent=self)
            return

        selected_sub = self.sub_dropdown.get()
        subject_id = self.subject_map.get(selected_sub, None)

        e_date = self.date_entry.get().strip()
        ok_d, msg_d = validate_date(e_date)
        if not ok_d:
            messagebox.showerror("Validation Error", msg_d, parent=self)
            return

        e_time = self.time_entry.get().strip()
        ok_t, msg_t = validate_time(e_time)
        if not ok_t:
            messagebox.showerror("Validation Error", msg_t, parent=self)
            return

        e_type = self.type_dropdown.get()
        notes = self.notes_entry.get().strip()

        try:
            if self.exam:
                self.db.update_exam(
                    exam_id=self.exam["id"],
                    user_id=self.user_id,
                    subject_id=subject_id,
                    name=name,
                    exam_date=e_date,
                    exam_time=e_time,
                    exam_type=e_type,
                    notes=notes
                )
            else:
                self.db.add_exam(
                    user_id=self.user_id,
                    subject_id=subject_id,
                    name=name,
                    exam_date=e_date,
                    exam_time=e_time,
                    exam_type=e_type,
                    notes=notes
                )
            if self.on_save:
                self.on_save()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save examination: {e}", parent=self)
