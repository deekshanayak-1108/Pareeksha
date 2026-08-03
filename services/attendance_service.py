from extensions import db
from models.models import Attendance, StudentAllocation, Student
from services.allocation_utils import AttendanceAlreadySubmittedError

def get_students_allocated_to_room(room_no, subject_code):
    """Retrieves list of students allocated to a specific room for a subject."""
    allocations = StudentAllocation.query.filter_by(
        room_no=room_no,
        subject_code=subject_code
    ).all()
    
    student_list = []
    for alloc in allocations:
        student = Student.query.get(alloc.student_id)
        if student:
            # Check if attendance is already marked
            att = Attendance.query.filter_by(
                student_id=student.id,
                subject_code=subject_code,
                room_no=room_no
            ).first()
            
            student_list.append({
                "student_id": student.id,
                "name": student.name,
                "usn": student.usn,
                "seat_no": alloc.seat_no,
                "attendance_status": att.status if att else None
            })
            
    return student_list

def save_attendance_records(room_no, subject_code, records):
    """
    Saves student attendance records.
    records is a list of dicts: [{"student_id": 1, "status": "Present"}]
    """
    saved_count = 0
    for record in records:
        student_id = record.get("student_id")
        status = record.get("status") # Present, Absent
        
        # Check if already submitted
        existing = Attendance.query.filter_by(
            student_id=student_id,
            subject_code=subject_code,
            room_no=room_no
        ).first()
        
        if existing:
            # Update status instead of throwing error if they want to override,
            # but per requirements: "Prevent duplicate attendance submission"
            # We will raise an error or ignore if already marked depending on preference.
            # Let's enforce prevention of duplicate submission.
            raise AttendanceAlreadySubmittedError(f"Attendance already submitted for student ID {student_id}.")

        attendance = Attendance(
            student_id=student_id,
            subject_code=subject_code,
            room_no=room_no,
            status=status
        )
        db.session.add(attendance)
        saved_count += 1
        
    db.session.commit()
    return {"status": "success", "saved_records": saved_count}
