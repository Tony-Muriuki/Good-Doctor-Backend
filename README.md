# GOOD-DOCTOR Management System




# Overview
This project is a Healthcare Management System designed to manage users, doctors, appointments, and prescriptions. It provides a RESTful API for managing these entities with functionalities for user and doctor authentication, session management, and CRUD operations on users, doctors, appointments, and prescriptions.

# Features
User Management: Sign up, log in, update, and retrieve user details.
Doctor Management: Doctor login, update, and retrieve doctor details.
Appointment Management: Create, update, delete, and retrieve appointments.
Prescription Management: Create, update, delete, and retrieve prescriptions.
Session Management: Check, clear, and logout sessions for users and doctors.
CORS Support: Enables Cross-Origin Resource Sharing for the API.
Technologies Used
Flask: Web framework used for creating the API.
Flask-RESTful: Extension for creating RESTful APIs.
Flask-Migrate: Extension for handling database migrations.
Flask-CORS: Extension for handling Cross-Origin Resource Sharing (CORS).
SQLAlchemy: ORM for database interaction.
SQLite: Database used for storage.
bcrypt: Library for hashing passwords.


# Project-Structure
.
├── app.py                  # Main application file
├── config.py               # Configuration file for the database
├── models.py               # Database models
├── seed.py                 # Script for seeding the database with initial data
├── README.md               # This

# Installation
Clone the repository:

git clone https://github.com/KellyAineah/good-Doctor.git

cd good-Doctor.git

Create and activate a virtual environment (optional):

python -m venv venv
source venv/bin/activate  

# Install The Dependecies

pip install -r requirements.txt


# Set Up The Database
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
Seed the database (optional):
python seed.py


# Run The Application

flask run
The application will be available at http://127.0.0.1:5000.

# API Endpoints
Authentication and User Management
Sign Up: POST /signup

Request Body: { "name": "string", "email": "string", "password": "string", "age": "int", "gender": "string", "phone_number": "string" }
Response: 201 Created
Login: POST /login

Request Body: { "email": "string", "password": "string" }
Response: 200 OK
Doctor Login: POST /doctor_login

Request Body: { "email": "string", "password": "string" }
Response: 200 OK
Logout: DELETE /logout

Response: 204 No Content
Check Session: GET /check_session

Response: 200 OK
Clear Session: DELETE /clear

Response: 204 No Content
User Resource
Get All Users: GET /users

Response: 200 OK
Get User by ID: GET /users/<int:user_id>

Response: 200 OK
Update User: PUT /users/<int:user_id>

Request Body: { "name": "string", "email": "string", "age": "int", "gender": "string", "phone_number": "string", "password": "string" (optional) }
Response: 200 OK
Doctor Resource
Get All Doctors: GET /doctors

Response: 200 OK
Get Doctor by ID: GET /doctors/<int:doctor_id>

Response: 200 OK
Create Doctor: POST /doctors

Request Body: { "name": "string", "email": "string", "password": "string", "specialty": "string", "experience_years": "int", "availability": "string" }
Response: 201 Created
Appointment Resource
Get All Appointments: GET /appointments

Response: 200 OK
Get Appointment by ID: GET /appointments/<int:appointment_id>

Response: 200 OK
Create Appointment: POST /appointments

Request Body: { "user_id": "int", "doctor_id": "int", "date": "string (YYYY-MM-DD)", "time": "string (HH:MM)", "status": "string" }
Response: 201 Created
Update Appointment: PUT /appointments/<int:appointment_id>

Request Body: { "user_id": "int", "doctor_id": "int", "date": "string (YYYY-MM-DD)", "time": "string (HH:MM)", "status": "string" }
Response: 200 OK
Delete Appointment: DELETE /appointments/<int:appointment_id>

Response: 204 No Content
Prescription Resource
Get All Prescriptions: GET /prescriptions

Response: 200 OK
Get Prescription by ID: GET /prescriptions/<int:prescription_id>

Response: 200 OK
Create Prescription: POST /prescriptions

Request Body: { "appointment_id": "int", "medicine": "string", "dosage": "string", "instructions": "string" }
Response: 201 Created
Update Prescription: PUT /prescriptions/<int:prescription_id>

Request Body: { "appointment_id": "int", "medicine": "string", "dosage": "string", "instructions": "string" }
Response: 200 OK
Delete Prescription: DELETE /prescriptions/<int:prescription_id>

Response: 204 No Content

# Database Models

# User
id: Integer, Primary Key
name: String, Not Null
email: String, Unique, Not Null
password_hash: String, Not Null
age: Integer, Not Null
gender: String, Not Null
phone_number: String, Not Null

# Doctor
id: Integer, Primary Key
name: String, Not Null
email: String, Unique, Not Null
password_hash: String, Not Null
specialty: String, Not Null
experience_years: Integer, Not Null
availability: String, Not Null

# Appointment
id: Integer, Primary Key
user_id: Integer, Foreign Key (users.id), Not Null
doctor_id: Integer, Foreign Key (doctors.id), Not Null
date: Date, Not Null
time: Time, Not Null
status: String, Not Null

# Prescription
id: Integer, Primary Key
appointment_id: Integer, Foreign Key (appointments.id), Not Null
medicine: String, Not Null
dosage: String, Not Null
instructions: String, Not Null

# Seeding The Database

To seed the database with some initial data, run:

python seed.py
This will create some users, doctors, appointments, and prescriptions with dummy data.

# Contributing
Fork the repository
Create a new branch (git checkout -b feature-branch)
Commit your changes (git commit -am 'Add some feature')
Push to the branch (git push origin feature-branch)
Create a new Pull Request


# Acknowledgements
Flask
SQLAlchemy
Flask-Migrate
Flask-RESTful
Flask-CORS
bcrypt
Contact
If you have any questions or suggestions, feel free to reach out to me at [kamandetonymuriuki@gmail.com].

This README provides a comprehensive overview of the Good Doctor Management System, including installation steps, API endpoints, and database models. Feel free to modify it based on your project's specific requirements.







