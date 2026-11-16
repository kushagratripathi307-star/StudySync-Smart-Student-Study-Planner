"""
StudySync - Smart Student Study Planner
Reusable Button Components
"""

from typing import Optional, Callable, Any
import customtkinter as ctk
from utils.theme import (
    COLOR_PRIMARY, COLOR_PRIMARY_HOVER,
    COLOR_SECONDARY, COLOR_SECONDARY_HOVER,
    COLOR_DANGER, COLOR_DANGER_HOVER,
    COLOR_CARD, COLOR_CARD_HOVER,
    COLOR_BORDER, COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY, FONT_BODY_BOLD,
    BUTTON_RADIUS
)


class PrimaryButton(ctk.CTkButton):
    """Accent colored main action button."""
    def __init__(self, master: Any, text: str, command: Optional[Callable] = None,
                 icon: Optional[ctk.CTkImage] = None, width: int = 140, height: int = 38, **kwargs):
        super().__init__(
            master=master,
            text=text,
            command=command,
            image=icon,
            compound="left",
            font=FONT_BODY_BOLD,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color="#FFFFFF",
            corner_radius=BUTTON_RADIUS,
            width=width,
            height=height,
            cursor="hand2",
            **kwargs
        )


class SecondaryButton(ctk.CTkButton):
    """Subtle neutral action button."""
    def __init__(self, master: Any, text: str, command: Optional[Callable] = None,
                 icon: Optional[ctk.CTkImage] = None, width: int = 130, height: int = 38, **kwargs):
        super().__init__(
            master=master,
            text=text,
            command=command,
            image=icon,
            compound="left",
            font=FONT_BODY_BOLD,
            fg_color=COLOR_CARD,
            hover_color=COLOR_CARD_HOVER,
            border_width=1,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT_PRIMARY,
            corner_radius=BUTTON_RADIUS,
            width=width,
            height=height,
            cursor="hand2",
            **kwargs
        )


class SuccessButton(ctk.CTkButton):
    """Emerald green success button."""
    def __init__(self, master: Any, text: str, command: Optional[Callable] = None,
                 icon: Optional[ctk.CTkImage] = None, width: int = 130, height: int = 38, **kwargs):
        super().__init__(
            master=master,
            text=text,
            command=command,
            image=icon,
            compound="left",
            font=FONT_BODY_BOLD,
            fg_color=COLOR_SECONDARY,
            hover_color=COLOR_SECONDARY_HOVER,
            text_color="#FFFFFF",
            corner_radius=BUTTON_RADIUS,
            width=width,
            height=height,
            cursor="hand2",
            **kwargs
        )


class DangerButton(ctk.CTkButton):
    """Coral red danger/destructive button."""
    def __init__(self, master: Any, text: str, command: Optional[Callable] = None,
                 icon: Optional[ctk.CTkImage] = None, width: int = 130, height: int = 38, **kwargs):
        super().__init__(
            master=master,
            text=text,
            command=command,
            image=icon,
            compound="left",
            font=FONT_BODY_BOLD,
            fg_color=COLOR_DANGER,
            hover_color=COLOR_DANGER_HOVER,
            text_color="#FFFFFF",
            corner_radius=BUTTON_RADIUS,
            width=width,
            height=height,
            cursor="hand2",
            **kwargs
        )


class IconButton(ctk.CTkButton):
    """Compact button for icons (e.g. edit, delete, reload)."""
    def __init__(self, master: Any, icon: ctk.CTkImage, command: Optional[Callable] = None,
                 tooltip: str = "", size: int = 34, is_danger: bool = False, **kwargs):
        fg = ("#FEE2E2", "#451B1F") if is_danger else ("#F1F5F9", "#202B3D")
        hover = ("#FCA5A5", "#6B2129") if is_danger else ("#E2E8F0", "#2D3B52")
        super().__init__(
            master=master,
            text="",
            image=icon,
            command=command,
            width=size,
            height=size,
            corner_radius=6,
            fg_color=fg,
            hover_color=hover,
            border_width=1,
            border_color=COLOR_BORDER,
            cursor="hand2",
            **kwargs
        )
