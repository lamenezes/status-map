status-map
~~~~~~~~~~

|version-badge| |pyversion-badge| |license-badge| |CI-badge| |cov-badge|

Handle status maps and status transitions easily.


How to use
==========

Install
-------

status-map is available on PyPI:

.. code-block:: bash

    $ pip install status-map


Basic Usage
-----------

Define your status map by creating a dict containing all the status and its possible transitions.

E.g. we can define a task workflow as follows:

.. code-block:: python

    from status_map import StatusMap

    status_map = StatusMap({
        'todo': ['doing'],
        'doing': ['todo', 'done'],
        'done': [],  # assuming a task once finished can't go back to other status
    })


We can validate if a status transition is valid:

.. code-block:: python

    >> status_map.validate_transition(from_status='todo', to_status='done')
    Traceback (most recent call last):
    ...
    status_map.exceptions.TransitionNotFound: transition from todo to done not found


Passing an inexistent status raises an exception:

.. code-block:: python

    >> status_map.validate_transition('todo', 'foo')
    Traceback (most recent call last):
    ...
    status_map.exceptions.StatusNotFound: to status foo not found


The validation raises a different exception if the to_status has already appeared before:

.. code-block:: python

    >> status_map.validate_transition('done', 'todo')
    Traceback (most recent call last):
    ...
    status_map.exceptions.RepeatedTransition: transition from done to todo should have happened in the past


How to contribute
=================

We welcome contributions of many forms, for example:

- Code (by submitting pull requests)
- Documentation improvements
- Bug reports and feature requests

Setting up for local development
--------------------------------

We use poetry_ to manage dependencies, so make sure you have it installed.

Roll up your virtual enviroment using your favorite tool and install development dependencies:

.. code-block:: bash

    $ poetry install

Install pre-commit hooks:

.. code-block:: bash

    $ pre-commit install


Run tests by evoking pytest:

.. code-block:: bash

    $ pytest

That's it! You're ready from development.


.. _poetry: https://github.com/sdispater/poetry

.. |version-badge| image:: https://badge.fury.io/py/status-map.svg
    :target: https://pypi.org/project/status-map/

.. |pyversion-badge| image:: https://img.shields.io/badge/python-3.6,3.7-blue.svg
    :target: https://github.com/lamenezes/status-map

.. |license-badge| image:: https://img.shields.io/github/license/lamenezes/status-map.svg
    :target: https://github.com/lamenezes/status-map/blob/master/LICENSE

.. |CI-badge| image:: https://circleci.com/gh/lamenezes/status-map.svg?style=shield
    :target: https://circleci.com/gh/lamenezes/status-map

.. |cov-badge| image:: https://codecov.io/gh/lamenezes/status-map/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/lamenezes/status-map
