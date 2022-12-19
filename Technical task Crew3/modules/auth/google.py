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
        raise exeptions.CantAuthenticateException("Program can't authenticate in Google")


def auth(webdriver: WebDriver) -> None:
    webdriver.driver.get(config.GOOGLE_LOGIN_URL)
    webdriver.delay(3)

    google_email_field = webdriver.driver.find_element(By.NAME, "identifier")
    google_email_field.send_keys(config.GOOGLE_EMAIL)

    google_email_field.send_keys(Keys.ENTER)
    webdriver.delay(3)

    google_password_field = webdriver.driver.find_element(By.NAME, "Passwd")
    google_password_field.send_keys(config.GOOGLE_PASSWORD)

    google_password_field.send_keys(Keys.ENTER)
    webdriver.delay(3)

    check_authentication(webdriver)


def check_authentication(webdriver: WebDriver) -> None:
    if "myaccount.google.com" not in webdriver.driver.current_url:
        raise exeptions.InvalidLoginData("Invalid login or password in Google")


def verify_discord_email(webdriver: WebDriver) -> None:
    webdriver.driver.get(config.GOOGLE_EMAIL_URL)
    webdriver.delay(3)

    discord_email = webdriver.driver.find_elements(By.NAME, 'Discord')[0]
    webdriver.driver.execute_script("arguments[0].click();", discord_email)
    webdriver.delay(3)

    webdriver.driver.find_elements(
        By.XPATH,
        "//a[text()[contains(., 'вхід')]]",
    )[-1].click()
    webdriver.press_key(Keys.ENTER)
    webdriver.delay(5)

    check_verification(webdriver)


def check_verification(webdriver: WebDriver) -> None:
    try:
        webdriver.find_element_by_xpath(
            "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{}')]",
            ('authorised',),
            False
        )
    except NoSuchElementException:
        raise exeptions.VerificationFailedException("Discord email verification failed")
