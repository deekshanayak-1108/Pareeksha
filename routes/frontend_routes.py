from flask import Blueprint, render_template, request, redirect, url_for, session
from models.models import Student, Faculty, Room, Subject, StudentAllocation, FacultyAllocation, Attendance

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role', 'student')
        email = request.form.get('email', '')
        
        session['role'] = role
        if role == 'admin':
            session['user_name'] = 'System Administrator'
            return redirect(url_for('frontend.admin_dashboard'))
        elif role == 'faculty':
            session['user_name'] = 'Dr. Smitha Rao (CSE)'
            return redirect(url_for('frontend.faculty_dashboard'))
        else:
            session['user_name'] = 'Deeksha Keshav Nayak (1MS22CS001)'
            return redirect(url_for('frontend.student_dashboard'))
            
    return render_template('login.html')

@frontend_bp.route('/admin')
def admin_dashboard():
    if not session.get('role'):
        session['role'] = 'admin'
        session['user_name'] = 'System Administrator'

    # Load dashboard counts
    stats = {
        "total_students": Student.query.count(),
        "total_faculty": Faculty.query.count(),
        "total_rooms": Room.query.count(),
        "total_subjects": Subject.query.count()
    }
    students = Student.query.limit(10).all()
    faculties = Faculty.query.all()
    rooms = Room.query.all()
    subjects = Subject.query.all()
    return render_template('admin_dashboard.html', stats=stats, students=students, faculties=faculties, rooms=rooms, subjects=subjects)

@frontend_bp.route('/faculty')
def faculty_dashboard():
    if not session.get('role'):
        session['role'] = 'faculty'
        session['user_name'] = 'Dr. Smitha Rao (CSE)'
    duties = FacultyAllocation.query.all()
    return render_template('faculty_dashboard.html', duties=duties)

@frontend_bp.route('/student')
def student_dashboard():
    if not session.get('role'):
        session['role'] = 'student'
        session['user_name'] = 'Deeksha Keshav Nayak (1MS22CS001)'

    # For demo/mockup, query allocations for an arbitrary student (e.g. Student ID 1)
    student = Student.query.first() or Student(name="Deeksha Nayak", usn="1MS22CS001", department="CSE", semester=6)
    allocations = StudentAllocation.query.filter_by(student_id=student.id).all()
    exams = []
    for alloc in allocations:
        subject = Subject.query.filter_by(subject_code=alloc.subject_code).first()
        if subject:
            exams.append({
                "subject_code": subject.subject_code,
                "subject_name": subject.subject_name,
                "exam_date": subject.exam_date,
                "start_time": subject.start_time,
                "end_time": subject.end_time,
                "room_no": alloc.room_no,
                "seat_no": alloc.seat_no
            })
    return render_template('student_dashboard.html', student=student, exams=exams)

@frontend_bp.route('/room-editor')
def room_layout_editor():
    rooms = Room.query.all()
    return render_template('room_layout_editor.html', rooms=rooms)

@frontend_bp.route('/blueprint/<room_no>/<subject_code>')
@frontend_bp.route('/blueprint')
def classroom_blueprint(room_no=None, subject_code=None):
    if not room_no:
        room_no = "101"
    if not subject_code:
        subject_code = "CS601"
        
    room = Room.query.filter_by(room_no=room_no).first() or Room(room_no=room_no, capacity=36, rows=6, columns=6)
    allocations = StudentAllocation.query.filter_by(room_no=room_no, subject_code=subject_code).all()
    
    # Structure allocations by seat for UI Blueprint
    alloc_map = {}
    for a in allocations:
        student = Student.query.get(a.student_id)
        alloc_map[a.seat_no] = {
            "name": student.name if student else "N/A",
            "usn": student.usn if student else "N/A"
        }
        
    return render_template('classroom_blueprint.html', room=room, subject_code=subject_code, alloc_map=alloc_map)

@frontend_bp.route('/attendance-page')
def attendance_page():
    rooms = Room.query.all()
    subjects = Subject.query.all()
    return render_template('attendance.html', rooms=rooms, subjects=subjects)

@frontend_bp.route('/reports')
def reports():
    student_allocs = StudentAllocation.query.all()
    faculty_allocs = FacultyAllocation.query.all()
    return render_template('reports.html', student_allocs=student_allocs, faculty_allocs=faculty_allocs)
