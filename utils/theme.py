"""
StudySync - Smart Student Study Planner
Theme and Design System Constants
"""

import customtkinter as ctk

# Color Palette (Light, Dark) tuples for seamless CustomTkinter theme toggling
COLOR_BG = ("#F4F6FC", "#101522")
COLOR_SIDEBAR = ("#FFFFFF", "#0B1020")
COLOR_CARD = ("#FFFFFF", "#1A2233")
COLOR_CARD_SECONDARY = ("#EDF2F9", "#202B3D")
COLOR_CARD_HOVER = ("#E8EEF8", "#242F44")

# Accent Colors
COLOR_PRIMARY = ("#7667F8", "#7667F8")
COLOR_PRIMARY_HOVER = ("#6151E8", "#6151E8")
COLOR_PRIMARY_LIGHT = ("#EBE9FE", "#26224D")

COLOR_SECONDARY = ("#2BAE76", "#38C98B")
COLOR_SECONDARY_HOVER = ("#239464", "#2FB079")
COLOR_SECONDARY_LIGHT = ("#DCFCE7", "#173B2E")

COLOR_WARNING = ("#D89B32", "#F5B84B")
COLOR_WARNING_HOVER = ("#C18825", "#DE9F35")
COLOR_WARNING_LIGHT = ("#FEF3C7", "#3D3016")

COLOR_DANGER = ("#E24B56", "#F16B75")
COLOR_DANGER_HOVER = ("#C83742", "#D8535D")
COLOR_DANGER_LIGHT = ("#FEE2E2", "#431C21")

COLOR_INFO = ("#3B82F6", "#60A5FA")
COLOR_INFO_LIGHT = ("#DBEAFE", "#1E2E4A")

# Text Colors
COLOR_TEXT_PRIMARY = ("#101522", "#F4F6FC")
COLOR_TEXT_SECONDARY = ("#556177", "#929CAF")
COLOR_TEXT_MUTED = ("#8390A5", "#677389")

# Structural & Controls
COLOR_BORDER = ("#D5DDE9", "#2A3447")
COLOR_BORDER_LIGHT = ("#E5EBF5", "#354259")
COLOR_INPUT_BG = ("#F8FAFD", "#141C2E")
COLOR_INPUT_BORDER = ("#CCD6E4", "#2A3447")

# Navigation Specific
COLOR_NAV_ACTIVE = ("#EFEFFD", "#26224D")
COLOR_NAV_ACTIVE_TEXT = ("#7667F8", "#7667F8")
COLOR_NAV_HOVER = ("#F3F5FA", "#151C2C")

# Subject Badge Colors (for variety across subjects)
SUBJECT_PALETTE = [
    ("#7667F8", "#9B8FF9"), # Purple
    ("#38C98B", "#4EE2A2"), # Emerald
    ("#3B82F6", "#60A5FA"), # Blue
    ("#F5B84B", "#FCD34D"), # Amber
    ("#EC4899", "#F472B6"), # Pink
    ("#06B6D4", "#22D3EE"), # Cyan
    ("#8B5CF6", "#A78BFA"), # Violet
    ("#F97316", "#FB923C"), # Orange
]

# Typography
FONT_FAMILY = "Segoe UI"
FONT_HEADING_XL = (FONT_FAMILY, 24, "bold")
FONT_HEADING_LG = (FONT_FAMILY, 20, "bold")
FONT_HEADING_MD = (FONT_FAMILY, 16, "bold")
FONT_SUBHEADING = (FONT_FAMILY, 14, "bold")
FONT_BODY = (FONT_FAMILY, 13)
FONT_BODY_BOLD = (FONT_FAMILY, 13, "bold")
FONT_BODY_SM = (FONT_FAMILY, 11)
FONT_CAPTION = (FONT_FAMILY, 10)
FONT_NUMBER_XL = (FONT_FAMILY, 28, "bold")
FONT_NUMBER_LG = (FONT_FAMILY, 22, "bold")
FONT_NUMBER_MD = (FONT_FAMILY, 18, "bold")

# Layout Geometry Constants
SIDEBAR_WIDTH = 250
HEADER_HEIGHT = 70
CARD_RADIUS = 12
BUTTON_RADIUS = 8
INPUT_RADIUS = 8
TAG_RADIUS = 6


class ThemeManager:
    """Manages application-wide theme state and transitions."""
    _current_mode = "Dark"

    @classmethod
    def set_theme(cls, mode: str):
        mode_norm = "Dark" if mode.lower() == "dark" else "Light"
        cls._current_mode = mode_norm
        ctk.set_appearance_mode(mode_norm)

    @classmethod
    def get_theme(cls) -> str:
        return cls._current_mode

    @classmethod
    def is_dark(cls) -> bool:
        return cls._current_mode == "Dark"

    @classmethod
    def get_chart_bg(cls) -> str:
        return "#1A2233" if cls.is_dark() else "#FFFFFF"

    @classmethod
    def get_chart_fg(cls) -> str:
        return "#F4F6FC" if cls.is_dark() else "#101522"

    @classmethod
    def get_chart_grid(cls) -> str:
        return "#2A3447" if cls.is_dark() else "#E2E8F0"

    @classmethod
    def get_chart_secondary(cls) -> str:
        return "#929CAF" if cls.is_dark() else "#64748B"
