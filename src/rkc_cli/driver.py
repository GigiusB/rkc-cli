# See https://pypi.org/project/webdriver-manager/
import os

from selenium import webdriver

from rkc_cli.cookies import Cookies


def _chrome():
    return webdriver.Chrome()


def _chromium():
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.core.os_manager import ChromeType

    return webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())


def _firefox():
    from selenium.webdriver.firefox.service import Service as FirefoxService
    from webdriver_manager.firefox import GeckoDriverManager

    return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))


def get_driver(cookies: bool = False) -> webdriver.remote.webdriver.WebDriver:
    browser: str = os.getenv("BROWSER") or "chrome"
    fx = {"chrome": _chrome, "firefox": _firefox}[browser]
    driver = fx()
    if cookies:
        driver.get("https://campus.college.ch")
        Cookies().load(driver)
    return driver
