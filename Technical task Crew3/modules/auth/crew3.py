from modules.webdriver import WebDriver

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

import requests
from bs4 import BeautifulSoup
from random import randrange

from .. import config
from .. import services


def login(webdriver: WebDriver) -> None:
    auth(webdriver)


def auth(webdriver: WebDriver) -> None:
    webdriver.driver.get(config.CREW3_SOURCE_URL)
    webdriver.delay(3)

    webdriver.find_element_by_xpath(
        "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{}')]",
        ('connect',),
        True
    )
    webdriver.delay(1)

    webdriver.find_element_by_xpath(
        "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{}')]",
        ('discord',),
        True
    )
    webdriver.delay(3)

    webdriver.find_element_by_xpath("//div[text()[contains(., '{}')]]", ('Авторизувати', 'Authorise',), True)
    webdriver.delay(3)


def solve_discord_quest(webdriver: WebDriver) -> None:
    webdriver.driver.get(config.CREW3_QUESTBOARD_URL)
    webdriver.delay(3)

    _close_popups(webdriver)

    _press_button_connect_discord(webdriver)

    webdriver.find_element_by_xpath(
        "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{}')]",
        ('connect', 'join', 'discord',),
        True
    )
    webdriver.delay(3)

    sitekey = _get_sitekey(config.ZKSYNC_CAPTCHA_URL)

    result = services.solve_captcha('recaptcha', sitekey, config.ZKSYNC_CAPTCHA_URL)

    _connect_discord_channel(webdriver, result['code'])

    try:
        send_message_element = webdriver.find_element_by_xpath(
            "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{}')]",
            ('1-verify',),
            False
        )
    except NoSuchElementException:
        pass
    else:
        verify_discord_step1(webdriver, send_message_element)

    claim_reward(webdriver)


def solve_quests(webdriver: WebDriver) -> None:
    ANSWERS = (
        "No", "zkSync", "they use the zkSync logo as a profile picture", "All the above", "All the above",
        "They private messaged you first (DM)", "All of the above",
        "NEVER! Sharing your secret phrase or private key means giving up control of your wallet and connecting your "
        "wallet to an unknown site can drain your funds from your wallet", "Agree"
    )

    webdriver.driver.get(config.CREW3_QUESTBOARD_URL)
    webdriver.delay(3)

    _close_popups(webdriver)

    for answer in ANSWERS:
        webdriver.driver.find_elements(By.CLASS_NAME, "chakra-heading")[1].click()
        webdriver.delay(3)

        try:
            answer_textarea_element = webdriver.driver.find_element(By.CLASS_NAME, "chakra-textarea")
            answer_textarea_element.send_keys(answer)
            webdriver.delay(1)
        except NoSuchElementException:
            for el in webdriver.driver.find_elements(By.CLASS_NAME, "chakra-text"):
                if el.text.strip().lower() == answer.strip().lower():
                    el.click()
            webdriver.delay(1)

        webdriver.find_element_by_xpath(
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{}')]",
            ('claim',),
            True
        )
        webdriver.delay(3)


def _close_popups(webdriver: WebDriver) -> None:
    for _ in range(2):
        for event in ('got it', 'skip', 'next', 'Not now', 'close', 'got it!'):
            try:
                button_element = webdriver.find_element_by_xpath(
                    "//div[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{}')]",
                    (event,),
                    False
                )
                webdriver.driver.execute_script("arguments[0].click();", button_element)
                webdriver.delay(1)
            except NoSuchElementException:
                continue
    webdriver.driver.get(webdriver.driver.current_url)
    webdriver.delay(2)


def _press_button_connect_discord(webdriver: WebDriver) -> None:
    for attempt in range(2):
        try:
            webdriver.find_element_by_xpath(
                "//h2[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{}')]",
                ('discord', 'join',),
                True
            )
            webdriver.delay(1)
            break
        except ElementClickInterceptedException:
            try:
                webdriver.driver.find_element(By.NAME, "name").send_keys(f"_newone{randrange(10, 99)}")
                button_element = webdriver.find_element_by_xpath(
                    "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{}')]",
                    ('next',),
                    False
                )
                webdriver.driver.execute_script("arguments[0].click();", button_element)
                webdriver.delay(1)
            except NoSuchElementException:
                continue
            else:
                webdriver.driver.get(config.CREW3_QUESTBOARD_URL)
                webdriver.delay(3)


def _get_sitekey(url: str) -> str:
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')

    sitekey = soup.find('div', class_='g-recaptcha').get('data-sitekey').strip()

    return sitekey


def _connect_discord_channel(webdriver, captcha_key) -> None:
    webdriver.switch_tab(1)
    webdriver.driver.get(config.ZKSYNC_CAPTCHA_URL + f"/?key={captcha_key}")
    webdriver.delay(3)

    discord_channel_id = webdriver.driver.current_url.split('/')[-1]
    webdriver.driver.get(config.DISCORD_CHANNEL_INVITE_URL + f"/{discord_channel_id}")
    webdriver.delay(5)

    webdriver.press_key(Keys.ESCAPE)
    webdriver.delay(1)


def verify_discord_step1(webdriver: WebDriver, element: WebElement) -> None:
    element.send_keys("/verify")
    element.send_keys(Keys.TAB)
    webdriver.delay(1)

    for attempt in range(2):
        webdriver.press_key(Keys.ENTER)
        webdriver.delay(2)


def claim_reward(webdriver: WebDriver) -> None:
    webdriver.close_tab(1, 0)
    webdriver.find_element_by_xpath(
        "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{}')]",
        ('claim',),
        True
    )
    webdriver.delay(10)