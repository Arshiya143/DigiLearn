# DigiLearn

The DigiLearn is a Learning Maanagement System. Here teachers may create and integrate course materials, articulate learning goals, align content and assessments, track studying progress, and create customized tests for students. An LMS allows the communication of learning objectives, and organize learning timelines.

# How to run DigiLearn
 
Open DigiLearn-master folder in editor like VScode,PyCharm,Sublime Text.

# Postgresql Setting

Create Learn_db databse into Postgresql.

Goto DigiLearn-master->DigiLearn->settings.py Change your password.

DATABASES = {

   'default': {
	 
       'ENGINE': 'django.db.backends.postgresql',
			 
       'NAME': 'Learn_db',
			 
       'USER': 'postgres',
			 
       'PASSWORD': 'write your password',
			 
       'HOST': '127.0.0.1',
			 
       'PORT': '5433',
			 
  	 }
	 
}

# Migration

run python manage.py makemigrations into terminal.

Then run python manage.py migrate in terminal.

Once migrations are done all the tables are created into our database.

Now you can successfully run the web application.

python manage.py runserver

# Teacher

Teachers can create their accounts.
Once they created accounts they are able to upload study material for their subject.

They are able to add,update,delete the course.
Teacher can upload video of perticular topic in course.

# Student

Students can create their accounts.
Once they created accounts they are able to access study material for their enrolled subject.

They can browse the courses which they enrolled.They are also able to download study material.
