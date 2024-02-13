from typing import Tuple

from appium.webdriver.common.appiumby import AppiumBy


def by_uiautomator_for(uiselector: str) -> Tuple[str, str]:
    return (
        AppiumBy.ANDROID_UIAUTOMATOR,
        "new UiScrollable(new UiSelector().scrollable(true))"
        f".scrollIntoView(new UiSelector().{uiselector})",
    )
