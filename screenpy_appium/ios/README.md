# ScreenPy Appium: iOS Example

This directory
houses an example
of a test suite
for an Android application.

## Set Up

### Appium and iOS

Before we can begin,
you will need to make sure
you have installed
the latest version of XCode.
It might take a while.

With that finished,
download a simulator as well.
This suite uses iOS version 15;
if you download that one,
you will have no further set up.

If you download a different version,
you will need to update the version number
in the `platformVersion` value
in `features/conftest.py`.

Once you've set this up,
start the Appium server in a terminal
with `appium`.

### Python

    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt

## Running the Suite

    python -m pytest features/ --log-cli-level=info


Ensure XCode is installed
Download the iOS 15 simulator
Start it up
Start up the Appium server
Run the test
