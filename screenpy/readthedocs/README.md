# ReadTheDocs

This is the fully functional example
used in the [ScreenPy docs](https://screenpy-docs.readthedocs.io/en/latest/).


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

## Running the Tests

To run the tests, call the following in the project root folder:

    python -m pytest features/

To run the tests with StdOut logging:

    python -m pytest features/ --log-cli-level=info
