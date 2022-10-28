import logging
import os
import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hlink
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from pathlib import Path
from random import randint

BASE_DIR = Path(__file__).resolve().parent
# BASE_DIR = Path("/home/roma/Downloads")


def download_video(url: str):
    proxy_auth = str(randint(10000, 2147483647)) + ':' + 'passwrd'
    proxies = {'http': 'socks5h://{}@localhost:9050'.format(
        proxy_auth), 'https': 'socks5h://{}@localhost:9050'.format(proxy_auth)}

    options = Options()
    options.add_argument(f"user-agent={UserAgent().random}")
    options.add_argument(f"proxies={proxies}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('headless')
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        window_before = driver.window_handles[0]
        time.sleep(2)
        while True:
            try:
                driver.find_element(By.CLASS_NAME, "def-btn-box").click()
                break
            except:
                time.sleep(0.5)
        driver.get(url)
        driver.switch_to.window(window_before)
        time.sleep(2)
        while True:
            try:
                video_name = driver.find_element(
                    By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[4]/div/div[1]/div[2]/div[1]/div[1]").text
                break
            except:
                time.sleep(0.5)
        attemps = 0
        while not os.path.exists(BASE_DIR / f"{video_name}.mp4"):
            attemps += 1
            time.sleep(0.5)
            if attemps == 60:
                return (False, "", "")
        return True, BASE_DIR / f"{video_name}.mp4", video_name
    except Exception as error:
        print(f"[-] {error}")
    finally:
        driver.close()
        driver.quit()


def tg_bot():
    API_TOKEN = os.getenv("API_TOKEN")
    bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot)

    logging.basicConfig(level=logging.INFO)

    @dp.message_handler(commands=['start', ])
    async def start(message: types.Message):
        await message.reply("Hey there! I can download and send YouTube Shorts videos. Just put a video link into the chat.")

    @dp.message_handler()
    async def echo(message: types.Message):
        global prev_message
        message_text = message.text
        if [1 for url in ("https://youtube.com/shorts/", "https://www.youtube.com/shorts/", "http://youtube.com/shorts/", "http://www.youtube.com/shorts/") if url in message_text.strip()]:
            video_id = message_text.split("/")[4].split("?")[0].strip()
            status, video_path, video_name = download_video(
                "https://www.ssyoutube.com/shorts/" + video_id)
            if status:
                with open(video_path, 'rb') as video:
                    await message.answer_video(video, caption=f"""<strong>{hlink(video_name, message_text.strip())}</strong>""")
                await bot.delete_message(chat_id=message['chat']['id'], message_id=message['message_id'])
                time.sleep(1)
                os.remove(video_path)
            else:
                await bot.send_message(chat_id=message['chat']['id'], text="""<strong>Failed to load the video.</strong>""")
        prev_message = message

    executor.start_polling(dp)


if __name__ == '__main__':
    tg_bot()
