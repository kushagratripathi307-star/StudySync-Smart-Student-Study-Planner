"""
StudySync - Smart Student Study Planner
Productivity Analytics Page - Dynamic Visual Charts and Academic Metrics
"""

from typing import Any, Callable, Dict, Optional, List
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from utils.theme import (
    COLOR_BG, COLOR_CARD, COLOR_CARD_SECONDARY, COLOR_BORDER,
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_WARNING, COLOR_DANGER,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    FONT_HEADING_LG, FONT_HEADING_MD, FONT_SUBHEADING, FONT_BODY,
    FONT_BODY_BOLD, FONT_BODY_SM, FONT_CAPTION, CARD_RADIUS,
    ThemeManager
)
from utils.helpers import load_icon
from components.stat_card import StatCard


class AnalyticsPage(ctk.CTkScrollableFrame):
    """
    Productivity Analytics Module:
    - 4 Key Academic Performance Indicators (KPIs)
    - 4 Embedded Dark Matplotlib Visualizations:
        1. Weekly Study Distribution (Bar Chart)
        2. Subject Hours Share (Donut Chart)
        3. Monthly Study Productivity Trend (Line Chart)
        4. Task Completion & Breakdown (Status Chart)
    - Friendly Empty State when no data has been logged
    """
    def __init__(self, master: Any, db: Any, user_id: int, **kwargs):
        super().__init__(master, fg_color=COLOR_BG, corner_radius=0, **kwargs)
        self.db = db
        self.user_id = user_id

        self.figs: Dict[str, Figure] = {}
        self.canvases: Dict[str, FigureCanvasTkAgg] = {}

        self._build_header()
        self._build_kpis()
        self._build_charts_grid()

        self.refresh()

    def _build_header(self):
        head = ctk.CTkFrame(self, fg_color="transparent")
        head.pack(fill="x", padx=32, pady=(28, 14))

        ctk.CTkLabel(
            head,
            text="Productivity Analytics",
            font=FONT_HEADING_LG,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            head,
            text="Comprehensive data-driven insights into your study habits, subject focus, and task velocity.",
            font=FONT_BODY,
            text_color=COLOR_TEXT_SECONDARY,
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))

    def _build_kpis(self):
        """Top KPI Cards row."""
        self.kpi_container = ctk.CTkFrame(self, fg_color="transparent")
        self.kpi_container.pack(fill="x", padx=32, pady=(0, 20))

        for i in range(4):
            self.kpi_container.columnconfigure(i, weight=1, uniform="kpi_cards")

        # 1. Total Study Hours
        clock_icon = load_icon("clock", size=(20, 20))
        self.kpi_total_hours = StatCard(
            self.kpi_container,
            title="Total Study Hours",
            value="0.0 hrs",
            subtitle="All-time completed sessions",
            icon=clock_icon,
            accent_color="#7667F8"
        )
        self.kpi_total_hours.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        # 2. Daily Average
        stat_icon = load_icon("analytics", size=(20, 20))
        self.kpi_daily_avg = StatCard(
            self.kpi_container,
            title="Daily Average",
            value="0.0 hrs",
            subtitle="Calculated this week",
            icon=stat_icon,
            accent_color="#38C98B"
        )
        self.kpi_daily_avg.grid(row=0, column=1, sticky="ew", padx=10)

        # 3. Top Studied Subject
        book_icon = load_icon("book", size=(20, 20))
        self.kpi_top_subject = StatCard(
            self.kpi_container,
            title="Most Studied",
            value="None",
            subtitle="Highest logged hours",
            icon=book_icon,
            accent_color="#3B82F6"
        )
        self.kpi_top_subject.grid(row=0, column=2, sticky="ew", padx=10)

        # 4. Task Completion Rate
        check_icon = load_icon("check", size=(20, 20))
        self.kpi_task_rate = StatCard(
            self.kpi_container,
            title="Task Success Rate",
            value="0%",
            subtitle="Completed / Total Tasks",
            icon=check_icon,
            accent_color="#F5B84B"
        )
        self.kpi_task_rate.grid(row=0, column=3, sticky="ew", padx=(10, 0))

    def _build_charts_grid(self):
        """2x2 Grid for Matplotlib Visualizations."""
        self.charts_grid = ctk.CTkFrame(self, fg_color="transparent")
        self.charts_grid.pack(fill="both", expand=True, padx=32, pady=(0, 28))

        self.charts_grid.columnconfigure((0, 1), weight=1, uniform="chart_cols")

        # 1. Weekly Study Hours Bar Chart
        self.card_c1, self.body_c1 = self._create_chart_card(
            self.charts_grid, row=0, col=0,
            title="Weekly Study Activity",
            subtitle="Logged hours from Monday to Sunday"
        )

        # 2. Subject Distribution Donut Chart
        self.card_c2, self.body_c2 = self._create_chart_card(
            self.charts_grid, row=0, col=1,
            title="Subject-wise Time Allocation",
            subtitle="Percentage share of completed study time"
        )

        # 3. Monthly Trend Line Chart
        self.card_c3, self.body_c3 = self._create_chart_card(
            self.charts_grid, row=1, col=0,
            title="Monthly Productivity Trend",
            subtitle="Weekly volume across the past 4 weeks"
        )

        # 4. Task Status Breakdown
        self.card_c4, self.body_c4 = self._create_chart_card(
            self.charts_grid, row=1, col=1,
            title="Task Status Breakdown",
            subtitle="Completed, In Progress, Pending & Overdue"
        )

    def _create_chart_card(self, parent: Any, row: int, col: int,
                           title: str, subtitle: str) -> tuple[ctk.CTkFrame, ctk.CTkFrame]:
        card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_CARD,
            corner_radius=CARD_RADIUS,
            border_width=1,
            border_color=COLOR_BORDER
        )
        card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)

        head = ctk.CTkFrame(card, fg_color="transparent")
        head.pack(fill="x", padx=18, pady=(16, 6))

        ctk.CTkLabel(
            head,
            text=title,
            font=FONT_HEADING_MD,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            head,
            text=subtitle,
            font=FONT_CAPTION,
            text_color=COLOR_TEXT_MUTED,
            anchor="w"
        ).pack(anchor="w", pady=(1, 0))

        body = ctk.CTkFrame(card, fg_color="transparent", height=230)
        body.pack(fill="both", expand=True, padx=12, pady=(0, 14))

        return card, body

    # =========================================================================
    # REFRESH & CHART DRAWING
    # =========================================================================

    def refresh(self):
        # 1. Update KPIs
        total_hours = self.db.get_total_study_hours_all_time(self.user_id)
        week_hours = self.db.get_total_hours_this_week(self.user_id)
        daily_avg = round(week_hours / 7.0, 1)

        self.kpi_total_hours.update_values(f"{total_hours:g} hrs", "All-time logged study")
        self.kpi_daily_avg.update_values(f"{daily_avg:g} hrs/day", f"{week_hours:g} hrs this week")

        subjects_dist = self.db.get_subject_distribution(self.user_id)
        if subjects_dist:
            top_sub = subjects_dist[0]["subject_name"]
            top_h = subjects_dist[0]["total_hours"]
            # Shorten if long
            top_display = top_sub if len(top_sub) <= 18 else top_sub[:16] + "..."
            self.kpi_top_subject.update_values(top_display, f"{top_h:g} hrs logged")
        else:
            self.kpi_top_subject.update_values("None Yet", "No study sessions logged")

        task_stats = self.db.get_task_stats(self.user_id)
        total_tasks = task_stats["total"]
        comp_tasks = task_stats["completed"]
        rate = int(round((comp_tasks / total_tasks) * 100)) if total_tasks > 0 else 0
        self.kpi_task_rate.update_values(f"{rate}%", f"{comp_tasks} of {total_tasks} completed")

        # 2. Draw Charts
        self._plot_weekly_bar()
        self._plot_subject_pie()
        self._plot_monthly_line()
        self._plot_tasks_bar()

    def _get_canvas(self, name: str, parent: ctk.CTkFrame, figsize=(4.8, 2.3)) -> tuple[Figure, FigureCanvasTkAgg]:
        bg_color = ThemeManager.get_chart_bg()
        if name not in self.figs:
            fig = Figure(figsize=figsize, dpi=100, facecolor=bg_color)
            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            self.figs[name] = fig
            self.canvases[name] = canvas
        else:
            fig = self.figs[name]
            canvas = self.canvases[name]
            fig.clear()
            fig.patch.set_facecolor(bg_color)
        return fig, canvas

    def _plot_weekly_bar(self):
        """Chart 1: Weekly Study Bar Chart."""
        fig, canvas = self._get_canvas("weekly", self.body_c1)
        bg_color = ThemeManager.get_chart_bg()
        fg_color = ThemeManager.get_chart_fg()
        grid_color = ThemeManager.get_chart_grid()

        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)

        data = self.db.get_weekly_study_hours(self.user_id)
        days = list(data.keys())
        hours = list(data.values())

        bars = ax.bar(days, hours, color="#7667F8", width=0.52, zorder=3, edgecolor="none")

        for bar, h in zip(bars, hours):
            if h > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                        f"{h:g}h", ha="center", va="bottom", fontsize=8, color=fg_color, fontweight="bold")

        ax.grid(axis="y", linestyle="--", alpha=0.3, color=grid_color, zorder=0)
        ax.tick_params(axis="x", colors=fg_color, labelsize=9)
        ax.tick_params(axis="y", colors=ThemeManager.get_chart_secondary(), labelsize=8)

        for sp in ["top", "right"]:
            ax.spines[sp].set_visible(False)
        for sp in ["bottom", "left"]:
            ax.spines[sp].set_color(grid_color)

        max_h = max(hours) if hours else 0
        ax.set_ylim(0, max(max_h + 1.2, 4.0))

        fig.tight_layout(pad=1.0)
        canvas.draw()

    def _plot_subject_pie(self):
        """Chart 2: Subject Allocation Donut Chart."""
        fig, canvas = self._get_canvas("subject_pie", self.body_c2)
        bg_color = ThemeManager.get_chart_bg()
        fg_color = ThemeManager.get_chart_fg()

        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)

        dist = self.db.get_subject_distribution(self.user_id)
        if not dist:
            ax.text(0.5, 0.5, "No completed study sessions\nto display distribution.",
                    ha="center", va="center", color=ThemeManager.get_chart_secondary(), fontsize=10)
            ax.axis("off")
            fig.tight_layout(pad=1.0)
            canvas.draw()
            return

        labels = [d["subject_name"] for d in dist]
        sizes = [d["total_hours"] for d in dist]
        colors = [d.get("subject_color") or "#7667F8" for d in dist]

        # Donut Chart
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=None,
            autopct="%1.0f%%",
            pctdistance=0.75,
            startangle=140,
            colors=colors,
            wedgeprops=dict(width=0.45, edgecolor=bg_color, linewidth=2)
        )

        for at in autotexts:
            at.set_color("#FFFFFF")
            at.set_fontsize(8)
            at.set_fontweight("bold")

        # Compact legend
        legend_labels = [l if len(l) <= 15 else l[:13] + "..." for l in labels]
        ax.legend(
            wedges, legend_labels,
            loc="center left",
            bbox_to_anchor=(0.9, 0.5),
            frameon=False,
            labelcolor=fg_color,
            fontsize=8
        )

        fig.tight_layout(pad=1.0)
        canvas.draw()

    def _plot_monthly_line(self):
        """Chart 3: 4-Week Trend Line Chart."""
        fig, canvas = self._get_canvas("monthly", self.body_c3)
        bg_color = ThemeManager.get_chart_bg()
        fg_color = ThemeManager.get_chart_fg()
        grid_color = ThemeManager.get_chart_grid()

        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)

        trend = self.db.get_monthly_study_trend(self.user_id)
        weeks = [t["week"] for t in trend]
        hours = [t["hours"] for t in trend]

        ax.plot(weeks, hours, marker="o", color="#38C98B", linewidth=2.5, markersize=6, zorder=4)
        ax.fill_between(weeks, hours, color="#38C98B", alpha=0.15, zorder=2)

        for w, h in zip(weeks, hours):
            if h > 0:
                ax.text(w, h + 0.3, f"{h:g}h", ha="center", va="bottom", fontsize=8,
                        color=fg_color, fontweight="bold")

        ax.grid(axis="y", linestyle="--", alpha=0.3, color=grid_color, zorder=0)
        ax.tick_params(axis="x", colors=fg_color, labelsize=9)
        ax.tick_params(axis="y", colors=ThemeManager.get_chart_secondary(), labelsize=8)

        for sp in ["top", "right"]:
            ax.spines[sp].set_visible(False)
        for sp in ["bottom", "left"]:
            ax.spines[sp].set_color(grid_color)

        max_h = max(hours) if hours else 0
        ax.set_ylim(0, max(max_h + 1.5, 5.0))

        fig.tight_layout(pad=1.0)
        canvas.draw()

    def _plot_tasks_bar(self):
        """Chart 4: Tasks Breakdown Horizontal Bar Chart."""
        fig, canvas = self._get_canvas("task_status", self.body_c4)
        bg_color = ThemeManager.get_chart_bg()
        fg_color = ThemeManager.get_chart_fg()
        grid_color = ThemeManager.get_chart_grid()

        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)

        stats = self.db.get_task_stats(self.user_id)
        categories = ["Completed", "In Progress", "Pending", "Overdue"]
        counts = [
            stats["completed"],
            stats["in_progress"],
            stats["pending"],
            stats["overdue"]
        ]
        bar_colors = ["#38C98B", "#3B82F6", "#F5B84B", "#F16B75"]

        # Horizontal Bar Chart
        y_pos = range(len(categories))
        bars = ax.barh(y_pos, counts, color=bar_colors, height=0.55, edgecolor="none", zorder=3)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(categories, fontsize=9, color=fg_color)
        ax.invert_yaxis()  # Labels read top-to-bottom

        for bar, count in zip(bars, counts):
            if count > 0:
                ax.text(bar.get_width() + 0.15, bar.get_y() + bar.get_height() / 2,
                        f"{count}", ha="left", va="center", fontsize=8, color=fg_color, fontweight="bold")

        ax.grid(axis="x", linestyle="--", alpha=0.3, color=grid_color, zorder=0)
        ax.tick_params(axis="x", colors=ThemeManager.get_chart_secondary(), labelsize=8)

        for sp in ["top", "right"]:
            ax.spines[sp].set_visible(False)
        for sp in ["bottom", "left"]:
            ax.spines[sp].set_color(grid_color)

        max_c = max(counts) if counts else 0
        ax.set_xlim(0, max(max_c + 2, 4))

        fig.tight_layout(pad=1.0)
        canvas.draw()
