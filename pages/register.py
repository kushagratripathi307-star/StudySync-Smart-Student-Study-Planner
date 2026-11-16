"""
StudySync - Smart Student Study Planner
Registration Page - Professional UI/UX Refined Edition
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


class RegisterPage(ctk.CTkFrame):
    """
    Refined, balanced registration interface:
    - Left column: StudySync branding & benefits
    - Right column: Clean registration inputs with validation
    - Fits within 1366x768 and 1440x900 screens without clipping
    """
    def __init__(self, master: Any, auth_service: Any,
                 on_register_success: Callable[[], None],
                 on_switch_to_login: Callable[[], None], **kwargs):
        super().__init__(master, fg_color=COLOR_BG, **kwargs)
        self.auth_service = auth_service
        self.on_register_success = on_register_success
        self.on_switch_to_login = on_switch_to_login

        self._build_ui()

    def _build_ui(self):
        # Master Card Container (900x580 px)
        self.center_container = ctk.CTkFrame(
            self,
            fg_color=COLOR_CARD,
            corner_radius=16,
            border_width=1,
            border_color=COLOR_BORDER,
            width=900,
            height=580
        )
        self.center_container.place(relx=0.5, rely=0.5, anchor="center")
        self.center_container.grid_propagate(False)
        self.center_container.pack_propagate(False)

        # 2 Equal-Width Columns Layout
        self.center_container.columnconfigure(0, weight=1, uniform="reg_split")
        self.center_container.columnconfigure(1, weight=1, uniform="reg_split")
        self.center_container.rowconfigure(0, weight=1)

        # -------------------------------------------------------------
        # LEFT COLUMN: Branding & Perks
        # -------------------------------------------------------------
        hero_card = ctk.CTkFrame(
            self.center_container,
            fg_color=("f1f5fc", "#141C2E"),
            corner_radius=12,
            border_width=1,
            border_color=COLOR_BORDER
        )
        hero_card.grid(row=0, column=0, sticky="nsew", padx=(18, 10), pady=18)
        hero_card.pack_propagate(False)

        hero_content = ctk.CTkFrame(hero_card, fg_color="transparent")
        hero_content.pack(fill="both", expand=True, padx=24, pady=24)

        logo_icon = load_icon("logo", size=(52, 52))
        if logo_icon:
            logo_lbl = ctk.CTkLabel(hero_content, text="", image=logo_icon)
            logo_lbl.pack(anchor="w", pady=(0, 10))

        title_lbl = ctk.CTkLabel(
            hero_content,
            text="StudySync",
            font=FONT_HEADING_XL,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        title_lbl.pack(fill="x", pady=(0, 2))

        tag_frame = ctk.CTkFrame(hero_content, fg_color=("E0E7FF", "#222544"), corner_radius=6)
        tag_frame.pack(anchor="w", pady=(0, 12))
        ctk.CTkLabel(
            tag_frame,
            text="JOIN THE PRODUCTIVE COMMUNITY",
            font=("Segoe UI", 10, "bold"),
            text_color=COLOR_PRIMARY
        ).pack(padx=8, pady=3)

        desc_lbl = ctk.CTkLabel(
            hero_content,
            text="Create your personalized student profile and take total command of your university coursework and routines.",
            font=FONT_BODY,
            text_color=COLOR_TEXT_SECONDARY,
            wraplength=340,
            justify="left",
            anchor="w"
        )
        desc_lbl.pack(fill="x", pady=(0, 16))

        ctk.CTkFrame(hero_content, height=1, fg_color=COLOR_BORDER).pack(fill="x", pady=(0, 14))

        perks = [
            ("⚡", "Instant timetable & schedule generation"),
            ("📈", "Dynamic weekly & monthly analytics"),
            ("🛡️", "Encrypted local SQLite3 persistence"),
            ("🔔", "Never miss assignment or exam deadlines"),
        ]

        for emoji_icon, perk_text in perks:
            row = ctk.CTkFrame(hero_content, fg_color="transparent")
            row.pack(fill="x", pady=2, anchor="w")

            ctk.CTkLabel(row, text=emoji_icon, font=("Segoe UI", 12), width=24, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=perk_text, font=FONT_BODY_SM, text_color=COLOR_TEXT_SECONDARY, anchor="w").pack(side="left", padx=(4, 0))

        footnote_lbl = ctk.CTkLabel(
            hero_content,
            text="Academic Production Edition • B.Tech CSE",
            font=FONT_CAPTION,
            text_color=COLOR_TEXT_MUTED,
            anchor="w"
        )
        footnote_lbl.pack(side="bottom", anchor="w", pady=(6, 0))

        # -------------------------------------------------------------
        # RIGHT COLUMN: Registration Form
        # -------------------------------------------------------------
        form_card = ctk.CTkFrame(self.center_container, fg_color="transparent")
        form_card.grid(row=0, column=1, sticky="nsew", padx=(10, 24), pady=20)
        form_card.pack_propagate(False)

        form_inner = ctk.CTkFrame(form_card, fg_color="transparent")
        form_inner.pack(fill="both", expand=True, padx=12, pady=6)

        heading_lbl = ctk.CTkLabel(
            form_inner,
            text="Create Account",
            font=FONT_HEADING_LG,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        heading_lbl.pack(fill="x", pady=(0, 2))

        subhead_lbl = ctk.CTkLabel(
            form_inner,
            text="Sign up for free to start planning your studies",
            font=FONT_BODY,
            text_color=COLOR_TEXT_SECONDARY,
            anchor="w"
        )
        subhead_lbl.pack(fill="x", pady=(0, 10))

        # Alert Banner
        self.alert_box = ctk.CTkFrame(
            form_inner,
            fg_color=("fee2e2", "#451B1F"),
            corner_radius=8,
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
        self.alert_lbl.pack(padx=12, pady=5, fill="x")
        self.alert_box.pack_forget()

        # Input Fields with consistent spacing
        self.name_entry = FormEntry(form_inner, label="Full Name", placeholder="e.g. Kushagra Verma")
        self.name_entry.pack(fill="x", pady=(0, 6))

        self.email_entry = FormEntry(form_inner, label="Email Address", placeholder="e.g. kushagra@college.edu")
        self.email_entry.pack(fill="x", pady=(0, 6))

        self.username_entry = FormEntry(form_inner, label="Username", placeholder="e.g. kushagra")
        self.username_entry.pack(fill="x", pady=(0, 6))

        self.pwd_entry = FormPasswordEntry(form_inner, label="Password", placeholder="At least 6 characters")
        self.pwd_entry.pack(fill="x", pady=(0, 6))

        self.conf_pwd_entry = FormPasswordEntry(form_inner, label="Confirm Password", placeholder="Re-enter password")
        self.conf_pwd_entry.pack(fill="x", pady=(0, 12))

        # Submit Button
        self.register_btn = PrimaryButton(
            form_inner,
            text="Create My Account",
            height=38,
            command=self._handle_register
        )
        self.register_btn.pack(fill="x", pady=(0, 10))

        # Switch to Login
        switch_row = ctk.CTkFrame(form_inner, fg_color="transparent")
        switch_row.pack(pady=(2, 0))

        ctk.CTkLabel(
            switch_row,
            text="Already have an account?",
            font=FONT_BODY_SM,
            text_color=COLOR_TEXT_SECONDARY
        ).pack(side="left", padx=(0, 6))

        login_link = ctk.CTkButton(
            switch_row,
            text="Sign In",
            font=FONT_BODY_BOLD,
            text_color=COLOR_PRIMARY,
            fg_color="transparent",
            hover=False,
            cursor="hand2",
            width=60,
            command=self.on_switch_to_login
        )
        login_link.pack(side="left")

    def _show_error(self, message: str):
        self.alert_lbl.configure(text=f"⚠️  {message}")
        self.alert_box.pack(fill="x", pady=(0, 8), before=self.name_entry)

    def _clear_error(self):
        self.alert_box.pack_forget()

    def _handle_register(self):
        self._clear_error()
        name = self.name_entry.get()
        email = self.email_entry.get()
        username = self.username_entry.get()
        pwd = self.pwd_entry.get()
        conf_pwd = self.conf_pwd_entry.get()

        success, msg = self.auth_service.register(
            full_name=name,
            email=email,
            username=username,
            password=pwd,
            confirm_password=conf_pwd
        )
        if success:
            self.on_register_success()
        else:
            self._show_error(msg)
