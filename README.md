
# DigiLearn - Online Learning Management System

This is an Online Learning Management System built with Django and PostgreSQL. The system allows users to create and manage courses, enroll students in courses, manage assignments.

# Features
- User authentication and authorization
- Course creation and management
- Course enrollment
- Assignment creation and submission

# Requirements
- Python 3.x
- Django 3.x
- PostgreSQL

# Installation
- Clone the repository
- Create a virtual environment and activate it
- Install the requirements: pip install -r requirements.txt
- Create a PostgreSQL database
- Create a .env file in the root directory and set the following environment variables:
	SECRET_KEY: Django secret key
	DATABASE_URL: PostgreSQL database URL
	DEBUG: Set to True for development
- Run migrations: python manage.py migrate
- Create a superuser: python manage.py createsuperuser
- Run the server: 
	```bash
	python manage.py runserver
	```
	
# Usage
- Once the server is running, navigate to http://localhost:8000 to access the application. 
- The homepage displays all the available courses. 
- Users can create an account, enroll in courses, view and submit assignments.

# Contributing
Contributions are welcome! To contribute, please create a pull request with your changes.
