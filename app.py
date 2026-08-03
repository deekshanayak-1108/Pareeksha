import os
from flask import Flask, render_template, redirect, url_for
from config import config_map
from extensions import db, migrate, login_manager
from routes.allocation_routes import allocation_bp
from routes.frontend_routes import frontend_bp

def create_app(config_name=None):
    """Application factory for creating Flask app instance."""
    if not config_name:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    
    # Load configuration
    config_class = config_map.get(config_name, config_map['default'])
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    register_blueprints(app)

    # Home route: redirect to login
    @app.route('/')
    def index():
        return redirect(url_for('frontend.login'))

    # Seed Database on startup
    with app.app_context():
        db.create_all()
        seed_data()

    return app

def register_blueprints(app):
    """Registers blueprints."""
    app.register_blueprint(allocation_bp)
    app.register_blueprint(frontend_bp)

def seed_data():
    """Seeds sample data for testing the allocation engine."""
    from models.models import Student, Faculty, Room, Subject
    
    if Student.query.count() == 0:
        # Create some students
        students = [
            Student(name="Deeksha Keshav Nayak", usn="1MS22CS001", department="CSE", semester=6),
            Student(name="Aditya Sen", usn="1MS22CS002", department="CSE", semester=6),
            Student(name="Riya Sharma", usn="1MS22CS003", department="CSE", semester=6),
            Student(name="Kabir Singh", usn="1MS22CS004", department="CSE", semester=6),
            Student(name="Neha Patel", usn="1MS22CS005", department="CSE", semester=6),
            Student(name="Amit Verma", usn="1MS22CS006", department="CSE", semester=6),
        ]
        db.session.bulk_save_objects(students)
        
    if Faculty.query.count() == 0:
        faculties = [
            Faculty(name="Dr. Smitha Rao", department="CSE", max_duties=3, available=True),
            Faculty(name="Prof. Rajesh Kumar", department="CSE", max_duties=2, available=True),
            Faculty(name="Dr. Anna Johnson", department="ECE", max_duties=4, available=True),
        ]
        db.session.bulk_save_objects(faculties)
        
    if Room.query.count() == 0:
        rooms = [
            Room(room_no="101", capacity=4, rows=2, columns=2),
            Room(room_no="102", capacity=30, rows=6, columns=5),
            Room(room_no="201", capacity=40, rows=8, columns=5),
        ]
        db.session.bulk_save_objects(rooms)
        
    if Subject.query.count() == 0:
        from datetime import datetime, date, time
        subjects = [
            Subject(
                subject_code="CS601",
                subject_name="Software Engineering",
                department="CSE",
                semester=6,
                exam_date=date(2026, 8, 10),
                start_time=time(9, 30),
                end_time=time(12, 30)
            ),
            Subject(
                subject_code="CS602",
                subject_name="Computer Networks",
                department="CSE",
                semester=6,
                exam_date=date(2026, 8, 12),
                start_time=time(9, 30),
                end_time=time(12, 30)
            )
        ]
        db.session.bulk_save_objects(subjects)
    
    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

