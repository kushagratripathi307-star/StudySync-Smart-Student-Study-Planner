"""
StudySync - Smart Student Study Planner
Study Planner Page - Daily & Weekly Timetable, Filters & Execution Tracker
"""

from typing import Any, Callable, Dict, Optional
import customtkinter as ctk
from datetime import date

from utils.theme import (
    COLOR_BG, COLOR_CARD, COLOR_CARD_SECONDARY, COLOR_BORDER,
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_WARNING, COLOR_DANGER,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    FONT_HEADING_LG, FONT_HEADING_MD, FONT_SUBHEADING, FONT_BODY,
    FONT_BODY_BOLD, FONT_BODY_SM, FONT_CAPTION, CARD_RADIUS,
    BUTTON_RADIUS
)
from utils.date_utils import format_date_display, calculate_days_left
from utils.helpers import load_icon
from components.buttons import PrimaryButton, SecondaryButton, IconButton
from components.dialogs import SessionDialog, ConfirmDialog


class PlannerPage(ctk.CTkScrollableFrame):
    """
    Study Planner Module:
    - View and organize daily/weekly study routines
    - Granular filtering by Date, Subject, and Status
    - Add, Edit, Delete, and Toggle completion states
    """
    def __init__(self, master: Any, db: Any, user_id: int, **kwargs):
        super().__init__(master, fg_color=COLOR_BG, corner_radius=0, **kwargs)
        self.db = db
        self.user_id = user_id

        self.current_date_filter = "all"
        self.current_subject_id: Optional[int] = None
        self.current_status_filter = "all"

        self._build_header()
        self._build_filter_bar()
        self._build_sessions_container()

        self.refresh()

    def _build_header(self):
        head = ctk.CTkFrame(self, fg_color="transparent")
        head.pack(fill="x", padx=32, pady=(28, 14))

        ctk.CTkLabel(
            head,
            text="Study Planner",
            font=FONT_HEADING_LG,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            head,
            text="Schedule focused study sessions, balance your workload, and build daily study momentum.",
            font=FONT_BODY,
            text_color=COLOR_TEXT_SECONDARY,
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))

    def _build_filter_bar(self):
        filter_card = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=10,
                                  border_width=1, border_color=COLOR_BORDER)
        filter_card.pack(fill="x", padx=32, pady=(0, 20))

        inner = ctk.CTkFrame(filter_card, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=12)

        # Date Filter segmented / option menu
        ctk.CTkLabel(inner, text="View:", font=FONT_BODY_BOLD, text_color=COLOR_TEXT_SECONDARY).pack(side="left", padx=(0, 6))

        self.date_menu = ctk.CTkOptionMenu(
            inner,
            values=["All Sessions", "Today", "This Week", "Upcoming", "Past"],
            font=FONT_BODY_SM,
            height=34,
            width=130,
            command=self._on_filter_changed
        )
        self.date_menu.pack(side="left", padx=(0, 16))

        # Subject Filter
        ctk.CTkLabel(inner, text="Subject:", font=FONT_BODY_BOLD, text_color=COLOR_TEXT_SECONDARY).pack(side="left", padx=(0, 6))
        self.subject_menu = ctk.CTkOptionMenu(
            inner,
            values=["All Subjects"],
            font=FONT_BODY_SM,
            height=34,
            width=170,
            command=self._on_filter_changed
        )
        self.subject_menu.pack(side="left", padx=(0, 16))

        # Status Filter
        ctk.CTkLabel(inner, text="Status:", font=FONT_BODY_BOLD, text_color=COLOR_TEXT_SECONDARY).pack(side="left", padx=(0, 6))
        self.status_menu = ctk.CTkOptionMenu(
            inner,
            values=["All", "Pending", "Completed"],
            font=FONT_BODY_SM,
            height=34,
            width=120,
            command=self._on_filter_changed
        )
        self.status_menu.pack(side="left")

        # Add Session Button on Right
        plus_icon = load_icon("plus", size=(16, 16))
        PrimaryButton(
            inner,
            text="Add Session",
            icon=plus_icon,
            height=34,
            width=130,
            command=self._on_add_session
        ).pack(side="right")

    def _build_sessions_container(self):
        self.sessions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.sessions_frame.pack(fill="both", expand=True, padx=32, pady=(0, 28))

    def _update_subject_dropdown(self):
        subjects = self.db.get_subjects(self.user_id)
        self.subject_map = {"All Subjects": None}
        sub_list = ["All Subjects"]
        for s in subjects:
            label = f"{s['code']} - {s['name']}"
            self.subject_map[label] = s['id']
            sub_list.append(label)

        curr = self.subject_menu.get()
        self.subject_menu.configure(values=sub_list)
        if curr in sub_list:
            self.subject_menu.set(curr)
        else:
            self.subject_menu.set("All Subjects")

    def _on_filter_changed(self, _=None):
        self.refresh(update_dropdown=False)

    def refresh(self, update_dropdown: bool = True):
        if update_dropdown:
            self._update_subject_dropdown()

        for w in self.sessions_frame.winfo_children():
            w.destroy()

        # Parse active filters
        d_val = self.date_menu.get()
        date_filter = None
        if d_val == "Today":
            date_filter = "today"
        elif d_val == "This Week":
            date_filter = "this_week"
        elif d_val == "Upcoming":
            date_filter = "upcoming"
        elif d_val == "Past":
            date_filter = "past"

        sub_val = self.subject_menu.get()
        subject_id = self.subject_map.get(sub_val, None) if hasattr(self, "subject_map") else None

        st_val = self.status_menu.get()
        status_filter = None if st_val == "All" else st_val.lower()

        sessions = self.db.get_sessions(
            user_id=self.user_id,
            date_filter=date_filter,
            subject_id=subject_id,
            status=status_filter
        )

        if not sessions:
            empty_card = ctk.CTkFrame(self.sessions_frame, fg_color=COLOR_CARD,
                                     corner_radius=CARD_RADIUS, border_width=1,
                                     border_color=COLOR_BORDER)
            empty_card.pack(fill="x", pady=20, ipady=30)

            ctk.CTkLabel(
                empty_card,
                text="🗓️  No study sessions found.",
                font=FONT_HEADING_MD,
                text_color=COLOR_TEXT_PRIMARY
            ).pack(pady=(10, 4))

            ctk.CTkLabel(
                empty_card,
                text="Plan a study session with clear time slots and priority goals.",
                font=FONT_BODY,
                text_color=COLOR_TEXT_SECONDARY
            ).pack(pady=(0, 16))

            PrimaryButton(
                empty_card,
                text="+ Plan First Session",
                width=180,
                command=self._on_add_session
            ).pack()
            return

        for sess in sessions:
            card = self._create_session_card(self.sessions_frame, sess)
            card.pack(fill="x", pady=6)

    def _create_session_card(self, parent: Any, sess: Dict[str, Any]) -> ctk.CTkFrame:
        card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_CARD,
            corner_radius=CARD_RADIUS,
            border_width=1,
            border_color=COLOR_BORDER
        )
        card.columnconfigure(1, weight=1)

        # Left color bar based on subject
        sub_color = sess.get("subject_color") or "#7667F8"
        bar = ctk.CTkFrame(card, width=5, fg_color=sub_color, corner_radius=2)
        bar.pack(side="left", fill="y", padx=(8, 12), pady=8)

        # Details body
        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(side="left", fill="both", expand=True, pady=12)

        # Top row: Title + Priority tag
        top_row = ctk.CTkFrame(body, fg_color="transparent")
        top_row.pack(fill="x", anchor="w")

        title_text = sess["title"]
        if sess["is_completed"]:
            t_lbl = ctk.CTkLabel(top_row, text=f"✓  {title_text}", font=FONT_HEADING_MD,
                                 text_color=COLOR_SECONDARY, anchor="w")
        else:
            t_lbl = ctk.CTkLabel(top_row, text=title_text, font=FONT_HEADING_MD,
                                 text_color=COLOR_TEXT_PRIMARY, anchor="w")
        t_lbl.pack(side="left")

        # Priority Badge
        prio = sess.get("priority", "Medium")
        if prio == "High":
            p_fg = ("#FEE2E2", "#451B1F")
            p_tc = COLOR_DANGER
        elif prio == "Medium":
            p_fg = ("#FEF3C7", "#423215")
            p_tc = COLOR_WARNING
        else:
            p_fg = ("#DCFCE7", "#173B2E")
            p_tc = COLOR_SECONDARY

        p_badge = ctk.CTkFrame(top_row, fg_color=p_fg, corner_radius=6)
        p_badge.pack(side="left", padx=(12, 0))
        ctk.CTkLabel(p_badge, text=prio.upper(), font=("Segoe UI", 10, "bold"),
                     text_color=p_tc).pack(padx=8, pady=2)

        # Second row: Subject, Date, Time, Duration
        meta_row = ctk.CTkFrame(body, fg_color="transparent")
        meta_row.pack(fill="x", anchor="w", pady=(4, 0))

        sub_name = sess.get("subject_name") or "General Study"
        date_formatted = format_date_display(sess["study_date"])
        time_info = f"{sess['start_time']} - {sess['end_time']}  ({sess['duration_hours']} hrs)"

        ctk.CTkLabel(
            meta_row,
            text=f"📚 {sub_name}   •   📅 {date_formatted}   •   ⏰ {time_info}",
            font=FONT_BODY_SM,
            text_color=COLOR_TEXT_MUTED,
            anchor="w"
        ).pack(side="left")

        # Notes if present
        if sess.get("description"):
            ctk.CTkLabel(
                body,
                text=sess["description"],
                font=FONT_BODY_SM,
                text_color=COLOR_TEXT_SECONDARY,
                anchor="w",
                wraplength=600,
                justify="left"
            ).pack(anchor="w", pady=(4, 0))

        # Actions on right
        actions = ctk.CTkFrame(card, fg_color="transparent")
        actions.pack(side="right", padx=16, pady=12)

        # Toggle Done button
        btn_txt = "Completed" if sess["is_completed"] else "Mark Done"
        btn_fg = ("#DCFCE7", "#173B2E") if sess["is_completed"] else COLOR_PRIMARY
        btn_tc = ("#15803D", "#38C98B") if sess["is_completed"] else "#FFFFFF"

        ctk.CTkButton(
            actions,
            text=btn_txt,
            font=FONT_BODY_SM,
            width=100,
            height=32,
            corner_radius=6,
            fg_color=btn_fg,
            hover_color=COLOR_SECONDARY,
            text_color=btn_tc,
            command=lambda sid=sess["id"]: self._toggle_session(sid)
        ).pack(side="left", padx=(0, 8))

        edit_icon = load_icon("edit", size=(14, 14))
        delete_icon = load_icon("delete", size=(14, 14))

        IconButton(actions, icon=edit_icon, size=32,
                   command=lambda s=sess: self._on_edit_session(s)).pack(side="left", padx=(0, 6))
        IconButton(actions, icon=delete_icon, is_danger=True, size=32,
                   command=lambda s=sess: self._on_delete_session(s)).pack(side="left")

        return card

    def _toggle_session(self, session_id: int):
        self.db.toggle_session_completed(session_id, self.user_id)
        self.refresh(update_dropdown=False)

    def _on_add_session(self):
        SessionDialog(self.winfo_toplevel(), self.db, self.user_id,
                      on_save_callback=lambda: self.refresh(update_dropdown=True))

    def _on_edit_session(self, sess: Dict[str, Any]):
        SessionDialog(self.winfo_toplevel(), self.db, self.user_id, session=sess,
                      on_save_callback=lambda: self.refresh(update_dropdown=False))

    def _on_delete_session(self, sess: Dict[str, Any]):
        def confirm():
            self.db.delete_session(sess["id"], self.user_id)
            self.refresh(update_dropdown=False)

        ConfirmDialog(
            parent=self.winfo_toplevel(),
            title="Delete Study Session?",
            message=f"Are you sure you want to delete session '{sess['title']}'?",
            confirm_text="Delete Session",
            is_danger=True,
            on_confirm=confirm
        )
