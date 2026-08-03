from extensions import db
from models.models import Student, Room, Subject, StudentAllocation
from services.allocation_utils import RoomCapacityExceededError, DuplicateAllocationError, NoRoomsAvailableError

def allocate_students_for_subject(subject_code):
    """
    Allocates students belonging to the same department and semester as the subject.
    Room capacity constraints are strictly respected.
    """
    # Fetch Subject
    subject = Subject.query.filter_by(subject_code=subject_code).first()
    if not subject:
        raise ValueError(f"Subject with code {subject_code} not found.")

    # Find eligible students (same department and semester)
    eligible_students = Student.query.filter_by(
        department=subject.department,
        semester=subject.semester
    ).all()

    if not eligible_students:
        return {"total_students": 0, "total_rooms_used": 0, "total_seats_allocated": 0}

    # Fetch available rooms
    rooms = Room.query.all()
    if not rooms:
        raise NoRoomsAvailableError("No exam rooms exist in the system.")

    allocated_count = 0
    rooms_used = set()
    
    # Track current room & seat index
    room_idx = 0
    current_room = rooms[room_idx]
    current_room_capacity = current_room.capacity
    current_room_allocated = StudentAllocation.query.filter_by(room_no=current_room.room_no, subject_code=subject_code).count()

    for student in eligible_students:
        # Check if already allocated for this subject
        existing = StudentAllocation.query.filter_by(
            student_id=student.id,
            subject_code=subject_code
        ).first()
        if existing:
            continue

        # Find next available room that has capacity
        while current_room_allocated >= current_room_capacity:
            room_idx += 1
            if room_idx >= len(rooms):
                raise RoomCapacityExceededError("Not enough room capacity for all eligible students.")
            current_room = rooms[room_idx]
            current_room_capacity = current_room.capacity
            current_room_allocated = StudentAllocation.query.filter_by(room_no=current_room.room_no, subject_code=subject_code).count()

        # Allocate seat sequentially
        seat_no = f"R{current_room.room_no}-S{current_room_allocated + 1}"
        
        allocation = StudentAllocation(
            student_id=student.id,
            subject_code=subject_code,
            room_no=current_room.room_no,
            seat_no=seat_no
        )
        db.session.add(allocation)
        allocated_count += 1
        current_room_allocated += 1
        rooms_used.add(current_room.room_no)

    db.session.commit()

    return {
        "total_students": len(eligible_students),
        "total_rooms_used": len(rooms_used),
        "total_seats_allocated": allocated_count
    }
