"""
StudySync - Smart Student Study Planner
Tasks & Assignments Page - Deadline Tracking, Priority Sorting & Task Lifecycle
"""

from typing import Any, Callable, Dict, Optional
import customtkinter as ctk

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
from components.dialogs import TaskDialog, ConfirmDialog


class TasksPage(ctk.CTkScrollableFrame):
    """
    Tasks and Assignments Module:
    - Status tabs (All, Pending, In Progress, Completed, Overdue)
    - Multi-criteria filtering (Subject, Priority, Keyword Search, Sort by)
    - Visual status badges and urgency indicators
    """
    def __init__(self, master: Any, db: Any, user_id: int, **kwargs):
        super().__init__(master, fg_color=COLOR_BG, corner_radius=0, **kwargs)
        self.db = db
        self.user_id = user_id
        self.active_tab = "All Tasks"

        self._build_header()
        self._build_tabs_and_filters()
        self._build_tasks_container()

        self.refresh()

    def _build_header(self):
        head = ctk.CTkFrame(self, fg_color="transparent")
        head.pack(fill="x", padx=32, pady=(28, 14))

        ctk.CTkLabel(
            head,
            text="Tasks & Assignments",
            font=FONT_HEADING_LG,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            head,
            text="Track assignments, project milestones, and homework deadlines with urgency prioritization.",
            font=FONT_BODY,
            text_color=COLOR_TEXT_SECONDARY,
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))

    def _build_tabs_and_filters(self):
        filter_card = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=10,
                                  border_width=1, border_color=COLOR_BORDER)
        filter_card.pack(fill="x", padx=32, pady=(0, 20))

        # Row 1: Segmented Tabs + Add Task Button
        top_row = ctk.CTkFrame(filter_card, fg_color="transparent")
        top_row.pack(fill="x", padx=16, pady=(14, 10))

        tabs = ["All Tasks", "Pending", "In Progress", "Completed", "Overdue"]
        self.tab_selector = ctk.CTkSegmentedButton(
            top_row,
            values=tabs,
            font=FONT_BODY_SM,
            height=34,
            command=self._on_tab_click
        )
        self.tab_selector.set("All Tasks")
        self.tab_selector.pack(side="left")

        plus_icon = load_icon("plus", size=(16, 16))
        PrimaryButton(
            top_row,
            text="Add Task",
            icon=plus_icon,
            height=34,
            width=130,
            command=self._on_add_task
        ).pack(side="right")

        # Row 2: Search, Subject Filter, Priority Filter, Sort
        bottom_row = ctk.CTkFrame(filter_card, fg_color="transparent")
        bottom_row.pack(fill="x", padx=16, pady=(0, 14))

        # Search Entry
        self.search_entry = ctk.CTkEntry(
            bottom_row,
            placeholder_text="Search tasks...",
            font=FONT_BODY_SM,
            height=32,
            width=220,
            fg_color=COLOR_CARD_SECONDARY,
            border_color=COLOR_BORDER,
            border_width=1,
            text_color=COLOR_TEXT_PRIMARY
        )
        self.search_entry.pack(side="left", padx=(0, 12))
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh(update_dropdown=False))

        # Subject Filter
        self.subject_menu = ctk.CTkOptionMenu(
            bottom_row,
            values=["All Subjects"],
            font=FONT_BODY_SM,
            height=32,
            width=170,
            command=lambda _: self.refresh(update_dropdown=False)
        )
        self.subject_menu.pack(side="left", padx=(0, 12))

        # Priority Filter
        self.priority_menu = ctk.CTkOptionMenu(
            bottom_row,
            values=["All Priorities", "High", "Medium", "Low"],
            font=FONT_BODY_SM,
            height=32,
            width=140,
            command=lambda _: self.refresh(update_dropdown=False)
        )
        self.priority_menu.pack(side="left", padx=(0, 12))

        # Sort By
        self.sort_menu = ctk.CTkOptionMenu(
            bottom_row,
            values=["Sort: Due Date", "Sort: Priority", "Sort: Newest"],
            font=FONT_BODY_SM,
            height=32,
            width=140,
            command=lambda _: self.refresh(update_dropdown=False)
        )
        self.sort_menu.pack(side="left")

    def _build_tasks_container(self):
        self.tasks_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tasks_frame.pack(fill="both", expand=True, padx=32, pady=(0, 28))

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

    def _on_tab_click(self, selected_tab: str):
        self.active_tab = selected_tab
        self.refresh(update_dropdown=False)

    def refresh(self, update_dropdown: bool = True):
        if update_dropdown:
            self._update_subject_dropdown()

        for w in self.tasks_frame.winfo_children():
            w.destroy()

        # Status filter
        status_filter = None
        if self.active_tab == "Pending":
            status_filter = "Pending"
        elif self.active_tab == "In Progress":
            status_filter = "In Progress"
        elif self.active_tab == "Completed":
            status_filter = "Completed"
        elif self.active_tab == "Overdue":
            status_filter = "overdue"

        # Subject filter
        sub_label = self.subject_menu.get()
        subject_id = self.subject_map.get(sub_label, None) if hasattr(self, "subject_map") else None

        # Priority filter
        prio_label = self.priority_menu.get()
        priority_filter = None if prio_label == "All Priorities" else prio_label

        # Sort by
        sort_sel = self.sort_menu.get()
        sort_by = "due_date"
        if "Priority" in sort_sel:
            sort_by = "priority"
        elif "Newest" in sort_sel:
            sort_by = "created"

        search = self.search_entry.get().strip() if hasattr(self, "search_entry") else ""

        tasks = self.db.get_tasks(
            user_id=self.user_id,
            status_filter=status_filter,
            subject_id=subject_id,
            priority_filter=priority_filter,
            search=search,
            sort_by=sort_by
        )

        if not tasks:
            empty_card = ctk.CTkFrame(self.tasks_frame, fg_color=COLOR_CARD,
                                     corner_radius=CARD_RADIUS, border_width=1,
                                     border_color=COLOR_BORDER)
            empty_card.pack(fill="x", pady=20, ipady=30)

            msg = "No tasks found matching your filters." if (search or priority_filter or subject_id) else "No tasks in this section."
            ctk.CTkLabel(
                empty_card,
                text=f"📋  {msg}",
                font=FONT_HEADING_MD,
                text_color=COLOR_TEXT_PRIMARY
            ).pack(pady=(10, 4))

            ctk.CTkLabel(
                empty_card,
                text="Create academic tasks to track deadlines and stay organized.",
                font=FONT_BODY,
                text_color=COLOR_TEXT_SECONDARY
            ).pack(pady=(0, 16))

            PrimaryButton(
                empty_card,
                text="+ Create New Task",
                width=170,
                command=self._on_add_task
            ).pack()
            return

        for task in tasks:
            card = self._create_task_card(self.tasks_frame, task)
            card.pack(fill="x", pady=5)

    def _create_task_card(self, parent: Any, task: Dict[str, Any]) -> ctk.CTkFrame:
        card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_CARD,
            corner_radius=CARD_RADIUS,
            border_width=1,
            border_color=COLOR_BORDER
        )
        card.columnconfigure(1, weight=1)

        # Subject color indicator
        sub_color = task.get("subject_color") or "#7667F8"
        bar = ctk.CTkFrame(card, width=5, fg_color=sub_color, corner_radius=2)
        bar.pack(side="left", fill="y", padx=(8, 12), pady=8)

        # Content column
        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(side="left", fill="both", expand=True, pady=12)

        # Header Row: Title + Status + Priority
        head_row = ctk.CTkFrame(body, fg_color="transparent")
        head_row.pack(fill="x", anchor="w")

        title_text = task["title"]
        if task["status"] == "Completed":
            t_lbl = ctk.CTkLabel(head_row, text=f"✓  {title_text}", font=FONT_HEADING_MD,
                                 text_color=COLOR_SECONDARY, anchor="w")
        else:
            t_lbl = ctk.CTkLabel(head_row, text=title_text, font=FONT_HEADING_MD,
                                 text_color=COLOR_TEXT_PRIMARY, anchor="w")
        t_lbl.pack(side="left")

        # Priority Tag
        prio = task.get("priority", "Medium")
        if prio == "High":
            p_fg = ("#FEE2E2", "#451B1F")
            p_tc = COLOR_DANGER
        elif prio == "Medium":
            p_fg = ("#FEF3C7", "#423215")
            p_tc = COLOR_WARNING
        else:
            p_fg = ("#DCFCE7", "#173B2E")
            p_tc = COLOR_SECONDARY

        p_badge = ctk.CTkFrame(head_row, fg_color=p_fg, corner_radius=6)
        p_badge.pack(side="left", padx=(10, 0))
        ctk.CTkLabel(p_badge, text=prio.upper(), font=("Segoe UI", 10, "bold"),
                     text_color=p_tc).pack(padx=8, pady=2)

        # Meta row: Subject, Due Date, Days Left
        meta_row = ctk.CTkFrame(body, fg_color="transparent")
        meta_row.pack(fill="x", anchor="w", pady=(4, 0))

        sub_name = task.get("subject_name") or "General"
        due_formatted = format_date_display(task["due_date"])
        days_count, days_text, urgency = calculate_days_left(task["due_date"])

        urgency_prefix = "⚠️ " if urgency in ("urgent", "past") else ""
        meta_text = f"📚 {sub_name}   •   📅 Due: {due_formatted}   •   {urgency_prefix}{days_text}"
        meta_color = COLOR_DANGER if urgency == "past" else (COLOR_WARNING if urgency == "urgent" else COLOR_TEXT_MUTED)

        ctk.CTkLabel(
            meta_row,
            text=meta_text,
            font=FONT_BODY_SM,
            text_color=meta_color,
            anchor="w"
        ).pack(side="left")

        # Description if present
        if task.get("description"):
            ctk.CTkLabel(
                body,
                text=task["description"],
                font=FONT_BODY_SM,
                text_color=COLOR_TEXT_SECONDARY,
                anchor="w",
                wraplength=600,
                justify="left"
            ).pack(anchor="w", pady=(4, 0))

        # Right Action Column: Status changer dropdown + Edit/Delete
        actions = ctk.CTkFrame(card, fg_color="transparent")
        actions.pack(side="right", padx=16, pady=12)

        status_menu = ctk.CTkOptionMenu(
            actions,
            values=["Pending", "In Progress", "Completed"],
            font=FONT_CAPTION,
            width=110,
            height=30,
            command=lambda new_st, tid=task["id"]: self._on_status_change(tid, new_st)
        )
        status_menu.set(task["status"])
        status_menu.pack(side="left", padx=(0, 10))

        edit_icon = load_icon("edit", size=(14, 14))
        delete_icon = load_icon("delete", size=(14, 14))

        IconButton(actions, icon=edit_icon, size=30,
                   command=lambda t=task: self._on_edit_task(t)).pack(side="left", padx=(0, 6))
        IconButton(actions, icon=delete_icon, is_danger=True, size=30,
                   command=lambda t=task: self._on_delete_task(t)).pack(side="left")

        return card

    def _on_status_change(self, task_id: int, new_status: str):
        self.db.update_task_status(task_id, self.user_id, new_status)
        self.refresh(update_dropdown=False)

    def _on_add_task(self):
        TaskDialog(self.winfo_toplevel(), self.db, self.user_id,
                   on_save_callback=lambda: self.refresh(update_dropdown=True))

    def _on_edit_task(self, task: Dict[str, Any]):
        TaskDialog(self.winfo_toplevel(), self.db, self.user_id, task=task,
                   on_save_callback=lambda: self.refresh(update_dropdown=False))

    def _on_delete_task(self, task: Dict[str, Any]):
        def confirm():
            self.db.delete_task(task["id"], self.user_id)
            self.refresh(update_dropdown=False)

        ConfirmDialog(
            parent=self.winfo_toplevel(),
            title="Delete Task?",
            message=f"Are you sure you want to delete '{task['title']}'?",
            confirm_text="Delete Task",
            is_danger=True,
            on_confirm=confirm
        )
