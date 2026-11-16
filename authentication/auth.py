"""
StudySync - Smart Student Study Planner
Authentication Service - Password Hashing, Login, and Registration
"""

import hashlib
import secrets
from typing import Tuple, Optional, Dict, Any
from database.db_manager import DatabaseManager
from utils.validators import validate_registration, validate_email, validate_password


class AuthService:
    """Manages student authentication, hashing, session state, and demo credentials."""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self._current_user: Optional[Dict[str, Any]] = None

    @property
    def current_user(self) -> Optional[Dict[str, Any]]:
        return self._current_user

    @property
    def is_authenticated(self) -> bool:
        return self._current_user is not None

    @staticmethod
    def generate_salt() -> str:
        """Generates a secure 16-byte hex salt."""
        return secrets.token_hex(16)

    @staticmethod
    def hash_password(password: str, salt: str) -> str:
        """Computes SHA-256 hash of salt + password."""
        combined = f"{salt}:{password}".encode("utf-8")
        return hashlib.sha256(combined).hexdigest()

    def register(self, full_name: str, email: str, username: str, 
                 password: str, confirm_password: str) -> Tuple[bool, str]:
        """Validates input, checks duplicates, and creates a new student user."""
        is_valid, err_msg = validate_registration(full_name, email, username, password, confirm_password)
        if not is_valid:
            return False, err_msg

        # Check existing username
        existing_username = self.db.get_user_by_identifier(username)
        if existing_username:
            return False, "This username is already taken. Please choose another."

        # Check existing email
        existing_email = self.db.get_user_by_identifier(email)
        if existing_email:
            return False, "An account with this email address already exists."

        salt = self.generate_salt()
        pwd_hash = self.hash_password(password, salt)

        try:
            user_id = self.db.create_user(
                username=username,
                email=email,
                password_hash=pwd_hash,
                salt=salt,
                full_name=full_name,
                theme="Dark"
            )
            # Fetch newly created user object
            self._current_user = self.db.get_user_by_id(user_id)
            return True, "Account registered successfully!"
        except Exception as e:
            return False, f"Failed to register account: {str(e)}"

    def login(self, username_or_email: str, password: str) -> Tuple[bool, str]:
        """Authenticates a user by username/email and password."""
        if not username_or_email or not username_or_email.strip():
            return False, "Please enter your username or email."
        if not password:
            return False, "Please enter your password."

        user = self.db.get_user_by_identifier(username_or_email.strip())
        if not user:
            return False, "Invalid username or password. Please try again."

        salt = user["salt"]
        expected_hash = user["password_hash"]
        computed_hash = self.hash_password(password, salt)

        if not secrets.compare_digest(expected_hash, computed_hash):
            return False, "Invalid username or password. Please try again."

        self._current_user = user
        return True, f"Welcome back, {user['full_name']}!"

    def login_demo_account(self) -> Tuple[bool, str]:
        """Logs in to or automatically provisions a rich demo account for presentation."""
        demo_user = self.db.get_user_by_identifier("demo_student")
        if not demo_user:
            # Create demo account
            salt = self.generate_salt()
            pwd_hash = self.hash_password("studysync123", salt)
            user_id = self.db.create_user(
                username="demo_student",
                email="kushagra@college.edu",
                password_hash=pwd_hash,
                salt=salt,
                full_name="Kushagra Verma",
                theme="Dark"
            )
            # Seed comprehensive academic sample data
            self.db.seed_sample_data(user_id)
            self._current_user = self.db.get_user_by_id(user_id)
        else:
            self._current_user = demo_user
            # Ensure sample data exists if empty
            subjects = self.db.get_subjects(demo_user["id"])
            if not subjects:
                self.db.seed_sample_data(demo_user["id"])

        return True, "Logged in with Demo Account successfully!"

    def logout(self):
        """Clears the active session."""
        self._current_user = None

    def refresh_current_user(self):
        """Reloads the user profile from database."""
        if self._current_user:
            self._current_user = self.db.get_user_by_id(self._current_user["id"])
