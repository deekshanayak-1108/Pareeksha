function toggleViewMode() {
    const isStudent = document.getElementById('studentView').checked;
    const details = document.querySelectorAll('.faculty-details');
    
    details.forEach(detail => {
        if (isStudent) {
            detail.style.display = 'none';
        } else {
            detail.style.display = 'block';
        }
    });
}

function seatClicked(element) {
    const seatCode = element.getAttribute('data-seat');
    const isFaculty = document.getElementById('facultyView').checked;
    
    if (isFaculty) {
        // Allow faculty to click on seat to toggle attendance
        if (element.classList.contains('bg-success') || element.classList.contains('bg-primary')) {
            // Toggle local class as demo for attendance marking
            if (element.style.opacity === '0.5') {
                element.style.opacity = '1';
                alert(`Marked seat ${seatCode} as Present.`);
            } else {
                element.style.opacity = '0.5';
                alert(`Marked seat ${seatCode} as Absent.`);
            }
        }
    } else {
        alert(`You selected Seat: ${seatCode}`);
    }
}
