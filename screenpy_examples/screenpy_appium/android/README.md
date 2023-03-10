# ScreenPy Appium: Android Example

This directory
houses an example
of a test suite
for an Android application.

## Set Up

### Appium and Android

Before we can begin,
you will need to make sure
your `ANDROID_HOME` is set.
Check the [Android development documentation](https://developer.android.com/studio/command-line/variables)
for more information on that.

You will also need to make sure
JAVA_HOME is set.
Check the [Java documentation](https://developer.android.com/studio/command-line/variables)
for more information on that.

Finally,
you will also need to set up
an Android virtual device.
To create an emulator,
follow the instructions
in the [Android Studio documentation](https://developer.android.com/studio/run/managing-avds).
You may want to have your emulator running
while you run the test scripts,
this will save on startup time.

Once these two environment variables are set
and your emulator is created,
start the Appium server in a terminal
with `appium`.

### Python

    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt

## Running the Suite

    python -m pytest features/ --log-cli-level=info
