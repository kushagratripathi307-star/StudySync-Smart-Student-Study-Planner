"""
StudySync - Smart Student Study Planner
Dashboard Page - Executive Overview, Dynamic Stats, Weekly Graph & Schedule
"""

from typing import Any, Callable, Dict, Optional, List
from datetime import date
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from utils.theme import (
    COLOR_BG, COLOR_CARD, COLOR_CARD_SECONDARY, COLOR_BORDER,
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_WARNING, COLOR_DANGER,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    FONT_HEADING_LG, FONT_HEADING_MD, FONT_SUBHEADING, FONT_BODY,
    FONT_BODY_BOLD, FONT_BODY_SM, FONT_CAPTION, CARD_RADIUS,
    BUTTON_RADIUS, ThemeManager
)
from utils.date_utils import (
    get_greeting, get_current_date_str, format_date_display,
    calculate_days_left
)
from utils.helpers import load_icon
from components.stat_card import StatCard
from components.buttons import PrimaryButton, SecondaryButton, SuccessButton
from components.dialogs import SubjectDialog, SessionDialog, TaskDialog, ExamDialog


class DashboardPage(ctk.CTkScrollableFrame):
    """
    Main Executive Dashboard:
    - Personalized greeting & header with live date
    - 4 Dynamic Statistics cards
    - Embedded weekly productivity bar chart (Matplotlib)
    - Today's interactive schedule
    - Upcoming assignment deadlines
    - 4 Quick-Action creation buttons
    """
    def __init__(self, master: Any, db: Any, user_id: int,
                 on_navigate: Optional[Callable[[str], None]] = None, **kwargs):
        super().__init__(master, fg_color=COLOR_BG, corner_radius=0, **kwargs)
        self.db = db
        self.user_id = user_id
        self.on_navigate = on_navigate

        self.fig: Optional[Figure] = None
        self.chart_canvas: Optional[FigureCanvasTkAgg] = None

        self._build_header()
        self._build_stats_section()
        self._build_quick_actions()
        self._build_main_grid()

        self.refresh()

    def _build_header(self):
        """Header with user greeting, subtitle, and date badge."""
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=32, pady=(28, 18))

        left_col = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        left_col.pack(side="left", fill="both")

        self.greeting_label = ctk.CTkLabel(
            left_col,
            text="Welcome to StudySync!",
            font=FONT_HEADING_LG,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        self.greeting_label.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            left_col,
            text="Let's make today productive. Here is your academic routine at a glance.",
            font=FONT_BODY,
            text_color=COLOR_TEXT_SECONDARY,
            anchor="w"
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        # Right date badge and refresh button
        right_col = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        right_col.pack(side="right", anchor="e")

        date_badge = ctk.CTkFrame(right_col, fg_color=COLOR_CARD, corner_radius=8,
                                 border_width=1, border_color=COLOR_BORDER)
        date_badge.pack(side="left", padx=(0, 10))

        cal_icon = load_icon("calendar", size=(16, 16))
        ctk.CTkLabel(date_badge, text=f"  {get_current_date_str()}", image=cal_icon,
                     compound="left", font=FONT_BODY_BOLD, text_color=COLOR_TEXT_PRIMARY).pack(padx=14, pady=8)

        refresh_icon = load_icon("refresh", size=(16, 16))
        refresh_btn = ctk.CTkButton(
            right_col,
            text="",
            image=refresh_icon,
            width=36,
            height=36,
            fg_color=COLOR_CARD,
            hover_color=COLOR_CARD_SECONDARY,
            border_width=1,
            border_color=COLOR_BORDER,
            corner_radius=8,
            command=self.refresh
        )
        refresh_btn.pack(side="left")

    def _build_stats_section(self):
        """Top 4 Stat Cards Row."""
        self.stats_container = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_container.pack(fill="x", padx=32, pady=(0, 20))

        for i in range(4):
            self.stats_container.columnconfigure(i, weight=1, uniform="stat_cards")

        # 1. Total Subjects
        sub_icon = load_icon("book", size=(20, 20))
        self.card_subjects = StatCard(
            self.stats_container,
            title="Total Subjects",
            value="0",
            subtitle="Enrolled subjects",
            icon=sub_icon,
            accent_color="#7667F8"
        )
        self.card_subjects.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        # 2. Study Hours
        clock_icon = load_icon("clock", size=(20, 20))
        self.card_hours = StatCard(
            self.stats_container,
            title="Study Hours",
            value="0h",
            subtitle="Studied this week",
            icon=clock_icon,
            accent_color="#38C98B"
        )
        self.card_hours.grid(row=0, column=1, sticky="ew", padx=10)

        # 3. Completed Tasks
        check_icon = load_icon("check", size=(20, 20))
        self.card_tasks = StatCard(
            self.stats_container,
            title="Completed Tasks",
            value="0",
            subtitle="Assignments finished",
            icon=check_icon,
            accent_color="#3B82F6"
        )
        self.card_tasks.grid(row=0, column=2, sticky="ew", padx=10)

        # 4. Upcoming Exams
        exam_icon = load_icon("exams", size=(20, 20))
        self.card_exams = StatCard(
            self.stats_container,
            title="Upcoming Exams",
            value="0",
            subtitle="Scheduled ahead",
            icon=exam_icon,
            accent_color="#F5B84B"
        )
        self.card_exams.grid(row=0, column=3, sticky="ew", padx=(10, 0))

    def _build_quick_actions(self):
        """Quick Actions Toolbar."""
        qa_bar = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=10,
                             border_width=1, border_color=COLOR_BORDER)
        qa_bar.pack(fill="x", padx=32, pady=(0, 22))

        inner = ctk.CTkFrame(qa_bar, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=12)

        ctk.CTkLabel(
            inner,
            text="⚡ Quick Actions:",
            font=FONT_BODY_BOLD,
            text_color=COLOR_TEXT_PRIMARY
        ).pack(side="left", padx=(0, 14))

        plus_icon = load_icon("plus", size=(14, 14))

        PrimaryButton(
            inner,
            text="Add Subject",
            icon=plus_icon,
            height=34,
            command=self._quick_add_subject
        ).pack(side="left", padx=4)

        PrimaryButton(
            inner,
            text="Create Study Task",
            icon=plus_icon,
            height=34,
            command=self._quick_add_session
        ).pack(side="left", padx=4)

        SecondaryButton(
            inner,
            text="Add Assignment",
            icon=plus_icon,
            height=34,
            command=self._quick_add_task
        ).pack(side="left", padx=4)

        SecondaryButton(
            inner,
            text="Add Exam",
            icon=plus_icon,
            height=34,
            command=self._quick_add_exam
        ).pack(side="left", padx=4)

    def _build_main_grid(self):
        """2-Column Layout: Left (Chart + Schedule), Right (Upcoming Deadlines)."""
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True, padx=32, pady=(0, 28))

        self.grid_frame.columnconfigure(0, weight=6, uniform="dash_main")
        self.grid_frame.columnconfigure(1, weight=4, uniform="dash_main")

        # -------------------------------------------------------------
        # LEFT COLUMN: Chart + Today's Schedule
        # -------------------------------------------------------------
        left_container = ctk.CTkFrame(self.grid_frame, fg_color="transparent")
        left_container.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        # Chart Card
        self.chart_card = ctk.CTkFrame(left_container, fg_color=COLOR_CARD,
                                      corner_radius=CARD_RADIUS, border_width=1,
                                      border_color=COLOR_BORDER)
        self.chart_card.pack(fill="x", pady=(0, 18))

        chart_head = ctk.CTkFrame(self.chart_card, fg_color="transparent")
        chart_head.pack(fill="x", padx=20, pady=(16, 8))

        ctk.CTkLabel(
            chart_head,
            text="Weekly Study Productivity",
            font=FONT_HEADING_MD,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        ).pack(side="left")

        ctk.CTkLabel(
            chart_head,
            text="Monday - Sunday (Hours)",
            font=FONT_CAPTION,
            text_color=COLOR_TEXT_MUTED
        ).pack(side="right")

        self.chart_body = ctk.CTkFrame(self.chart_card, fg_color="transparent", height=230)
        self.chart_body.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        # Today's Schedule Card
        self.schedule_card = ctk.CTkFrame(left_container, fg_color=COLOR_CARD,
                                         corner_radius=CARD_RADIUS, border_width=1,
                                         border_color=COLOR_BORDER)
        self.schedule_card.pack(fill="both", expand=True)

        sched_head = ctk.CTkFrame(self.schedule_card, fg_color="transparent")
        sched_head.pack(fill="x", padx=20, pady=(16, 12))

        ctk.CTkLabel(
            sched_head,
            text="Today's Study Schedule",
            font=FONT_HEADING_MD,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        ).pack(side="left")

        self.sched_count_lbl = ctk.CTkLabel(
            sched_head,
            text="0 sessions planned",
            font=FONT_BODY_SM,
            text_color=COLOR_TEXT_MUTED
        )
        self.sched_count_lbl.pack(side="right")

        self.schedule_list_frame = ctk.CTkFrame(self.schedule_card, fg_color="transparent")
        self.schedule_list_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # -------------------------------------------------------------
        # RIGHT COLUMN: Upcoming Deadlines
        # -------------------------------------------------------------
        self.deadlines_card = ctk.CTkFrame(self.grid_frame, fg_color=COLOR_CARD,
                                          corner_radius=CARD_RADIUS, border_width=1,
                                          border_color=COLOR_BORDER)
        self.deadlines_card.grid(row=0, column=1, sticky="nsew", padx=(12, 0))

        dl_head = ctk.CTkFrame(self.deadlines_card, fg_color="transparent")
        dl_head.pack(fill="x", padx=20, pady=(16, 12))

        ctk.CTkLabel(
            dl_head,
            text="Upcoming Deadlines",
            font=FONT_HEADING_MD,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        ).pack(side="left")

        self.dl_count_lbl = ctk.CTkLabel(
            dl_head,
            text="0 tasks pending",
            font=FONT_BODY_SM,
            text_color=COLOR_TEXT_MUTED
        )
        self.dl_count_lbl.pack(side="right")

        self.deadlines_list_frame = ctk.CTkFrame(self.deadlines_card, fg_color="transparent")
        self.deadlines_list_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    # =========================================================================
    # REFRESH & DATA POPULATION
    # =========================================================================

    def refresh(self):
        """Fetches fresh data and refreshes all widgets and charts."""
        user = self.db.get_user_by_id(self.user_id)
        if user:
            name = user.get("full_name", "Student")
            self.greeting_label.configure(text=get_greeting(name))

        # 1. Update Stat Cards
        subjects = self.db.get_subjects(self.user_id)
        self.card_subjects.update_values(str(len(subjects)), f"{len(subjects)} active courses")

        hours_this_week = self.db.get_total_hours_this_week(self.user_id)
        total_hours = self.db.get_total_study_hours_all_time(self.user_id)
        self.card_hours.update_values(f"{hours_this_week} hrs", f"All-time: {total_hours} hrs")

        task_stats = self.db.get_task_stats(self.user_id)
        self.card_tasks.update_values(str(task_stats["completed"]), f"{task_stats['pending']} pending")

        upcoming_exams = self.db.get_upcoming_exams_count(self.user_id)
        self.card_exams.update_values(str(upcoming_exams), "Upcoming tests")

        # 2. Render Weekly Chart
        self._render_weekly_chart()

        # 3. Populate Today's Schedule
        self._populate_schedule()

        # 4. Populate Deadlines
        self._populate_deadlines()

    def _render_weekly_chart(self):
        """Draws the dark-themed weekly study hours bar chart."""
        weekly_data = self.db.get_weekly_study_hours(self.user_id)
        days = list(weekly_data.keys())
        hours = list(weekly_data.values())

        is_dark = ThemeManager.is_dark()
        bg_color = ThemeManager.get_chart_bg()
        fg_color = ThemeManager.get_chart_fg()
        grid_color = ThemeManager.get_chart_grid()
        bar_color = "#7667F8"
        accent_hl = "#38C98B"

        if self.fig is None:
            self.fig = Figure(figsize=(5.5, 2.2), dpi=100, facecolor=bg_color)
            self.chart_canvas = FigureCanvasTkAgg(self.fig, master=self.chart_body)
            self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)

        self.fig.clear()
        self.fig.patch.set_facecolor(bg_color)
        ax = self.fig.add_subplot(111)
        ax.set_facecolor(bg_color)

        colors = [accent_hl if h > 3.0 else bar_color for h in hours]
        bars = ax.bar(days, hours, color=colors, width=0.52, zorder=3, edgecolor="none",
                      capstyle="round")

        # Add data labels above bars
        for bar, h in zip(bars, hours):
            if h > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.15,
                    f"{h:g}h",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                    color=fg_color,
                    fontweight="bold"
                )

        ax.grid(axis="y", linestyle="--", alpha=0.3, color=grid_color, zorder=0)
        ax.tick_params(axis="x", colors=fg_color, labelsize=9)
        ax.tick_params(axis="y", colors=ThemeManager.get_chart_secondary(), labelsize=8)

        # Style Spines
        for sp in ["top", "right"]:
            ax.spines[sp].set_visible(False)
        for sp in ["bottom", "left"]:
            ax.spines[sp].set_color(grid_color)

        max_h = max(hours) if hours else 0
        ax.set_ylim(0, max(max_h + 1.2, 4.0))

        self.fig.tight_layout(pad=1.2)
        self.chart_canvas.draw()

    def _populate_schedule(self):
        """Displays today's study sessions with live toggle completion."""
        for w in self.schedule_list_frame.winfo_children():
            w.destroy()

        today_sessions = self.db.get_today_sessions(self.user_id)
        self.sched_count_lbl.configure(text=f"{len(today_sessions)} planned today")

        if not today_sessions:
            empty_box = ctk.CTkFrame(self.schedule_list_frame, fg_color="transparent")
            empty_box.pack(fill="x", pady=24)
            ctk.CTkLabel(
                empty_box,
                text="☕ No study sessions planned for today.",
                font=FONT_BODY,
                text_color=COLOR_TEXT_MUTED
            ).pack()
            PrimaryButton(
                empty_box,
                text="+ Plan Study Session",
                height=32,
                width=160,
                command=self._quick_add_session
            ).pack(pady=(10, 0))
            return

        for sess in today_sessions:
            item = ctk.CTkFrame(
                self.schedule_list_frame,
                fg_color=COLOR_CARD_SECONDARY,
                corner_radius=8,
                border_width=1,
                border_color=COLOR_BORDER
            )
            item.pack(fill="x", pady=4)

            # Left color bar
            sub_color = sess.get("subject_color") or "#7667F8"
            bar = ctk.CTkFrame(item, width=4, fg_color=sub_color, corner_radius=2)
            bar.pack(side="left", fill="y", padx=(6, 8), pady=6)

            # Details
            details = ctk.CTkFrame(item, fg_color="transparent")
            details.pack(side="left", fill="both", expand=True, pady=8)

            title_row = ctk.CTkFrame(details, fg_color="transparent")
            title_row.pack(fill="x", anchor="w")

            t_text = sess["title"]
            if sess["is_completed"]:
                t_lbl = ctk.CTkLabel(title_row, text=f"✓ {t_text}", font=FONT_BODY_BOLD,
                                     text_color=COLOR_SECONDARY, anchor="w")
            else:
                t_lbl = ctk.CTkLabel(title_row, text=t_text, font=FONT_BODY_BOLD,
                                     text_color=COLOR_TEXT_PRIMARY, anchor="w")
            t_lbl.pack(side="left")

            sub_name = sess.get("subject_name") or "General"
            time_str = f"{sess['start_time']} - {sess['end_time']} ({sess['duration_hours']}h)"
            sub_lbl = ctk.CTkLabel(details, text=f"{sub_name}  •  {time_str}",
                                  font=FONT_CAPTION, text_color=COLOR_TEXT_MUTED, anchor="w")
            sub_lbl.pack(anchor="w", pady=(2, 0))

            # Status action button
            btn_txt = "Completed" if sess["is_completed"] else "Mark Done"
            btn_fg = ("#DCFCE7", "#173B2E") if sess["is_completed"] else COLOR_PRIMARY
            btn_text_color = ("#15803D", "#38C98B") if sess["is_completed"] else "#FFFFFF"

            toggle_btn = ctk.CTkButton(
                item,
                text=btn_txt,
                font=FONT_CAPTION,
                width=80,
                height=28,
                corner_radius=6,
                fg_color=btn_fg,
                hover_color=COLOR_SECONDARY,
                text_color=btn_text_color,
                command=lambda sid=sess["id"]: self._toggle_session(sid)
            )
            toggle_btn.pack(side="right", padx=12)

    def _populate_deadlines(self):
        """Displays upcoming assignment deadlines."""
        for w in self.deadlines_list_frame.winfo_children():
            w.destroy()

        deadlines = self.db.get_upcoming_deadlines(self.user_id, limit=6)
        self.dl_count_lbl.configure(text=f"{len(deadlines)} due soon")

        if not deadlines:
            empty_box = ctk.CTkFrame(self.deadlines_list_frame, fg_color="transparent")
            empty_box.pack(fill="x", pady=24)
            ctk.CTkLabel(
                empty_box,
                text="🎉 All caught up! No pending deadlines.",
                font=FONT_BODY,
                text_color=COLOR_TEXT_MUTED
            ).pack()
            SecondaryButton(
                empty_box,
                text="+ Add Assignment",
                height=32,
                width=150,
                command=self._quick_add_task
            ).pack(pady=(10, 0))
            return

        for dl in deadlines:
            item = ctk.CTkFrame(
                self.deadlines_list_frame,
                fg_color=COLOR_CARD_SECONDARY,
                corner_radius=8,
                border_width=1,
                border_color=COLOR_BORDER
            )
            item.pack(fill="x", pady=5)

            details = ctk.CTkFrame(item, fg_color="transparent")
            details.pack(side="left", fill="both", expand=True, padx=12, pady=10)

            title_row = ctk.CTkFrame(details, fg_color="transparent")
            title_row.pack(fill="x", anchor="w")

            ctk.CTkLabel(
                title_row,
                text=dl["title"],
                font=FONT_BODY_BOLD,
                text_color=COLOR_TEXT_PRIMARY,
                anchor="w"
            ).pack(side="left")

            sub_name = dl.get("subject_name") or "General"
            due_formatted = format_date_display(dl["due_date"])
            meta_lbl = ctk.CTkLabel(
                details,
                text=f"{sub_name}  •  Due: {due_formatted}",
                font=FONT_CAPTION,
                text_color=COLOR_TEXT_MUTED,
                anchor="w"
            )
            meta_lbl.pack(anchor="w", pady=(2, 0))

            # Remaining days badge
            days_count, days_text, urgency = calculate_days_left(dl["due_date"])
            if urgency == "past":
                badge_fg = ("#FEE2E2", "#451B1F")
                badge_text_color = COLOR_DANGER
            elif urgency == "urgent":
                badge_fg = ("#FEF3C7", "#423215")
                badge_text_color = COLOR_WARNING
            else:
                badge_fg = ("#E0E7FF", "#252B4D")
                badge_text_color = COLOR_PRIMARY

            badge = ctk.CTkFrame(item, fg_color=badge_fg, corner_radius=6)
            badge.pack(side="right", padx=12)

            ctk.CTkLabel(
                badge,
                text=days_text,
                font=("Segoe UI", 10, "bold"),
                text_color=badge_text_color
            ).pack(padx=8, pady=4)

    def _toggle_session(self, session_id: int):
        self.db.toggle_session_completed(session_id, self.user_id)
        self.refresh()

    # =========================================================================
    # QUICK ACTION MODALS
    # =========================================================================

    def _quick_add_subject(self):
        SubjectDialog(self.winfo_toplevel(), self.db, self.user_id, on_save_callback=self.refresh)

    def _quick_add_session(self):
        SessionDialog(self.winfo_toplevel(), self.db, self.user_id, on_save_callback=self.refresh)

    def _quick_add_task(self):
        TaskDialog(self.winfo_toplevel(), self.db, self.user_id, on_save_callback=self.refresh)

    def _quick_add_exam(self):
        ExamDialog(self.winfo_toplevel(), self.db, self.user_id, on_save_callback=self.refresh)
