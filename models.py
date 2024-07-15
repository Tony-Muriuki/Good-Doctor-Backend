from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from config import db
import bcrypt

# Define the User model
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)

    appointments = db.relationship('Appointment', back_populates='user', cascade='all, delete-orphan')

    serialize_rules = ('-password_hash', '-appointments.user',)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

# Define the Doctor model
class Doctor(db.Model, SerializerMixin):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)  # Added email field
    password_hash = db.Column(db.String, nullable=False)  # Added password_hash field
    specialty = db.Column(db.String, nullable=False)
    experience_years = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.String, nullable=False)

    appointments = db.relationship('Appointment', back_populates='doctor', cascade='all, delete-orphan')

    serialize_rules = ('-password_hash', '-appointments.doctor',)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

# Define the Appointment model
class Appointment(db.Model, SerializerMixin):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_appointments_user_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', name='fk_appointments_doctor_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String, nullable=False)

    user = db.relationship('User', back_populates='appointments')
    doctor = db.relationship('Doctor', back_populates='appointments')
    prescriptions = db.relationship('Prescription', back_populates='appointment', cascade='all, delete-orphan')
    
    serialize_rules = ('-user.appointments', '-doctor.appointments', '-prescriptions.appointment',)

# Define the Prescription model
class Prescription(db.Model, SerializerMixin):
    __tablename__ = 'prescriptions'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id', name='fk_prescriptions_appointment_id'), nullable=False)
    medicine = db.Column(db.String, nullable=False)
    dosage = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)

    appointment = db.relationship('Appointment', back_populates='prescriptions')

    serialize_rules = ('-appointment.prescriptions',)
