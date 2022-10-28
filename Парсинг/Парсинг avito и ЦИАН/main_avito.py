from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests, time, csv, lxml


def main(product_type, url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,\
                                                                                                               application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6",
        "user-agent": f"{UserAgent().random}",
    }

    # get html page
    html = requests.get(url=url, headers=headers)

    # parse html page
    soup = BeautifulSoup(html.text, 'lxml')

    # get pagination
    pages = soup.find_all('span', class_="pagination-item-JJq_j")[-2].text
    print(f"[INFO] Pages found: {pages}...")

    # bypass all pages
    for page in range(1, pages+1):
        print(f"[INFO] Processing the {page}th page of {pages} pages...")
        time.sleep(2)
        # change url
        if "p=" in url:
            first_url, second_url = url.split("p=")[0], (url.split("p=")[1])[1:]
            url = first_url + str(page) + second_url

        # get html page
        html = requests.get(url=url, headers=headers)

        # parse html page
        soup = BeautifulSoup(html.text, 'lxml')

        # get all products links on the page
        try:
            products_links = ["https://www.avito.ru/" + el.find('a', class_="iva-item-sliderLink-bJ9Pv").get('href') for el
                              in soup.find('div', class_="items-items-kAJAg")
                                  .find_all('div', class_="iva-item-root-Nj_hb")]
        except:
            products_links = []
        print(f"[INFO] Products found: {len(products_links)}...")

        # bypass all links
        for link in products_links:
            time.sleep(2)

            # get html page
            html = requests.get(url=link, headers=headers)

            # parse html page
            soup = BeautifulSoup(html.text, 'lxml')

            # get all data about product
            try:
                product_id = soup.find('div', class_="item-view-search-info-redesign").find('span').text.strip().split()[-1]
            except:
                product_id = None
            try:
                product_seller = soup.find('div', class_="item-view-seller-info")\
                    .find('div', class_="seller-info-value").text.strip()
            except:
                product_seller = None
            try:
                product_address = soup.find('div', class_="item-view-main").find('div', class_="item-address").text.strip()
            except:
                product_address = None
            try:
                product_price = soup.find('div', class_="item-price-wrapper")\
                    .find('span', class_="price-value-string")\
                    .find('div', "seller-info-name").text.strip()
            except:
                product_price = None

            print()
            print(f"# {link}")
            print(product_id)
            print(product_seller)
            print(product_address)
            print(product_price)
            print('#'*50)

            with open('Продажа Ж.csv', 'a', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow([product_type, product_id, product_seller, product_address, product_price])
        break


if __name__ == '__main__':
    # write standard data in a csv file
    with open('Продажа Ж.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Раздел: Жилая недвижимость', 'id (№) объявления', 'Продавец', 'Адрес', 'Цена продажи'])

    file = open("data/avito_urls_1.txt", encoding='utf-8').read()
    for el in file.strip().split("\n"):
        time.sleep(2)
        product_type, url = el.strip().split()[0:2]
        print(product_type, url)
        main(product_type, url)