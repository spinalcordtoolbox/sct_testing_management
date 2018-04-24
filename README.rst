SCT testing management web application
======================================

A web application to manage the metadata of MRI images.

.. image:: https://travis-ci.org/neuropoly/sct_testing_management.svg?branch=master
     :target: https://travis-ci.org/neuropoly/sct_testing_management


:License: MIT

Installation
------------

The web application is a django application developed and tested on Python==3.6
and PostgresSQL==9.6. Follow these instructions if you plan to `install
locally`_ or `install using docker`_

.. _`install locally`: https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html
.. _`install using docker`: https://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html


Settings
--------
Important settings constant to keep track of.

- `POSTGRES_PASSWORD`: The password the web application logs in with
- `POSTGRES_USER`: The web application's user name when connecting to the DB

- `DOMAIN_NAME`: The full domain path the web application resides on,
- `DJANGO_SETTINGS_MODULE`: python path to the settings file. The production
  settings is "config.settings.production"
- `DJANGO_ALLOWED_HOSTS`: A list of domain name that the web application will
  accept connections from
- `SCT_DATASET_ROOT`: The absolute path to the sct_testing/large dataset.

Basic Commands
--------------

Goes through the database and checks if the image filename exists and are valid
nifti files::

  $ python manage.py check_filenames


Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form.
  Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your
  console to see a simulated email verification message. Copy the link into your
  browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

  $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your
superuser logged in on Firefox (or similar), so that you can see how the site
behaves for both kinds of users.

Setting up the development environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Make sure the environment variables are set. A development web application
should be launched with sqlite instead of postgres. Here's an example of the
.env file::

  DJANGO_SETTINGS_MODULE=config.settings.local
  DJANGO_DEBUG=True
  DATABASE_URL=sqlite:///sct_annotation.db

The database initialization is needed for the first time::

   $ export DJANGO_READ_DOT_ENV_FILE=1; python manage.py migrate

Once setup is done, you can run an instance of web application, you can run::

   $ export DJANGO_READ_DOT_ENV_FILE=1; python manage.py runserver_plus


Running tests
^^^^^^^^^^^^^

Tests are focused on the API and the ORM testing. All the tests run by running::

  $ export DJANGO_READ_DOT_ENV_FILE=1; python manage.py test


Deployment
----------

The web application can be deployed either natively or within a container. In
the current production it is running in a docker container. It is managed by
[internal ansible scripts](https://github.com/neuropoly/sct_testing_management_ansible).


Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html
