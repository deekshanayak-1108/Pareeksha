import csv
import io
from flask import Blueprint, request, redirect, url_for, flash, jsonify
from extensions import db
from models.models import Student, Faculty, Room, Subject
from datetime import datetime

admin_bp = Blueprint('admin_api', __name__, url_prefix='/admin')

@admin_bp.route('/upload/<data_type>', methods=['POST'])
def upload_csv(data_type):
    if 'file' not in request.files:
        flash('No file selected', 'danger')
        return redirect(url_for('frontend.admin_dashboard'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('frontend.admin_dashboard'))
    
    try:
        stream = io.StringIO(file.stream.read().decode("UTF-8"), newline=None)
        csv_reader = csv.DictReader(stream)
        count = 0
        
        if data_type == 'students':
            for row in csv_reader:
                name = row.get('name')
                usn = row.get('usn')
                department = row.get('department', 'CSE')
                semester = int(row.get('semester', 6))
                if name and usn:
                    existing = Student.query.filter_by(usn=usn).first()
                    if not existing:
                        db.session.add(Student(name=name, usn=usn, department=department, semester=semester))
                        count += 1
                        
        elif data_type == 'faculty':
            for row in csv_reader:
                name = row.get('name')
                department = row.get('department', 'CSE')
                max_duties = int(row.get('max_duties', 3))
                if name:
                    db.session.add(Faculty(name=name, department=department, max_duties=max_duties))
                    count += 1
                    
        elif data_type == 'rooms':
            for row in csv_reader:
                room_no = row.get('room_no')
                capacity = int(row.get('capacity', 36))
                rows = int(row.get('rows', 6))
                columns = int(row.get('columns', 6))
                if room_no:
                    existing = Room.query.filter_by(room_no=room_no).first()
                    if not existing:
                        db.session.add(Room(room_no=room_no, capacity=capacity, rows=rows, columns=columns))
                        count += 1
                        
        elif data_type == 'subjects':
            for row in csv_reader:
                subject_code = row.get('subject_code')
                subject_name = row.get('subject_name')
                department = row.get('department', 'CSE')
                semester = int(row.get('semester', 6))
                exam_date_str = row.get('exam_date', '2026-08-10')
                start_time_str = row.get('start_time', '09:30')
                end_time_str = row.get('end_time', '12:30')
                
                exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date()
                start_time = datetime.strptime(start_time_str, '%H:%M').time()
                end_time = datetime.strptime(end_time_str, '%H:%M').time()
                
                if subject_code and subject_name:
                    existing = Subject.query.filter_by(subject_code=subject_code).first()
                    if not existing:
                        db.session.add(Subject(
                            subject_code=subject_code,
                            subject_name=subject_name,
                            department=department,
                            semester=semester,
                            exam_date=exam_date,
                            start_time=start_time,
                            end_time=end_time
                        ))
                        count += 1
                        
        db.session.commit()
        flash(f'Successfully imported {count} {data_type} records!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error processing CSV: {str(e)}', 'danger')
        
    return redirect(url_for('frontend.admin_dashboard'))

@admin_bp.route('/add/<data_type>', methods=['POST'])
def add_record(data_type):
    try:
        if data_type == 'students':
            name = request.form.get('name')
            usn = request.form.get('usn')
            dept = request.form.get('department')
            sem = int(request.form.get('semester', 6))
            db.session.add(Student(name=name, usn=usn, department=dept, semester=sem))
            
        elif data_type == 'faculty':
            name = request.form.get('name')
            dept = request.form.get('department')
            max_duties = int(request.form.get('max_duties', 3))
            db.session.add(Faculty(name=name, department=dept, max_duties=max_duties))
            
        elif data_type == 'rooms':
            room_no = request.form.get('room_no')
            capacity = int(request.form.get('capacity', 36))
            rows = int(request.form.get('rows', 6))
            columns = int(request.form.get('columns', 6))
            db.session.add(Room(room_no=room_no, capacity=capacity, rows=rows, columns=columns))
            
        elif data_type == 'subjects':
            code = request.form.get('subject_code')
            name = request.form.get('subject_name')
            dept = request.form.get('department')
            sem = int(request.form.get('semester', 6))
            exam_date = datetime.strptime(request.form.get('exam_date'), '%Y-%m-%d').date()
            start_time = datetime.strptime(request.form.get('start_time'), '%H:%M').time()
            end_time = datetime.strptime(request.form.get('end_time'), '%H:%M').time()
            db.session.add(Subject(
                subject_code=code, subject_name=name, department=dept,
                semester=sem, exam_date=exam_date, start_time=start_time, end_time=end_time
            ))
            
        db.session.commit()
        flash(f'{data_type.capitalize()} record added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding record: {str(e)}', 'danger')
        
    return redirect(url_for('frontend.admin_dashboard'))

@admin_bp.route('/edit/<data_type>/<int:record_id>', methods=['POST'])
def edit_record(data_type, record_id):
    try:
        if data_type == 'students':
            item = Student.query.get_or_404(record_id)
            item.name = request.form.get('name')
            item.usn = request.form.get('usn')
            item.department = request.form.get('department')
            item.semester = int(request.form.get('semester', 6))
            
        elif data_type == 'faculty':
            item = Faculty.query.get_or_404(record_id)
            item.name = request.form.get('name')
            item.department = request.form.get('department')
            item.max_duties = int(request.form.get('max_duties', 3))
            
        elif data_type == 'rooms':
            item = Room.query.get_or_404(record_id)
            item.room_no = request.form.get('room_no')
            item.capacity = int(request.form.get('capacity', 36))
            item.rows = int(request.form.get('rows', 6))
            item.columns = int(request.form.get('columns', 6))
            
        elif data_type == 'subjects':
            item = Subject.query.get_or_404(record_id)
            item.subject_code = request.form.get('subject_code')
            item.subject_name = request.form.get('subject_name')
            item.department = request.form.get('department')
            item.semester = int(request.form.get('semester', 6))
            item.exam_date = datetime.strptime(request.form.get('exam_date'), '%Y-%m-%d').date()
            item.start_time = datetime.strptime(request.form.get('start_time'), '%H:%M').time()
            item.end_time = datetime.strptime(request.form.get('end_time'), '%H:%M').time()
            
        db.session.commit()
        flash(f'Record updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating record: {str(e)}', 'danger')
        
    return redirect(url_for('frontend.admin_dashboard'))

@admin_bp.route('/delete/<data_type>/<int:record_id>', methods=['POST'])
def delete_record(data_type, record_id):
    try:
        if data_type == 'students':
            item = Student.query.get_or_404(record_id)
        elif data_type == 'faculty':
            item = Faculty.query.get_or_404(record_id)
        elif data_type == 'rooms':
            item = Room.query.get_or_404(record_id)
        elif data_type == 'subjects':
            item = Subject.query.get_or_404(record_id)
            
        db.session.delete(item)
        db.session.commit()
        flash(f'Record deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting record: {str(e)}', 'danger')
        
    return redirect(url_for('frontend.admin_dashboard'))
