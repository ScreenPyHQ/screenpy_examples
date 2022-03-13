unittest Example
================

This example uses [unittest](https://docs.python.org/3/library/unittest.html)'s test organization style.


Setup
-----

It is assumed you have `geckodriver` installed.

Virtual environment
^^^^^^^^^^^^^^^^^^^

    python -m venv env
    source env/bin/activate

You can use `deactivate`
to leave the virtual environment.
Re-run the `source` command above
to re-enter your virtual environment.

Install Requirements
^^^^^^^^^^^^^^^^^^^^

    pip install -r requirements.txt

Running the Tests
----------
To run the tests, call the following in the project root folder:

    python -m unittest features/*
