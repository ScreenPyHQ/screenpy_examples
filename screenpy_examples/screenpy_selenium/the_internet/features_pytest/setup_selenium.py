from __future__ import annotations

import errno
import logging
import os as os
import platform
import shutil
from typing import TYPE_CHECKING

import pyderman as pydm
import requests
from selenium import webdriver  # noqa: E402
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
from selenium.webdriver.chrome.service import (
    Service as ChromeService,
)
from selenium.webdriver.edge.service import (
    Service as EdgeService,
)
from selenium.webdriver.firefox.service import (
    Service as FirefoxService,
)
from semantic_version import Version  # type: ignore

if TYPE_CHECKING:
    from collections.abc import Mapping

    from selenium.webdriver.common.options import ArgOptions

__all__ = ["Selenium"]

typeWebDriver = webdriver.Firefox | webdriver.Chrome | webdriver.Edge


CHROME_DEFAULT_DRIVER_PATH = "chromedriver"
EDGE_DEFAULT_DRIVER_PATH = "msedgedriver"
FF_DEFAULT_DRIVER_PATH = "geckodriver"


def create_logger(name: str) -> logging.Logger:
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    log.propagate = False
    return log


logger = create_logger("sel")


def _log_method(msg: str | None = None) -> None:
    # if msg is None:
    #     msg = get_methodcall(1)
    # logger.info(msg)
    return


EDGE = "edge"
CHROME = "chrome"
CHROMIUM = "chromium"
FIREFOX = "firefox"

CHROME_PATHS = {
    "Darwin": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "Windows": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "Linux": "/usr/bin/google-chrome",
}

CHROMIUM_PATHS = {
    "Darwin": "/Applications/Chromium.app/Contents/MacOS/Chromium",
    # "Windows": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "Linux": "/usr/bin/chromium",
}

EDGE_PATHS = {
    "Darwin": "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    # "Windows": (
    #     "C:\\Windows\\SystemApps\\Edge\\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\\"
    #     "MicrosoftEdge.exe"
    # ),
    "Windows": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "Linux": "/usr/bin/microsoft-edge",
}

FIREFOX_PATHS = {
    "Darwin": "/Applications/Firefox.app/Contents/MacOS/firefox",
    "Windows": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "Linux": "/usr/bin/firefox",
}

DEFAULT_WEBDRIVER_PATHS: dict[str, str] = {
    EDGE: EDGE_DEFAULT_DRIVER_PATH,
    CHROME: CHROME_DEFAULT_DRIVER_PATH,
    CHROMIUM: CHROME_DEFAULT_DRIVER_PATH,
    FIREFOX: FF_DEFAULT_DRIVER_PATH,
}


# geckodriver is reported to only work with selenium 3.11 or higher
# https://firefox-source-docs.mozilla.org/testing/geckodriver/geckodriver/Support.html
# safari does not work with selenium 3.10 or 3.11 -- use 3.9 or 3.14?
# safari doesn't seem to like the frame navigation currently implemented in base
################################################################################
################################################################################
class Selenium:
    DIMENSIONS: Mapping[str, tuple[int, int]] = {
        # 4:3
        "1024": (1024, 768),
        "1280": (1280, 960),
        "1600": (1600, 1200),
        "1920": (1920, 1440),
        # 16:9
        "720": (1280, 720),
        "1080": (1920, 1080),
        "1440": (2560, 1440),
        "2160": (3840, 2160),  # 4k
        "4320": (7680, 4320),  # 8k
    }

    def __init__(
            self,
            browser: str = CHROME,
            baseurl: str = "",
            timeout: int = 15,
            headless: bool = False,
            window_size: str = "720",
            enable_log_performance: bool = False,
            enable_log_console: bool = False,
            enable_log_driver: bool = False,
            log_path: str = "./logs",
            driver_version: str = "auto",
    ) -> None:
        """
        driver_version: the options are 'latest', 'auto', or a specific version
        """
        log_path = os.path.abspath(os.path.expanduser(log_path))
        self.main_window_handle: str = ""
        self.screenshot_path: str = self.make_screenshot_path(log_path)
        self.log_path: str = log_path
        self.timeout: int = timeout
        self.baseurl: str = baseurl
        self.driver: typeWebDriver = self.create_driver(
            browser,
            headless,
            enable_log_performance,
            enable_log_console,
            enable_log_driver,
            log_path,
            driver_version,
        )

        # driver must be setup before the following
        self.set_window_size(window_size)
        # self.driver.set_window_position(0, 0)
        # self.driver.maximize_window()
        self.set_main_window_handle()
        return

    ############################################################################
    @staticmethod
    def make_screenshot_path(
            output_dir: str = "./logs", screenshots: str = "screenshots"
    ) -> str:
        """
        Set the output directory for where screenshots should go.
        """
        output_dir = os.path.abspath(os.path.expanduser(output_dir))
        if os.path.split(output_dir)[-1].lower() != screenshots:
            output_dir = os.path.join(output_dir, screenshots)

        try:
            os.makedirs(output_dir)
        except OSError as e:
            if e.errno == errno.EEXIST and os.path.isdir(output_dir):
                pass
            else:
                raise

        return output_dir

    ############################################################################
    @staticmethod
    def log_options(options: ArgOptions) -> None:
        opts = "\n".join(options.arguments)
        logger.debug(f"{opts}")

    @staticmethod
    def webdriver_native_install_path(browser: str) -> str | None:
        browser = browser.lower()
        driver_path = DEFAULT_WEBDRIVER_PATHS.get(browser)
        return shutil.which(f"{driver_path}")

    @staticmethod
    def install_driver(
            browser: str,
            drv_dir: str = "./driver",
            version: str | None = None,
            binary: str | None = None,
    ) -> str:
        browser = browser.lower()
        drvdir = os.path.abspath(os.path.expanduser(drv_dir))
        version = version or "latest"
        binary = binary or Selenium.auto_determine_binary(browser)

        if browser == FIREFOX:
            if version == "auto":
                version = "latest"
                # version = Selenium.get_firefox_version(binary)
                # TODO: need a "best" version function

            logger.debug(f"installing geckodriver {drvdir}")
            driver_path = pydm.install(
                browser=pydm.firefox,
                file_directory=drvdir,
                verbose=True,
                chmod=True,
                overwrite=False,
                return_info=False,
                version=version,
            )
            if not os.path.exists(f"{driver_path}"):
                raise FileNotFoundError("Geckodriver was not downloaded.")

        elif browser in CHROME:
            if version == "auto":
                browser_version = Selenium.get_chrome_version(binary)
                version = Selenium.get_chromedriver_best_version(browser_version)

            logger.debug(f"installing chromedriver {drvdir}")
            driver_path = pydm.install(
                browser=pydm.chrome,
                file_directory=drvdir,
                verbose=True,
                chmod=True,
                overwrite=False,
                return_info=False,
                version=version,
            )
            if not os.path.exists(f"{driver_path}"):
                raise FileNotFoundError("Chromedriver was not downloaded.")

        elif browser == CHROMIUM:
            # chromedriver releases almost never conform to the versions
            # so it's unknown how well the 'closest' verison will work.
            # if version == "auto":
            #     browser_version = Selenium.get_chromium_version(binary)
            #     version = Selenium.get_chromedriver_best_version(browser_version)

            driver_path = None
            raise Exception("We can't really determine the version of chromium")

        elif browser == EDGE:
            if version == "auto":
                browser_version = Selenium.get_edge_version(binary)
                version = Selenium.get_edgedriver_best_version(browser_version)

            logger.debug(f"installing msedgedriver {drvdir}")
            driver_path = pydm.install(
                browser=pydm.edge,
                file_directory=drvdir,
                verbose=True,
                chmod=True,
                overwrite=False,
                return_info=False,
                version=version,
            )
            if not os.path.exists(f"{driver_path}"):
                raise FileNotFoundError("Edgedriver was not downloaded.")
        else:
            raise ValueError(f"Unknown browser: {browser}")

        return driver_path  # type: ignore[return-value]

    @staticmethod
    def create_driver(
            browser: str,
            headless: bool = False,
            enable_log_performance: bool = False,
            enable_log_console: bool = False,
            enable_log_driver: bool = False,
            log_dir: str = "./logs",
            binary: str | None = None,
            driver_path: str | None = None,
    ) -> typeWebDriver:
        browser = browser.lower()
        driver: typeWebDriver
        if browser == FIREFOX:
            driver = Selenium.firefox(
                headless=headless,
                enable_log_driver=enable_log_driver,
                log_dir=log_dir,
                binary=binary,
                driver_path=driver_path,
            )

        elif browser == CHROME:
            driver = Selenium.chrome(
                headless=headless,
                enable_log_performance=enable_log_performance,
                enable_log_console=enable_log_console,
                enable_log_driver=enable_log_driver,
                log_dir=log_dir,
                binary=binary,
                driver_path=driver_path,
            )

        elif browser == CHROMIUM:
            driver = Selenium.chromium(
                headless=headless,
                enable_log_performance=enable_log_performance,
                enable_log_console=enable_log_console,
                enable_log_driver=enable_log_driver,
                log_dir=log_dir,
                binary=binary,
                driver_path=driver_path,
            )

        elif browser == EDGE:
            driver = Selenium.edge(
                headless=headless,
                enable_log_performance=enable_log_performance,
                enable_log_console=enable_log_console,
                enable_log_driver=enable_log_driver,
                log_dir=log_dir,
                binary=binary,
                driver_path=driver_path,
            )

        else:
            raise ValueError(f"Unknown browser: {browser}")

        # driver.set_page_load_timeout(self.timeout)
        # driver.set_script_timeout(self.timeout)
        return driver

    @staticmethod
    def auto_determine_binary(browser: str) -> str | None:
        osname = platform.system()
        # arch = platform.processor()

        if browser == FIREFOX:
            binary = FIREFOX_PATHS[osname]

        elif browser == CHROME:
            binary = CHROME_PATHS[osname]

        elif browser == CHROMIUM:
            binary = CHROMIUM_PATHS[osname]

        elif browser == EDGE:
            binary = EDGE_PATHS[osname]
        else:
            raise ValueError(f"Unknown browser: {browser}")

        if os.path.exists(binary):
            return binary
        return None

    @staticmethod
    def get_firefox_version(binary: str | None = None) -> str:
        logger.debug("get_firefox_version")
        osname = platform.system()

        if not binary:
            binary = CHROME_PATHS.get(osname, None)
            if not binary:
                raise OSError(f"Unknown OS '{osname}'")

        if osname == "Windows":
            cmd = rf"""wmic datafile where "name={binary!r}" get version /value"""
            verstr = os.popen(cmd).read().strip().removeprefix("Version=")
        else:
            verstr = (
                os.popen(f"'{binary}' --version")
                .read()
                .removeprefix("Google Chrome ")
                .strip()
            )
        return verstr

    # @staticmethod
    # def get_geckodriver_best_version(verstr):
    #     return

    @staticmethod
    def firefox_options() -> webdriver.FirefoxOptions:
        options = webdriver.FirefoxOptions()
        options.set_capability("unhandledPromptBehavior", "ignore")

        # profile settings
        options.set_preference("app.update.auto", False)
        options.set_preference("app.update.enabled", False)
        options.set_preference("network.prefetch-next", False)
        options.set_preference("network.dns.disablePrefetch", True)
        return options

    @staticmethod
    def firefox(
            headless: bool = False,
            # enable_log_performance=False,
            # enable_log_console=False,
            enable_log_driver: bool = False,
            log_dir: str = "./logs",
            driver_path: str | None = None,
            binary: str | None = None,
            options: webdriver.FirefoxOptions | None = None,
    ) -> webdriver.Firefox:
        """
        version: the options are 'auto', or a specific version
        this method doesn't auto match geckodriver to firefox version
        """
        _log_method()

        options = options or Selenium.firefox_options()
        if binary:
            options.binary_location = binary

        if headless:
            options.add_argument("--headless")

        # setting log_dir to /dev/null will prevent geckodriver from creating it's own
        # log file. if we enable root logging, we can capture the logging from
        # geckodriver, ourselves.
        logpath = "/dev/null"
        options.log.level = "fatal"  # type: ignore[assignment]
        if enable_log_driver:
            lp = os.path.abspath(os.path.expanduser(log_dir))
            logpath = os.path.join(lp, "geckodriver.log")

        if driver_path:
            service = FirefoxService(executable_path=driver_path, log_path=logpath)
        else:
            service = FirefoxService(log_path=logpath)

        driver = webdriver.Firefox(service=service, options=options)

        driverversion = driver.capabilities["moz:geckodriverVersion"]
        browserversion = driver.capabilities["browserVersion"]

        logger.info(f"Driver info: geckodriver={driverversion}")
        logger.info(f"Browser info:    firefox={browserversion}")
        Selenium.log_options(options)
        return driver

    @staticmethod
    def get_chrome_version(binary: str | None = None) -> str:
        logger.debug("get_chrome_version")
        osname = platform.system()
        binary = binary or CHROME_PATHS.get(osname, None)
        if not binary:
            raise OSError(f"Unknown OS '{osname}'")

        if osname == "Windows":
            # work around for https://bugs.chromium.org/p/chromium/issues/detail?id=158372
            cmd = rf"""wmic datafile where "name={binary!r}" get version /value"""
            verstr = os.popen(cmd).read().strip().removeprefix("Version=")
        else:
            verstr = (
                os.popen(f"'{binary}' --version")
                .read()
                .removeprefix("Google Chrome ")
                .strip()
            )
        return verstr

    @staticmethod
    def get_chromedriver_best_version(verstr: str) -> str:
        version = Version.coerce(verstr)

        major_version = version.major

        url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        if resp.status_code != 200:
            raise Exception(f"Unexpected status {resp.status_code} {resp.reason} {url}")

        logger.debug(f"Chrome version {resp.content.decode('utf-8')}")
        return resp.content.decode("utf-8")

    @staticmethod
    def chrome_options() -> webdriver.ChromeOptions:
        logger.debug("Setting up chrome options")
        # The list of options set below mostly came from this StackOverflow post
        # https://stackoverflow.com/q/48450594/2532408
        opts = (
            "--disable-extensions",
            "--allow-running-insecure-content",
            "--ignore-certificate-errors",
            "--disable-single-click-autofill",
            "--disable-autofill-keyboard-accessory-view[8]",
            "--disable-full-form-autofill-ios",
            # https://bugs.chromium.org/p/chromedriver/issues/detail?id=402#c128
            # "--dns-prefetch-disable",
            "--disable-infobars",
            # chromedriver crashes without these two in linux
            "--no-sandbox",
            "--disable-dev-shm-usage",
            # it's possible we no longer need to do these
            # "enable-automation",  # https://stackoverflow.com/a/43840128/1689770
            # "--disable-browser-side-navigation",  # https://stackoverflow.com/a/49123152/1689770
            # "--disable-gpu",  # https://stackoverflow.com/q/51959986/2532408
            # # https://groups.google.com/forum/m/#!topic/chromedriver-users/ktp-s_0M5NM[21-40]
            # "--enable-features=NetworkService,NetworkServiceInProcess",
        )

        options = webdriver.ChromeOptions()
        for opt in opts:
            options.add_argument(opt)
        return options

    @staticmethod
    def chrome(
            headless: bool = False,
            enable_log_performance: bool = False,
            enable_log_console: bool = False,
            enable_log_driver: bool = False,
            log_dir: str = "./logs",
            driver_path: str | None = None,
            binary: str | None = None,
            options: webdriver.ChromeOptions | None = None,
    ) -> webdriver.Chrome:
        """
        version: the options are 'latest', 'auto', or a specific version
        """
        _log_method()

        options = options or Selenium.chrome_options()
        if binary:
            options.binary_location = binary

        options.headless = headless
        # This is the new way to run headless. Unfortunately it crashes a lot.
        # https://crbug.com/chromedriver/4353
        # https://crbug.com/chromedriver/4406
        # if headless:
        #     options.add_argument("--headless=new")

        logging_prefs = {"browser": "OFF", "performance": "OFF", "driver": "OFF"}
        # https://www.skptricks.com/2018/08/timed-out-receiving-message-from-renderer-selenium.html
        # options.set_capability('pageLoadStrategy', 'none')
        # options.set_capability('pageLoadStrategy', 'normal')

        if enable_log_console:
            logging_prefs["browser"] = "ALL"

        # by default performance is disabled.
        if enable_log_performance:
            logging_prefs["performance"] = "ALL"
            options.set_capability(
                "perfLoggingPrefs",
                {
                    "enableNetwork": True,
                    "enablePage": False,
                    "enableTimeline": False,
                },
            )

        args: list | None = None
        logpath = None
        if enable_log_driver:
            lp = os.path.abspath(os.path.expanduser(log_dir))
            logpath = os.path.join(lp, "chromedriver.log")
            args = [
                # "--verbose"
            ]
            logging_prefs["driver"] = "ALL"

        options.set_capability("goog:loggingPrefs", logging_prefs)

        logger.debug("initializing chromedriver")
        if driver_path:
            service = ChromeService(
                executable_path=driver_path,
                service_args=args,
                log_path=logpath,
            )
        else:
            service = ChromeService(
                service_args=args,
                log_path=logpath,
            )

        driver = webdriver.Chrome(service=service, options=options)

        driver_vers = driver.capabilities["chrome"]["chromedriverVersion"].split(" ")[0]
        browser_vers = driver.capabilities["browserVersion"]

        drvmsg = f"Driver info: chromedriver={driver_vers}"
        bsrmsg = f"Browser info:      chrome={browser_vers}"

        dver = Version.coerce(driver_vers)
        bver = Version.coerce(browser_vers)
        if dver.major != bver.major:
            logger.critical(drvmsg)
            logger.critical(bsrmsg)
            logger.critical("chromedriver and browser versions not in sync!!")
            logger.warning(
                "https://chromedriver.chromium.org/downloads for the latest version"
            )
        else:
            logger.info(drvmsg)
            logger.info(bsrmsg)
        Selenium.log_options(options)

        # experimental settings to slow down browser
        # network_conditions = {
        #     # latency, down, up
        #     "GPRS"     : (500, 50,    20),
        #     "SLOW3G"   : (100, 250,   100),
        #     "FAST3G"   : (40,  750,   250),
        #     "LTE"      : (20,  4000,  3000),
        #     "DSL"      : (5,   2000,  1000),
        #     "WIFI"     : (2,   30000, 15000),
        #     }
        # net_type = "SLOW3G"
        # net_lat, net_down, net_up = network_conditions[net_type]
        # net_down = net_down / 8 * 1024
        # net_up = net_up / 8 * 1024
        # driver.set_network_conditions(offline=False,
        #                               latency=net_lat,
        #                               download_throughput=net_down,
        #                               upload_throughput=net_up,
        #                               )
        # driver.execute_cdp_cmd("Emulation.setCPUThrottlingRate", {'rate': 100})
        return driver

    @staticmethod
    def get_chromium_version(binary: str | None = None) -> str:
        logger.debug("get_chromium_version")
        osname = platform.system()
        binary = binary or CHROMIUM_PATHS.get(osname, None)
        if not binary:
            raise OSError(f"Unknown OS '{osname}'")

        if osname == "Windows":
            # work around for https://bugs.chromium.org/p/chromium/issues/detail?id=158372
            cmd = rf"""wmic datafile where "name={binary!r}" get version /value"""
            verstr = os.popen(cmd).read().strip().removeprefix("Version=")
        else:
            verstr = (
                os.popen(f"'{binary}' --version")
                .read()
                .removeprefix("Chromium ")
                .strip()
            )
        return verstr

    @staticmethod
    def chromium(
            headless: bool = False,
            enable_log_performance: bool = False,
            enable_log_console: bool = False,
            enable_log_driver: bool = False,
            log_dir: str = "./logs",
            driver_path: str | None = None,
            binary: str | None = None,
            options: webdriver.ChromeOptions | None = None,
    ) -> webdriver.Chrome:
        """
        this method assumes you're on linux and the driver is already installed
        """
        _log_method()

        options = options or Selenium.chrome_options()
        if binary:
            options.binary_location = binary
        else:
            raise FileNotFoundError("Must provide Chromium path.")

        options.headless = headless

        # This is the new way to run headless in the future. Unfortunately it crashes a lot.  # noqa: E501
        # https://crbug.com/chromedriver/4353
        # https://crbug.com/chromedriver/4406
        # if headless:
        #     options.add_argument("--headless=new")

        logging_prefs = {"browser": "OFF", "performance": "OFF", "driver": "OFF"}
        # https://www.skptricks.com/2018/08/timed-out-receiving-message-from-renderer-selenium.html
        # options.set_capability('pageLoadStrategy', 'none')
        # options.set_capability('pageLoadStrategy', 'normal')

        if enable_log_console:
            logging_prefs["browser"] = "ALL"

        # by default performance is disabled.
        if enable_log_performance:
            logging_prefs["performance"] = "ALL"
            options.set_capability(
                "perfLoggingPrefs",
                {
                    "enableNetwork": True,
                    "enablePage": False,
                    "enableTimeline": False,
                },
            )

        args: list | None = None
        logpath = None
        if enable_log_driver:
            lp = os.path.abspath(os.path.expanduser(log_dir))
            logpath = os.path.join(lp, "chromedriver.log")
            args = [
                # "--verbose"
            ]
            logging_prefs["driver"] = "ALL"

        options.set_capability("loggingPrefs", logging_prefs)

        logger.debug("initializing chromedriver")
        if driver_path:
            service = ChromeService(
                executable_path=driver_path,
                service_args=args,
                log_path=logpath,
            )
        else:
            service = ChromeService(
                service_args=args,
                log_path=logpath,
            )

        driver = webdriver.Chrome(service=service, options=options)

        driver_vers = driver.capabilities["chrome"]["chromedriverVersion"].split(" ")[0]
        browser_vers = driver.capabilities["browserVersion"]

        drvmsg = f"Driver info: chromedriver={driver_vers}"
        bsrmsg = f"Browser info:    chromium={browser_vers}"

        dver = Version.coerce(driver_vers)
        bver = Version.coerce(browser_vers)
        if dver.major != bver.major:
            logger.critical(drvmsg)
            logger.critical(bsrmsg)
            logger.critical("chromedriver and browser versions not in sync!!")
            logger.warning(
                "https://chromedriver.chromium.org/downloads for the latest version"
            )
        else:
            logger.info(drvmsg)
            logger.info(bsrmsg)
        Selenium.log_options(options)

        return driver

    @staticmethod
    def get_edge_version(binary: str | None = None) -> str:
        logger.debug("get_edge_version")
        osname = platform.system()
        if not binary:
            binary = EDGE_PATHS.get(osname, None)
            if not binary:
                raise OSError(f"Unknown OS '{osname}'")

        if osname == "Windows":
            # work around for https://bugs.chromium.org/p/chromium/issues/detail?id=158372
            cmd = rf"""wmic datafile where "name={binary!r}" get version /value"""
            verstr = os.popen(cmd).read().strip().removeprefix("Version=")
        else:
            cmd = f"'{binary}' --version"
            verstr = os.popen(cmd).read().removeprefix("Microsoft Edge ").strip()
        return verstr

    @staticmethod
    def get_edgedriver_best_version(verstr: str) -> str:
        os_to_azure = {
            "Darwin": "MACOS",
            "Windows": "WINDOWS",
            "Linux": "LINUX",
        }
        osname = platform.system()
        _os_name = os_to_azure.get(osname, None)

        version = Version.coerce(verstr)

        major_version = version.major

        url = f"https://msedgedriver.azureedge.net/LATEST_RELEASE_{major_version}_{_os_name}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        if resp.status_code != 200:
            raise Exception(f"Unexpected status {resp.status_code} {resp.reason} {url}")

        return resp.content.decode(resp.apparent_encoding).strip()

    @staticmethod
    def edge_options() -> webdriver.EdgeOptions:
        opts = (
            "--disable-extensions",
            "--allow-running-insecure-content",
            "--ignore-certificate-errors",
            "--disable-single-click-autofill",
            "--disable-autofill-keyboard-accessory-view[8]",
            "--disable-full-form-autofill-ios",
            # https://bugs.chromium.org/p/chromedriver/issues/detail?id=402#c128
            # "--dns-prefetch-disable",
            "--disable-infobars",
            # edgedriver crashes without these two in linux
            "--no-sandbox",
            "--disable-dev-shm-usage",
            # it's possible we no longer need to do these
            # "enable-automation",  # https://stackoverflow.com/a/43840128/1689770
            # "--disable-browser-side-navigation",  # https://stackoverflow.com/a/49123152/1689770
            # "--disable-gpu",  # https://stackoverflow.com/q/51959986/2532408
            # # https://groups.google.com/forum/m/#!topic/chromedriver-users/ktp-s_0M5NM[21-40]
            # "--enable-features=NetworkService,NetworkServiceInProcess",
        )
        options = webdriver.EdgeOptions()
        for opt in opts:
            options.add_argument(opt)
        return options

    @staticmethod
    def edge(
            headless: bool = False,
            enable_log_performance: bool = False,
            enable_log_console: bool = False,
            enable_log_driver: bool = False,
            log_dir: str = "./logs",
            driver_path: str | None = None,
            binary: str | None = None,
            options: webdriver.EdgeOptions | None = None,
    ) -> webdriver.Edge:
        _log_method()

        # edge
        # https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

        options = options or Selenium.edge_options()
        if binary:
            options.binary_location = binary

        options.headless = headless

        logging_prefs = {"browser": "OFF", "performance": "OFF", "driver": "OFF"}
        # https://www.skptricks.com/2018/08/timed-out-receiving-message-from-renderer
        # -selenium.html
        # options.set_capability('pageLoadStrategy', 'none')
        # options.set_capability('pageLoadStrategy', 'normal')

        if enable_log_console:
            logging_prefs["browser"] = "ALL"

        # by default performance is disabled.
        if enable_log_performance:
            logging_prefs["performance"] = "ALL"
            options.set_capability(
                "perfLoggingPrefs",
                {
                    "enableNetwork": True,
                    "enablePage": False,
                    "enableTimeline": False,
                },
            )

        args: list | None = None
        logpath = None
        if enable_log_driver:
            lp = os.path.abspath(os.path.expanduser(log_dir))
            logpath = os.path.join(lp, "chromedriver.log")
            args = [
                # "--verbose"
            ]
            logging_prefs["driver"] = "ALL"

        options.set_capability("loggingPrefs", logging_prefs)

        logger.debug("initializing edgedriver")
        if driver_path:
            service = EdgeService(
                executable_path=driver_path,
                service_args=args,
                log_path=logpath,
            )
        else:
            service = EdgeService(
                service_args=args,
                log_path=logpath,
            )
        driver = webdriver.Edge(service=service, options=options)

        driver_vers = driver.capabilities["msedge"]["msedgedriverVersion"].split(" ")[0]
        browser_vers = driver.capabilities["browserVersion"]

        drvmsg = f"Driver info: msedge webdriver={driver_vers}"
        bsrmsg = f"Browser info:          msedge={browser_vers}"

        dver = Version.coerce(driver_vers)
        bver = Version.coerce(browser_vers)
        if dver.major != bver.major:
            logger.critical(drvmsg)
            logger.critical(bsrmsg)
            logger.critical("msedgedriver and browser versions not in sync!!")
            logger.warning(
                "https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ "
                "for the latest version"
            )
        else:
            logger.info(drvmsg)
            logger.info(bsrmsg)
        Selenium.log_options(options)
        return driver

    ############################################################################
    def set_window_size(self, size: str = "720") -> None:
        if size == "max":
            self.driver.maximize_window()
            return

        width, height = Selenium.DIMENSIONS.get(
            size, Selenium.DIMENSIONS.get(size, (1280, 720))
        )
        self.driver.set_window_size(width, height)

    def set_main_window_handle(self, window: str | None = None) -> str:
        if not window:
            # does the main_window_handle exist and point to an available window?
            if not self.main_window_handle:
                try:
                    window = self.driver.current_window_handle
                except NoSuchWindowException:
                    try:
                        window = self.driver.window_handles[0]
                    except WebDriverException:
                        # Have we closed all the windows?
                        raise
        if window:
            self.main_window_handle = window
        return self.main_window_handle

    ############################################################################
    def close(self) -> None:
        if self.driver is not None:
            self.driver.close()

    ############################################################################
    def quit(self) -> None:  # noqa: A003
        if self.driver is not None:
            self.driver.quit()

    ############################################################################
    # def __del__(self):
    #     print("__del__ called in acuselenium")
    #     self.quit()

    ############################################################################
    def __repr__(self) -> str:
        browser = self.driver.name if self.driver is not None else "NoBrowserSet"
        url = self.baseurl
        return f"{self.__class__.__name__} :: {browser} -> {url}"
