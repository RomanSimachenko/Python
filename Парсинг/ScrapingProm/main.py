from bs4 import BeautifulSoup
import requests


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6",
    "cache-control": "max-age=0",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}


def get_pagination(url: str) -> int:
    url = url[:url.find('?')] + ";1" + url[url.find('?'):]
    page = 2
    while True:
        url = url.replace(str(page - 1), str(page)).strip()
        response = requests.get(url=url, headers=headers)
        print(url)
        print(response.url)
        print('#' * 20)
        if url != response.url:
            return page - 1
        page += 1


print(get_pagination(
    url="https://prom.ua/ua/Naushniki-i-mikrofony?a14127=143012&a14127=143013"))
