"""
=============================================================================
STUDYSYNC – SMART STUDENT STUDY PLANNER
College-Level Academic Productivity Desktop Application
Technology: Python 3.11+, CustomTkinter, SQLite3, Matplotlib, Pillow
=============================================================================
"""

import sys
import os
import customtkinter as ctk

# Ensure workspace root is in python path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utils.theme import (
    COLOR_BG, ThemeManager, SIDEBAR_WIDTH
)
from utils.helpers import get_asset_path
from database.db_manager import DatabaseManager
from authentication.auth import AuthService
from components.sidebar import Sidebar
from components.navigation import NavigationController
from pages.login import LoginPage
from pages.register import RegisterPage
from pages.dashboard import DashboardPage
from pages.subjects import SubjectsPage
from pages.planner import PlannerPage
from pages.tasks import TasksPage
from pages.exams import ExamsPage
from pages.analytics import AnalyticsPage
from pages.settings import SettingsPage


class StudySyncApp(ctk.CTk):
    """
    Main Application Window:
    - Orchestrates Authentication views (Login / Register)
    - Orchestrates Workspace views (Sidebar + Content Container)
    - Manages theme transitions and lifecycle
    """

    def __init__(self):
        super().__init__()

        # Window Metadata & Configuration
        self.title("StudySync – Smart Student Study Planner")
        self.minsize(1050, 640)
        self._configure_window_geometry(1440, 900)

        # Set Window Icon if present
        icon_path = get_asset_path("logo.png")
        if os.path.exists(icon_path):
            try:
                # Tkinter on Windows supports iconbitmap or iconphoto
                self.iconbitmap(default="")
            except Exception:
                pass

        # Set Initial Theme
        ThemeManager.set_theme("Dark")
        self.configure(fg_color=COLOR_BG)

        # Core Services
        self.db = DatabaseManager()
        self.auth_service = AuthService(self.db)

        # Layout State Holders
        self.auth_container: ctk.CTkFrame = None
        self.main_container: ctk.CTkFrame = None
        self.sidebar: Sidebar = None
        self.nav_controller: NavigationController = None

        # Start with Auth Screen
        self.show_auth_view()

    def _configure_window_geometry(self, default_w: int, default_h: int):
        """Sets responsive window geometry and centers or zooms on screen."""
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        target_w = min(default_w, screen_w - 60)
        target_h = min(default_h, screen_h - 80)
        x = max(10, (screen_w - target_w) // 2)
        y = max(10, (screen_h - target_h) // 2)

        self.geometry(f"{target_w}x{target_h}+{x}+{y}")

        # If on large screen, maximize for optimal viewing
        if screen_w >= 1600:
            try:
                self.state("zoomed")
            except Exception:
                pass

    # =========================================================================
    # AUTHENTICATION VIEWS
    # =========================================================================

    def show_auth_view(self, initial_mode: str = "login"):
        """Displays either Login or Register view."""
        self._teardown_all_views()

        self.auth_container = ctk.CTkFrame(self, fg_color=COLOR_BG)
        self.auth_container.pack(fill="both", expand=True)

        if initial_mode == "register":
            page = RegisterPage(
                self.auth_container,
                auth_service=self.auth_service,
                on_register_success=self.show_workspace_view,
                on_switch_to_login=lambda: self.show_auth_view("login")
            )
        else:
            page = LoginPage(
                self.auth_container,
                auth_service=self.auth_service,
                on_login_success=self.show_workspace_view,
                on_switch_to_register=lambda: self.show_auth_view("register")
            )

        page.pack(fill="both", expand=True)

    # =========================================================================
    # WORKSPACE VIEWS (MAIN DESKTOP UI)
    # =========================================================================

    def show_workspace_view(self):
        """Builds the main dashboard layout with fixed sidebar and content area."""
        self._teardown_all_views()

        current_user = self.auth_service.current_user
        if not current_user:
            self.show_auth_view()
            return

        # Restore user theme preference if stored
        user_theme = current_user.get("theme", "Dark")
        ThemeManager.set_theme(user_theme)

        # Master Container
        self.main_container = ctk.CTkFrame(self, fg_color=COLOR_BG)
        self.main_container.pack(fill="both", expand=True)

        # 1. Fixed Left Sidebar
        self.sidebar = Sidebar(
            master=self.main_container,
            current_user=current_user,
            on_navigate=self._handle_navigation,
            on_logout=self._handle_logout
        )
        self.sidebar.pack(side="left", fill="y")

        # 2. Main Page Content Container
        self.content_container = ctk.CTkFrame(self.main_container, fg_color=COLOR_BG, corner_radius=0)
        self.content_container.pack(side="right", fill="both", expand=True)

        # 3. Navigation Controller & Registry
        self.nav_controller = NavigationController(self.content_container, self.sidebar)

        user_id = current_user["id"]

        dashboard_page = DashboardPage(self.content_container, db=self.db, user_id=user_id,
                                       on_navigate=self._handle_navigation)
        subjects_page = SubjectsPage(self.content_container, db=self.db, user_id=user_id)
        planner_page = PlannerPage(self.content_container, db=self.db, user_id=user_id)
        tasks_page = TasksPage(self.content_container, db=self.db, user_id=user_id)
        exams_page = ExamsPage(self.content_container, db=self.db, user_id=user_id)
        analytics_page = AnalyticsPage(self.content_container, db=self.db, user_id=user_id)
        settings_page = SettingsPage(
            self.content_container,
            db=self.db,
            auth_service=self.auth_service,
            on_logout=self._handle_logout,
            on_profile_updated=self._on_profile_updated
        )

        self.nav_controller.register_page("Dashboard", dashboard_page)
        self.nav_controller.register_page("My Subjects", subjects_page)
        self.nav_controller.register_page("Study Planner", planner_page)
        self.nav_controller.register_page("Tasks & Assignments", tasks_page)
        self.nav_controller.register_page("Exam Countdown", exams_page)
        self.nav_controller.register_page("Analytics", analytics_page)
        self.nav_controller.register_page("Settings", settings_page)

        # Default to Dashboard
        self.nav_controller.show_page("Dashboard")

    def _handle_navigation(self, page_name: str):
        if self.nav_controller:
            self.nav_controller.show_page(page_name)

    def _handle_logout(self):
        self.auth_service.logout()
        self.show_auth_view()

    def _on_profile_updated(self):
        """Propagates updated user details to the sidebar footer."""
        if self.sidebar and self.auth_service.current_user:
            self.sidebar.update_user_info(self.auth_service.current_user)

    def _teardown_all_views(self):
        """Cleans up widgets before major layout switch."""
        if self.auth_container:
            self.auth_container.destroy()
            self.auth_container = None
        if self.main_container:
            self.main_container.destroy()
            self.main_container = None


def main():
    """Application entry point."""
    try:
        app = StudySyncApp()
        app.mainloop()
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
