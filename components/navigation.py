"""
StudySync - Smart Student Study Planner
Navigation Controller - Manages Page Switching in Main Content Area
"""

from typing import Dict, Any, Type
import customtkinter as ctk


class NavigationController:
    """Coordinates page transitions inside the main workspace container."""

    def __init__(self, container: ctk.CTkFrame, sidebar: Any):
        self.container = container
        self.sidebar = sidebar
        self.pages: Dict[str, ctk.CTkFrame] = {}
        self.current_page_name: str = ""

    def register_page(self, name: str, page_instance: ctk.CTkFrame):
        """Registers an initialized page frame into the controller."""
        self.pages[name] = page_instance

    def show_page(self, name: str):
        """Switches visible frame to the target page and triggers refresh if supported."""
        if name not in self.pages:
            print(f"Page '{name}' not found in registry.")
            return

        # Hide current page
        if self.current_page_name and self.current_page_name in self.pages:
            self.pages[self.current_page_name].pack_forget()

        # Display target page
        target_page = self.pages[name]
        target_page.pack(fill="both", expand=True)
        self.current_page_name = name

        # Update sidebar active highlight
        if self.sidebar:
            self.sidebar.set_active(name)

        # Call page refresh if available
        if hasattr(target_page, "refresh") and callable(getattr(target_page, "refresh")):
            target_page.refresh()
