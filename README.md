# Pareeksha Flask Scaffold

This is a premium Flask project scaffold structured using the Application Factory pattern.

## Tech Stack
- **Framework**: Flask
- **ORM & Migrations**: Flask-SQLAlchemy, Flask-Migrate
- **Authentication**: Flask-Login
- **Database Driver**: PyMySQL (MySQL)
- **Deployment**: Gunicorn

## Setup Instructions

1. **Create and Activate Virtual Environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   Copy `.env.example` to `.env` and fill in the required database credentials and secret key:
   ```bash
   copy .env.example .env
   ```

4. **Run Application:**
   ```bash
   flask run
   ```
