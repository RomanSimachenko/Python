from modules.webdriver import WebDriver

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import requests

from . import google
from .. import config
from .. import services
from .. import exeptions


def login(webdriver: WebDriver) -> None:
    try:
        auth(webdriver)
    except NoSuchElementException:
        raise exeptions.CantAuthenticateException("Program can't authenticate in Discord")

    try:
        sitekey = requests.post(
            url=config.DISCORD_API_AUTH_URL,
            headers=config.DISCORD_HEADERS,
            json=config.DISCORD_JSON
        ).json()['captcha_sitekey']
    except KeyError:
        pass
    else:
        result = services.solve_captcha('hcaptcha', sitekey, config.DISCORD_API_AUTH_URL)

        _send_verification_email(result['code'])
        webdriver.delay(1)

        google.verify_discord_email(webdriver)
        webdriver.close_tab(1)

        auth(webdriver)


def auth(webdriver: WebDriver) -> None:
    webdriver.driver.get(config.DISCORD_LOGIN_URL)
    webdriver.delay(3)

    webdriver.driver.find_element(By.NAME, 'email').send_keys(config.DISCORD_EMAIL)
    discord_password_field = webdriver.driver.find_element(By.NAME, 'password')
    discord_password_field.send_keys(config.DISCORD_PASSWORD)

    webdriver.find_element_by_xpath("//button[@type='{}']", ('submit',), True)
    webdriver.delay(3)


def _send_verification_email(captcha_key: str) -> None:
    json_data = config.DISCORD_JSON.copy()
    json_data['captcha_key'] = captcha_key

    response = requests.post(
        url=config.DISCORD_API_AUTH_URL,
        headers=config.DISCORD_HEADERS,
        json=json_data
    )
    print(response.text)
