"""
StudySync - Smart Student Study Planner
Exam Countdown Page - Live Evaluation Timers & Exam Management
"""

from typing import Any, Callable, Dict, Optional
import customtkinter as ctk

from utils.theme import (
    COLOR_BG, COLOR_CARD, COLOR_CARD_SECONDARY, COLOR_BORDER,
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_WARNING, COLOR_DANGER,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    FONT_HEADING_LG, FONT_HEADING_MD, FONT_SUBHEADING, FONT_BODY,
    FONT_BODY_BOLD, FONT_BODY_SM, FONT_CAPTION, FONT_NUMBER_LG,
    CARD_RADIUS, BUTTON_RADIUS
)
from utils.date_utils import format_date_display, calculate_days_left
from utils.helpers import load_icon
from components.buttons import PrimaryButton, SecondaryButton, IconButton
from components.dialogs import ExamDialog, ConfirmDialog


class ExamsPage(ctk.CTkScrollableFrame):
    """
    Exam Countdown Module:
    - Dynamic real-time day countdown badges (12 DAYS LEFT, TOMORROW, TODAY)
    - Critical warning styling for exams within 7 days
    - Filter tabs: Upcoming Exams vs Past Exams
    - CRUD management
    """
    def __init__(self, master: Any, db: Any, user_id: int, **kwargs):
        super().__init__(master, fg_color=COLOR_BG, corner_radius=0, **kwargs)
        self.db = db
        self.user_id = user_id
        self.active_tab = "upcoming"

        self._build_header()
        self._build_toolbar()
        self._build_exams_container()

        self.refresh()

    def _build_header(self):
        head = ctk.CTkFrame(self, fg_color="transparent")
        head.pack(fill="x", padx=32, pady=(28, 14))

        ctk.CTkLabel(
            head,
            text="Exam Countdown",
            font=FONT_HEADING_LG,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            head,
            text="Never be caught unprepared. Track midterms, practicals, and semester finals with dynamic countdowns.",
            font=FONT_BODY,
            text_color=COLOR_TEXT_SECONDARY,
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))

    def _build_toolbar(self):
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=32, pady=(0, 20))

        # Tabs: Upcoming vs Past
        self.tab_selector = ctk.CTkSegmentedButton(
            toolbar,
            values=["Upcoming Examinations", "Past Examinations"],
            font=FONT_BODY_SM,
            height=36,
            command=self._on_tab_change
        )
        self.tab_selector.set("Upcoming Examinations")
        self.tab_selector.pack(side="left")

        # Add Exam button
        plus_icon = load_icon("plus", size=(16, 16))
        PrimaryButton(
            toolbar,
            text="Add Exam",
            icon=plus_icon,
            height=36,
            width=130,
            command=self._on_add_exam
        ).pack(side="right")

    def _build_exams_container(self):
        self.exams_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.exams_frame.pack(fill="both", expand=True, padx=32, pady=(0, 28))

    def _on_tab_change(self, tab_val: str):
        self.active_tab = "upcoming" if "Upcoming" in tab_val else "past"
        self.refresh()

    def refresh(self):
        for w in self.exams_frame.winfo_children():
            w.destroy()

        exams = self.db.get_exams(self.user_id, filter_type=self.active_tab)

        if not exams:
            empty_card = ctk.CTkFrame(self.exams_frame, fg_color=COLOR_CARD,
                                     corner_radius=CARD_RADIUS, border_width=1,
                                     border_color=COLOR_BORDER)
            empty_card.pack(fill="x", pady=20, ipady=30)

            title_text = "🎯  No upcoming exams scheduled!" if self.active_tab == "upcoming" else "📚  No past examinations recorded."
            sub_text = "Add your syllabus test dates to enable countdown tracking." if self.active_tab == "upcoming" else ""

            ctk.CTkLabel(
                empty_card,
                text=title_text,
                font=FONT_HEADING_MD,
                text_color=COLOR_TEXT_PRIMARY
            ).pack(pady=(10, 4))

            if sub_text:
                ctk.CTkLabel(
                    empty_card,
                    text=sub_text,
                    font=FONT_BODY,
                    text_color=COLOR_TEXT_SECONDARY
                ).pack(pady=(0, 16))

                PrimaryButton(
                    empty_card,
                    text="+ Schedule Exam",
                    width=170,
                    command=self._on_add_exam
                ).pack()
            return

        # Render 2-column or 1-column responsive countdown cards
        self.exams_frame.columnconfigure((0, 1), weight=1, uniform="exam_col")

        for idx, ex in enumerate(exams):
            row = idx // 2
            col = idx % 2
            card = self._create_exam_card(self.exams_frame, ex)
            card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)

    def _create_exam_card(self, parent: Any, exam: Dict[str, Any]) -> ctk.CTkFrame:
        days_count, days_text, urgency = calculate_days_left(exam["exam_date"])

        # Determine urgency borders and accent
        if urgency == "past":
            border_c = COLOR_BORDER
            accent_c = COLOR_TEXT_MUTED
            banner_bg = ("#F1F5F9", "#1D2433")
            banner_fg = COLOR_TEXT_MUTED
        elif urgency in ("urgent", "warning"):
            border_c = COLOR_WARNING
            accent_c = COLOR_WARNING
            banner_bg = ("#FEF3C7", "#3B2E15")
            banner_fg = COLOR_WARNING
        else:
            border_c = COLOR_BORDER
            accent_c = COLOR_PRIMARY
            banner_bg = ("#EEF2FF", "#222544")
            banner_fg = COLOR_PRIMARY

        card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_CARD,
            corner_radius=CARD_RADIUS,
            border_width=1.5 if urgency in ("urgent", "warning") else 1,
            border_color=border_c
        )
        card.columnconfigure(0, weight=1)

        # Header: Subject Badge + Type Tag + Actions
        top_row = ctk.CTkFrame(card, fg_color="transparent")
        top_row.pack(fill="x", padx=18, pady=(16, 8))

        sub_name = exam.get("subject_name") or "General Course"
        sub_code = exam.get("subject_code") or "EXAM"
        sub_color = exam.get("subject_color") or "#7667F8"

        code_badge = ctk.CTkFrame(top_row, fg_color=("E0E7FF", "#222544"), corner_radius=6)
        code_badge.pack(side="left")
        ctk.CTkLabel(code_badge, text=sub_code, font=("Segoe UI", 10, "bold"),
                     text_color=sub_color).pack(padx=8, pady=2)

        type_badge = ctk.CTkFrame(top_row, fg_color=COLOR_CARD_SECONDARY, corner_radius=6)
        type_badge.pack(side="left", padx=(8, 0))
        ctk.CTkLabel(type_badge, text=exam.get("exam_type", "Exam"), font=FONT_CAPTION,
                     text_color=COLOR_TEXT_SECONDARY).pack(padx=8, pady=2)

        edit_icon = load_icon("edit", size=(14, 14))
        delete_icon = load_icon("delete", size=(14, 14))

        IconButton(top_row, icon=delete_icon, is_danger=True, size=28,
                   command=lambda e=exam: self._on_delete_exam(e)).pack(side="right", padx=(4, 0))
        IconButton(top_row, icon=edit_icon, size=28,
                   command=lambda e=exam: self._on_edit_exam(e)).pack(side="right")

        # Exam Name
        ctk.CTkLabel(
            card,
            text=exam["name"],
            font=FONT_HEADING_MD,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        ).pack(fill="x", padx=18, pady=(0, 10))

        # Big Countdown Banner
        countdown_banner = ctk.CTkFrame(card, fg_color=banner_bg, corner_radius=8)
        countdown_banner.pack(fill="x", padx=18, pady=(0, 12))

        clock_ic = load_icon("clock", size=(18, 18))
        cd_inner = ctk.CTkFrame(countdown_banner, fg_color="transparent")
        cd_inner.pack(padx=14, pady=10)

        ctk.CTkLabel(
            cd_inner,
            text=f"  {days_text}",
            image=clock_ic,
            compound="left",
            font=FONT_NUMBER_LG,
            text_color=banner_fg
        ).pack()

        # Date & Time Details
        formatted_date = format_date_display(exam["exam_date"])
        time_text = exam.get("exam_time", "10:00")
        info_row = ctk.CTkFrame(card, fg_color="transparent")
        info_row.pack(fill="x", padx=18, pady=(0, 6))

        ctk.CTkLabel(
            info_row,
            text=f"📅 Date: {formatted_date}   •   ⏰ Time: {time_text}",
            font=FONT_BODY_SM,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w")

        # Notes if available
        if exam.get("notes"):
            notes_lbl = ctk.CTkLabel(
                card,
                text=f"📝 {exam['notes']}",
                font=FONT_CAPTION,
                text_color=COLOR_TEXT_MUTED,
                anchor="w",
                wraplength=380,
                justify="left"
            )
            notes_lbl.pack(fill="x", padx=18, pady=(0, 14))
        else:
            ctk.CTkFrame(card, height=8, fg_color="transparent").pack()

        return card

    def _on_add_exam(self):
        ExamDialog(self.winfo_toplevel(), self.db, self.user_id, on_save_callback=self.refresh)

    def _on_edit_exam(self, exam: Dict[str, Any]):
        ExamDialog(self.winfo_toplevel(), self.db, self.user_id, exam=exam, on_save_callback=self.refresh)

    def _on_delete_exam(self, exam: Dict[str, Any]):
        def confirm():
            self.db.delete_exam(exam["id"], self.user_id)
            self.refresh()

        ConfirmDialog(
            parent=self.winfo_toplevel(),
            title="Delete Examination?",
            message=f"Are you sure you want to remove '{exam['name']}'?",
            confirm_text="Delete Exam",
            is_danger=True,
            on_confirm=confirm
        )
