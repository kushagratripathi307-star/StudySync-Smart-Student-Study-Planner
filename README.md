# StudySync – Smart Student Study Planner

<p align="center">
  <img src="assets/logo.png" width="100" alt="StudySync Logo" />
</p>

<p align="center">
  <strong>An Intelligent Academic Productivity Desktop Platform for College & University Students</strong><br>
  <em>Developed as a 2nd-Year B.Tech Computer Science & Engineering Academic Project</em>
</p>

---

## 1. Project Introduction

**StudySync** is a modern, commercial-grade Python desktop application designed to centralize and automate student academic management. Traditional methods of academic tracking—such as scattered notes, generic calendar apps, and paper planners—fail to provide dedicated workflows for subject quotas, assignment urgencies, syllabus completion, and dynamic exam countdowns.

StudySync eliminates academic fragmentation by uniting:
- **Coursework Management**: Syllabus completion, course credits, and target study hours.
- **Smart Study Scheduling**: Precise time-slot allocation with real-time duration calculations.
- **Assignment & Task Tracking**: Multi-criteria priority filtering with live urgency tags.
- **Dynamic Examination Countdown**: Automated date-difference algorithms highlighting upcoming assessments.
- **Productivity Analytics**: Embedded dark-themed data visualizations powered by Matplotlib.

---

## 2. Project Objectives

1. **Academic Centralization**: Provide a unified platform where students manage all coursework, tasks, schedules, and exams.
2. **Actionable Analytics**: Compute study velocities and subject allocations dynamically from actual database records.
3. **Data Security & Privacy**: Secure local storage with SQLite3 and cryptographic password hashing (SHA-256 + 16-byte cryptographic salts).
4. **Professional UI/UX**: Deliver an elegant, responsive desktop interface inspired by Notion and Linear, adhering to strict design hierarchy and custom dark/light appearance modes.
5. **Robust Architecture**: Modularize components using Object-Oriented Programming (OOP) and layered architecture separating database operations from UI rendering.

---

## 3. Key Features by Module

### Module 1: Authentication & User Management
- **Registration**: Full Name, Email, Username, and Password with instant validation.
- **Cryptographic Security**: Passwords are salted with 16-byte random hex values and hashed using `hashlib.sha256`.
- **Duplicate Prevention**: Rejects duplicate usernames and email addresses.
- **One-Click Demo Mode**: Allows immediate testing with pre-seeded 2nd-year B.Tech CSE coursework (DSA, OS, DBMS, OOP, Computer Architecture).

### Module 2: Executive Dashboard
- **Personalized Header**: Dynamic greeting based on time of day (Good Morning / Afternoon / Evening) with student's first name and live date badge.
- **4 Key Statistic Cards**:
  1. *Total Subjects*: Active courses enrolled.
  2. *Study Hours*: Total hours studied during the current calendar week.
  3. *Completed Tasks*: Total assignments submitted/completed.
  4. *Upcoming Exams*: Live count of scheduled examinations.
- **Embedded Weekly Bar Chart**: Visualizes Monday–Sunday study activity in real time.
- **Interactive Daily Schedule**: Displays today's planned sessions with instant "Mark Done" toggles.
- **Upcoming Deadlines**: Identifies pending assignments with urgency badges.
- **Quick Actions Bar**: Instant modal access to add subjects, study sessions, tasks, or exams.

### Module 3: My Subjects
- **Visual Course Cards**: Display subject name, code, description, and semester.
- **Target vs. Logged Hours**: Automatically sums hours from completed study sessions against the target quota.
- **Syllabus Progress Bars**: Visual completion bar with percentage indicators.
- **Search & Filter**: Real-time filtering by subject name or course code.
- **Subject Management**: Full Add, Edit, and Delete (with confirmation dialog) support.

### Module 4: Study Planner
- **Session Scheduling**: Session title, subject association, date, start time, end time, priority, and notes.
- **Automatic Duration Calculation**: Computes exact decimal hours from 24-hour time inputs (e.g., `14:00` to `16:30` → 2.5 hrs).
- **Time Range Validation**: Enforces valid chronological time intervals.
- **Multi-Filter Controls**: Filter by Date Range (All, Today, This Week, Upcoming, Past), Subject, and Status (Pending, Completed).

### Module 5: Tasks & Assignments
- **Status Tabs**: *All Tasks*, *Pending*, *In Progress*, *Completed*, and *Overdue*.
- **Live Urgency Indicators**: Calculates remaining days and flags tasks as *TODAY*, *TOMORROW*, *X DAYS LEFT*, or *OVERDUE*.
- **Sorting & Priority**: Sort by Due Date, Priority (High, Medium, Low), or Newest.
- **Quick Status Changer**: In-place status dropdown for instant workflow updates.

### Module 6: Exam Countdown
- **Dynamic Countdown Cards**: Displays prominent remaining day counters (e.g., `12 DAYS LEFT`).
- **Urgency Alerts**: Highlights examinations approaching within 7 days using amber warning borders and banners.
- **Exam Types**: Supports Internal Exams, Midterms, End Semesters, Practicals, and Quizzes.
- **Categorized Views**: Separate tabs for *Upcoming Examinations* and *Past Examinations*.

### Module 7: Productivity Analytics
- **Top Metrics**: Total study hours all-time, daily average, most studied course, and task completion percentage.
- **4 Embedded Dark Matplotlib Visualizations**:
  1. *Weekly Activity Bar Chart*: Daily study hours (Mon–Sun).
  2. *Subject Distribution Donut Chart*: Percentage allocation of completed study time per course.
  3. *Monthly Productivity Trend*: 4-week study volume line graph with gradient area fill.
  4. *Task Status Breakdown*: Horizontal breakdown of Completed, In Progress, Pending, and Overdue tasks.
- **Zero-Data State**: Displays informative empty state rather than simulated numbers when data is absent.

### Module 8: Settings & Preferences
- **Student Profile**: View and edit student name, email, and program standing.
- **Password Security**: Change password with current password verification.
- **Appearance Switcher**: Seamless toggle between *Dark Theme* and *Light Theme*, persisted in SQLite.
- **Demo Data Controls**: Instant sample data loader and data reset button with confirmation modals.
- **Session Management**: Secure logout with session teardown.

---

## 4. Technology Stack & Architecture

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.11+ (Tested on 3.14) | Core programming language |
| **GUI Framework** | CustomTkinter 6.0+ | Modern high-DPI desktop widgets & theming |
| **Native Dialogs** | Tkinter & `tkinter.messagebox` | OS-level alerts and modal dialog bindings |
| **Database** | SQLite3 | Local, persistent, ACID-compliant relational storage |
| **Data Visualization** | Matplotlib 3.10+ (`FigureCanvasTkAgg`) | Dark-themed embedded charts |
| **Image Processing** | Pillow 12.0+ (PIL) | High-resolution anti-aliased icon rendering |
| **Security** | Python `hashlib` & `secrets` | SHA-256 password hashing with 16-byte random salts |

### Design System Palette

- **Main Background**: `#101522`
- **Sidebar Background**: `#0B1020`
- **Card Background**: `#1A2233`
- **Secondary Card**: `#202B3D`
- **Primary Accent**: `#7667F8` (SaaS Purple)
- **Secondary Accent**: `#38C98B` (Emerald Green)
- **Warning**: `#F5B84B` (Amber Gold)
- **Danger**: `#F16B75` (Coral Red)
- **Primary Text**: `#F4F6FC`
- **Secondary Text**: `#929CAF`
- **Border**: `#2A3447`

---

## 5. Folder Structure

```text
STUDYSYNC/
├── main.py                     # Application entry point & master coordinator
├── requirements.txt            # Python package dependencies
├── README.md                   # Comprehensive project documentation
├── .gitignore                  # Git ignore rules
├── studysync.db                # SQLite3 persistent relational database
├── test_app.py                 # Core automated test suite
├── test_gui.py                 # GUI lifecycle & navigation verification
├── test_dialogs.py             # Modal dialogs & validation test
│
├── database/
│   ├── __init__.py
│   ├── schema.py               # SQL DDL schemas for all tables
│   └── db_manager.py           # Parameterized CRUD operations & connection manager
│
├── authentication/
│   ├── __init__.py
│   └── auth.py                 # Salt generation, password hashing & session state
│
├── pages/
│   ├── __init__.py
│   ├── login.py                # Authentication login screen
│   ├── register.py             # User registration screen
│   ├── dashboard.py            # Main executive dashboard
│   ├── subjects.py             # Subject & syllabus management
│   ├── planner.py              # Daily & weekly timetable scheduler
│   ├── tasks.py                # Tasks & assignment tracking
│   ├── exams.py                # Exam countdown timers
│   ├── analytics.py            # Productivity analytics & Matplotlib charts
│   └── settings.py             # Profile, appearance & system info
│
├── components/
│   ├── __init__.py
│   ├── sidebar.py              # Fixed left navigation sidebar
│   ├── stat_card.py            # Rounded KPI metric card
│   ├── buttons.py              # Primary, Secondary, Danger, and Icon buttons
│   ├── forms.py                # Form inputs, password eye toggle, dropdowns
│   ├── dialogs.py              # Modal dialogs for adding/editing records
│   └── navigation.py           # Page container controller
│
├── utils/
│   ├── __init__.py
│   ├── theme.py                # Color palette, typography, and ThemeManager
│   ├── date_utils.py           # Date calculations, countdowns, durations
│   ├── validators.py           # Regex-based email, time, date, input validators
│   ├── helpers.py              # Icon caching and formatting utilities
│   └── icon_gen.py             # High-DPI icon generator using Pillow
│
└── assets/
    ├── logo.png                # StudySync application logo
    └── icons/                  # 22 crisp UI icons
```

---

## 6. Database Schema Architecture

The database (`studysync.db`) is normalized and enforces foreign key constraints (`PRAGMA foreign_keys = ON;`):

### 1. `users`
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `username` (TEXT UNIQUE NOT NULL)
- `email` (TEXT UNIQUE NOT NULL)
- `password_hash` (TEXT NOT NULL)
- `salt` (TEXT NOT NULL)
- `full_name` (TEXT NOT NULL)
- `theme` (TEXT DEFAULT 'Dark')
- `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

### 2. `subjects`
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `user_id` (INTEGER NOT NULL, FK → `users(id)` ON DELETE CASCADE)
- `name` (TEXT NOT NULL)
- `code` (TEXT)
- `description` (TEXT)
- `target_hours` (REAL DEFAULT 40.0)
- `syllabus_progress` (REAL DEFAULT 0.0)
- `semester` (TEXT DEFAULT 'Semester 4')
- `color` (TEXT DEFAULT '#7667F8')
- `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

### 3. `study_sessions`
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `user_id` (INTEGER NOT NULL, FK → `users(id)` ON DELETE CASCADE)
- `subject_id` (INTEGER, FK → `subjects(id)` ON DELETE SET NULL)
- `title` (TEXT NOT NULL)
- `study_date` (TEXT NOT NULL, `YYYY-MM-DD`)
- `start_time` (TEXT NOT NULL, `HH:MM`)
- `end_time` (TEXT NOT NULL, `HH:MM`)
- `duration_hours` (REAL NOT NULL)
- `priority` (TEXT DEFAULT 'Medium')
- `description` (TEXT)
- `is_completed` (INTEGER DEFAULT 0)
- `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

### 4. `tasks`
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `user_id` (INTEGER NOT NULL, FK → `users(id)` ON DELETE CASCADE)
- `subject_id` (INTEGER, FK → `subjects(id)` ON DELETE SET NULL)
- `title` (TEXT NOT NULL)
- `description` (TEXT)
- `due_date` (TEXT NOT NULL, `YYYY-MM-DD`)
- `priority` (TEXT DEFAULT 'Medium')
- `status` (TEXT DEFAULT 'Pending')
- `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

### 5. `exams`
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `user_id` (INTEGER NOT NULL, FK → `users(id)` ON DELETE CASCADE)
- `subject_id` (INTEGER, FK → `subjects(id)` ON DELETE SET NULL)
- `name` (TEXT NOT NULL)
- `exam_date` (TEXT NOT NULL, `YYYY-MM-DD`)
- `exam_time` (TEXT DEFAULT '10:00')
- `exam_type` (TEXT DEFAULT 'Internal Exam')
- `notes` (TEXT)
- `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

---

## 7. Installation & Setup Instructions

### Prerequisites
- Python 3.11 or newer installed on Windows, macOS, or Linux.
- `pip` package manager.

### Step 1: Install Dependencies
Open your command terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

### Step 2: Run Automated Verification Tests (Optional)
To verify database, authentication, GUI lifecycle, and dialogs before launching:

```bash
python test_app.py
python test_gui.py
python test_dialogs.py
```

### Step 3: Launch the Application
Run the main script with Python:

```bash
python main.py
```

---

## 8. How to Demonstrate to an Academic Evaluator

1. **Launch**: Execute `python main.py`. The sleek authentication view appears with the StudySync branding hero on the left and login form on the right.
2. **Instant Demo Login**: Click **"Explore with Demo Account"** to bypass manual form filling and immediately load realistic 2nd-year B.Tech CSE coursework (DSA, OS, DBMS, OOP, Computer Architecture).
3. **Explore Dashboard**: Point out the personalized greeting ("Good Evening, Kushagra!"), live date badge, the 4 dynamic statistics cards, the embedded weekly productivity bar chart, interactive today's schedule, and upcoming deadlines.
4. **My Subjects**: Open *My Subjects* to show syllabus progress bars, logged study hours computed dynamically from completed sessions, and the search filter. Click "+ Add Subject" to demonstrate the custom modal dialog.
5. **Study Planner**: Add a study session; show how duration is automatically calculated from start/end times and how clicking "Mark Done" instantly updates the weekly chart.
6. **Tasks & Assignments**: Switch between tabs (*All*, *Pending*, *In Progress*, *Completed*, *Overdue*), demonstrating real-time urgency calculation.
7. **Exam Countdown**: Show upcoming evaluations with live day countdown banners (e.g. `5 DAYS LEFT` in urgent warning styling).
8. **Productivity Analytics**: Review the 4 embedded Matplotlib charts (Weekly bar, Subject allocation donut, 4-week trend line, and Task breakdown).
9. **Settings**: Demonstrate theme switching (Dark to Light mode and back), edit profile, or click "Load Academic Sample Data" / "Clear All My Study Data".
10. **Logout**: Click "Sign Out" to demonstrate confirmation modal and secure session termination.

---

## 9. Academic Credit & Verification

- **Project Title**: STUDYSYNC – SMART STUDENT STUDY PLANNER
- **Candidate Level**: 2nd Year B.Tech Computer Science & Engineering
- **Domain**: Desktop Application Development, Database Systems & UI/UX Engineering
- **Status**: Complete, Fully Functional & Verified
