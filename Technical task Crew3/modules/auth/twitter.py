from modules.webdriver import WebDriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from .. import config
from .. import exeptions


def login(webdriver: WebDriver) -> None:
    try:
        auth(webdriver)
    except NoSuchElementException:
        raise exeptions.CantAuthenticateException("Program can't authenticate in Twitter")


def auth(webdriver: WebDriver) -> None:
    webdriver.driver.get(config.TWITTER_LOGIN_URL)
    webdriver.delay(3)

    twitter_email_field = webdriver.driver.find_element(By.NAME, "text")
    twitter_email_field.send_keys(config.TWITTER_EMAIL)
    webdriver.delay(1)
    twitter_email_field.send_keys(Keys.ENTER)
    webdriver.delay(3)

    try:
        twitter_password_field = webdriver.driver.find_element(By.NAME, "password")
        twitter_password_field.send_keys(config.TWITTER_PASSWORD)
        webdriver.delay(1)
    except NoSuchElementException:
        twitter_username_field = webdriver.driver.find_element(By.NAME, "text")
        twitter_username_field.send_keys(config.TWITTER_USERNAME)
        webdriver.delay(1)
        twitter_username_field.send_keys(Keys.ENTER)
        webdriver.delay(3)

        twitter_password_field = webdriver.driver.find_element(By.NAME, "password")
        twitter_password_field.send_keys(config.TWITTER_PASSWORD)
        webdriver.delay(1)

    twitter_password_field.send_keys(Keys.ENTER)
    webdriver.delay(3)

    check_authentication(webdriver)


def check_authentication(webdriver: WebDriver) -> None:
    if not webdriver.driver.current_url.endswith("/home"):
        raise exeptions.InvalidLoginData("Invalid login or password in Twitter")
