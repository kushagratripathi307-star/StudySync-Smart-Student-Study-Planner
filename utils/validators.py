"""
StudySync - Smart Student Study Planner
Input Validation Utilities
"""

import re
from typing import Tuple


EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
TIME_REGEX = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")
DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate_email(email: str) -> Tuple[bool, str]:
    if not email or not email.strip():
        return False, "Email address is required."
    clean = email.strip()
    if not EMAIL_REGEX.match(clean):
        return False, "Please enter a valid email address (e.g., student@university.edu)."
    return True, ""


def validate_username(username: str) -> Tuple[bool, str]:
    if not username or not username.strip():
        return False, "Username is required."
    clean = username.strip()
    if len(clean) < 3:
        return False, "Username must be at least 3 characters long."
    if not re.match(r"^[a-zA-Z0-9_.-]+$", clean):
        return False, "Username can only contain letters, numbers, dots, and underscores."
    return True, ""


def validate_password(password: str) -> Tuple[bool, str]:
    if not password:
        return False, "Password is required."
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, ""


def validate_registration(full_name: str, email: str, username: str, 
                          password: str, confirm_password: str) -> Tuple[bool, str]:
    if not full_name or len(full_name.strip()) < 2:
        return False, "Please enter your full name."
    
    ok, msg = validate_email(email)
    if not ok:
        return False, msg
    
    ok, msg = validate_username(username)
    if not ok:
        return False, msg
    
    ok, msg = validate_password(password)
    if not ok:
        return False, msg
    
    if password != confirm_password:
        return False, "Passwords do not match."
    
    return True, ""


def validate_time(time_str: str) -> Tuple[bool, str]:
    if not time_str or not time_str.strip():
        return False, "Time is required (format HH:MM)."
    if not TIME_REGEX.match(time_str.strip()):
        return False, "Invalid time format. Please use 24-hour format HH:MM (e.g. 14:30)."
    return True, ""


def validate_date(date_str: str) -> Tuple[bool, str]:
    if not date_str or not date_str.strip():
        return False, "Date is required (format YYYY-MM-DD)."
    if not DATE_REGEX.match(date_str.strip()):
        return False, "Invalid date format. Please use YYYY-MM-DD (e.g. 2026-11-28)."
    return True, ""


def validate_number(value_str: str, min_val: float = 0, max_val: float = 1000, 
                    field_name: str = "Value") -> Tuple[bool, str, float]:
    try:
        val = float(value_str.strip())
        if val < min_val or val > max_val:
            return False, f"{field_name} must be between {min_val} and {max_val}.", 0.0
        return True, "", val
    except (ValueError, TypeError):
        return False, f"{field_name} must be a valid number.", 0.0
