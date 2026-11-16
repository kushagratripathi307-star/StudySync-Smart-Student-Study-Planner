"""
StudySync - Smart Student Study Planner
Date & Time Utilities
"""

from datetime import datetime, date, timedelta
from typing import Tuple, Optional


def get_current_date_str() -> str:
    """Returns today's date formatted for display, e.g. 'Monday, Nov 16, 2026'."""
    now = datetime.now()
    return now.strftime("%A, %b %d, %Y")


def get_current_iso_date() -> str:
    """Returns today's date in ISO format YYYY-MM-DD."""
    return date.today().strftime("%Y-%m-%d")


def get_greeting(name: str = "") -> str:
    """Generates a warm, time-appropriate greeting."""
    hour = datetime.now().hour
    if hour < 12:
        period = "Good Morning"
    elif hour < 17:
        period = "Good Afternoon"
    else:
        period = "Good Evening"
    
    clean_name = name.strip()
    if clean_name:
        # Extract first name if full name provided
        first_name = clean_name.split()[0]
        return f"{period}, {first_name}!"
    return f"{period}!"


def parse_date(date_str: str) -> Optional[date]:
    """Safely parse a date string in YYYY-MM-DD format."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
    except (ValueError, TypeError):
        try:
            return datetime.strptime(date_str.strip(), "%d-%m-%Y").date()
        except (ValueError, TypeError):
            return None


def format_date_display(date_str: str) -> str:
    """Formats '2026-11-28' into 'Nov 28, 2026'."""
    parsed = parse_date(date_str)
    if not parsed:
        return date_str
    return parsed.strftime("%b %d, %Y")


def calculate_days_left(target_date_str: str) -> Tuple[int, str, str]:
    """
    Calculates remaining days from today to target_date_str.
    Returns:
        (days_count, display_text, urgency_level)
        urgency_level in ['urgent', 'warning', 'upcoming', 'past']
    """
    target = parse_date(target_date_str)
    if not target:
        return 0, "No Date", "upcoming"

    today = date.today()
    delta = (target - today).days

    if delta > 7:
        return delta, f"{delta} DAYS LEFT", "upcoming"
    elif 1 < delta <= 7:
        return delta, f"{delta} DAYS LEFT", "warning"
    elif delta == 1:
        return 1, "TOMORROW", "urgent"
    elif delta == 0:
        return 0, "TODAY", "urgent"
    else:
        past_days = abs(delta)
        text = "OVERDUE (1 day ago)" if past_days == 1 else f"OVERDUE ({past_days} days ago)"
        return delta, text, "past"


def calculate_duration_hours(start_time_str: str, end_time_str: str) -> float:
    """
    Calculates duration in decimal hours between start_time and end_time (format 'HH:MM').
    Returns 0.0 if invalid or end <= start.
    """
    try:
        fmt = "%H:%M"
        t1 = datetime.strptime(start_time_str.strip(), fmt)
        t2 = datetime.strptime(end_time_str.strip(), fmt)
        delta = (t2 - t1).total_seconds()
        if delta <= 0:
            return 0.0
        return round(delta / 3600.0, 2)
    except (ValueError, TypeError):
        return 0.0


def format_duration(hours: float) -> str:
    """Formats 2.5 hours as '2h 30m' or '2.5 hrs'."""
    if hours <= 0:
        return "0h 0m"
    h = int(hours)
    m = int(round((hours - h) * 60))
    if m == 60:
        h += 1
        m = 0
    if h == 0:
        return f"{m}m"
    if m == 0:
        return f"{h}h"
    return f"{h}h {m}m"


def get_current_week_dates() -> list[date]:
    """Returns a list of 7 date objects for the current week (Monday to Sunday)."""
    today = date.today()
    # Monday is weekday 0
    start_of_week = today - timedelta(days=today.weekday())
    return [start_of_week + timedelta(days=i) for i in range(7)]


def get_last_30_days_range() -> Tuple[date, date]:
    """Returns (start_date, end_date) for past 30 days."""
    today = date.today()
    start_date = today - timedelta(days=29)
    return start_date, today
