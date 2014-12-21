Flask Boilerplate Utilities
================================================
Boilerplate utilities for use with `Flask-Boilerplate <https://github.com/nickw444/Flask-Boilerplate>`_. 

Created to allow easy upgrading of boilerplates

Also very useful as a standalone package.

Installation
------------------------------------

.. code-block:: bash

	pip install flask-boilerplate-utils

Usage
-----------------------------------

.. code-block:: python

    from flask import Flask
    from flask_boilerplate_utils import Boilerplate()
    
    app = Flask(__name__)
    Boilerplate(app)


Full usage available at `read the docs <http://flask-boilerplate-utils.readthedocs.org/en/latest/>`_

This module is part of the flask-boilerplate project.

- `flask-boilerplate <https://github.com/nickw444/Flask-Boilerplate>`_
- `flask-boilerplate-buildutils <https://github.com/nickw444/flask-boilerplate-buildutils>`_
- `flask-boilerplate-utils <https://github.com/nickw444/flask-boilerplate-utils>`_
- `maketools <https://github.com/nickw444/python-maketools>`_