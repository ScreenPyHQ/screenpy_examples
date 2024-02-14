from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy


def by_uiautomator_for(uiselector: str) -> tuple[str, str]:
    return (
        AppiumBy.ANDROID_UIAUTOMATOR,
        "new UiScrollable(new UiSelector().scrollable(true))"
        f".scrollIntoView(new UiSelector().{uiselector})",
    )
