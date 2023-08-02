from __future__ import annotations

import errno
import os as os
import platform
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Tuple, Union

import pyderman as pydm
import requests
from selenium import webdriver  # noqa: E402
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.service import Service as FirefoxService
from semantic_version import Version  # type: ignore

from screenpy_examples.screenpy_logger import create_logger

if TYPE_CHECKING:
    from selenium.webdriver.common.options import ArgOptions

__all__ = ["Selenium"]

typeWebDriver = Union[
    webdriver.Firefox,
    webdriver.Chrome,
    webdriver.Edge,
]


logger = create_logger("sel")

EDGE = "edge"
CHROME = "chrome"
FIREFOX = "firefox"


################################################################################
################################################################################
class Selenium:
    DIMENSIONS: Mapping[str, Tuple[int, int]] = {
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
        enable_log_performance=False,
        enable_log_console=False,
        enable_log_driver=False,
        log_path: str = "./logs",
        driver_version="auto",
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
        return

    ############################################################################
    @staticmethod
    def make_screenshot_path(output_dir="./logs", screenshots="screenshots"):
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
    def log_options(options: ArgOptions):
        opts = "\n".join(options.arguments)
        logger.debug(f"{opts}")

    @staticmethod
    def create_driver(
        browser: str,
        headless: bool = False,
        enable_log_performance=False,
        enable_log_console=False,
        enable_log_driver=False,
        log_path: str = "./logs",
        version="auto",
    ):
        """
        driver_version: the options are 'latest', 'auto', or a specific version
        """
        if browser.lower() == FIREFOX:
            driver = Selenium.firefox(
                headless=headless,
                enable_log_driver=enable_log_driver,
                log_path=log_path,
                version=version,
            )

        elif browser.lower() == CHROME:
            driver = Selenium.chrome(
                headless,
                enable_log_performance,
                enable_log_console,
                enable_log_driver,
                log_path,
                version,
            )

        elif browser.lower() == EDGE:
            driver = Selenium.edge(
                headless,
                enable_log_performance,
                enable_log_console,
                enable_log_driver,
                log_path,
                version,
            )

        else:
            raise ValueError(f"Unknown browser: {browser}")

        # driver.set_page_load_timeout(self.timeout)
        # driver.set_script_timeout(self.timeout)
        return driver

    @staticmethod
    def firefox_version():
        return

    @staticmethod
    def firefox_options():
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
        headless=False,
        enable_log_performance=False,
        enable_log_console=False,
        enable_log_driver=False,
        log_path: str = "./logs",
        version="auto",
        options: webdriver.FirefoxOptions = None,
    ):
        """
        version: the options are 'auto', or a specific version
        this method doesn't auto match geckodriver to firefox version
        """
        if not options:
            options = Selenium.firefox_options()
        if headless:
            options.add_argument("--headless")

        if version == "auto":
            version = "latest"

        # 20.1 has a bug where headless doesn't work
        # 19 has a bug where it closes a frame?

        # setting log_path to /dev/null will prevent geckodriver from creating it's
        # own log file.
        # if we enable root logging, we can capture the logging from geckodriver
        # ourselves.
        logpath = "/dev/null"
        options.log.level = "fatal"
        if enable_log_driver:
            log_path = os.path.abspath(os.path.expanduser(log_path))
            logpath = os.path.join(log_path, "geckodriver.log")

        drvdir = os.path.abspath(os.path.join(log_path, os.pardir, "driver/"))
        driverpath = pydm.install(
            browser=pydm.firefox,
            file_directory=drvdir,
            verbose=True,
            chmod=True,
            overwrite=False,
            return_info=False,
            version=version,
        )
        if not os.path.exists(driverpath):
            raise FileNotFoundError("Geckodriver was not downloaded.")

        try:
            driver = webdriver.Firefox(
                service=FirefoxService(executable_path=driverpath, log_path=logpath),
                options=options,
            )
        except OSError:
            logger.critical(
                "OSError: it's possible this ran with the wrong binary already in the "
                "folder.  Attempting to overwrite."
            )
            driverpath = pydm.install(
                browser=pydm.firefox,
                file_directory=drvdir,
                verbose=True,
                chmod=True,
                overwrite=True,
                return_info=False,
                version=version,
            )
            driver = webdriver.Firefox(
                service=FirefoxService(executable_path=driverpath, log_path=logpath),
                options=options,
            )

        driverversion = driver.capabilities["moz:geckodriverVersion"]
        browserversion = driver.capabilities["browserVersion"]

        logger.info(f"Driver info: geckodriver={driverversion}")
        logger.info(f"Browser info:    firefox={browserversion}")
        Selenium.log_options(options)

        if driverversion == "0.20.1":
            if headless:
                raise Exception("Headless mode doesn't work in Gecko Driver 0.20.1")
        return driver

    @staticmethod
    def get_chrome_version():
        install_paths = {
            "Darwin": (
                "/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome"
            ),
            "Windows": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "Linux": "/usr/bin/google-chrome",
        }
        osname = platform.system()
        path = install_paths.get(osname, None)
        if not path:
            raise OSError(f"Unknown OS '{osname}'")

        verstr = os.popen(f"{path} --version").read().strip("Google Chrome ").strip()
        version = Version.coerce(verstr)

        major_version = version.major

        url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        if resp.status_code != 200:
            raise Exception(f"Unexpected status {resp.status_code} {resp.reason} {url}")

        return resp.content.decode("utf-8")

    @staticmethod
    def chrome_options() -> webdriver.ChromeOptions:
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
        headless=False,
        enable_log_performance=False,
        enable_log_console=False,
        enable_log_driver=False,
        log_path: str = "./logs",
        version="auto",
        options: webdriver.ChromeOptions = None,
    ):
        """
        version: the options are 'latest', 'auto', or a specific version
        """
        if not options:
            options = Selenium.chrome_options()
        options.headless = headless

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

        args: Optional[List] = None
        logpath = None
        if enable_log_driver:
            log_path = os.path.abspath(os.path.expanduser(log_path))
            logpath = os.path.join(log_path, "chromedriver.log")
            args = [
                # "--verbose"
            ]
            logging_prefs["driver"] = "ALL"

        options.set_capability("loggingPrefs", logging_prefs)
        if version == "auto":
            try:
                version = Selenium.get_chrome_version()
            except Exception:
                logger.critical(
                    "Exception raised while trying to auto determine chromedriver "
                    "version.  Using 'latest' instead."
                )
                # logger.print_stack_trace()
                version = "latest"

        # create the driver/ folder next to the logs directory
        drvdir = os.path.abspath(os.path.join(log_path, os.pardir, "driver/"))
        driverpath = pydm.install(
            browser=pydm.chrome,
            file_directory=drvdir,
            verbose=True,
            chmod=True,
            overwrite=False,
            return_info=False,
            version=version,
        )
        if not os.path.exists(driverpath):
            raise FileNotFoundError("Chromedriver was not downloaded.")

        try:
            driver = webdriver.Chrome(
                service=ChromeService(
                    executable_path=driverpath, service_args=args, log_path=logpath
                ),
                options=options,
            )
        except OSError:
            logger.critical(
                "OSError: it's possible this ran with the wrong binary already in the "
                "folder.  Attempting to overwrite."
            )
            driverpath = pydm.install(
                browser=pydm.chrome,
                file_directory=drvdir,
                verbose=True,
                chmod=True,
                overwrite=True,
                return_info=False,
                version=version,
            )
            driver = webdriver.Chrome(
                service=ChromeService(
                    executable_path=driverpath, service_args=args, log_path=logpath
                ),
                options=options,
            )

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
    def get_edge_version():
        os_to_azure = {
            "Darwin": "MACOS",
            "Windows": "WINDOWS",
            "Linux": "LINUX",
        }

        install_paths = {
            "Darwin": (
                "/Applications/Microsoft\\ Edge.app/Contents/MacOS/Microsoft\\ Edge"
            ),
            "Windows": (
                "C:\\Windows\\SystemApps\\Edge\\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\\MicrosoftEdge.exe"
            ),
            "Linux": "/usr/bin/microsoft-edge",
        }
        osname = platform.system()
        path = install_paths.get(osname, None)
        _os_name = os_to_azure.get(osname, None)
        if not path:
            raise OSError(f"Unknown OS '{osname}'")

        verstr = os.popen(f"{path} --version").read().strip("Microsoft Edge ").strip()
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
        headless=False,
        enable_log_performance=False,
        enable_log_console=False,
        enable_log_driver=False,
        log_path: str = "./logs",
        version="auto",
        options: webdriver.EdgeOptions = None,
    ):
        # edge
        # https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

        if not options:
            options = Selenium.edge_options()
        options.headless = headless

        caps: Dict[str, Any] = DesiredCapabilities.EDGE
        caps["loggingPrefs"] = {"browser": "OFF", "performance": "OFF", "driver": "OFF"}
        # https://www.skptricks.com/2018/08/timed-out-receiving-message-from-renderer-selenium.html
        # caps['pageLoadStrategy'] = 'none'
        # caps['pageLoadStrategy'] = 'normal'

        if enable_log_console:
            caps["loggingPrefs"]["browser"] = "ALL"

        # by default performance is disabled.
        if enable_log_performance:
            caps["loggingPrefs"]["performance"] = "ALL"
            caps["perfLoggingPrefs"] = {
                "enableNetwork": True,
                "enablePage": False,
                "enableTimeline": False,
            }

        args: Optional[List] = None
        logpath = None
        if enable_log_driver:
            log_path = os.path.abspath(os.path.expanduser(log_path))
            logpath = os.path.join(log_path, "msedgedriver.log")
            args = [
                # "--verbose"
            ]
            caps["loggingPrefs"]["driver"] = "ALL"
        if version == "auto":
            try:
                version = Selenium.get_edge_version()
            except Exception:
                logger.critical(
                    "Exception raised while trying to auto determine edgedriver "
                    "version.  Using 'latest' instead."
                )
                # logger.print_stack_trace()
                version = "latest"

        drvdir = os.path.abspath(os.path.join(log_path, os.pardir, "driver/"))
        driverpath = pydm.install(
            browser=pydm.edge,
            file_directory=drvdir,
            verbose=True,
            chmod=True,
            overwrite=False,
            return_info=False,
            version=version,
        )
        if not os.path.exists(driverpath):
            raise FileNotFoundError("Edgedriver was not downloaded.")

        try:
            driver = webdriver.Edge(
                executable_path=driverpath,
                options=options,
                service_log_path=logpath,
                service_args=args,
                capabilities=caps,
            )
        except OSError:
            logger.critical(
                "OSError: it's possible this ran with the wrong binary already in the "
                "folder.  Attempting to overwrite."
            )
            # try again.
            driverpath = pydm.install(
                browser=pydm.edge,
                file_directory=drvdir,
                verbose=True,
                chmod=True,
                overwrite=True,
                return_info=False,
                version=version,
            )
            driver = webdriver.Edge(
                executable_path=driverpath,
                options=options,
                service_log_path=logpath,
                service_args=args,
                capabilities=caps,
            )

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
    def set_window_size(self, size: str = "720"):
        if size == "max":
            self.driver.maximize_window()
            return

        width, height = Selenium.DIMENSIONS.get(
            size, Selenium.DIMENSIONS.get(size, (1280, 720))
        )
        self.driver.set_window_size(width, height)

    ############################################################################
    def close(self):
        if self.driver is not None:
            self.driver.close()

    ############################################################################
    def quit(self):
        if self.driver is not None:
            self.driver.quit()

    ############################################################################
    # def __del__(self):
    #     self.quit()

    ############################################################################
    def __repr__(self):
        browser = self.driver.name if self.driver is not None else "NoBrowserSet"
        url = self.baseurl
        return f"{self.__class__.__name__} :: {browser} -> {url}"
