from extensions import db
from models.models import Faculty, Subject, FacultyAllocation, Room
from services.allocation_utils import FacultyUnavailableError, DuplicateAllocationError, NoFacultyAvailableError, times_overlap
from datetime import datetime

def allocate_faculty_to_room(subject_code, room_no):
    """
    Allocate available faculty to a room for a subject exam.
    Checks availability, max duties limit, and schedule conflicts.
    """
    subject = Subject.query.filter_by(subject_code=subject_code).first()
    if not subject:
        raise ValueError(f"Subject with code {subject_code} not found.")

    # Check if a duty is already assigned for this subject and room
    existing_duty = FacultyAllocation.query.filter_by(
        subject_code=subject_code,
        room_no=room_no
    ).first()
    if existing_duty:
        raise DuplicateAllocationError("Faculty duty already assigned to this room for this exam.")

    # Find all active & available faculty
    faculties = Faculty.query.filter_by(available=True).all()
    
    selected_faculty = None
    for faculty in faculties:
        # Check Max Duties
        duty_count = FacultyAllocation.query.filter_by(
            faculty_id=faculty.id,
            status='Accepted'
        ).count()
        if duty_count >= faculty.max_duties:
            continue

        # Check overlapping schedule conflict on the same date
        has_overlap = False
        existing_allocations = FacultyAllocation.query.filter_by(
            faculty_id=faculty.id,
            date=subject.exam_date
        ).all()
        for alloc in existing_allocations:
            if times_overlap(subject.start_time, subject.end_time, alloc.start_time, alloc.end_time):
                has_overlap = True
                break
        
        if not has_overlap:
            selected_faculty = faculty
            break

    if not selected_faculty:
        raise NoFacultyAvailableError(f"No available/eligible faculty found for Subject {subject_code} in Room {room_no}.")

    # Create allocation
    new_allocation = FacultyAllocation(
        faculty_id=selected_faculty.id,
        subject_code=subject_code,
        room_no=room_no,
        date=subject.exam_date,
        start_time=subject.start_time,
        end_time=subject.end_time,
        status='Pending'
    )
    db.session.add(new_allocation)
    db.session.commit()

    return {
        "allocation_id": new_allocation.id,
        "faculty_id": selected_faculty.id,
        "faculty_name": selected_faculty.name,
        "subject_code": subject_code,
        "room_no": room_no,
        "status": new_allocation.status
    }

def accept_faculty_duty(allocation_id):
    """Marks a faculty allocation duty as Accepted."""
    alloc = FacultyAllocation.query.get(allocation_id)
    if not alloc:
        raise ValueError("Faculty allocation not found.")
    alloc.status = 'Accepted'
    db.session.commit()
    return {"status": "success", "message": "Duty accepted successfully."}

def decline_faculty_duty(allocation_id, reason):
    """
    Marks a faculty allocation duty as Declined, saves the reason,
    and triggers automatic reallocation.
    """
    alloc = FacultyAllocation.query.get(allocation_id)
    if not alloc:
        raise ValueError("Faculty allocation not found.")
    
    alloc.status = 'Declined'
    alloc.decline_reason = reason
    db.session.commit()

    # Trigger auto reallocation
    try:
        reallocated = reallocate_declined_duty(alloc)
        return {
            "status": "success",
            "message": "Duty declined. Successfully reallocated to new faculty.",
            "reallocated": True,
            "new_faculty_name": reallocated["faculty_name"]
        }
    except NoFacultyAvailableError:
        # Notify Admin flow (in real app, send notifications/emails; here we return status)
        return {
            "status": "success",
            "message": "Duty declined. Admin has been notified since no available replacement was found.",
            "reallocated": False
        }

def reallocate_declined_duty(declined_alloc):
    """
    Tries to find another eligible faculty to replace the declined one.
    """
    faculties = Faculty.query.filter_by(available=True).all()
    
    replacement_faculty = None
    for faculty in faculties:
        # Exclude the faculty who just declined
        if faculty.id == declined_alloc.faculty_id:
            continue

        # Check Max Duties
        duty_count = FacultyAllocation.query.filter_by(
            faculty_id=faculty.id,
            status='Accepted'
        ).count()
        if duty_count >= faculty.max_duties:
            continue

        # Check overlapping schedule conflict
        has_overlap = False
        existing_allocations = FacultyAllocation.query.filter_by(
            faculty_id=faculty.id,
            date=declined_alloc.date
        ).all()
        for alloc in existing_allocations:
            if times_overlap(declined_alloc.start_time, declined_alloc.end_time, alloc.start_time, alloc.end_time):
                has_overlap = True
                break

        if not has_overlap:
            replacement_faculty = faculty
            break

    if not replacement_faculty:
        raise NoFacultyAvailableError("No alternative faculty available to take over this duty.")

    # Create new allocation
    new_allocation = FacultyAllocation(
        faculty_id=replacement_faculty.id,
        subject_code=declined_alloc.subject_code,
        room_no=declined_alloc.room_no,
        date=declined_alloc.date,
        start_time=declined_alloc.start_time,
        end_time=declined_alloc.end_time,
        status='Pending'
    )
    db.session.add(new_allocation)
    db.session.commit()

    return {
        "faculty_id": replacement_faculty.id,
        "faculty_name": replacement_faculty.name
    }
