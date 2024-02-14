# SwagLabs Example

[SwagLabs](https://www.saucedemo.com)
is an ecommerce demo website
built by [SauceLabs](https://saucelabs.com/)
for automated testing practice.

This example uses [pytest](https://docs.pytest.org/)'s test organization style.

## Setup

### Virtual environment

    python -m venv env
    source env/bin/activate

You can use `deactivate`
to leave the virtual environment.
Re-run the `source` command above
to re-enter your virtual environment.

### Install requirements

    pip install -r requirements.txt
    playwright install

## Running the Tests

To run the tests, call the following in the project root folder:

    python -m pytest features --log-cli-level=INFO
