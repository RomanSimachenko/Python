import json
from operator import index
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def collect_mark_data(mark_url):
    HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6",
        "User-Agent": UserAgent().random,
    }
    print(HEADERS['User-Agent'])
    response = requests.get(mark_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    with open("test.html", 'w') as file:
        file.write(soup.text)


def main():
    # with open("tmp.json") as file:
    #     data = json.load(file)
    # with open("urls.txt", 'a') as file:
    #     for row in data['rows']:
    #         file.write(f"{row['ST13']} ")
    collect_mark_data(
        mark_url="http://www.asean-tmview.org/tmview/get-detail?st13=PH502005000000520")


if __name__ == '__main__':
    main()
