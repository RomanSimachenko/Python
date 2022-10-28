import requests
import img2pdf


def get_data():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    img_list = []
    for num in range(1, 49):
        url = f'https://recordpower.co.uk/flip/Winter2020/files/mobile/{num}.jpg'
        temp = requests.get(url=url, headers=headers)
        html = temp.content
        with open(f'data/img_{num}.jpg', 'wb') as file:
            file.write(html)
            img_list.append(f'data/img_{num}.jpg')
            print(f'Downloaded {num} of 48')
    print('#' * 50)
    print(img_list)
    with open(f'result.pdf', 'wb') as file:
        file.write(img2pdf.convert(img_list))
    print('PDF file created successfully!')


def main():
    get_data()


if __name__ == '__main__':
    main()