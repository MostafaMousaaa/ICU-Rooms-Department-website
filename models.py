from __init__ import db  # Use absolute import
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'patient', 'doctor', 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    blood_group = db.Column(db.String(10))
    phone = db.Column(db.String(20))  # This field might still be named "phone" not "primary_phone"
    address = db.Column(db.String(200))
    photo = db.Column(db.String(200))  # File path to photo
    
    # Relationships
    user = db.relationship('User', backref='patient_profile')
    admissions = db.relationship('ICUAdmission', backref='patient', lazy=True)
    medical_records = db.relationship('MedicalRecord', backref='patient', lazy=True)
    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    
    def __repr__(self):
        return f'<Patient {self.first_name} {self.last_name}>'

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(200))
    experience = db.Column(db.Integer)  # Years of experience
    phone = db.Column(db.String(20))
    photo = db.Column(db.String(200))  # File path to photo
    
    # Relationships
    user = db.relationship('User', backref='doctor_profile')
    admissions = db.relationship('ICUAdmission', backref='doctor', lazy=True)
    medical_records = db.relationship('MedicalRecord', backref='doctor', lazy=True)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    
    def __repr__(self):
        return f'<Doctor {self.first_name} {self.last_name}>'

class ICURoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(20), nullable=False, unique=True)
    capacity = db.Column(db.Integer, nullable=False, default=1)
    is_available = db.Column(db.Boolean, default=True)
    equipment = db.Column(db.Text)  # Equipment in the room
    
    # Relationships
    admissions = db.relationship('ICUAdmission', backref='room', lazy=True)
    
    def __repr__(self):
        return f'<ICURoom {self.room_number}>'

class ICUAdmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('icu_room.id'), nullable=False)
    admission_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    discharge_date = db.Column(db.DateTime)
    diagnosis = db.Column(db.Text)
    treatment_plan = db.Column(db.Text)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<ICUAdmission {self.id}>'

class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    symptoms = db.Column(db.Text)
    diagnosis = db.Column(db.Text)
    treatment = db.Column(db.Text)
    medications = db.Column(db.Text)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<MedicalRecord {self.id}>'

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    purpose = db.Column(db.String(200))
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, canceled
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Appointment {self.id}>'

class VitalSigns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    admission_id = db.Column(db.Integer, db.ForeignKey('icu_admission.id'))
    recorded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(db.Float)
    blood_pressure = db.Column(db.String(20))
    heart_rate = db.Column(db.Integer)
    respiratory_rate = db.Column(db.Integer)
    oxygen_saturation = db.Column(db.Float)
    notes = db.Column(db.Text)
    
    # Relationships
    patient = db.relationship('Patient', backref='vital_signs')
    admission = db.relationship('ICUAdmission', backref='vital_signs')
    recorder = db.relationship('User', backref='recorded_vitals')
    
    def __repr__(self):
        return f'<VitalSigns {self.id}>'
