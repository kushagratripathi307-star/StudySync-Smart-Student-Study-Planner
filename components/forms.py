"""
StudySync - Smart Student Study Planner
Reusable Form Inputs & Controls
"""

from typing import Any, Optional, List, Callable
from datetime import datetime, date
import customtkinter as ctk
from utils.theme import (
    COLOR_INPUT_BG, COLOR_INPUT_BORDER, COLOR_PRIMARY,
    COLOR_BORDER, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY,
    COLOR_TEXT_MUTED, COLOR_DANGER, FONT_BODY, FONT_BODY_BOLD,
    FONT_BODY_SM, FONT_CAPTION, INPUT_RADIUS
)
from utils.helpers import load_icon


class FormEntry(ctk.CTkFrame):
    """Clean labeled text input field."""
    def __init__(self, master: Any, label: str, placeholder: str = "",
                 initial_value: str = "", width: int = 320, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.columnconfigure(0, weight=1)

        self.lbl = ctk.CTkLabel(
            self,
            text=label,
            font=FONT_BODY_BOLD,
            text_color=COLOR_TEXT_SECONDARY,
            anchor="w"
        )
        self.lbl.grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            font=FONT_BODY,
            fg_color=COLOR_INPUT_BG,
            border_color=COLOR_INPUT_BORDER,
            border_width=1,
            corner_radius=INPUT_RADIUS,
            height=38,
            width=width,
            text_color=COLOR_TEXT_PRIMARY
        )
        self.entry.grid(row=1, column=0, sticky="ew")

        if initial_value:
            self.entry.insert(0, str(initial_value))

        self.error_label = ctk.CTkLabel(
            self,
            text="",
            font=FONT_CAPTION,
            text_color=COLOR_DANGER,
            anchor="w"
        )
        self.error_label.grid(row=2, column=0, sticky="w", pady=(2, 0))
        self.error_label.grid_remove()

    def get(self) -> str:
        return self.entry.get().strip()

    def set(self, text: str):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(text))

    def show_error(self, message: str):
        self.error_label.configure(text=message)
        self.error_label.grid()
        self.entry.configure(border_color=COLOR_DANGER)

    def clear_error(self):
        self.error_label.configure(text="")
        self.error_label.grid_remove()
        self.entry.configure(border_color=COLOR_INPUT_BORDER)


class FormPasswordEntry(ctk.CTkFrame):
    """Labeled password input with seamlessly integrated show/hide toggle."""
    def __init__(self, master: Any, label: str, placeholder: str = "••••••••",
                 width: int = 320, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.columnconfigure(0, weight=1)
        self.show_password = False

        self.lbl = ctk.CTkLabel(
            self,
            text=label,
            font=FONT_BODY_BOLD,
            text_color=COLOR_TEXT_SECONDARY,
            anchor="w"
        )
        self.lbl.grid(row=0, column=0, sticky="w", pady=(0, 4))

        # Input container matches FormEntry dimensions and borders exactly
        self.input_container = ctk.CTkFrame(
            self,
            fg_color=COLOR_INPUT_BG,
            border_color=COLOR_INPUT_BORDER,
            border_width=1,
            corner_radius=INPUT_RADIUS,
            height=38,
            width=width
        )
        self.input_container.grid(row=1, column=0, sticky="ew")
        self.input_container.pack_propagate(False)

        self.entry = ctk.CTkEntry(
            self.input_container,
            placeholder_text=placeholder,
            font=FONT_BODY,
            show="•",
            fg_color="transparent",
            border_width=0,
            corner_radius=0,
            height=36,
            text_color=COLOR_TEXT_PRIMARY
        )
        self.entry.pack(side="left", fill="both", expand=True, padx=(12, 0))

        self.toggle_btn = ctk.CTkButton(
            self.input_container,
            text="👁",
            font=("Segoe UI", 12),
            width=32,
            height=32,
            fg_color="transparent",
            hover=False,
            corner_radius=6,
            text_color=COLOR_TEXT_SECONDARY,
            cursor="hand2",
            command=self._toggle_show
        )
        self.toggle_btn.pack(side="right", padx=(2, 6))

        self.error_label = ctk.CTkLabel(
            self,
            text="",
            font=FONT_CAPTION,
            text_color=COLOR_DANGER,
            anchor="w"
        )
        self.error_label.grid(row=2, column=0, sticky="w", pady=(2, 0))
        self.error_label.grid_remove()

    def _toggle_show(self):
        self.show_password = not self.show_password
        self.entry.configure(show="" if self.show_password else "•")
        self.toggle_btn.configure(text="🔒" if self.show_password else "👁")

    def get(self) -> str:
        return self.entry.get()

    def show_error(self, message: str):
        self.error_label.configure(text=message)
        self.error_label.grid()
        self.input_container.configure(border_color=COLOR_DANGER)

    def clear_error(self):
        self.error_label.configure(text="")
        self.error_label.grid_remove()
        self.input_container.configure(border_color=COLOR_INPUT_BORDER)


class FormDropdown(ctk.CTkFrame):
    """Labeled dropdown selector."""
    def __init__(self, master: Any, label: str, values: List[str],
                 default_value: Optional[str] = None, width: int = 320,
                 command: Optional[Callable] = None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.columnconfigure(0, weight=1)

        self.lbl = ctk.CTkLabel(
            self,
            text=label,
            font=FONT_BODY_BOLD,
            text_color=COLOR_TEXT_SECONDARY,
            anchor="w"
        )
        self.lbl.grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.option_menu = ctk.CTkOptionMenu(
            self,
            values=values,
            command=command,
            font=FONT_BODY,
            dropdown_font=FONT_BODY,
            fg_color=COLOR_INPUT_BG,
            button_color=COLOR_INPUT_BORDER,
            button_hover_color=COLOR_PRIMARY,
            text_color=COLOR_TEXT_PRIMARY,
            dropdown_fg_color=("white", "#1A2233"),
            dropdown_text_color=COLOR_TEXT_PRIMARY,
            dropdown_hover_color=COLOR_PRIMARY,
            corner_radius=INPUT_RADIUS,
            height=38,
            width=width
        )
        self.option_menu.grid(row=1, column=0, sticky="ew")

        if default_value and default_value in values:
            self.option_menu.set(default_value)
        elif values:
            self.option_menu.set(values[0])

    def get(self) -> str:
        return self.option_menu.get()

    def set(self, val: str):
        self.option_menu.set(val)


class FormDateEntry(ctk.CTkFrame):
    """Date input field (YYYY-MM-DD) with 'Today' convenience button."""
    def __init__(self, master: Any, label: str, default_date: Optional[str] = None,
                 width: int = 320, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.columnconfigure(0, weight=1)

        self.lbl = ctk.CTkLabel(
            self,
            text=f"{label} (YYYY-MM-DD)",
            font=FONT_BODY_BOLD,
            text_color=COLOR_TEXT_SECONDARY,
            anchor="w"
        )
        self.lbl.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 4))

        self.entry = ctk.CTkEntry(
            self,
            placeholder_text="YYYY-MM-DD",
            font=FONT_BODY,
            fg_color=COLOR_INPUT_BG,
            border_color=COLOR_INPUT_BORDER,
            border_width=1,
            corner_radius=INPUT_RADIUS,
            height=38,
            width=width - 70,
            text_color=COLOR_TEXT_PRIMARY
        )
        self.entry.grid(row=1, column=0, sticky="ew")

        val = default_date if default_date else date.today().strftime("%Y-%m-%d")
        self.entry.insert(0, val)

        self.today_btn = ctk.CTkButton(
            self,
            text="Today",
            font=FONT_BODY_SM,
            width=60,
            height=38,
            fg_color=("e2e8f0", "#202B3D"),
            hover_color=COLOR_PRIMARY,
            text_color=COLOR_TEXT_PRIMARY,
            corner_radius=INPUT_RADIUS,
            command=self._set_today
        )
        self.today_btn.grid(row=1, column=1, padx=(6, 0))

    def _set_today(self):
        self.entry.delete(0, "end")
        self.entry.insert(0, date.today().strftime("%Y-%m-%d"))

    def get(self) -> str:
        return self.entry.get().strip()

    def set(self, date_str: str):
        self.entry.delete(0, "end")
        self.entry.insert(0, date_str)


class FormTextBox(ctk.CTkFrame):
    """Labeled multi-line text area."""
    def __init__(self, master: Any, label: str, initial_text: str = "",
                 height: int = 90, width: int = 320, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.columnconfigure(0, weight=1)

        self.lbl = ctk.CTkLabel(
            self,
            text=label,
            font=FONT_BODY_BOLD,
            text_color=COLOR_TEXT_SECONDARY,
            anchor="w"
        )
        self.lbl.grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.textbox = ctk.CTkTextbox(
            self,
            font=FONT_BODY,
            fg_color=COLOR_INPUT_BG,
            border_color=COLOR_INPUT_BORDER,
            border_width=1,
            corner_radius=INPUT_RADIUS,
            height=height,
            width=width,
            text_color=COLOR_TEXT_PRIMARY
        )
        self.textbox.grid(row=1, column=0, sticky="ew")

        if initial_text:
            self.textbox.insert("1.0", initial_text)

    def get(self) -> str:
        return self.textbox.get("1.0", "end-1c").strip()

    def set(self, text: str):
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", text)
