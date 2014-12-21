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