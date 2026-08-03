function triggerStudentAllocation() {
    const subject = document.getElementById('student-alloc-subject').value;
    const resultDiv = document.getElementById('student-alloc-result');
    resultDiv.innerHTML = '<div class="spinner-border spinner-border-sm text-primary"></div> Allocating...';
    
    fetch('/allocate/students', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ subject_code: subject })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            resultDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
        } else {
            resultDiv.innerHTML = `<div class="alert alert-success">Successfully allocated ${data.total_seats_allocated} seats across ${data.total_rooms_used} rooms!</div>`;
        }
    })
    .catch(err => {
        resultDiv.innerHTML = `<div class="alert alert-danger">Error running allocation.</div>`;
    });
}

function triggerFacultyAllocation() {
    const subject = document.getElementById('faculty-alloc-subject').value;
    const room = document.getElementById('faculty-alloc-room').value;
    const resultDiv = document.getElementById('faculty-alloc-result');
    resultDiv.innerHTML = '<div class="spinner-border spinner-border-sm text-success"></div> Assigning...';
    
    fetch('/allocate/faculty', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ subject_code: subject, room_no: room })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            resultDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
        } else {
            resultDiv.innerHTML = `<div class="alert alert-success">Assigned duty to ${data.faculty_name} in Room ${data.room_no}.</div>`;
        }
    })
    .catch(err => {
        resultDiv.innerHTML = `<div class="alert alert-danger">Error assigning duty.</div>`;
    });
}

function acceptDuty(id) {
    fetch(`/faculty/accept/${id}`, {
        method: 'POST'
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert('Duty accepted successfully!');
            location.reload();
        }
    });
}

function openDeclineModal(id) {
    document.getElementById('decline-allocation-id').value = id;
    const myModal = new bootstrap.Modal(document.getElementById('declineModal'));
    myModal.show();
}

function submitDecline() {
    const id = document.getElementById('decline-allocation-id').value;
    const reason = document.getElementById('decline-reason').value;
    
    if (!reason.trim()) {
        alert('Please enter a decline reason.');
        return;
    }
    
    fetch(`/faculty/decline/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ reason: reason })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert(data.message);
            location.reload();
        }
    });
}
