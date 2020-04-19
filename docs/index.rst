.. routedsl documentation master file, created by
   sphinx-quickstart on Sun Apr 19 14:12:42 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===============================
Python eDSL for your Web Routes
===============================

.. code-block:: bash

    pip install routedsl


Compose everything in one place

.. code-block:: python

    from routedsl import *

    routes = Routes() (
        GET / 'users' / ('user_id', User, "User identifier")
            | HEADERS | Headers
            | RETURNS | JSON [ User ]
            | HANDLER | get_user_info
            | GUARDS  | ( Headers.content_type | IS | 'application/json'
                        )
            | DOCS    | """Get a user profile in JSON format"""
    )(
        POST / 'users' / ('user_id', User)
            | HEADERS | Headers
            | PAYLOAD | JSON [ User ]
            | RETURNS | OK [ JSON [ bool ] ]
            | HANDLER | update_user_info
    )


or define pieces separately, then assemble your routing map:

.. code-block:: python

    DefaultHeaders = HEADERS | Headers
    DefaultHandler = HANDLER | default_handler

    DefaultEndpoint = GET / DefaultHeaders
                          | DefaultHandler

    routes = Routes() | DefaultEndpoint

Use nesting under common prefix

.. code-block::  python

    routes = (routes / 'users' / ('user_id', User)) (
        POST / 'edit'
            | HEADERS | Headers
            | RETURNS | JSON [ User ]
            | HANDLER | update_user_info
    )


Matching Routes
===============

TODO


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
