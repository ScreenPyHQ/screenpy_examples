# GitHub Example

Yep,
we're automating some tests
against GitHub itself!

This example uses [pytest](https://docs.pytest.org/en/latest/)'s
test organization style.

## Setup

It is assumed you have `chromedriver` installed.

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

    python -m pytest features/

To run the tests with Allure reporting:

    python -m pytest features/ --alluredir allure_report/
    allure serve allure_report
