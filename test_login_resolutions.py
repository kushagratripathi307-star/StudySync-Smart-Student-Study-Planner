"""
StudySync - Login Screen Resolution & Clipping Verification Test
Tests login screen visibility and alignment at 1366x768 and 1440x900.
"""

import os
import sys
import customtkinter as ctk

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from main import StudySyncApp


def test_resolutions():
    print("Testing resolutions: 1366x768 and 1440x900...")
    app = StudySyncApp()

    for width, height in [(1366, 768), (1440, 900)]:
        print(f"\n--- Testing resolution {width}x{height} ---")
        app.geometry(f"{width}x{height}+50+50")
        app.update()

        login_page = [w for w in app.auth_container.winfo_children()][0]

        # 1. Check center container bounds
        c_x = login_page.center_container.winfo_x()
        c_y = login_page.center_container.winfo_y()
        c_w = login_page.center_container.winfo_width()
        c_h = login_page.center_container.winfo_height()

        win_w = app.winfo_width()
        win_h = app.winfo_height()

        print(f"Window actual dimensions: {win_w}x{win_h}")
        print(f"Center container: {c_w}x{c_h} at x={c_x}, y={c_y}")
        assert c_x >= 0, f"Container x should be >= 0, got {c_x}"
        assert c_y >= 0, f"Container y should be >= 0, got {c_y}"
        assert c_x + c_w <= win_w, f"Container exceeds window width: {c_x + c_w} > {win_w}"
        assert c_y + c_h <= win_h, f"Container exceeds window height: {c_y + c_h} > {win_h}"

        # 2. Check Username and Password Alignment
        u_w = login_page.ident_entry.winfo_width()
        p_w = login_page.pwd_entry.winfo_width()
        b_w = login_page.login_btn.winfo_width()
        d_w = login_page.demo_btn.winfo_width()

        print(f"Widths: Username={u_w}, Password={p_w}, LoginBtn={b_w}, DemoBtn={d_w}")
        assert u_w == p_w, f"Username width ({u_w}) and Password width ({p_w}) must match!"
        assert u_w == b_w, f"Input width ({u_w}) and Button width ({b_w}) must match!"

        # 3. Check Username Label visibility
        lbl_text = login_page.ident_entry.lbl.cget("text")
        lbl_h = login_page.ident_entry.lbl.winfo_height()
        print(f"Username label: '{lbl_text}', height={lbl_h}")
        assert "Username" in lbl_text, "Username label must be visible and correct"
        assert lbl_h > 0, "Username label must have positive height"

        # 4. Check Login and Demo buttons are not cut off
        btn_y = login_page.login_btn.winfo_y()
        btn_h = login_page.login_btn.winfo_height()
        demo_y = login_page.demo_btn.winfo_y()
        demo_h = login_page.demo_btn.winfo_height()
        form_h = login_page.login_btn.master.winfo_height()

        print(f"Form height: {form_h}, Login button bottom: {btn_y + btn_h}, Demo button bottom: {demo_y + demo_h}")
        assert demo_y + demo_h <= form_h, f"Demo button cut off! {demo_y + demo_h} > {form_h}"

        print(f"Resolution {width}x{height} passed perfectly with zero clipping!")

    app.destroy()
    print("\nAll resolution & clipping verification checks passed successfully!")


if __name__ == "__main__":
    test_resolutions()
