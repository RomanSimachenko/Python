from twocaptcha import TwoCaptcha
from typing import Dict

from . import config


def solve_captcha(captcha: str, sitekey: str, url: str) -> Dict:
    result = {}

    solver = TwoCaptcha(config.TWOCAPTCHA_API_KEY)

    match captcha:
        case 'recaptcha': result = solver.recaptcha(sitekey=sitekey, url=url)
        case 'hcaptcha': result = solver.hcaptcha(sitekey=sitekey, url=url)

    return result
