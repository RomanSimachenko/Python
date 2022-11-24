import requests, csv, lxml, json, os, time, datetime
from bs4 import BeautifulSoup


def get_data():
    url = 'https://imperiya-untov.ru/shop'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    html = requests.get(url=url, headers=headers)
    with open('data/main_html.html', 'w', encoding='utf-8') as file:
        file.write(html.text)
    with open('data/main_html.html', encoding='utf-8') as file:
        html = file.read()
    soup = BeautifulSoup(html, 'lxml')
    pages_count = int(soup.find('ul', class_='page-numbers').find_all('li')[-2].text)
    with open('data/all_items.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Цена', 'Ссылка'])
    for page in range(1, pages_count + 1):
        time.sleep(3)
        print(f'Пройдено страниц {page}/{pages_count}')
        url = f'https://imperiya-untov.ru/shop/page/{page}'
        html = requests.get(url=url, headers=headers)
        folder_name = f'data/page_{page}'
        if os.path.exists(folder_name):
            print('Папка уже существует')
        else:
            os.mkdir(folder_name)
        with open(f'{folder_name}/html_page_{page}.html', 'w', encoding='utf-8') as file:
            file.write(html.text)
        with open(f'{folder_name}/html_page_{page}.html', encoding='utf-8') as file:
            html = file.read()
        soup = BeautifulSoup(html, 'lxml')
        items = soup.find('ul', class_='products columns-3').find_all('li')
        with open(f'{folder_name}/data_page_{page}.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Название', 'Цена', 'Ссылка'])
        for item in items:
            try:
                title = item.find('h2', class_='woocommerce-loop-product__title').text
            except:
                title = 'Нету названия'
            try:
                price = ''.join(item.find('span', class_='price').text.split()[:-1]) + ' рублей'
            except:
                price = 'Нету цены'
            try:
                link = item.find('a').get('href')
            except:
                link = 'Нету ссылки'
            with open(f'{folder_name}/data_page_{page}.csv', 'a', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow([title, price, link])
            with open('data/all_items.csv', 'a', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow([title, price, link])


def main():
    get_data()


if __name__ == '__main__':
    main()
