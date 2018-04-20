Code Sample
-----------
This repo contains Django code with some basics feature you can use in 
any of your application. Contains authentication module with JWT. It has
django debug toolbar to check the performance and other useful packages
are there too. A good example to start app with django using good coding
and structural practices.

Requirements
------------
Code Sample is a Python Django based platform. 

- Python 3.4.3
- Django 2.0.4
- Postgres

Installation
------------
Following are the steps to install this platform.

- Get in the root directory of the project
- Create Virtual Environment
```sh
$ cd ..
$ virtualenv -p python3 code_sample_venv
$ cd code_sample
$ source ../code_sample_venv/bin/activate
```
- Install Requirements
```sh
$ pip install -r requirements.txt
```
- Setting up the Database
```sh
$ cd code_sample
$ pwd //It should display like this "/Users/(user)/code_sample/code_sample"
$ sudo vim local_settings.py
    //Add the code below and save the file
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'code_sample',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
    // Note: Settings are for POSTGRES SQL
$ cd .. 
$ python manage.py migrate 
```

Create a Super Admin to get things started. 
```sh
$ python manage.py createsuperuser
```
Access the Django Admin and login with the credentials. 

Seeds
-----
In order to populate mandatory data you need to run the management 
command that will auto populate items.
```sh
$ python manage.py seeds
```
This seeds will create a Super User and you can login to Django Admin 
Dashboard to perform needed actions and to walk through the APIs.
