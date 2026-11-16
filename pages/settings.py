"""
StudySync - Smart Student Study Planner
Settings Page - Profile Management, Theme Switcher, Demo Data Controls, and System Info
"""

from typing import Any, Callable, Dict, Optional
import customtkinter as ctk
from tkinter import messagebox

from utils.theme import (
    COLOR_BG, COLOR_CARD, COLOR_CARD_SECONDARY, COLOR_BORDER,
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_DANGER,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    FONT_HEADING_LG, FONT_HEADING_MD, FONT_SUBHEADING, FONT_BODY,
    FONT_BODY_BOLD, FONT_BODY_SM, FONT_CAPTION, CARD_RADIUS,
    BUTTON_RADIUS, ThemeManager
)
from utils.helpers import load_icon
from components.buttons import PrimaryButton, SecondaryButton, DangerButton
from components.forms import FormEntry, FormPasswordEntry
from components.dialogs import ConfirmDialog, center_window
from utils.validators import validate_email, validate_password


class SettingsPage(ctk.CTkScrollableFrame):
    """
    Settings & Profile Module:
    - User Profile review and editing
    - Security (Password change)
    - Appearance (Dark/Light mode switcher with instant application)
    - Demonstration mode controls (Seed realistic data / Reset account)
    - System & Academic Project specifications
    - Logout action
    """
    def __init__(self, master: Any, db: Any, auth_service: Any,
                 on_logout: Callable[[], None],
                 on_profile_updated: Optional[Callable[[], None]] = None,
                 **kwargs):
        super().__init__(master, fg_color=COLOR_BG, corner_radius=0, **kwargs)
        self.db = db
        self.auth_service = auth_service
        self.on_logout = on_logout
        self.on_profile_updated = on_profile_updated

        self._build_header()
        self._build_profile_section()
        self._build_appearance_section()
        self._build_demo_data_section()
        self._build_system_info_section()
        self._build_danger_zone()

    def _build_header(self):
        head = ctk.CTkFrame(self, fg_color="transparent")
        head.pack(fill="x", padx=32, pady=(28, 14))

        ctk.CTkLabel(
            head,
            text="Settings & Profile",
            font=FONT_HEADING_LG,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            head,
            text="Manage your account profile, customize appearance preferences, and configure application settings.",
            font=FONT_BODY,
            text_color=COLOR_TEXT_SECONDARY,
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))

    def _build_profile_section(self):
        """User profile card."""
        card = self._create_section_card("Student Profile", "Your personal academic credentials and contact details")

        user = self.auth_service.current_user or {}
        full_name = user.get("full_name", "Student")
        username = user.get("username", "student")
        email = user.get("email", "student@college.edu")

        info_grid = ctk.CTkFrame(card, fg_color="transparent")
        info_grid.pack(fill="x", padx=20, pady=(0, 16))
        info_grid.columnconfigure(0, weight=1)
        info_grid.columnconfigure(1, weight=1)

        # Name & Username
        col1 = ctk.CTkFrame(info_grid, fg_color="transparent")
        col1.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(col1, text="Full Name", font=FONT_CAPTION, text_color=COLOR_TEXT_MUTED).pack(anchor="w")
        self.profile_name_lbl = ctk.CTkLabel(col1, text=full_name, font=FONT_BODY_BOLD, text_color=COLOR_TEXT_PRIMARY)
        self.profile_name_lbl.pack(anchor="w", pady=(2, 0))

        col2 = ctk.CTkFrame(info_grid, fg_color="transparent")
        col2.grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(col2, text="Username", font=FONT_CAPTION, text_color=COLOR_TEXT_MUTED).pack(anchor="w")
        ctk.CTkLabel(col2, text=f"@{username}", font=FONT_BODY_BOLD, text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", pady=(2, 0))

        # Email & Role
        col3 = ctk.CTkFrame(info_grid, fg_color="transparent")
        col3.grid(row=1, column=0, sticky="w", pady=(12, 0))
        ctk.CTkLabel(col3, text="Email Address", font=FONT_CAPTION, text_color=COLOR_TEXT_MUTED).pack(anchor="w")
        self.profile_email_lbl = ctk.CTkLabel(col3, text=email, font=FONT_BODY_BOLD, text_color=COLOR_TEXT_PRIMARY)
        self.profile_email_lbl.pack(anchor="w", pady=(2, 0))

        col4 = ctk.CTkFrame(info_grid, fg_color="transparent")
        col4.grid(row=1, column=1, sticky="w", pady=(12, 0))
        ctk.CTkLabel(col4, text="Program / Standing", font=FONT_CAPTION, text_color=COLOR_TEXT_MUTED).pack(anchor="w")
        ctk.CTkLabel(col4, text="2nd Year B.Tech Computer Science", font=FONT_BODY_BOLD, text_color=COLOR_PRIMARY).pack(anchor="w", pady=(2, 0))

        # Action buttons
        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=20, pady=(0, 18))

        PrimaryButton(
            btn_row,
            text="Edit Profile",
            width=120,
            height=34,
            command=self._on_edit_profile
        ).pack(side="left", padx=(0, 10))

        SecondaryButton(
            btn_row,
            text="Change Password",
            width=140,
            height=34,
            command=self._on_change_password
        ).pack(side="left")

    def _build_appearance_section(self):
        """Theme settings (Dark / Light)."""
        card = self._create_section_card("Appearance & Theme", "Customize desktop interface visual theme")

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=(0, 18))

        ctk.CTkLabel(
            inner,
            text="Interface Appearance Mode:",
            font=FONT_BODY_BOLD,
            text_color=COLOR_TEXT_PRIMARY
        ).pack(side="left", padx=(0, 16))

        current_theme = ThemeManager.get_theme()

        self.theme_selector = ctk.CTkSegmentedButton(
            inner,
            values=["Dark Theme", "Light Theme"],
            font=FONT_BODY_SM,
            height=34,
            width=220,
            command=self._on_theme_toggle
        )
        self.theme_selector.set("Dark Theme" if current_theme == "Dark" else "Light Theme")
        self.theme_selector.pack(side="left")

    def _build_demo_data_section(self):
        """Demonstration mode / Sample data generation."""
        card = self._create_section_card("Demonstration & Academic Sample Data",
                                         "Quickly load realistic 2nd year B.Tech coursework to showcase features to evaluators")

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=(0, 18))

        sparkles_ic = load_icon("sparkles", size=(16, 16))
        SecondaryButton(
            inner,
            text="Load Academic Sample Data",
            icon=sparkles_ic,
            width=220,
            height=36,
            command=self._on_load_sample_data
        ).pack(side="left", padx=(0, 12))

        ctk.CTkLabel(
            inner,
            text="Populates DSA, OS, DBMS, OOP courses with real study sessions, assignments, and exams.",
            font=FONT_CAPTION,
            text_color=COLOR_TEXT_MUTED
        ).pack(side="left")

    def _build_system_info_section(self):
        """Application & Technology Specifications."""
        card = self._create_section_card("About StudySync", "Application architecture and technology stack")

        info_box = ctk.CTkFrame(card, fg_color=COLOR_CARD_SECONDARY, corner_radius=8)
        info_box.pack(fill="x", padx=20, pady=(0, 18))

        specs = [
            ("Application Name", "STUDYSYNC – Smart Student Study Planner"),
            ("Version", "2.0.0 (Production Academic Edition)"),
            ("Developer Role", "2nd Year B.Tech Computer Science Student"),
            ("Primary GUI", "CustomTkinter 6.0 (Tkinter-native Desktop Framework)"),
            ("Database Engine", "SQLite3 (Normalized local schema with foreign keys)"),
            ("Visual Analytics", "Matplotlib 3.10 (Dark embedded canvases)"),
            ("Security", "SHA-256 cryptographic password hashing with 16-byte random salts"),
            ("Storage File", "studysync.db (Active database persistent store)"),
        ]

        for idx, (label, val) in enumerate(specs):
            row = ctk.CTkFrame(info_box, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=4)
            ctk.CTkLabel(row, text=label, font=FONT_BODY_SM, text_color=COLOR_TEXT_MUTED, width=170, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=val, font=FONT_BODY_BOLD, text_color=COLOR_TEXT_PRIMARY, anchor="w").pack(side="left")

    def _build_danger_zone(self):
        """Account & Danger Zone."""
        card = self._create_section_card("Account Actions", "Log out of session or reset study data")

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=(0, 18))

        logout_ic = load_icon("logout", size=(16, 16))
        DangerButton(
            inner,
            text="Sign Out",
            icon=logout_ic,
            width=130,
            height=36,
            command=self._confirm_logout
        ).pack(side="left", padx=(0, 14))

        delete_ic = load_icon("delete", size=(16, 16))
        SecondaryButton(
            inner,
            text="Clear All My Study Data",
            icon=delete_ic,
            width=200,
            height=36,
            command=self._confirm_clear_data
        ).pack(side="left")

    def _create_section_card(self, title: str, subtitle: str) -> ctk.CTkFrame:
        card = ctk.CTkFrame(
            self,
            fg_color=COLOR_CARD,
            corner_radius=CARD_RADIUS,
            border_width=1,
            border_color=COLOR_BORDER
        )
        card.pack(fill="x", padx=32, pady=(0, 18))

        head = ctk.CTkFrame(card, fg_color="transparent")
        head.pack(fill="x", padx=20, pady=(16, 12))

        ctk.CTkLabel(head, text=title, font=FONT_HEADING_MD, text_color=COLOR_TEXT_PRIMARY, anchor="w").pack(anchor="w")
        ctk.CTkLabel(head, text=subtitle, font=FONT_CAPTION, text_color=COLOR_TEXT_MUTED, anchor="w").pack(anchor="w", pady=(1, 0))

        return card

    # =========================================================================
    # ACTIONS & HANDLERS
    # =========================================================================

    def _on_theme_toggle(self, selection: str):
        mode = "Dark" if "Dark" in selection else "Light"
        ThemeManager.set_theme(mode)
        # Persist to database if logged in
        user = self.auth_service.current_user
        if user:
            self.db.update_user_theme(user["id"], mode)

    def _on_edit_profile(self):
        user = self.auth_service.current_user
        if not user:
            return

        modal = ctk.CTkToplevel(self.winfo_toplevel())
        modal.title("Edit Student Profile")
        modal.resizable(False, False)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()
        modal.configure(fg_color=COLOR_BG)
        center_window(modal, 460, 340, self.winfo_toplevel())

        card = ctk.CTkFrame(modal, fg_color=COLOR_CARD, corner_radius=CARD_RADIUS,
                            border_width=1, border_color=COLOR_BORDER)
        card.pack(fill="both", expand=True, padx=14, pady=14)

        # Header
        top_header = ctk.CTkFrame(card, fg_color="transparent")
        top_header.pack(side="top", fill="x", padx=20, pady=(16, 8))
        ctk.CTkLabel(top_header, text="Edit Student Profile", font=FONT_HEADING_MD,
                     text_color=COLOR_TEXT_PRIMARY, anchor="w").pack(side="left")

        # Fixed bottom action bar
        ctk.CTkFrame(card, height=1, fg_color=COLOR_BORDER).pack(side="bottom", fill="x", padx=16, pady=(0, 0))
        btn_bar = ctk.CTkFrame(card, fg_color="transparent")
        btn_bar.pack(side="bottom", fill="x", padx=20, pady=14)

        SecondaryButton(btn_bar, text="Cancel", width=110, height=38,
                        command=modal.destroy).pack(side="right", padx=(10, 0))

        # Body
        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(side="top", fill="both", expand=True, padx=20, pady=(4, 8))

        name_entry = FormEntry(body, label="Full Name", initial_value=user.get("full_name", ""))
        name_entry.pack(fill="x", pady=6)

        email_entry = FormEntry(body, label="Email Address", initial_value=user.get("email", ""))
        email_entry.pack(fill="x", pady=6)

        def save():
            new_name = name_entry.get().strip()
            new_email = email_entry.get().strip()
            ok_em, msg_em = validate_email(new_email)
            if not ok_em:
                messagebox.showerror("Validation Error", msg_em, parent=modal)
                return
            if len(new_name) < 2:
                messagebox.showerror("Validation Error", "Please enter your full name.", parent=modal)
                return

            self.db.update_user_profile(user["id"], new_name, new_email)
            self.auth_service.refresh_current_user()
            self.profile_name_lbl.configure(text=new_name)
            self.profile_email_lbl.configure(text=new_email)
            if self.on_profile_updated:
                self.on_profile_updated()
            messagebox.showinfo("Success", "Profile updated successfully!", parent=modal)
            modal.destroy()

        PrimaryButton(btn_bar, text="Save Changes", width=140, height=38,
                      command=save).pack(side="right")

    def _on_change_password(self):
        user = self.auth_service.current_user
        if not user:
            return

        modal = ctk.CTkToplevel(self.winfo_toplevel())
        modal.title("Change Password")
        modal.resizable(False, False)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()
        modal.configure(fg_color=COLOR_BG)
        center_window(modal, 460, 420, self.winfo_toplevel())

        card = ctk.CTkFrame(modal, fg_color=COLOR_CARD, corner_radius=CARD_RADIUS,
                            border_width=1, border_color=COLOR_BORDER)
        card.pack(fill="both", expand=True, padx=14, pady=14)

        # Header
        top_header = ctk.CTkFrame(card, fg_color="transparent")
        top_header.pack(side="top", fill="x", padx=20, pady=(16, 8))
        ctk.CTkLabel(top_header, text="Change Password", font=FONT_HEADING_MD,
                     text_color=COLOR_TEXT_PRIMARY, anchor="w").pack(side="left")

        # Fixed bottom action bar
        ctk.CTkFrame(card, height=1, fg_color=COLOR_BORDER).pack(side="bottom", fill="x", padx=16, pady=(0, 0))
        btn_bar = ctk.CTkFrame(card, fg_color="transparent")
        btn_bar.pack(side="bottom", fill="x", padx=20, pady=14)

        SecondaryButton(btn_bar, text="Cancel", width=110, height=38,
                        command=modal.destroy).pack(side="right", padx=(10, 0))

        # Body
        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(side="top", fill="both", expand=True, padx=20, pady=(4, 8))

        cur_pwd_entry = FormPasswordEntry(body, label="Current Password", placeholder="Enter current password")
        cur_pwd_entry.pack(fill="x", pady=4)

        new_pwd_entry = FormPasswordEntry(body, label="New Password", placeholder="At least 6 characters")
        new_pwd_entry.pack(fill="x", pady=4)

        conf_pwd_entry = FormPasswordEntry(body, label="Confirm New Password", placeholder="Repeat new password")
        conf_pwd_entry.pack(fill="x", pady=4)

        def save_pwd():
            cur = cur_pwd_entry.get()
            new = new_pwd_entry.get()
            conf = conf_pwd_entry.get()

            # Verify current
            salt = user["salt"]
            if self.auth_service.hash_password(cur, salt) != user["password_hash"]:
                messagebox.showerror("Validation Error", "Incorrect current password.", parent=modal)
                return

            ok_p, msg_p = validate_password(new)
            if not ok_p:
                messagebox.showerror("Validation Error", msg_p, parent=modal)
                return

            if new != conf:
                messagebox.showerror("Validation Error", "New passwords do not match.", parent=modal)
                return

            new_salt = self.auth_service.generate_salt()
            new_hash = self.auth_service.hash_password(new, new_salt)
            self.db.update_user_password(user["id"], new_hash, new_salt)
            self.auth_service.refresh_current_user()
            messagebox.showinfo("Success", "Password updated successfully!", parent=modal)
            modal.destroy()

        PrimaryButton(btn_bar, text="Update Password", width=150, height=38,
                      command=save_pwd).pack(side="right")

    def _on_load_sample_data(self):
        user = self.auth_service.current_user
        if not user:
            return

        if self.db.has_sample_data(user["id"]):
            messagebox.showinfo("Sample Data Already Loaded",
                                "Academic sample data (DSA, OS, DBMS, OOP, Computer Architecture) is already loaded in your account.",
                                parent=self.winfo_toplevel())
            return

        def confirm():
            self.db.seed_sample_data(user["id"])
            messagebox.showinfo("Sample Data Loaded",
                                "Realistic academic sample records for DSA, OS, DBMS, OOP, and Computer Architecture have been loaded successfully!",
                                parent=self.winfo_toplevel())

        ConfirmDialog(
            parent=self.winfo_toplevel(),
            title="Load Academic Sample Data?",
            message="This will add demonstration courses, study sessions, assignments, and exam countdowns to your account.",
            confirm_text="Load Data",
            is_danger=False,
            on_confirm=confirm
        )

    def _confirm_clear_data(self):
        user = self.auth_service.current_user
        if not user:
            return

        def confirm():
            self.db.clear_user_data(user["id"])
            messagebox.showinfo("Data Reset", "All your subjects, study sessions, tasks, and exams have been removed.",
                                parent=self.winfo_toplevel())

        ConfirmDialog(
            parent=self.winfo_toplevel(),
            title="Clear All Study Data?",
            message="Are you sure you want to delete all your subjects, sessions, tasks, and exams? This action cannot be undone.",
            confirm_text="Wipe Data",
            is_danger=True,
            on_confirm=confirm
        )

    def _confirm_logout(self):
        ConfirmDialog(
            parent=self.winfo_toplevel(),
            title="Sign Out?",
            message="Are you sure you want to end your current session?",
            confirm_text="Sign Out",
            is_danger=True,
            on_confirm=self.on_logout
        )
