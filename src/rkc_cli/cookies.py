import json
import os
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


class Cookies:
    def __init__(self):
        self.storage = Path(os.getenv("COOKIES_DIR", Path(__file__).parent)) / ".cookies.json"

    def load(self, driver: "WebDriver"):
        if not self.storage.exists():
            raise FileNotFoundError(f"Cookies file not found: {self.storage}")
        cookies = json.loads(self.storage.read_text())
        for cookie in cookies:
            driver.add_cookie(cookie)

    def store(self, driver: "WebDriver"):
        with self.storage.open("w") as f:
            json.dump(driver.get_cookies(), f, indent=2)
