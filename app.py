from flask import Flask, request, session, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from config import db
from models import User, Doctor, Appointment, Prescription
from datetime import datetime 


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# Authentication and User Management
class Signup(Resource):
    def post(self):
        data = request.get_json()
        new_user = User(
            name=data['name'],
            email=data['email'],
            age=data['age'],
            gender=data['gender'],
            phone_number=data['phone_number']
        )
        new_user.password = data['password']
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict(), 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and user.verify_password(data['password']):
            session['user_id'] = user.id
            return user.to_dict(), 200
        return {'error': 'Invalid credentials'}, 401

class DoctorLogin(Resource):
    def post(self):
        data = request.get_json()
        doctor = Doctor.query.filter_by(email=data['email']).first()
        if doctor and doctor.verify_password(data['password']):
            session['doctor_id'] = doctor.id
            return doctor.to_dict(), 200
        return {'error': 'Invalid credentials'}, 401

class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        session.pop('doctor_id', None)
        return {}, 204

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        doctor_id = session.get('doctor_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200
        elif doctor_id:
            doctor = Doctor.query.get(doctor_id)
            if doctor:
                return doctor.to_dict(), 200
        return {}, 204

class ClearSession(Resource):
    def delete(self):
        session.clear()
        return {}, 204

# User Resource
class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200
            return {'error': 'User not found'}, 404
        users = User.query.all()
        return [user.to_dict() for user in users], 200

    def put(self, user_id):
        data = request.get_json()
        user = User.query.get(user_id)
        if user:
            user.name = data['name']
            user.email = data['email']
            user.age = data['age']
            user.gender = data['gender']
            user.phone_number = data['phone_number']
            if 'password' in data:
                user.password = data['password']
            db.session.commit()
            return user.to_dict(), 200
        return {'error': 'User not found'}, 404

# Doctor Resource
class DoctorResource(Resource):
    def get(self, doctor_id=None):
        if doctor_id:
            doctor = Doctor.query.get(doctor_id)
            if doctor:
                return doctor.to_dict(), 200
            return {'error': 'Doctor not found'}, 404
        doctors = Doctor.query.all()
        return [doctor.to_dict() for doctor in doctors], 200

    def post(self):
        data = request.get_json()
        new_doctor = Doctor(
            name=data['name'],
            email=data['email'],
            specialty=data['specialty'],
            experience_years=data['experience_years'],
            availability=data['availability']
        )
        new_doctor.password = data['password']
        db.session.add(new_doctor)
        db.session.commit()
        return new_doctor.to_dict(), 201

# Appointment Resource
class AppointmentResource(Resource):
    def get(self, appointment_id=None):
        if appointment_id:
            appointment = Appointment.query.get(appointment_id)
            if appointment:
                return appointment.to_dict(), 200
            return {'error': 'Appointment not found'}, 404
        appointments = Appointment.query.all()
        return [appointment.to_dict() for appointment in appointments], 200

    def post(self):
        try:
            data = request.get_json()
            date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
            time_obj = datetime.strptime(data['time'], '%H:%M').time()

            new_appointment = Appointment(
                user_id=data['user_id'],
                doctor_id=data['doctor_id'],
                date=date_obj,
                time=time_obj,
                status=data['status']
            )

            db.session.add(new_appointment)
            db.session.commit()
            return new_appointment.to_dict(), 201
        except Exception as e:
            print(f"Error: {e}")  # Debug log
            return {'error': 'Failed to create appointment', 'message': str(e)}, 400

    def put(self, appointment_id):
        try:
            data = request.get_json()
            appointment = Appointment.query.get(appointment_id)
            if appointment:
                appointment.user_id = data['user_id']
                appointment.doctor_id = data['doctor_id']
                appointment.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
                appointment.time = datetime.strptime(data['time'], '%H:%M').time()
                appointment.status = data['status']
                db.session.commit()
                return appointment.to_dict(), 200
            return {'error': 'Appointment not found'}, 404
        except Exception as e:
            print(f"Error: {e}")  # Debug log
            return {'error': 'Failed to update appointment', 'message': str(e)}, 400

    def delete(self, appointment_id):
        appointment = Appointment.query.get(appointment_id)
        if appointment:
            db.session.delete(appointment)
            db.session.commit()
            return {}, 204
        return {'error': 'Appointment not found'}, 404

# Prescription Resource
class PrescriptionResource(Resource):
    def get(self, prescription_id=None):
        if prescription_id:
            prescription = Prescription.query.get(prescription_id)
            if prescription:
                return prescription.to_dict(), 200
            return {'error': 'Prescription not found'}, 404
        prescriptions = Prescription.query.all()
        return [prescription.to_dict() for prescription in prescriptions], 200

    def post(self):
        data = request.get_json()
        new_prescription = Prescription(
            appointment_id=data['appointment_id'],
            medicine=data['medicine'],
            dosage=data['dosage'],
            instructions=data['instructions']
        )
        db.session.add(new_prescription)
        db.session.commit()
        return new_prescription.to_dict(), 201

    def put(self, prescription_id):
        data = request.get_json()
        prescription = Prescription.query.get(prescription_id)
        if prescription:
            prescription.appointment_id = data['appointment_id']
            prescription.medicine = data['medicine']
            prescription.dosage = data['dosage']
            prescription.instructions = data['instructions']
            db.session.commit()
            return prescription.to_dict(), 200
        return {'error': 'Prescription not found'}, 404

    def delete(self, prescription_id):
        prescription = Prescription.query.get(prescription_id)
        if prescription:
            db.session.delete(prescription)
            db.session.commit()
            return {}, 204
        return {'error': 'Prescription not found'}, 404

# Register resources with the API
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(DoctorLogin, '/doctor_login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')
api.add_resource(ClearSession, '/clear')
api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(DoctorResource, '/doctors', '/doctors/<int:doctor_id>')
api.add_resource(AppointmentResource, '/appointments', '/appointments/<int:appointment_id>', '/appointments/user/<int:user_id>', '/appointments/doctor/<int:doctor_id>')
api.add_resource(PrescriptionResource, '/prescriptions', '/prescriptions/<int:prescription_id>')

if __name__ == '__main__':
    app.run(debug=True)
