Academic Helper Calendar
============

### Project Description
This project is a web app created using Django, a free and open source web application framework written in Python. It stores the user information after registration in its database and generates personal calendars that are created based on HTMLCalendar module in Python. The home page of the web app displays the personal calendar for the user after he or she logs in. The personal calendar is in a monthly view, with title and start time of each event displayed in the corresponding table. The user can click on the title of the event to edit it or delete it. The home page also embeds the course content page for 15-112 and a collaborative real-time online text-editor, with which user can take notes and save it while studying the course material.

## Requirements
* Python 3.6
* Django (1.11.7+)

## Installation
#### Virtual environment
Before installing requirements for this project, consider installing a virtual environment. Virtualenv will isolate your Python/Django setup on a per-project basis. Open terminal and type:
$ pip install virtualenv
Create a new virtual environment by entering:
$ virtualenv venv
where venv is the name of this environment and can be anything.
Then, activate the virtual environment. This sets up various environment variables to effectively bypass the system's Python install and uses the venv one instead.
$ source venv/bin/activate
You should see (venv) $ at your prompt, letting you know that you're running under the 'env' virtualenv install. At any time, just type:
$ deactivate
to stop using the virtualenv

#### Django
Before installing Django, make sure that you have the latest version of pip. 
Then, run 
$ python3 pip install django 
to install the latest version of Django.
After unzipping the code, cd TP to the directory containing manage.py.
Then, in your terminal, type following commands
$ python manage.py migrate
which migrates and registers the models of this project
$ python manage.py createsuperuser
to create an admin account where you can access the entire database
$ python manage.py runserver
to start the web app on local host. 
Paste the link given in your own browser(google chrome recommended) to view the web page.# AcademicHelperCalendar
