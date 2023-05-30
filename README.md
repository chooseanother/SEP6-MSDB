# Movies and Social DB

Social platform for movies, build with Django.

License: MIT

## Table of Contents
1. [First time setup](#first-time-setup)
2. [Deployment](#deployment)
3. [Admin](#admin)
4. [Python Packages](#python-packages)
5. [Migrations](#migrations)
6. [Postgres database shell](#postgres-database-shell)
7. [Testing](#testing)
8. [Deleting database](#deleting-database)
9. [Python shell](#python-shell)
10. [Static files](#static-files)

---

## First time setup [^](#table-of-contents)

1. Install Docker, follow this guide: [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)
2. Install Git
3. Install pre-commit: `pip install pre-commit`
4. Clone the repository.
    - SSH: `git clone git@github.com:chooseanother/SEP6-MSDB.git`
    - HTTPS: `git clone https://github.com/chooseanother/SEP6-MSDB.git`
5. Navigate to the project folder: `cd SEP6-MSDB/`
6. Execute this command: `pre-commit install`
7. Build the project: `docker compose -f local.yml build`
8. Run the project: `docker compose -f local.yml up`
9. Access project: http://0.0.0.0:8000


## Deployment [^](#table-of-contents)
1. Install gcloud cli [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)
2. Login to gcloud cli: `glcoud auth login`
3. Config project with gcloud cli: `gcloud config set project msdb-sep6-1337`
    - To get a list of projects `gcloud projects list`
6. SSH into vm instance with glcoud cli: `gcloud compute ssh msdb-web –zone=europe-west3-c`
7. Navigate to project folder: `cd SEP6-MSDB/msdb/`
8. Git pull to get the latest changes: `git pull`
8. Stop the containers: `docker compose -f production.yml down`
9. Build images: `docker compose -f production.yml build`
10. Run the containers in detached mode: `docker compose -f production.yml up -d`



## Admin [^](#table-of-contents)
1. Navigate to the `SEP6-MSDB/msdb/` folder
2. Create a superuser: `docker compose -f local.yml run --rm django python manage.py createsuperuser`
3. Enter email and password
4. When the project is running you can now login on the admin page: http://0.0.0.0:8000/admin/
    - accessing admin page when deployed requires the random generated string found in `msdb/.envs/.production/.django`

## Python packages [^](#table-of-contents)
If new 3rd party python packages needs to be added
1. Add package in the file matching the enviornemnt it is needed it. If needed in all enviornments add it in `SEP6-MSDB/msdb/requirements/base.txt`. For development or production only `local.txt` or `production.txt`
   - Example `<package_name>==<package_version>`
2. Navigate to the `SEP6-MSDB/msdb/` folder
3. Stop all running containers `docker compose -f local.yml down`
4. Build the project: `docker compose -f local.yml build`
5. Run the project: `docker compose -f local.yml up`

## Migrations [^](#table-of-contents)
If there are made changes to django models, it is important to create migrations and add them to VCS
1. Navigate to the `SEP6-MSDB/msdb/` folder
2. First make migrations: `docker compose -f local.yml run --rm django python manage.py makemigrations`
3. Update the role of migration files. This is done so that they can be added to the git repository: `sudo chown -R $USER:$USER "path"/SEP6-MSDB/`
4. Apply the migrations: `docker compose -f local.yml run --rm django python manage.py migrate`
5. Don't forget to add the new migration files to git


## Postgres database shell [^](#table-of-contents)
This only works for local development.
1. Navigate to the `SEP6-MSDB/msdb/` folder
2. Run the following command to open the postgres dbshell: `docker exec -it msdb_local_postgres bash -c 'psql msdb -U $POSTGRES_USER'`

## Testing [^](#table-of-contents)
Running tests
1. Navigate to the `SEP6-MSDB/msdb/` folder
2. Run tests: `docker compose -f local.yml run --rm django coverage run -m pytest`
    - If any errors with missing tables, try to add `--no-migrations`
3. Generate coverage report: `docker compose -f local.yml run --rm django coverage report`

## Deleting database [^](#table-of-contents)
While doing development you might need to clear the database
1. Navigate to the `SEP6-MSDB/msdb/` folder
2. Stop all running containers `docker compose -f local.yml down`
3. Remove database volume `docker volume rm msdb_msdb_local_postgres_data`
4. Build the project: `docker compose -f local.yml build`
5. Run the project: `docker compose -f local.yml up`

## Python shell [^](#table-of-contents)
Run python inside docker container
1. Navigate to the `SEP6-MSDB/msdb/` folder
2. Run this command: `docker compose -f local.yml run --rm django python manage.py shell`


## Static files [^](#table-of-contents)
If new static files are added
1. Navigate to the `SEP6-MSDB/msdb/` folder
2. Run this command: `docker compose -f local.yml run --rm django python manage.py collectstatic`
