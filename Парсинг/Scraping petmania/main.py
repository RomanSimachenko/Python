from bs4 import BeautifulSoup
import requests
import json
import os

HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
}

try:
    ID = sorted(map(int, os.listdir("./data/images/")))[-1] + 1
except:
    ID = 1


def save_image(img_url: str, k: int) -> str:
    img = requests.get(img_url)
    with open(f"./data/images/{ID}/{k}.jpg", 'wb') as file:
        file.write(img.content)
    return f"./data/images/{ID}/{k}.jpg"


def collect_product_data(product_url: str, product_id: int) -> dict:
    global ID
    print(ID)
    response = requests.get(url=product_url, headers=HEADERS)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')

    images = [soup.find('div', class_="product_carousel").find(
        'div', class_="carousel-container").find('a', class_="thumbnail").get('href').strip()]
    try:
        tmp = soup.find('div', class_="product_carousel").find(
            'div', class_="image_show").find_all('a', class_="thumbnail")
        for a in tmp:
            images.append(a.get('href').strip())
    except:
        pass
    os.mkdir(f"./data/images/{ID}")
    images = [save_image(img_url, k + 1) for k, img_url in enumerate(images)]

    details = {}
    try:
        tmp = [li.text.strip().split(':') for li in soup.find(
            'div', class_="product_carousel").find('ul', class_="list-unstyled attr").find_all('li')]
        for detail in tmp:
            details[detail[0].strip()] = detail[1].strip()
    except:
        pass

    reviews = []
    try:
        r = requests.get(
            url=f"https://petmania.com.ua/index.php?route=product/product/review&product_id={product_id}", headers=HEADERS)
        s = BeautifulSoup(r.text, 'lxml')
        tmp = s.find_all('table')
        for table in tmp:
            reviews.append({
                "Ім'я": table.find_all('tr')[0].find_all('td')[0].text.strip(),
                "Текст": table.find_all('tr')[1].text.strip(),
            })
    except:
        pass

    features = {}
    try:
        tmp = [tr.text.strip().split(':') for tr in soup.find('div', class_="product_carousel").find(
            'div', class_="tabs_info clearfix").find('table', class_="table table-bordered").find_all('tr')]
        for feature in tmp:
            features[feature[0].strip()] = feature[1].strip()
    except:
        pass

    description = {}
    try:
        tmp = soup.find('div', class_="product_carousel").find(
            'div', class_="tabs_info clearfix").find('div', class_="tab-description").find_all('p')
        for index in range(1, len(tmp) + 1):
            description[f"p{str(index)}"] = tmp[index - 1].text.strip()
    except:
        pass

    product_json = {
        'id': ID,
        'Назва': soup.find('div', class_="product_carousel").find('h1', class_="product-title").text.strip(),
        'Зображення': images,
        'Ціна': soup.find('div', class_="product_carousel").find('span', class_="autocalc-product-price").text.strip(),
    }

    try:
        product_json[soup.find('div', class_="product_carousel").find('div', id="product").find('label').text.strip()] = [
            div.text.strip() for div in soup.find('div', class_="product_carousel").find('div', id="product").find_all('div', class_="radio")]
    except:
        pass

    product_json['Деталі'] = details
    product_json['Опис'] = description
    product_json['Відгуки'] = reviews
    product_json['Характеристики'] = features

    ID += 1

    return product_json


def get_product_urls(url: str) -> list:
    try:
        with open("./data/data.json") as file:
            data = json.load(file)
    except:
        data = []
    response = requests.get(url=url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    page_products = soup.find('div', class_="products").find(
        'div', class_="row product-list-js").find_all('div', class_="product-thumb")
    for product in page_products:
        product_url = product.find('div', class_="image").find(
            'a').get('href').strip()
        product_id = int(product.find('div', class_="button-group").find(
            'a', class_="quickbox").get('href').strip().split("product_id=")[-1].split("&")[0])
        data.append(collect_product_data(
            product_url=product_url, product_id=product_id))
    return data


def main():
    url = input().strip()
    data = get_product_urls(url=url)
    with open('./data/data.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
