"""
StudySync - Smart Student Study Planner
General Helper Functions & Asset Loaders
"""

import os
from typing import Dict, Tuple, Optional
from PIL import Image, ImageOps
import customtkinter as ctk

_ICON_CACHE: Dict[Tuple[str, int, int], ctk.CTkImage] = {}


def get_base_dir() -> str:
    """Returns the root directory of the StudySync application."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def get_asset_path(relative_path: str) -> str:
    """Returns the absolute path to an asset."""
    return os.path.join(get_base_dir(), "assets", relative_path)


def load_icon(name: str, size: Tuple[int, int] = (20, 20)) -> Optional[ctk.CTkImage]:
    """
    Loads and caches an icon as a CTkImage.
    Supports names like 'dashboard', 'tasks', 'logo.png', etc.
    """
    cache_key = (name, size[0], size[1])
    if cache_key in _ICON_CACHE:
        return _ICON_CACHE[cache_key]

    # Resolve filename
    filename = name if name.endswith(".png") else f"{name}.png"
    if name == "logo" or name == "logo.png":
        full_path = get_asset_path(filename)
    else:
        full_path = os.path.join(get_asset_path("icons"), filename)

    if not os.path.exists(full_path):
        # Return None if not found
        return None

    try:
        pil_img = Image.open(full_path)
        ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=size)
        _ICON_CACHE[cache_key] = ctk_img
        return ctk_img
    except Exception as e:
        print(f"Error loading icon {name}: {e}")
        return None


def truncate_text(text: str, max_chars: int = 40) -> str:
    """Truncates text with ellipsis if exceeding max_chars."""
    if not text:
        return ""
    clean = text.strip()
    if len(clean) <= max_chars:
        return clean
    return clean[:max_chars - 3] + "..."


def format_hours_short(hours: float) -> str:
    """Formats 3.5 -> '3.5h' or 4.0 -> '4h'."""
    if hours == int(hours):
        return f"{int(hours)}h"
    return f"{hours:.1f}h"
