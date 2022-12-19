import undetected_chromedriver as webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver as WB
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from abc import ABC, abstractmethod
from typing import Union
import time
from urllib.error import URLError

from . import exeptions


class Driver(ABC):
    @abstractmethod
    def init_driver(self) -> WB:
        """Initializes the driver"""


class ChromeDriver(Driver):
    def init_driver(self) -> WB:
        options = webdriver.ChromeOptions()

        options.add_argument('--start-maximized')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        # options.add_argument('--proxy-server=%s' % "socks5://127.0.0.1:9050")
        options.add_argument('--ignore-certificate-errors')

        try:
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        except (ConnectionError, URLError):
            raise exeptions.NoInternetConnectionException("You have no internet connection")

        return driver


class WebDriver:
    """Main class of the Selenium Web Driver"""

    def __init__(self, driver: Driver) -> None:
        self.driver = driver.init_driver()

    def delay(self, seconds: int) -> None:
        time.sleep(seconds)

    def switch_tab(self, tab_number: int) -> None:
        self.driver.switch_to.window(self.driver.window_handles[tab_number])

    def close_tab(self, tab_number: int, tab_next: int = 0) -> None:
        self.switch_tab(tab_number)
        self.driver.close()
        self.switch_tab(tab_next)

    def press_key(self, key: str) -> None:
        ActionChains(self, self.driver).key_down(key)

    def find_element_by_xpath(self, xpath_expression: str, alternatives: tuple, click: True) -> Union[None, WebElement]:
        for alt in alternatives:
            try:
                element = self.driver.find_element(By.XPATH, xpath_expression.format(alt))
                if click:
                    element.click()
                    return None
                else:
                    return element
            except NoSuchElementException:
                continue

        raise NoSuchElementException
