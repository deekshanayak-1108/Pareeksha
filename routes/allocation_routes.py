from flask import Blueprint, request, jsonify
from services.student_allocator import allocate_students_for_subject
from services.faculty_allocator import (
    allocate_faculty_to_room,
    accept_faculty_duty,
    decline_faculty_duty
)
from services.attendance_service import get_students_allocated_to_room, save_attendance_records
from services.allocation_utils import AllocationError
from models.models import StudentAllocation, FacultyAllocation

allocation_bp = Blueprint('allocation_api', __name__)

@allocation_bp.route('/allocate/students', methods=['POST'])
def allocate_students():
    data = request.get_json() or {}
    subject_code = data.get('subject_code')
    if not subject_code:
        return jsonify({"error": "subject_code is required"}), 400
    try:
        summary = allocate_students_for_subject(subject_code)
        return jsonify(summary), 200
    except AllocationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error: " + str(e)}), 500

@allocation_bp.route('/allocate/faculty', methods=['POST'])
def allocate_faculty():
    data = request.get_json() or {}
    subject_code = data.get('subject_code')
    room_no = data.get('room_no')
    if not subject_code or not room_no:
        return jsonify({"error": "subject_code and room_no are required"}), 400
    try:
        summary = allocate_faculty_to_room(subject_code, room_no)
        return jsonify(summary), 200
    except AllocationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error: " + str(e)}), 500

@allocation_bp.route('/faculty/accept/<int:allocation_id>', methods=['POST'])
def accept_duty(allocation_id):
    try:
        res = accept_faculty_duty(allocation_id)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@allocation_bp.route('/faculty/decline/<int:allocation_id>', methods=['POST'])
def decline_duty(allocation_id):
    data = request.get_json() or {}
    reason = data.get('reason', 'No reason provided')
    try:
        res = decline_faculty_duty(allocation_id, reason)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@allocation_bp.route('/attendance/save', methods=['POST'])
def save_attendance():
    data = request.get_json() or {}
    room_no = data.get('room_no')
    subject_code = data.get('subject_code')
    records = data.get('records') # list of {"student_id": x, "status": "Present/Absent"}
    if not room_no or not subject_code or not records:
        return jsonify({"error": "room_no, subject_code and records are required"}), 400
    try:
        res = save_attendance_records(room_no, subject_code, records)
        return jsonify(res), 200
    except AllocationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error: " + str(e)}), 500

@allocation_bp.route('/attendance/<room_no>/<subject_code>', methods=['GET'])
def get_attendance(room_no, subject_code):
    try:
        students = get_students_allocated_to_room(room_no, subject_code)
        return jsonify(students), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@allocation_bp.route('/allocation/student', methods=['GET'])
def get_student_allocations():
    allocs = StudentAllocation.query.all()
    result = []
    for a in allocs:
        result.append({
            "id": a.id,
            "student_id": a.student_id,
            "subject_code": a.subject_code,
            "room_no": a.room_no,
            "seat_no": a.seat_no
        })
    return jsonify(result), 200

@allocation_bp.route('/allocation/faculty', methods=['GET'])
def get_faculty_allocations():
    allocs = FacultyAllocation.query.all()
    result = []
    for a in allocs:
        result.append({
            "id": a.id,
            "faculty_id": a.faculty_id,
            "subject_code": a.subject_code,
            "room_no": a.room_no,
            "date": str(a.date),
            "start_time": str(a.start_time),
            "end_time": str(a.end_time),
            "status": a.status,
            "decline_reason": a.decline_reason
        })
    return jsonify(result), 200
