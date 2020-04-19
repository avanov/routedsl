.. _badges:

.. image:: https://travis-ci.org/avanov/routedsl.svg?branch=develop
    :target: https://travis-ci.org/avanov/routedsl

.. image:: https://circleci.com/gh/avanov/routedsl/tree/develop.svg?style=svg
    :target: https://circleci.com/gh/avanov/routedsl/tree/develop

.. image:: https://coveralls.io/repos/github/avanov/routedsl/badge.svg?branch=develop
    :target: https://coveralls.io/github/avanov/routedsl?branch=develop

.. image:: https://requires.io/github/avanov/routedsl/requirements.svg?branch=develop
    :target: https://requires.io/github/avanov/routedsl/requirements/?branch=develop
    :alt: Requirements Status

.. image:: https://readthedocs.org/projects/routedsl/badge/?version=develop
    :target: http://routedsl.readthedocs.org/en/develop/
    :alt: Documentation Status

.. image:: http://img.shields.io/pypi/v/routedsl.svg
    :target: https://pypi.python.org/pypi/routedsl
    :alt: Latest PyPI Release

Python eDSL for your Web Routes
===============================

.. code-block:: bash

    pip install routedsl


Compose everything in one place

.. code-block:: python

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

Read more in `Official Documentation <https://routedsl.readthedocs.io/en/develop/>`_.
