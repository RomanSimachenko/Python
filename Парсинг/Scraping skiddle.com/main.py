import csv
import requests
from bs4 import BeautifulSoup
import lxml
import json


def get_data():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    with open(f'data/all_fest.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Name', 'Date', 'Place', 'Age', 'Contacts'])
    with open(f'data/all_fest.json', 'a') as file:
        json.dump([], file, indent=4, ensure_ascii=False)
    for num in range(0, 192, 24):
        page = (num // 24) + 1
        print(f'page {page}/8')
        url = f'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=21%20Jul%202021&to_date=&where%5B%5D=2&where%5B%5D=3&where%5B%5D=4&maxprice=500&o={num}&bannertitle=July'
        html = requests.get(url=url, headers=headers)
        json_data = json.loads(html.text)
        html = json_data['html']
        with open(f'data/html_{page}.html', 'w') as file:
            file.write(html)
        with open(f'data/html_{page}.html') as file:
            html = file.read()
        soup = BeautifulSoup(html, 'lxml')
        all_links = []
        [all_links.append('https://www.skiddle.com/' + el.get('href')) for el in soup.find_all('a', class_='card-details-link')]
        for url in all_links:
            html = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(html.text, 'lxml')
            fest_block = soup.find('div', class_='top-info-cont')
            try:
                fest_name = fest_block.find('h1').text.strip()
            except Exception as error:
                print(error)
                fest_name = 'None'
            try:
                fest_date = fest_block.find('h3').text.strip()
            except Exception as error:
                print(error)
                fest_date = 'None'
            try:
                fest_place = fest_block.find_all('p')[1].text.strip()
            except Exception as error:
                print(error)
                fest_place = 'None'
            try:
                fest_age = fest_block.find_all('p')[2].text.strip()
            except Exception as error:
                print(error)
                fest_age = 'None'
            fest_place_link = 'https://www.skiddle.com/' + fest_block.find('a', class_='tc-white').get('href')
            html = requests.get(url=fest_place_link, headers=headers)
            soup = BeautifulSoup(html.text, 'lxml')
            fest_contacts = ''
            try:
                contact_items = soup.find_all('div', class_='margin-bottom-20')[-1].find_all('p')
                for item in contact_items:
                    fest_contacts = fest_contacts + item.text + '; '
            except Exception as error:
                print(error)
                contact_items = 'None'
            all_fest = []
            with open(f'data/all_fest.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow([fest_name, fest_date, fest_place, fest_age, fest_contacts])
            all_fest.append({
                'Name': fest_name,
                'Date': fest_date,
                'Place': fest_place,
                'Age': fest_age,
                'Contacts': fest_contacts,
                })
    with open(f'data/all_fest.json', 'w') as file:
        json.dump(all_fest, file, indent=4, ensure_ascii=False)


def main():
    get_data()


if __name__ == '__main__':
    main()
