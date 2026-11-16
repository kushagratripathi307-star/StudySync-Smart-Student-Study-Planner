"""
StudySync - Smart Student Study Planner
Login Page - Professional UI/UX Refined Edition
"""

from typing import Any, Callable
import customtkinter as ctk
from utils.theme import (
    COLOR_BG, COLOR_CARD, COLOR_BORDER, COLOR_PRIMARY,
    COLOR_PRIMARY_HOVER, COLOR_SECONDARY, COLOR_DANGER,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    FONT_HEADING_XL, FONT_HEADING_LG, FONT_HEADING_MD, FONT_SUBHEADING,
    FONT_BODY, FONT_BODY_BOLD, FONT_BODY_SM, FONT_CAPTION,
    CARD_RADIUS, BUTTON_RADIUS
)
from utils.helpers import load_icon
from components.buttons import PrimaryButton, SecondaryButton
from components.forms import FormEntry, FormPasswordEntry


class LoginPage(ctk.CTkFrame):
    """
    Refined, balanced dual-column authentication view:
    - Left column: StudySync branding, description & academic highlights
    - Right column: Sign In form, password toggle, demo account button, register link
    - Engineered for zero clipping and pixel-perfect responsiveness across 1366x768 & 1440x900
    """
    def __init__(self, master: Any, auth_service: Any,
                 on_login_success: Callable[[], None],
                 on_switch_to_register: Callable[[], None], **kwargs):
        super().__init__(master, fg_color=COLOR_BG, **kwargs)
        self.auth_service = auth_service
        self.on_login_success = on_login_success
        self.on_switch_to_register = on_switch_to_register

        self._build_ui()

    def _build_ui(self):
        # Master Center Card (860x520 px: Gold standard sizing for 1366x768 & 1440x900)
        self.center_container = ctk.CTkFrame(
            self,
            fg_color=COLOR_CARD,
            corner_radius=16,
            border_width=1,
            border_color=COLOR_BORDER,
            width=860,
            height=520
        )
        self.center_container.place(relx=0.5, rely=0.5, anchor="center")
        self.center_container.grid_propagate(False)
        self.center_container.pack_propagate(False)

        # 2 Equal-Width Columns Layout
        self.center_container.columnconfigure(0, weight=1, uniform="auth_split")
        self.center_container.columnconfigure(1, weight=1, uniform="auth_split")
        self.center_container.rowconfigure(0, weight=1)

        # -------------------------------------------------------------
        # LEFT COLUMN: Branding & Academic Showcase
        # -------------------------------------------------------------
        hero_card = ctk.CTkFrame(
            self.center_container,
            fg_color=("f1f5fc", "#141C2E"),
            corner_radius=12,
            border_width=1,
            border_color=COLOR_BORDER
        )
        hero_card.grid(row=0, column=0, sticky="nsew", padx=(16, 8), pady=16)
        hero_card.pack_propagate(False)

        # Inner container using sequential vertical packing
        hero_content = ctk.CTkFrame(hero_card, fg_color="transparent")
        hero_content.pack(fill="both", expand=True, padx=22, pady=20)

        # Top Header Row: Logo + App Title & Tagline
        header_row = ctk.CTkFrame(hero_content, fg_color="transparent")
        header_row.pack(fill="x", anchor="w", pady=(0, 12))

        logo_icon = load_icon("logo", size=(44, 44))
        if logo_icon:
            logo_lbl = ctk.CTkLabel(header_row, text="", image=logo_icon)
            logo_lbl.pack(side="left", padx=(0, 12))

        brand_col = ctk.CTkFrame(header_row, fg_color="transparent")
        brand_col.pack(side="left", fill="both")

        title_lbl = ctk.CTkLabel(
            brand_col,
            text="StudySync",
            font=FONT_HEADING_LG,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        title_lbl.pack(anchor="w")

        tag_badge = ctk.CTkFrame(brand_col, fg_color=("E0E7FF", "#222544"), corner_radius=4)
        tag_badge.pack(anchor="w", pady=(2, 0))
        ctk.CTkLabel(
            tag_badge,
            text="SMART STUDENT PLANNER",
            font=("Segoe UI", 9, "bold"),
            text_color=COLOR_PRIMARY
        ).pack(padx=6, pady=2)

        # Welcome Description (Carefully formatted to fit comfortably with wrap)
        desc_lbl = ctk.CTkLabel(
            hero_content,
            text="Your centralized academic command center. Plan daily study sessions, track syllabus quotas, and master deadlines with precision.",
            font=FONT_BODY_SM,
            text_color=COLOR_TEXT_SECONDARY,
            wraplength=340,
            justify="left",
            anchor="w"
        )
        desc_lbl.pack(fill="x", pady=(0, 14))

        # Divider line
        ctk.CTkFrame(hero_content, height=1, fg_color=COLOR_BORDER).pack(fill="x", pady=(0, 14))

        # Feature Highlights List (Clean 4-point bullet set)
        feature_box = ctk.CTkFrame(hero_content, fg_color="transparent")
        feature_box.pack(fill="x", anchor="w", pady=(0, 10))

        features = [
            ("🎯", "Subject & Syllabus Progress Tracker"),
            ("⏱️", "Intelligent Daily Study Timetable"),
            ("📋", "Assignment Priorities & Deadlines"),
            ("⏳", "Live Real-Time Exam Countdowns"),
        ]

        for icon_emoji, text_desc in features:
            f_row = ctk.CTkFrame(feature_box, fg_color="transparent")
            f_row.pack(fill="x", pady=2, anchor="w")

            ctk.CTkLabel(
                f_row,
                text=icon_emoji,
                font=("Segoe UI", 11),
                width=22,
                anchor="w"
            ).pack(side="left")

            ctk.CTkLabel(
                f_row,
                text=text_desc,
                font=FONT_BODY_SM,
                text_color=COLOR_TEXT_SECONDARY,
                anchor="w"
            ).pack(side="left", padx=(4, 0))

        # Academic Edition Footnote
        footnote_lbl = ctk.CTkLabel(
            hero_content,
            text="Academic Production Edition • 2nd Year B.Tech CSE",
            font=FONT_CAPTION,
            text_color=COLOR_TEXT_MUTED,
            anchor="w"
        )
        footnote_lbl.pack(side="bottom", anchor="w", pady=(4, 0))

        # -------------------------------------------------------------
        # RIGHT COLUMN: Sign In Form
        # -------------------------------------------------------------
        form_card = ctk.CTkFrame(self.center_container, fg_color="transparent")
        form_card.grid(row=0, column=1, sticky="nsew", padx=(8, 20), pady=16)
        form_card.pack_propagate(False)

        form_inner = ctk.CTkFrame(form_card, fg_color="transparent")
        form_inner.pack(fill="both", expand=True, padx=14, pady=10)

        # Form Header
        heading_lbl = ctk.CTkLabel(
            form_inner,
            text="Welcome Back",
            font=FONT_HEADING_LG,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        heading_lbl.pack(fill="x", pady=(0, 2))

        subhead_lbl = ctk.CTkLabel(
            form_inner,
            text="Sign in to your student study workspace",
            font=FONT_BODY_SM,
            text_color=COLOR_TEXT_SECONDARY,
            anchor="w"
        )
        subhead_lbl.pack(fill="x", pady=(0, 12))

        # Alert Banner for Validation Errors
        self.alert_box = ctk.CTkFrame(
            form_inner,
            fg_color=("fee2e2", "#451B1F"),
            corner_radius=6,
            border_width=1,
            border_color=COLOR_DANGER
        )
        self.alert_lbl = ctk.CTkLabel(
            self.alert_box,
            text="",
            font=FONT_BODY_SM,
            text_color=COLOR_DANGER,
            anchor="w"
        )
        self.alert_lbl.pack(padx=10, pady=5, fill="x")
        self.alert_box.pack_forget()

        # Input 1: Username or Email with clear visible label
        self.ident_entry = FormEntry(
            form_inner,
            label="Username or Email",
            placeholder="e.g. kushagra or student@college.edu"
        )
        self.ident_entry.pack(fill="x", pady=(0, 8))

        # Input 2: Password with integrated eye toggle
        self.pwd_entry = FormPasswordEntry(
            form_inner,
            label="Password",
            placeholder="Enter your password"
        )
        self.pwd_entry.pack(fill="x", pady=(0, 8))

        # Remember Me Option Row
        opts_row = ctk.CTkFrame(form_inner, fg_color="transparent")
        opts_row.pack(fill="x", pady=(0, 12))

        self.remember_var = ctk.BooleanVar(value=True)
        self.remember_chk = ctk.CTkCheckBox(
            opts_row,
            text="Remember me on this computer",
            variable=self.remember_var,
            font=FONT_BODY_SM,
            fg_color=COLOR_PRIMARY,
            text_color=COLOR_TEXT_SECONDARY,
            corner_radius=4,
            width=18,
            height=18
        )
        self.remember_chk.pack(side="left")

        # Submit Action Button ("Sign In to StudySync")
        self.login_btn = PrimaryButton(
            form_inner,
            text="Sign In to StudySync",
            height=38,
            command=self._handle_login
        )
        self.login_btn.pack(fill="x", pady=(0, 8))

        # Demo Mode Quick Action Button
        sparkles_icon = load_icon("sparkles", size=(16, 16))
        self.demo_btn = SecondaryButton(
            form_inner,
            text="Explore with Demo Account",
            icon=sparkles_icon,
            height=34,
            command=self._handle_demo_login
        )
        self.demo_btn.pack(fill="x", pady=(0, 12))

        # Switch to Register Row
        switch_row = ctk.CTkFrame(form_inner, fg_color="transparent")
        switch_row.pack()

        ctk.CTkLabel(
            switch_row,
            text="Don't have an account?",
            font=FONT_BODY_SM,
            text_color=COLOR_TEXT_SECONDARY
        ).pack(side="left", padx=(0, 6))

        reg_link = ctk.CTkButton(
            switch_row,
            text="Create Account",
            font=FONT_BODY_BOLD,
            text_color=COLOR_PRIMARY,
            fg_color="transparent",
            hover=False,
            cursor="hand2",
            width=80,
            command=self.on_switch_to_register
        )
        reg_link.pack(side="left")

    def _show_error(self, message: str):
        self.alert_lbl.configure(text=f"⚠️  {message}")
        self.alert_box.pack(fill="x", pady=(0, 8), before=self.ident_entry)

    def _clear_error(self):
        self.alert_box.pack_forget()

    def _handle_login(self):
        self._clear_error()
        ident = self.ident_entry.get()
        pwd = self.pwd_entry.get()

        success, msg = self.auth_service.login(ident, pwd)
        if success:
            self.on_login_success()
        else:
            self._show_error(msg)

    def _handle_demo_login(self):
        self._clear_error()
        success, msg = self.auth_service.login_demo_account()
        if success:
            self.on_login_success()
        else:
            self._show_error(msg)
