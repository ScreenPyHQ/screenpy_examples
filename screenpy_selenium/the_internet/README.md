# The Internet Example

[The Internet](http://the-internet.herokuapp.com/)
is a website
created by Dave Haeffner.
It provides several examples
of modern web design
to practice interacting with
through Selenium.

This example uses [unittest](https://docs.python.org/3/library/unittest.html)'s test organization style.

## Setup

It is assumed you have `geckodriver` installed.

### Virtual environment

    python -m venv env
    source env/bin/activate

You can use `deactivate`
to leave the virtual environment.
Re-run the `source` command above
to re-enter your virtual environment.

### Install requirements

    pip install -r requirements.txt

## Running the Tests

To run the tests, call the following in the project root folder:

    python -m unittest features/*
