from extensions import db
from datetime import datetime

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    usn = db.Column(db.String(20), unique=True, nullable=False)
    department = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    
    allocations = db.relationship('StudentAllocation', backref='student', lazy=True)
    attendance = db.relationship('Attendance', backref='student', lazy=True)

class Faculty(db.Model):
    __tablename__ = 'faculty'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    max_duties = db.Column(db.Integer, default=3, nullable=False)
    available = db.Column(db.Boolean, default=True, nullable=False)
    
    allocations = db.relationship('FacultyAllocation', backref='faculty', lazy=True)

class Room(db.Model):
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    room_no = db.Column(db.String(20), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    rows = db.Column(db.Integer, nullable=False)
    columns = db.Column(db.Integer, nullable=False)
    layout_json = db.Column(db.Text, nullable=True) # stores structural positions: blackboard, door, walkways

class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(20), unique=True, nullable=False)
    subject_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    exam_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

class StudentAllocation(db.Model):
    __tablename__ = 'student_allocations'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject_code = db.Column(db.String(20), nullable=False)
    room_no = db.Column(db.String(20), nullable=False)
    seat_no = db.Column(db.String(20), nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('student_id', 'subject_code', name='_student_subject_allocation_uc'),
    )

class FacultyAllocation(db.Model):
    __tablename__ = 'faculty_allocations'
    
    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    subject_code = db.Column(db.String(20), nullable=False)
    room_no = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False) # Pending, Accepted, Declined
    decline_reason = db.Column(db.String(255), nullable=True)
    
    __table_args__ = (
        db.UniqueConstraint('faculty_id', 'subject_code', 'date', 'start_time', name='_faculty_schedule_duty_uc'),
    )

class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject_code = db.Column(db.String(20), nullable=False)
    room_no = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False) # Present, Absent
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('student_id', 'subject_code', 'room_no', name='_student_attendance_uc'),
    )
