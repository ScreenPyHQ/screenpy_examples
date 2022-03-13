HTTPBin Example
===============

[HTTPBin](https://httpbin.org/)
is a handy website
for testing HTTP Requests.
We will be using it
to try out some API requests.

Setup
-----

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
-----------------
To run the tests, call the following in the project root folder:

    python -m pytest features/

To run the tests with Allure reporting:

    python -m pytest features/ --alluredir allure_report/
    allure serve allure_report
