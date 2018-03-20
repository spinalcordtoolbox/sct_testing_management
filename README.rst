SCT testing management web application
======================================

A web application to manage the metadata of MRI images.

.. image:: https://travis-ci.org/neuropoly/sct_testing_management.svg?branch=master
     :target: https://travis-ci.org/neuropoly/sct_testing_management


:License: MIT


Settings
--------

[WIP]

Basic Commands
--------------

[WIP]

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

[wip]

Running tests
~~~~~~~~~~~~~

::

  $ py.test


Deployment
----------

The following details how to deploy this application.



Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html
