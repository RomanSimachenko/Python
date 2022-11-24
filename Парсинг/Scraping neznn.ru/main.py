from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests

# create headers
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6",
}
# set site url
url = "https://neznn.ru/"


def get_data(url):
    '''
    get data from site
    '''
    # get html
    # save html
    # html = requests.get(url=url, headers=headers)
    # with open('main_page.html', 'w') as file:
    #     file.write(html.text)
    # load html
    with open('main_page.html') as file:
        html = file.read()
    soup = BeautifulSoup(html, 'lxml')
    all_products = soup.find('div', class_='mdl catalog_main categories_on_main').find_all('div', class_='item_block ctgs_block')
    for product in all_products:
        product_title = product.find_all('span')[-1].text
        product_link = "https://neznn.ru/" + product.find('a').get('href')
        print(product_title)
        print(product_link)
        break


def main():
    get_data(url)


if __name__ == '__main__':
    main()
