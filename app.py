from __init__ import app, db
from flask import render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from models import User, Patient, Doctor, ICURoom, ICUAdmission, MedicalRecord, Appointment, VitalSigns

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        
        # Check if user already exists
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('Username already exists')
            return redirect(url_for('register'))
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password, user_type=user_type)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            
            # If user is a patient or doctor, redirect to complete profile
            if user_type == 'patient':
                return redirect(url_for('complete_patient_profile', user_id=new_user.id))
            elif user_type == 'doctor':
                return redirect(url_for('complete_doctor_profile', user_id=new_user.id))
            
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except:
            flash('There was an issue with registration')
            return redirect(url_for('register'))
    
    return render_template('auth/register.html')

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_type'] = user.user_type
            
            flash('Login successful!')
            
            # Redirect based on user type
            if user.user_type == 'patient':
                patient = Patient.query.filter_by(user_id=user.id).first()
                if patient:
                    return redirect(url_for('patient_profile', patient_id=patient.id))
                else:
                    return redirect(url_for('complete_patient_profile', user_id=user.id))
            elif user.user_type == 'doctor':
                doctor = Doctor.query.filter_by(user_id=user.id).first()
                if doctor:
                    return redirect(url_for('doctor_profile', doctor_id=doctor.id))
                else:
                    return redirect(url_for('complete_doctor_profile', user_id=user.id))
            else:
                return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password')
            
    return render_template('auth/login.html')

# Patient profile setup
@app.route('/complete-patient-profile/<int:user_id>', methods=['GET', 'POST'])
def complete_patient_profile(user_id):
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        blood_group = request.form['blood_group']
        phone = request.form['phone']
        address = request.form['address']
        
        # Handle photo upload
        photo = None
        if 'photo' in request.files and request.files['photo'].filename != '':
            photo_file = request.files['photo']
            filename = secure_filename(f"patient_{user_id}_{photo_file.filename}")
            photo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo = filename
        
        new_patient = Patient(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
            blood_group=blood_group,
            phone=phone,
            address=address,
            photo=photo
        )
        
        try:
            db.session.add(new_patient)
            db.session.commit()
            flash('Profile completed successfully!')
            return redirect(url_for('patient_profile', patient_id=new_patient.id))
        except:
            flash('There was an issue completing your profile')
            
    return render_template('profiles/complete_patient_profile.html')

# Doctor profile setup
@app.route('/complete-doctor-profile/<int:user_id>', methods=['GET', 'POST'])
def complete_doctor_profile(user_id):
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        specialization = request.form['specialization']
        qualification = request.form['qualification']
        experience = request.form['experience']
        phone = request.form['phone']
        
        # Handle photo upload
        photo = None
        if 'photo' in request.files and request.files['photo'].filename != '':
            photo_file = request.files['photo']
            filename = secure_filename(f"doctor_{user_id}_{photo_file.filename}")
            photo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo = filename
        
        new_doctor = Doctor(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            specialization=specialization,
            qualification=qualification,
            experience=experience,
            phone=phone,
            photo=photo
        )
        
        try:
            db.session.add(new_doctor)
            db.session.commit()
            flash('Profile completed successfully!')
            return redirect(url_for('doctor_profile', doctor_id=new_doctor.id))
        except:
            flash('There was an issue completing your profile')
            
    return render_template('profiles/complete_doctor_profile.html')

# Patient profile page
@app.route('/patient/<int:patient_id>')
def patient_profile(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template('profiles/patient_profile.html', patient=patient)

# Doctor profile page
@app.route('/doctor/<int:doctor_id>')
def doctor_profile(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    return render_template('profiles/doctor_profile.html', doctor=doctor)

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
