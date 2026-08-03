# Pareeksha - Exam Allocation & Invigilation Management System

Pareeksha is a modern, premium College ERP portal built with Python Flask and Bootstrap 5. It features a complete Student & Faculty Seating Allocation Engine, visual Room Layout Editor, dynamic Classroom Blueprint views, and a dedicated Attendance Management system.

---

## 🛠️ Tech Stack
- **Backend:** Python Flask, SQLAlchemy (ORM), Flask-Migrate
- **Frontend:** HTML5, CSS3 (Custom Glassmorphism styling), Bootstrap 5, Vanilla JavaScript, Bootstrap Icons
- **Database:** SQLite (default/development fallback), MySQL (production configuration support)

---

## 📂 Project Structure
```text
Pareeksha/
│
├── app.py                      # Application Factory & Seeding Logic
├── config.py                   # Environment configuration (Dev/Test/Prod)
├── extensions.py               # Extension instances (db, migrate, login)
├── requirements.txt            # Project Dependencies
├── README.md                   # Setup & Instructions
├── .gitignore                  # Git tracking rules
├── .env.example                # Template configuration
│
├── models/
│   └── models.py               # SQLAlchemy Database Schemas
│
├── routes/
│   ├── allocation_routes.py    # JSON APIs for student/faculty allocations & attendance
│   └── frontend_routes.py      # UI Controllers (Login, Dashboards, Blueprints)
│
├── services/
│   ├── student_allocator.py    # Sequential student seating logic
│   ├── faculty_allocator.py    # Invigilation logic & auto-reallocation
│   ├── attendance_service.py   # Student checklists & attendance validations
│   └── allocation_utils.py     # Custom exceptions & collision logic
│
├── templates/                  # Jinja2 HTML templates
│   ├── base.html               # Master layout
│   ├── login.html              # ERP Login with Role Selection
│   ├── admin_dashboard.html    # Admin management panel & triggers
│   ├── faculty_dashboard.html  # Invigilation portal with Accept/Decline flow
│   ├── student_dashboard.html  # Seating location & rules card
│   ├── classroom_blueprint.html# Dynamic classroom grid (Showcase)
│   ├── room_layout_editor.html # Interactive visual seating grid constructor
│   ├── attendance.html         # Classroom checkin
│   └── reports.html            # Exportable lists
│
└── static/
    ├── css/                    # Custom stylesheets (glassmorphism/ERP)
    └── js/                     # Component scripts (blueprints, layout editor)
```

---

## 🚀 Getting Started

Follow these steps to run the application locally on your machine:

### 1. Clone the repository
Make sure you have cloned the repository and navigated to the project root:
```bash
cd Pareeksha
```

### 2. Create and Activate a Virtual Environment
Initialize a clean Python environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install all required backend modules:
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Config
Copy the environment template file:
```bash
copy .env.example .env
```
*(By default, the application will initialize a local SQLite file named `pareeksha.db` on startup if MySQL variables are not configured in your `.env`.)*

### 5. Run the Application
Launch the Flask development server:
```bash
python app.py
```
Or use the Flask CLI:
```bash
flask run --debug
```

Once running, navigate to **`http://127.0.0.1:5000/`** in your browser.

---

## 💡 How to Test the Portals

We have included automated **database seeding** on first boot. When you open the login page, you can choose from three role dashboard mockups:
1. **Student Dashboard:** View custom seating details (e.g., `Room 101`, seat `R101-S1`) and review student guidelines.
2. **Faculty Dashboard:** Accept or decline invigilation duties. Declining a duty prompts you for a reason and instantly triggers **auto-reallocation** to another available teacher on the backend.
3. **Admin Dashboard:** Access overall ERP stats, upload roster CSV templates, or click **"Run Allocator"** to recalculate classroom seating seating allocations dynamically on the fly.
4. **Layout Editor & Blueprint:** Check `/room-editor` to interactively adjust grid parameters and `/blueprint` to render custom CSS Grid classrooms with color-coded seat assignments.
