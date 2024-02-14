# The Internet Example (unittest edition)
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

~~You can use `deactivate`
to leave the virtual environment.
Re-run the `source` command above
to re-enter your virtual environment.~~

Create a virtual environment for screenpy_examples. See [link-here]() for
guidance.  _the link should show how to install the entire package_

### Install requirements

    pip install -r requirements.txt

## Running the Tests

Navigate to the features_pytest folder:

    cd your_projects/screenpy_examples/the_internet/features_unittest/

    python -m unittest
