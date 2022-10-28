import requests, datetime, csv, os, json, time
from bs4 import BeautifulSoup


start_time = time.time()
def get_data():
    cuttent_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    with open(f'labirint_{cuttent_time}.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([
            'Название книги',
            'Автор',
            'Издательство',
            'Цена со скидкой',
            'Цена без скидки',
            'Скидка',
            'Наличие на складе',
        ])
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    url = 'https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table'
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    pages_count = int(soup.find('div', class_='pagination-number').find_all('a')[-1].get_text(strip=True))
    pages_count = 2
    books_data = []
    for page in range(1, pages_count + 1):
        url = f'https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table&page={page}'
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        books_items = soup.find('tbody', class_='products-table__body').find_all('tr')
        for book in books_items:
            book_data = book.find_all('td')
            try:
                book_title = book_data[0].find('a').text.strip()
            except:
                book_title = 'Нету названия'
            try:
                book_author = book_data[1].find('a').text.strip()
            except:
                book_author = 'Нету автора'
            try:
                book_publish = book_data[2].get_text(strip=True).replace(':', ': ')
            except:
                book_publish = 'Нету издательства'
            try:
                book_new_price = int(book_data[3].find('div', class_='price').find('span', class_='price-val').find('span').text.strip().replace(' ', ''))
            except:
                book_new_price = 'Нету новой цены'
            try:
                book_old_price = int(book_data[3].find('div', class_='price').find('span', class_='price-old').find('span').text.strip().replace(' ', ''))
            except:
                book_old_price = 'Нету старой цены'
            try:
                book_discount = book_data[3].find('div', class_='price').find('a').text.strip().replace('?', '')
            except:
                try:
                    book_discount = '-' + str(int(100 - (book_new_price * 100) / book_old_price)) + '%'
                except:
                    book_discount = '0%'
            try:
                book_state = book_data[-1].find('div').text.strip()
            except:
                book_state = 'Нет в наличии'
            # print(book_title)
            # print(book_author)
            # print(book_publish)
            # print(book_new_price)
            # print(book_old_price)
            # print(book_discount)
            # print(book_state)
            # print('#'*20)
            books_data.append({
                'book_title': book_title,
                'book_author': book_author,
                'book_publish': book_publish,
                'book_new_price': book_new_price,
                'book_old_price': book_old_price,
                'book_discount': book_discount,
                'book_state': book_state,
            })
            with open(f'labirint_{cuttent_time}.csv', 'a', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow([
                    book_title,
                    book_author,
                    book_publish,
                    book_new_price,
                    book_old_price,
                    book_discount,
                    book_state,
                ])
        print(f'Обработано {page}/{pages_count}...')
        time.sleep(1)
        with open(f'labirint_{cuttent_time}.json', 'w') as file:
            json.dump(books_data, file, indent=4, ensure_ascii=False)


def main():
    get_data()
    finish_time = int(time.time() - start_time)
    print(f'Затраченое на работу скрипта время: {finish_time} секунд')


if __name__ == '__main__':
    main()