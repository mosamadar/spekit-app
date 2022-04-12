# soccer backend
soccer-app Application Hosted on https://spekit-app.herokuapp.com/

# Features #
* Django 3.1
* Uses PIP3 for python package management
* Postgres for database with Pyscopg2

# Pre requisites #

* Install Python 3.9 if not previously installed (for ubuntu 16.04).  
```
$ sudo add-apt-repository ppa:jonathonf/python-3.6
$ sudo apt-get update
$ sudo apt-get install python3.6
```  

* Install PostgreSQL if not previously installed.  
```
$ sudo apt-get install postgresql postgresql-contrib
$ sudo apt-get install libpq-dev
```

* Install Python Package Index Tool pip3  
` $ sudo apt-get install -y python3-pip `  

* Install Docker  
` Donwlaod and install Docker setup from this URL(https://docs.docker.com/docker-for-mac/) `  

* Install virtual environment wrapper  
(further info found here: [https://gist.github.com/Geoyi/d9fab4f609e9f75941946be45000632b](https://gist.github.com/Geoyi/d9fab4f609e9f75941946be45000632b))
` $ sudo pip3 install virtualenv `  

* Create directory for development, name it anything.
```
$ mkdir soccer-app
$ cd soccer-app
```

* When inside the directory create virtual environment, called spekit_venv in example. Then activate the environment.  
```
$ virtualenv .soccer_venv
$  source .soccer_venv/bin/activate
```  
# Installation #

1. Enter created directory for development in created virtual development environment where project files will be stored.  
` (soccer_venv) $ cd <directory name/location> `
2. Clone branch from repository.  
` (soccer_venv) $ git clone <remote repository name> `

Example:
` (soccer_venv) $ git clone https://github.com/mosamadar/soccer-app.git

3. Install requirements  
pip install -r install_requirements.sh`
4. Installing the Geospatial Libraries (GEOS, GDAL and PROJ.4) Only for UBUNTU
  
([help link for differetn OS](https://www.techiediaries.com/django-gis-geodjango/))

    ```
    $ sudo apt-get install libgeos-dev
    $ sudo apt-get install binutils libproj-dev
    $ sudo apt-get install gdal-bin libgdal-dev
    $ sudo apt-get install python3-gdal   
    ```


4. Set up PostgreSQL  
Switch over to the postgres account by typing:  
`$ sudo -i -u postgres`   

You can now access a Postgres prompt immediately by typing:  
```
$ psql  
postgres=# ALTER USER postgres WITH ENCRYPTED PASSWORD SET_PASSWD;

postgres=# CREATE DATABASE spekit_db;

postgres=# CREATE ROLE ROLE_NAME WITH ENCRYPTED PASSWORD SET_PASSWD;

postgres=# GRANT ALL PRIVILEGES ON DATABASE soccer_db TO ROLE_NAME;

postgres=# ALTER ROLE ROLE_NAME WITH LOGIN;

postgres# ALTER ROLE <user_name> SUPERUSER;
```  

5. Installing PostGIS in your Database:
([How To Install PostGIS on Ubuntu 18.04 /](https://computingforgeeks.com/how-to-install-postgis-on-ubuntu-debian/))
```
You first need to install PostGIS extension usign above link:
Now you need to connect to your created database using psql:
    $ sudo -u postgres psql -d <DB NAME>
    
Next, you can to enable the postgis extension in your database:
    $ CREATE EXTENSION postgis;
```

spekit_db

6. Set the shell environment variables, Write the following commands in bash Shell
```
export PG_DB_NAME='soccer_app'
export PG_USER=ROLE_NAME 
export PG_PASSWD=SET_PASSWE  
export PG_HOST='localhost'  
export SECRET_KEY='Your_secret_key'   
export DJANGO_SETTINGS_MODULE=spekit_app.settings
export HOST_URL='http://127.0.0.1:8000'
```


6. RUN Admin site migrations and other django app migrations.  
`python manage.py  migrate`

8. Build Docker container
`sudo docker-compose build` 

9. Run Docker container
`sudo docker-compose up` 

10. Run the server without Docker container

`python manage.py  runserver`

This should run the server and give an IP address that when entered into a 
web browser will bring up the development server. Address of the server is your IP address
most likely http://127.0.0.1:8000/.


# Run Tests #

1.Run From Shell for running Database Test.  
`python manage.py test api.tests`

2.Run From Shell for running Api Test.  
`python manage.py test api.test_views`

# Deployment Guide #  
([Deployment doc](https://docs.google.com/document/d/1HmrH7-W-wsok7pQ45xEnvM6vvX45w50Ef2GJLR1OTs0/edit))

