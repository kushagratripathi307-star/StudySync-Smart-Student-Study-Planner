"""
StudySync - Smart Student Study Planner
Statistics Card Component
"""

from typing import Any, Optional
import customtkinter as ctk
from utils.theme import (
    COLOR_CARD, COLOR_CARD_HOVER, COLOR_BORDER,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    FONT_SUBHEADING, FONT_NUMBER_XL, FONT_BODY_SM,
    CARD_RADIUS
)


class StatCard(ctk.CTkFrame):
    """
    Modern SaaS metric card displaying:
    - Title
    - Numeric stat value
    - Trend or contextual note
    - Styled icon badge
    """
    def __init__(self, master: Any, title: str, value: str,
                 subtitle: str = "", icon: Optional[ctk.CTkImage] = None,
                 accent_color: str = "#7667F8", width: int = 250, height: int = 135,
                 **kwargs):
        super().__init__(
            master=master,
            fg_color=COLOR_CARD,
            corner_radius=CARD_RADIUS,
            border_width=1,
            border_color=COLOR_BORDER,
            width=width,
            height=height,
            **kwargs
        )
        self.grid_propagate(False)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

        # Header: Title + Icon Badge
        self.title_label = ctk.CTkLabel(
            self,
            text=title.upper(),
            font=("Segoe UI", 11, "bold"),
            text_color=COLOR_TEXT_MUTED,
            anchor="w"
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=(18, 5), pady=(16, 0))

        if icon:
            # Icon badge with tinted background
            self.icon_badge = ctk.CTkLabel(
                self,
                text="",
                image=icon,
                width=36,
                height=36,
                fg_color=accent_color,
                corner_radius=8
            )
            self.icon_badge.grid(row=0, column=1, rowspan=2, sticky="ne", padx=(0, 18), pady=(14, 0))

        # Main numeric value
        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=FONT_NUMBER_XL,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        self.value_label.grid(row=1, column=0, sticky="w", padx=(18, 5), pady=(2, 0))

        # Subtitle / trend indicator
        self.sub_label = ctk.CTkLabel(
            self,
            text=subtitle,
            font=FONT_BODY_SM,
            text_color=COLOR_TEXT_SECONDARY,
            anchor="w"
        )
        self.sub_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=(18, 18), pady=(4, 14))

    def update_values(self, value: str, subtitle: Optional[str] = None):
        self.value_label.configure(text=value)
        if subtitle is not None:
            self.sub_label.configure(text=subtitle)
