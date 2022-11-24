# -- coding: utf-8 --
import requests, csv, os, time
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import cv2, pytesseract


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}
pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'


start_time = time.time()
def get_data(urllib2=None):
    with open('all_firms.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['nazwa firmy', 'adres', 'www', 'email', 'telefony', 'branże'])
    if not os.path.exists('data'):
        os.mkdir('data')
    links = open('links.txt', 'r').read().strip().split('\n')
    firm_names = []
    firm_sites = []
    j = 0
    for link in links:
        j += 1
        print(f"Link {j} of 44...")
        print(link)
        html = requests.get(url=link, headers=headers)
        soup = BeautifulSoup(html.text, 'lxml')
        pages_count = int(soup.find('div', class_='pagination').find_all('a')[-2].text)
        for page in range(1, pages_count+1):
            url = f'{link}strona-{page}/'
            html = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(html.text, 'lxml')
            get_links = soup.find('ul', class_='wizResBox').find_all('a', class_='wizLnk')
            data_links = [el.get('href') for el in get_links]
            i = 0
            for url in data_links:
                i += 1
                html = requests.get(url=url, headers=headers)
                soup = BeautifulSoup(html.text, 'lxml')
                try:
                    firm_name = soup.find('div', id='nazwaLogo').find('h1').text.strip()
                except:
                    firm_name = 'None'
                try:
                    firm_address = soup.find('div', class_='addrNipBox').find_all('div')[0].text.strip()
                except:
                    firm_address = 'None'

                try:
                    firm_site = soup.find('div', id='wwwAddrBox').find('a',
                                                                       class_='wizLnk allCornerRound3').text.strip()
                except:
                    firm_site = 'None'
                try:
                    tmp = soup.find('div', id='telBox').find('div').find_all('span')
                    firm_telephones = [el.text.strip() for el in tmp]
                except:
                    firm_telephones = 'None'
                try:
                    tmp = soup.find('div', id='brBox').find_all('li')
                    firm_sfera = [el.text.strip() for el in tmp]
                except:
                    firm_sfera = 'None'
                try:
                    image_src = 'https://www.baza-firm.com.pl/' + soup.find_all('div', class_='displayInlineBlock')[-1].find('img').get('src')
                    req = Request(image_src, headers=headers)
                    webpage = urlopen(req).read()
                    with open(f'data/page_{page}_image_{i}.jpeg', 'wb') as file:
                        file.write(webpage)
                    image = cv2.imread(f'data/page_1_image_{i}.jpeg')
                    img = cv2.resize(image, None, fx=2, fy=2)
                    custom = '--oem 3 --psm 6'
                    firm_email = pytesseract.image_to_string(img, config=custom).replace(' ', '').replace('I', 'l').strip()
                except:
                    firm_email = 'None'
                if '@' not in firm_email:
                    firm_email = firm_email.replace('cs', '@')
                if (firm_name not in firm_names) and (firm_site not in firm_sites):
                    with open('all_firms.csv', 'a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file, delimiter=';')
                        writer.writerow([firm_name, firm_address, firm_site, firm_email, firm_telephones, firm_sfera])
                    if firm_name != 'None':
                        firm_names.append(firm_name)
                    if firm_site != 'None':
                        firm_sites.append(firm_site)
                else:
                    print(firm_name)
                    print(firm_site)
                    print(firm_email)
            print(f'Page {page} of {pages_count}...')


def main():
    get_data()
    finish_time = int(time.time() - start_time)
    print(f'Затрачено времени на работу скрипта: {finish_time} секунд')


if __name__ == '__main__':
    main()
