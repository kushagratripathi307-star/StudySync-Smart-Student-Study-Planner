"""
StudySync - Smart Student Study Planner
Asset & Icon Generator using Pillow
Generates clean, modern vector-style icons at crisp resolutions.
"""

import os
from PIL import Image, ImageDraw


def create_base_canvas(size=(64, 64), scale=4):
    """Creates a high-res canvas for supersampled antialiasing."""
    real_size = (size[0] * scale, size[1] * scale)
    img = Image.new("RGBA", real_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    return img, draw, scale, size


def save_canvas(img, path, target_size):
    """Downsamples high-res canvas to target_size using high-quality LANCZOS filter."""
    final = img.resize(target_size, Image.Resampling.LANCZOS)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    final.save(path, "PNG")


def generate_all_icons(assets_dir: str):
    icons_dir = os.path.join(assets_dir, "icons")
    os.makedirs(icons_dir, exist_ok=True)

    # 1. Main Logo (App Logo: Modern geometric hexagon/diamond with book & sync symbol)
    logo_path = os.path.join(assets_dir, "logo.png")
    img, draw, s, sz = create_base_canvas((128, 128), scale=4)
    # Background rounded square with vibrant gradient
    w, h = 128 * s, 128 * s
    draw.rounded_rectangle([12 * s, 12 * s, 116 * s, 116 * s], radius=28 * s, fill="#7667F8")
    # Stylized sync arrows / open book
    # Left page
    draw.polygon([(36 * s, 42 * s), (60 * s, 36 * s), (60 * s, 86 * s), (36 * s, 80 * s)], fill="#FFFFFF")
    # Right page
    draw.polygon([(68 * s, 36 * s), (92 * s, 42 * s), (92 * s, 80 * s), (68 * s, 86 * s)], fill="#E0DDFF")
    # Bookmark / accent spark
    draw.polygon([(62 * s, 32 * s), (66 * s, 32 * s), (66 * s, 58 * s), (62 * s, 54 * s)], fill="#38C98B")
    save_canvas(img, logo_path, (128, 128))

    # Helper for drawing icons
    c_white = "#FFFFFF"

    # 2. Dashboard Icon (Grid / Layout 4 squares)
    img, draw, s, sz = create_base_canvas((48, 48), scale=4)
    r = 3 * s
    draw.rounded_rectangle([8 * s, 8 * s, 21 * s, 21 * s], radius=r, fill=c_white)
    draw.rounded_rectangle([27 * s, 8 * s, 40 * s, 21 * s], radius=r, fill=c_white)
    draw.rounded_rectangle([8 * s, 27 * s, 21 * s, 40 * s], radius=r, fill=c_white)
    draw.rounded_rectangle([27 * s, 27 * s, 40 * s, 40 * s], radius=r, fill=c_white)
    save_canvas(img, os.path.join(icons_dir, "dashboard.png"), (48, 48))

    # 3. Subjects Icon (Books stacked / Notebook)
    img, draw, s, sz = create_base_canvas((48, 48), scale=4)
    draw.rounded_rectangle([10 * s, 8 * s, 38 * s, 40 * s], radius=4 * s, outline=c_white, width=3 * s)
    draw.line([18 * s, 8 * s, 18 * s, 40 * s], fill=c_white, width=3 * s)
    draw.line([24 * s, 18 * s, 32 * s, 18 * s], fill=c_white, width=3 * s)
    draw.line([24 * s, 26 * s, 32 * s, 26 * s], fill=c_white, width=3 * s)
    save_canvas(img, os.path.join(icons_dir, "subjects.png"), (48, 48))

    # 4. Planner Icon (Calendar with clock / timetable)
    img, draw, s, sz = create_base_canvas((48, 48), scale=4)
    draw.rounded_rectangle([8 * s, 12 * s, 40 * s, 40 * s], radius=5 * s, outline=c_white, width=3 * s)
    draw.line([8 * s, 20 * s, 40 * s, 20 * s], fill=c_white, width=3 * s)
    draw.line([15 * s, 7 * s, 15 * s, 13 * s], fill=c_white, width=3 * s)
    draw.line([33 * s, 7 * s, 33 * s, 13 * s], fill=c_white, width=3 * s)
    # Check lines or dot inside
    draw.ellipse([21 * s, 27 * s, 27 * s, 33 * s], fill=c_white)
    save_canvas(img, os.path.join(icons_dir, "planner.png"), (48, 48))

    # 5. Tasks Icon (Checklist with ticks)
    img, draw, s, sz = create_base_canvas((48, 48), scale=4)
    # Checkmark 1
    draw.line([(10 * s, 16 * s), (14 * s, 20 * s), (20 * s, 12 * s)], fill=c_white, width=3 * s)
    draw.line([25 * s, 16 * s, 38 * s, 16 * s], fill=c_white, width=3 * s)
    # Checkmark 2
    draw.line([(10 * s, 28 * s), (14 * s, 32 * s), (20 * s, 24 * s)], fill=c_white, width=3 * s)
    draw.line([25 * s, 28 * s, 38 * s, 28 * s], fill=c_white, width=3 * s)
    # Line 3
    draw.ellipse([12 * s, 37 * s, 16 * s, 41 * s], fill=c_white)
    draw.line([25 * s, 39 * s, 38 * s, 39 * s], fill=c_white, width=3 * s)
    save_canvas(img, os.path.join(icons_dir, "tasks.png"), (48, 48))

    # 6. Exams Icon (Hourglass / Target / Trophy / Clock)
    img, draw, s, sz = create_base_canvas((48, 48), scale=4)
    # Graduation cap or timer
    draw.polygon([(24 * s, 10 * s), (42 * s, 18 * s), (24 * s, 26 * s), (6 * s, 18 * s)], fill=c_white)
    draw.polygon([(14 * s, 24 * s), (24 * s, 34 * s), (34 * s, 24 * s), (24 * s, 28 * s)], fill=c_white)
    draw.line([38 * s, 20 * s, 38 * s, 34 * s], fill=c_white, width=2 * s)
    draw.ellipse([36 * s, 34 * s, 40 * s, 38 * s], fill=c_white)
    save_canvas(img, os.path.join(icons_dir, "exams.png"), (48, 48))

    # 7. Analytics Icon (Bar chart ascending)
    img, draw, s, sz = create_base_canvas((48, 48), scale=4)
    draw.rounded_rectangle([9 * s, 28 * s, 15 * s, 40 * s], radius=2 * s, fill=c_white)
    draw.rounded_rectangle([18 * s, 20 * s, 24 * s, 40 * s], radius=2 * s, fill=c_white)
    draw.rounded_rectangle([27 * s, 12 * s, 33 * s, 40 * s], radius=2 * s, fill=c_white)
    draw.rounded_rectangle([36 * s, 6 * s, 42 * s, 40 * s], radius=2 * s, fill=c_white)
    save_canvas(img, os.path.join(icons_dir, "analytics.png"), (48, 48))

    # 8. Settings Icon (Gear / Sliders)
    img, draw, s, sz = create_base_canvas((48, 48), scale=4)
    draw.ellipse([14 * s, 14 * s, 34 * s, 34 * s], outline=c_white, width=4 * s)
    draw.ellipse([20 * s, 20 * s, 28 * s, 28 * s], fill=c_white)
    # Cog teeth
    teeth = [
        (22 * s, 6 * s, 26 * s, 14 * s),
        (22 * s, 34 * s, 26 * s, 42 * s),
        (6 * s, 22 * s, 14 * s, 26 * s),
        (34 * s, 22 * s, 42 * s, 26 * s),
    ]
    for t in teeth:
        draw.rounded_rectangle(t, radius=2 * s, fill=c_white)
    save_canvas(img, os.path.join(icons_dir, "settings.png"), (48, 48))

    # 9. Logout Icon
    img, draw, s, sz = create_base_canvas((48, 48), scale=4)
    draw.line([22 * s, 10 * s, 12 * s, 10 * s], fill=c_white, width=3 * s)
    draw.line([12 * s, 10 * s, 12 * s, 38 * s], fill=c_white, width=3 * s)
    draw.line([12 * s, 38 * s, 22 * s, 38 * s], fill=c_white, width=3 * s)
    # Arrow
    draw.line([18 * s, 24 * s, 36 * s, 24 * s], fill=c_white, width=3 * s)
    draw.line([30 * s, 17 * s, 37 * s, 24 * s], fill=c_white, width=3 * s)
    draw.line([30 * s, 31 * s, 37 * s, 24 * s], fill=c_white, width=3 * s)
    save_canvas(img, os.path.join(icons_dir, "logout.png"), (48, 48))

    # 10. Plus Icon
    img, draw, s, sz = create_base_canvas((48, 48), scale=4)
    draw.line([24 * s, 12 * s, 24 * s, 36 * s], fill=c_white, width=4 * s)
    draw.line([12 * s, 24 * s, 36 * s, 24 * s], fill=c_white, width=4 * s)
    save_canvas(img, os.path.join(icons_dir, "plus.png"), (48, 48))

    # 11. Edit / Pencil Icon
    img, draw, s, sz = create_base_canvas((48, 48), scale=4)
    draw.polygon([(34 * s, 10 * s), (38 * s, 14 * s), (18 * s, 34 * s), (14 * s, 34 * s), (14 * s, 30 * s)], fill=c_white)
    draw.polygon([(10 * s, 38 * s), (14 * s, 34 * s), (14 * s, 38 * s)], fill=c_white)
    save_canvas(img, os.path.join(icons_dir, "edit.png"), (48, 48))

    # 12. Delete / Trash Icon
    img, draw, s, sz = create_base_canvas((48, 48), scale=4)
    draw.line([12 * s, 14 * s, 36 * s, 14 * s], fill=c_white, width=3 * s)
    draw.line([20 * s, 10 * s, 28 * s, 10 * s], fill=c_white, width=3 * s)
    draw.rounded_rectangle([15 * s, 16 * s, 33 * s, 39 * s], radius=3 * s, outline=c_white, width=3 * s)
    draw.line([20 * s, 21 * s, 20 * s, 34 * s], fill=c_white, width=2 * s)
    draw.line([28 * s, 21 * s, 28 * s, 34 * s], fill=c_white, width=2 * s)
    save_canvas(img, os.path.join(icons_dir, "delete.png"), (48, 48))

    # 13. Check / Success Icon
    img, draw, s, sz = create_base_canvas((48, 48), scale=4)
    draw.ellipse([8 * s, 8 * s, 40 * s, 40 * s], fill="#38C98B")
    draw.line([(16 * s, 24 * s), (22 * s, 30 * s), (32 * s, 18 * s)], fill=c_white, width=4 * s)
    save_canvas(img, os.path.join(icons_dir, "check.png"), (48, 48))

    # 14. Clock Icon
    img, draw, s, sz = create_base_canvas((48, 48), scale=4)
    draw.ellipse([8 * s, 8 * s, 40 * s, 40 * s], outline=c_white, width=3 * s)
    draw.line([24 * s, 15 * s, 24 * s, 24 * s], fill=c_white, width=3 * s)
    draw.line([24 * s, 24 * s, 32 * s, 24 * s], fill=c_white, width=3 * s)
    save_canvas(img, os.path.join(icons_dir, "clock.png"), (48, 48))

    # 15. Calendar Icon
    img, draw, s, sz = create_base_canvas((48, 48), scale=4)
    draw.rounded_rectangle([8 * s, 11 * s, 40 * s, 39 * s], radius=4 * s, outline=c_white, width=3 * s)
    draw.line([8 * s, 20 * s, 40 * s, 20 * s], fill=c_white, width=3 * s)
    draw.line([16 * s, 7 * s, 16 * s, 12 * s], fill=c_white, width=3 * s)
    draw.line([32 * s, 7 * s, 32 * s, 12 * s], fill=c_white, width=3 * s)
    save_canvas(img, os.path.join(icons_dir, "calendar.png"), (48, 48))

    # 16. Book Icon
    img, draw, s, sz = create_base_canvas((48, 48), scale=4)
    draw.polygon([(10 * s, 12 * s), (23 * s, 8 * s), (23 * s, 36 * s), (10 * s, 40 * s)], fill=c_white)
    draw.polygon([(25 * s, 8 * s), (38 * s, 12 * s), (38 * s, 40 * s), (25 * s, 36 * s)], fill=c_white)
    save_canvas(img, os.path.join(icons_dir, "book.png"), (48, 48))

    # 17. Search Icon
    img, draw, s, sz = create_base_canvas((48, 48), scale=4)
    draw.ellipse([10 * s, 10 * s, 28 * s, 28 * s], outline=c_white, width=3 * s)
    draw.line([25 * s, 25 * s, 38 * s, 38 * s], fill=c_white, width=4 * s)
    save_canvas(img, os.path.join(icons_dir, "search.png"), (48, 48))

    # 18. User / Profile Avatar Icon
    img, draw, s, sz = create_base_canvas((48, 48), scale=4)
    draw.ellipse([16 * s, 8 * s, 32 * s, 24 * s], fill=c_white)
    draw.pieslice([8 * s, 22 * s, 40 * s, 54 * s], 180, 360, fill=c_white)
    save_canvas(img, os.path.join(icons_dir, "user.png"), (48, 48))

    # 19. Bell / Notification Icon
    img, draw, s, sz = create_base_canvas((48, 48), scale=4)
    draw.arc([16 * s, 12 * s, 32 * s, 28 * s], 180, 360, fill=c_white, width=3 * s)
    draw.line([16 * s, 20 * s, 12 * s, 34 * s], fill=c_white, width=3 * s)
    draw.line([32 * s, 20 * s, 36 * s, 34 * s], fill=c_white, width=3 * s)
    draw.line([10 * s, 34 * s, 38 * s, 34 * s], fill=c_white, width=3 * s)
    draw.ellipse([21 * s, 36 * s, 27 * s, 40 * s], fill=c_white)
    save_canvas(img, os.path.join(icons_dir, "bell.png"), (48, 48))

    # 20. Refresh / Sync Icon
    img, draw, s, sz = create_base_canvas((48, 48), scale=4)
    draw.arc([10 * s, 10 * s, 38 * s, 38 * s], 30, 310, fill=c_white, width=3 * s)
    draw.polygon([(36 * s, 12 * s), (42 * s, 22 * s), (30 * s, 22 * s)], fill=c_white)
    save_canvas(img, os.path.join(icons_dir, "refresh.png"), (48, 48))

    # 21. Alert / Warning Icon
    img, draw, s, sz = create_base_canvas((48, 48), scale=4)
    draw.polygon([(24 * s, 8 * s), (42 * s, 39 * s), (6 * s, 39 * s)], fill="#F5B84B")
    draw.line([24 * s, 18 * s, 24 * s, 28 * s], fill="#101522", width=3 * s)
    draw.ellipse([22 * s, 32 * s, 26 * s, 36 * s], fill="#101522")
    save_canvas(img, os.path.join(icons_dir, "alert.png"), (48, 48))

    # 22. Sparkles / Demo Data Icon
    img, draw, s, sz = create_base_canvas((48, 48), scale=4)
    # 4-pointed star
    cx, cy = 24 * s, 24 * s
    draw.polygon([(cx, 8 * s), (cx + 4 * s, cy - 4 * s), (cx + 16 * s, cy), (cx + 4 * s, cy + 4 * s),
                  (cx, cy + 16 * s), (cx - 4 * s, cy + 4 * s), (cx - 16 * s, cy), (cx - 4 * s, cy - 4 * s)], fill="#7667F8")
    save_canvas(img, os.path.join(icons_dir, "sparkles.png"), (48, 48))


if __name__ == "__main__":
    import sys
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
    generate_all_icons(base)
    print("All icons successfully generated in:", base)
