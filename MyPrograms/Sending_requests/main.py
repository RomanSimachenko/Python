from fake_useragent import UserAgent
from random import randrange
from datetime import datetime
from time import sleep
import requests


def sending_requests(url="https://r0m1mPL.herokuapp.com"):
    try:
        while True:
            headers = {
                "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6",
                "User-Agent": UserAgent().random
            }
            choose_time = randrange(100, 250)
            date_time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                requests.get(url=url, headers=headers)
                sleep(choose_time)
            except Exception as error:
                print(f"[{date_time_now}][ERROR] {error}")
                sleep(choose_time)
    except Exception as error:
        return f"[{date_time_now}][ERROR] {error}, script has stopped!!!"


if __name__ == '__main__':
    print(sending_requests())
