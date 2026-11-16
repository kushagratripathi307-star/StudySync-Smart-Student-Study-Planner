"""
StudySync - Smart Student Study Planner
Sidebar Navigation Component
"""

from typing import Any, Callable, Dict, Optional
import customtkinter as ctk
from utils.theme import (
    COLOR_SIDEBAR, COLOR_BORDER, COLOR_PRIMARY,
    COLOR_NAV_ACTIVE, COLOR_NAV_ACTIVE_TEXT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    COLOR_CARD, COLOR_CARD_HOVER, FONT_HEADING_MD, FONT_SUBHEADING,
    FONT_BODY, FONT_BODY_BOLD, FONT_BODY_SM, FONT_CAPTION,
    SIDEBAR_WIDTH, BUTTON_RADIUS
)
from utils.helpers import load_icon


class Sidebar(ctk.CTkFrame):
    """
    Fixed left sidebar containing:
    - StudySync branding
    - 7 core navigation items with active indicator
    - Student profile preview & logout action
    """
    def __init__(self, master: Any, current_user: Dict[str, Any],
                 on_navigate: Callable[[str], None], on_logout: Callable[[], None],
                 **kwargs):
        super().__init__(
            master=master,
            width=SIDEBAR_WIDTH,
            fg_color=COLOR_SIDEBAR,
            corner_radius=0,
            border_width=1,
            border_color=COLOR_BORDER,
            **kwargs
        )
        self.pack_propagate(False)
        self.current_user = current_user
        self.on_navigate = on_navigate
        self.on_logout = on_logout
        self.nav_buttons: Dict[str, ctk.CTkButton] = {}
        self.active_page = "Dashboard"

        self._build_header()
        self._build_menu()
        self._build_footer()

    def _build_header(self):
        """Top branding section with Logo and Subtitle."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=18, pady=(22, 16))

        logo_row = ctk.CTkFrame(header_frame, fg_color="transparent")
        logo_row.pack(fill="x", anchor="w")

        logo_icon = load_icon("logo", size=(34, 34))
        if logo_icon:
            logo_lbl = ctk.CTkLabel(logo_row, text="", image=logo_icon)
            logo_lbl.pack(side="left", padx=(0, 10))

        title_col = ctk.CTkFrame(logo_row, fg_color="transparent")
        title_col.pack(side="left", fill="both")

        app_title = ctk.CTkLabel(
            title_col,
            text="StudySync",
            font=FONT_HEADING_MD,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        app_title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            title_col,
            text="Your Academic Companion",
            font=FONT_CAPTION,
            text_color=COLOR_TEXT_MUTED,
            anchor="w"
        )
        subtitle.pack(anchor="w")

        # Subtle divider
        divider = ctk.CTkFrame(self, height=1, fg_color=COLOR_BORDER)
        divider.pack(fill="x", padx=16, pady=(0, 14))

    def _build_menu(self):
        """Main navigation menu with 7 distinct pages."""
        menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        menu_frame.pack(fill="both", expand=True, padx=12, pady=0)

        nav_items = [
            ("Dashboard", "dashboard"),
            ("My Subjects", "subjects"),
            ("Study Planner", "planner"),
            ("Tasks & Assignments", "tasks"),
            ("Exam Countdown", "exams"),
            ("Analytics", "analytics"),
            ("Settings", "settings"),
        ]

        for page_name, icon_name in nav_items:
            icon = load_icon(icon_name, size=(18, 18))
            btn = ctk.CTkButton(
                menu_frame,
                text=f"  {page_name}",
                image=icon,
                compound="left",
                anchor="w",
                font=FONT_BODY_BOLD,
                height=42,
                corner_radius=BUTTON_RADIUS,
                fg_color="transparent",
                hover_color=("e8eef8", "#1A2233"),
                text_color=COLOR_TEXT_SECONDARY,
                command=lambda name=page_name: self._handle_click(name)
            )
            btn.pack(fill="x", pady=3)
            self.nav_buttons[page_name] = btn

        # Set default active
        self.set_active("Dashboard")

    def _build_footer(self):
        """Student profile summary and logout button."""
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(fill="x", side="bottom", padx=14, pady=16)

        # Profile Card
        card = ctk.CTkFrame(
            footer_frame,
            fg_color=COLOR_CARD,
            corner_radius=10,
            border_width=1,
            border_color=COLOR_BORDER
        )
        card.pack(fill="x", pady=(0, 10))

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=10, pady=10)

        user_icon = load_icon("user", size=(28, 28))
        if user_icon:
            avatar = ctk.CTkLabel(inner, text="", image=user_icon)
            avatar.pack(side="left", padx=(0, 10))

        info_col = ctk.CTkFrame(inner, fg_color="transparent")
        info_col.pack(side="left", fill="both", expand=True)

        full_name = self.current_user.get("full_name", "Student") if self.current_user else "Student"
        username = self.current_user.get("username", "student") if self.current_user else "student"

        self.name_label = ctk.CTkLabel(
            info_col,
            text=full_name,
            font=FONT_BODY_BOLD,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        self.name_label.pack(anchor="w")

        self.role_label = ctk.CTkLabel(
            info_col,
            text=f"@{username}",
            font=FONT_CAPTION,
            text_color=COLOR_TEXT_MUTED,
            anchor="w"
        )
        self.role_label.pack(anchor="w")

        # Logout button
        logout_icon = load_icon("logout", size=(16, 16))
        logout_btn = ctk.CTkButton(
            footer_frame,
            text="  Log Out",
            image=logout_icon,
            compound="left",
            font=FONT_BODY_BOLD,
            height=36,
            corner_radius=BUTTON_RADIUS,
            fg_color=("fee2e2", "#35191C"),
            hover_color=("fecaca", "#4F1F24"),
            text_color=("#dc2626", "#F16B75"),
            command=self.on_logout
        )
        logout_btn.pack(fill="x")

    def _handle_click(self, page_name: str):
        self.set_active(page_name)
        self.on_navigate(page_name)

    def set_active(self, page_name: str):
        """Highlights the currently active navigation item."""
        self.active_page = page_name
        for name, btn in self.nav_buttons.items():
            if name == page_name:
                btn.configure(
                    fg_color=COLOR_NAV_ACTIVE,
                    text_color=COLOR_NAV_ACTIVE_TEXT
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=COLOR_TEXT_SECONDARY
                )

    def update_user_info(self, user: Dict[str, Any]):
        """Refreshes the profile footer card when user updates profile."""
        self.current_user = user
        if hasattr(self, "name_label") and hasattr(self, "role_label"):
            full_name = user.get("full_name", "Student")
            username = user.get("username", "student")
            self.name_label.configure(text=full_name)
            self.role_label.configure(text=f"@{username}")
