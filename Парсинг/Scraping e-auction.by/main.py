# -*- coding: cp1251 -*-
from selenium import webdriver
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from auth_data import login, password, with_cookies
import requests, time, pickle


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
    "application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/91.0.4472.124 Safari/537.36",
}


def get_post_url(url):
    html = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    tmp = soup.find('div', class_='bx-catalog-element').find_all('div')[-1]
    id = tmp.get('id').strip().split("_")[2]
    tmp = tmp.find_all('input')
    shop, region_user = [el.get('value') for el in tmp]
    return f"https://e-auction.by/shop/zapchasti-dlya-avto/%D0%98%D0%9C.3.2021.07109/?action=ADD2BASKET&id=" \
           f"{id}/&ajax_basket=Y&quantity=1&prop%5BSHOP%5D={shop}&prop%5BREGION_USER%5D={region_user}"


def recaptcha():
    frames = driver.find_element_by_tag_name("iframe")
    # driver.switch_to.frame(frames[0])
    time.sleep(3)

    # driver.find_element_by_class_name("recaptcha-checkbox-border").click()
    #
    # driver.switch_to.default_content()
    # frames = driver.find_element_by_xpath("/html/body/div[2]/div[4]").find_elements_by_tag_name("iframe")
    # driver.switch_to.frame(frames[0])
    # time.sleep(3)
    #
    # driver.find_element_by_id("recaptcha-audio-button").click()


def buy_product(url):
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={UserAgent().random}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless")
    try:
        driver = webdriver.Chrome(executable_path="chromedriver/chromedriver.exe",
                                  options=options)
        if with_cookies:
            driver.get("https://e-auction.by/shop/")
            time.sleep(3)
            for cookie in pickle.load(open(f"{login.split('@')[0]}_cookies", "rb")):
                driver.add_cookie(cookie)
            time.sleep(5)
            driver.refresh()
            time.sleep(5)
        else:
            driver.get("https://e-auction.by/personal/")
            time.sleep(3)
            user_login = driver.find_element_by_id("USER_LOGIN")
            user_login.clear()
            user_login.send_keys(login)
            time.sleep(1)
            user_password = driver.find_element_by_id("USER_PASSWORD")
            user_password.clear()
            user_password.send_keys(password)
            time.sleep(1)
            driver.find_element_by_class_name("label-check").click()
            time.sleep(2)
            user_password.send_keys(Keys.ENTER)
            time.sleep(5)
            pickle.dump(driver.get_cookies(), open(f"{login.split('@')[0]}_cookies", "wb"))
        time.sleep(1)
        driver.get(url)
        print("Òîâàð óñïåøíî äîáàâëåí â êîðçèíó.")
        time.sleep(2)
        driver.get("https://e-auction.by/order/")
        time.sleep(3)
        driver.find_element_by_class_name("checkbox").click()
        time.sleep(2)
        driver.find_element_by_class_name("rc-anchor").click()
        time.sleep(5)
        recaptcha()
        time.sleep(5)
    except Exception as error:
        print(error)
    finally:
        driver.close()
        driver.quit()


def main():
    url = input("Ââåäèòå ññûëêó íà òîâàð: ")
    post_url = get_post_url(url)
    print(post_url)
    buy_product(post_url)
    print("Òîâàð óñïåøíî çàêàçàí.")


if __name__ == '__main__':
    main()
# https://e-auction.by/shop/zapchasti-dlya-avto/%D0%98%D0%9C.3.2021.07125/
