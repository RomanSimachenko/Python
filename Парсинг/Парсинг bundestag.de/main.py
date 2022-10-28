import os
import requests
import json
import csv
from bs4 import BeautifulSoup


def get_data():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    for number in range(2, 752, 10):
        page = ((number - 2) // 10) + 1
        print(f'page {page}/{str(75)}')
        print('#'*50)
        folder_name = f'data/page_{page}'
        url = f'https://www.bundestag.de/ajax/filterlist/en/members/453158-453158?limit=20&noFilterSet=true&offset={number}'
        if os.path.exists(folder_name):
            print(f'folder {page} is already exists...')
        else:
            os.mkdir(folder_name)
        html = requests.get(url=url, headers=headers)
        with open(f'{folder_name}/html_{page}.html', 'w', encoding='utf-8') as file:
            file.write(html.text)
        with open(f'{folder_name}/html_{page}.html') as file:
            html = file.read()
        soup = BeautifulSoup(html, 'lxml')
        items = soup.find('body').find_all(class_='bt-open-in-overlay')
        with open('data/all_data.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(["Name", 'Organization', 'Link', 'Profession', 'Social networks', 'logo'])
        for item in items:
            try:
                title1 = item.get('title').strip()
            except:
                title1 = 'None'
            try:
                title2 = item.find('p', class_='bt-person-fraktion').text.strip()
            except:
                title2 = 'None'
            main_site_link = item.get('href')
            html = requests.get(url=main_site_link, headers=headers)
            soup = BeautifulSoup(html.text, 'lxml')
            try:
                job = soup.find('div', class_='bt-profil row').find('div', class_='bt-biografie-beruf').text.strip()
            except:
                job = 'None'
            try:
                links = soup.find('div', class_='bt-profil row').find('ul', class_='bt-linkliste').find_all('a')
                social_networks = ''
                for link in links:
                    social_networks = social_networks + link.get('title') + ' - ' + link.get('href') + ';'
            except:
                social_networks = 'None'
            try:
                logo = 'https://www.bundestag.de' + soup.find('div', class_='bt-profil row').find('div', class_='col-xs-12 col-sm-8 col-md-9 pull-right bt-logo-partei').find('img').get('src')
            except:
                logo = 'None'
            # print(title1)
            # print(title2)
            # print(main_site_link)
            # print(job)
            # print(social_networks)
            # print(logo)
            # print('#'*50)
            with open('data/all_data.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow([title1, title2, main_site_link, job, social_networks, logo])


def main():
    get_data()


if __name__ == '__main__':
    main()