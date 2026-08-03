from datetime import datetime, time

class AllocationError(Exception):
    """Custom exception for allocation logic errors."""
    pass

class RoomCapacityExceededError(AllocationError):
    pass

class DuplicateAllocationError(AllocationError):
    pass

class FacultyUnavailableError(AllocationError):
    pass

class NoRoomsAvailableError(AllocationError):
    pass

class NoFacultyAvailableError(AllocationError):
    pass

class AttendanceAlreadySubmittedError(AllocationError):
    pass

def times_overlap(start1, end1, start2, end2):
    """Check if two time intervals overlap on the same day."""
    return max(start1, start2) < min(end1, end2)
