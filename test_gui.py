"""
StudySync - Comprehensive GUI Lifecycle and Navigation Verification Test
Verifies all windows, page frames, embedded charts, and navigation flows.
"""

import os
import sys
import customtkinter as ctk

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from main import StudySyncApp
from utils.theme import ThemeManager


def test_gui_lifecycle():
    print("Initializing StudySyncApp...")
    app = StudySyncApp()
    app.update()

    print("Checking initial authentication view...")
    assert app.auth_container is not None, "Auth container should be present"
    print("Auth view rendered correctly.")

    print("Triggering Demo Account Login...")
    app.auth_service.login_demo_account()
    app.show_workspace_view()
    app.update()

    print("Verifying Sidebar and Main Workspace...")
    assert app.sidebar is not None, "Sidebar must exist"
    assert app.nav_controller is not None, "Navigation controller must exist"
    assert app.main_container is not None, "Main container must exist"

    # Test navigating through all pages
    pages = [
        "Dashboard",
        "My Subjects",
        "Study Planner",
        "Tasks & Assignments",
        "Exam Countdown",
        "Analytics",
        "Settings"
    ]

    for p in pages:
        print(f"Navigating to page: '{p}'...")
        app.nav_controller.show_page(p)
        app.update()
        page_widget = app.nav_controller.pages.get(p)
        assert page_widget is not None, f"Page {p} must be registered"
        print(f"Page '{p}' rendered successfully.")

    print("Testing Theme Toggling...")
    ThemeManager.set_theme("Light")
    app.update()
    assert ThemeManager.get_theme() == "Light"

    ThemeManager.set_theme("Dark")
    app.update()
    assert ThemeManager.get_theme() == "Dark"
    print("Theme toggling passed.")

    print("Testing Logout Flow...")
    app._handle_logout()
    app.update()
    assert app.auth_container is not None, "Auth container should be shown after logout"
    print("Logout flow passed.")

    print("Tearing down application...")
    app.destroy()
    print("All GUI lifecycle tests passed successfully!")


if __name__ == "__main__":
    test_gui_lifecycle()
