# Movies and Social DB

Social platform for movies

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## First time setup

1. Install docker stuff
3. clone the repository
4. Navigate to the `SEP6-MSDB/msdb/` folder
4. Build the project: `docker-compose -f local.yml build`
5. Run the project: `docker-compose -f local.yml up`
6. Access project: http://0.0.0.0:8000

## Admin

1. Navigate to the `SEP6-MSDB/msdb/` folder
2. Create a superuser: `docker-compose -f local.yml run --rm django python manage.py createsuperuser`
3. Enter email and password
4. When the project is running you can now login on the admin page: http://0.0.0.0:8000/admin/

## Add 3rd party python packages
1. Add it in req file
2. Down
4. Build
3. Up

## Changes to django models

1. Navigate to the `SEP6-MSDB/msdb/` folder
2. First make migrations: `docker-compose -f local.yml run --rm django python manage.py makemigrations`
3. Update the role of migration files. This is done so that they can be added to the git repository: `sudo chown -R $USER:$USER "path"/SEP6-MSDB/`
4. Apply the migrations: `docker-compose -f local.yml run --rm django python manage.py migrate`


## Access postgres database shell

1. Navigate to the `SEP6-MSDB/msdb/` folder
2. Run the following command to open the postgres dbshell: `docker exec -it msdb_local_postgres bash -c 'psql msdb -U $POSTGRES_USER'`

## Running tests

1. Navigate to the `SEP6-MSDB/msdb/` folder
2. Run tests: `docker-compose -f local.yml run --rm django coverage run -m pytest`
3. Generate coverage report: `docker-compose -f local.yml run --rm django coverage report`



<s>
## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy msdb

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
</s>
