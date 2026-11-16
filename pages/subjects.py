"""
StudySync - Smart Student Study Planner
Subjects Page - Manage Courses, Target Hours, and Syllabus Progress
"""

from typing import Any, Callable, Dict, Optional
import customtkinter as ctk

from utils.theme import (
    COLOR_BG, COLOR_CARD, COLOR_CARD_SECONDARY, COLOR_BORDER,
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_DANGER,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    FONT_HEADING_LG, FONT_HEADING_MD, FONT_SUBHEADING, FONT_BODY,
    FONT_BODY_BOLD, FONT_BODY_SM, FONT_CAPTION, CARD_RADIUS,
    BUTTON_RADIUS
)
from utils.helpers import load_icon
from components.buttons import PrimaryButton, SecondaryButton, IconButton
from components.dialogs import SubjectDialog, ConfirmDialog


class SubjectsPage(ctk.CTkScrollableFrame):
    """
    My Subjects View:
    - Searchable course list
    - Add New Subject button
    - Visual course cards with syllabus progress bars, logged study hours, and management actions
    """
    def __init__(self, master: Any, db: Any, user_id: int, **kwargs):
        super().__init__(master, fg_color=COLOR_BG, corner_radius=0, **kwargs)
        self.db = db
        self.user_id = user_id

        self._build_header()
        self._build_toolbar()
        self._build_cards_container()

        self.refresh()

    def _build_header(self):
        head = ctk.CTkFrame(self, fg_color="transparent")
        head.pack(fill="x", padx=32, pady=(28, 14))

        ctk.CTkLabel(
            head,
            text="My Subjects",
            font=FONT_HEADING_LG,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            head,
            text="Organize your academic learning, track syllabus completion, and monitor study quotas.",
            font=FONT_BODY,
            text_color=COLOR_TEXT_SECONDARY,
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))

    def _build_toolbar(self):
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=32, pady=(0, 20))

        # Search Bar
        search_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        search_frame.pack(side="left", fill="x", expand=True, padx=(0, 16))

        search_icon = load_icon("search", size=(16, 16))
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search subjects by name or code (e.g. CS201)...",
            font=FONT_BODY,
            height=38,
            corner_radius=BUTTON_RADIUS,
            fg_color=COLOR_CARD,
            border_color=COLOR_BORDER,
            border_width=1,
            text_color=COLOR_TEXT_PRIMARY
        )
        self.search_entry.pack(fill="x")
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh())

        # Add Subject Button
        plus_icon = load_icon("plus", size=(16, 16))
        PrimaryButton(
            toolbar,
            text="Add Subject",
            icon=plus_icon,
            height=38,
            width=140,
            command=self._on_add_subject
        ).pack(side="right")

    def _build_cards_container(self):
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(fill="both", expand=True, padx=32, pady=(0, 28))

    def refresh(self):
        for w in self.cards_frame.winfo_children():
            w.destroy()

        search_term = self.search_entry.get().strip() if hasattr(self, "search_entry") else ""
        subjects = self.db.get_subjects(self.user_id, search_term=search_term)

        if not subjects:
            empty_card = ctk.CTkFrame(self.cards_frame, fg_color=COLOR_CARD,
                                     corner_radius=CARD_RADIUS, border_width=1,
                                     border_color=COLOR_BORDER)
            empty_card.pack(fill="x", pady=20, ipady=30)

            msg = "No subjects matching your search." if search_term else "You haven't added any subjects yet."
            ctk.CTkLabel(
                empty_card,
                text=f"📚  {msg}",
                font=FONT_HEADING_MD,
                text_color=COLOR_TEXT_PRIMARY
            ).pack(pady=(10, 4))

            ctk.CTkLabel(
                empty_card,
                text="Create subjects to organize your study sessions, assignments, and exams.",
                font=FONT_BODY,
                text_color=COLOR_TEXT_SECONDARY
            ).pack(pady=(0, 16))

            if not search_term:
                PrimaryButton(
                    empty_card,
                    text="+ Add First Subject",
                    width=170,
                    command=self._on_add_subject
                ).pack()
            return

        # Render 2-column card grid
        self.cards_frame.columnconfigure((0, 1), weight=1, uniform="subject_col")

        for idx, sub in enumerate(subjects):
            row = idx // 2
            col = idx % 2
            card = self._create_subject_card(self.cards_frame, sub)
            card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)

    def _create_subject_card(self, parent: Any, sub: Dict[str, Any]) -> ctk.CTkFrame:
        card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_CARD,
            corner_radius=CARD_RADIUS,
            border_width=1,
            border_color=COLOR_BORDER
        )
        card.columnconfigure(0, weight=1)

        # Top Bar: Code Badge + Action Buttons (Edit, Delete)
        top_bar = ctk.CTkFrame(card, fg_color="transparent")
        top_bar.pack(fill="x", padx=18, pady=(16, 8))

        # Subject Code Badge
        accent_color = sub.get("color") or "#7667F8"
        code_badge = ctk.CTkFrame(top_bar, fg_color=("E0E7FF", "#222544"), corner_radius=6)
        code_badge.pack(side="left")

        ctk.CTkLabel(
            code_badge,
            text=sub.get("code") or "COURSE",
            font=("Segoe UI", 11, "bold"),
            text_color=accent_color
        ).pack(padx=8, pady=3)

        # Semester pill
        sem_lbl = ctk.CTkLabel(
            top_bar,
            text=sub.get("semester", "Semester 4"),
            font=FONT_CAPTION,
            text_color=COLOR_TEXT_MUTED
        )
        sem_lbl.pack(side="left", padx=(10, 0))

        # Edit and Delete icon buttons
        edit_icon = load_icon("edit", size=(14, 14))
        delete_icon = load_icon("delete", size=(14, 14))

        IconButton(top_bar, icon=delete_icon, is_danger=True, size=28,
                   command=lambda s=sub: self._on_delete_subject(s)).pack(side="right", padx=(4, 0))
        IconButton(top_bar, icon=edit_icon, size=28,
                   command=lambda s=sub: self._on_edit_subject(s)).pack(side="right")

        # Subject Name
        name_lbl = ctk.CTkLabel(
            card,
            text=sub["name"],
            font=FONT_HEADING_MD,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        name_lbl.pack(fill="x", padx=18, pady=(0, 4))

        # Description
        desc_text = sub.get("description") or "No description provided."
        desc_lbl = ctk.CTkLabel(
            card,
            text=desc_text,
            font=FONT_BODY_SM,
            text_color=COLOR_TEXT_SECONDARY,
            anchor="w",
            wraplength=380,
            justify="left"
        )
        desc_lbl.pack(fill="x", padx=18, pady=(0, 14))

        # Divider
        ctk.CTkFrame(card, height=1, fg_color=COLOR_BORDER).pack(fill="x", padx=18, pady=(0, 12))

        # Progress & Study Hours Info
        meta_row = ctk.CTkFrame(card, fg_color="transparent")
        meta_row.pack(fill="x", padx=18, pady=(0, 6))

        syl_prog = float(sub.get("syllabus_progress", 0.0))
        ctk.CTkLabel(
            meta_row,
            text=f"Syllabus: {int(syl_prog)}% Completed",
            font=FONT_BODY_BOLD,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        ).pack(side="left")

        logged_h = float(sub.get("logged_hours", 0.0))
        target_h = float(sub.get("target_hours", 40.0))
        ctk.CTkLabel(
            meta_row,
            text=f"Logged: {logged_h:.1f} / {target_h:.0f} hrs",
            font=FONT_BODY_SM,
            text_color=COLOR_TEXT_MUTED,
            anchor="e"
        ).pack(side="right")

        # Syllabus Progress Bar
        prog_bar = ctk.CTkProgressBar(
            card,
            height=8,
            corner_radius=4,
            fg_color=COLOR_CARD_SECONDARY,
            progress_color=COLOR_SECONDARY if syl_prog >= 80 else COLOR_PRIMARY
        )
        prog_bar.pack(fill="x", padx=18, pady=(0, 18))
        prog_bar.set(min(1.0, max(0.0, syl_prog / 100.0)))

        return card

    def _on_add_subject(self):
        SubjectDialog(self.winfo_toplevel(), self.db, self.user_id, on_save_callback=self.refresh)

    def _on_edit_subject(self, sub: Dict[str, Any]):
        SubjectDialog(self.winfo_toplevel(), self.db, self.user_id, subject=sub, on_save_callback=self.refresh)

    def _on_delete_subject(self, sub: Dict[str, Any]):
        def confirm():
            self.db.delete_subject(sub["id"], self.user_id)
            self.refresh()

        ConfirmDialog(
            parent=self.winfo_toplevel(),
            title="Delete Subject?",
            message=f"Are you sure you want to delete '{sub['name']}'? All associated study sessions, tasks, and exams will also be removed.",
            confirm_text="Delete Subject",
            is_danger=True,
            on_confirm=confirm
        )
