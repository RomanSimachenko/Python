import logging
from aiogram import Bot, Dispatcher, executor, types
import config
from downloader import download_video


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=('start', 'help',))
async def start_help(message: types.Message):
    await message.reply("Hey! This bot can download and send back \
TikTok videos. Just put the video link in the chat!")


@dp.message_handler()
async def echo(message: types.Message):
    if 'tiktok.com' in message.text:
        video = await download_video(message.text.strip())
        if video:
            video.title = video.title if video.title.strip() else "Without title"
            video_caption = f"<a href=\"{video.url}\"><b>{video.title}</b></a>"
            if message['from']['id'] != message['chat']['id']:
                video_caption += f"\n(from <a href=\
\"https://t.me/{message['from']['username']}\">{message['from']['first_name']}</a>)"
            await message.answer_video(open(video.path, 'rb'), caption=video_caption, parse_mode='html')
            await message.delete()
        else:
            await message.reply("🚫 Something went wrong! The video may be hidden or removed")


def run_bot():
    executor.start_polling(dp, skip_updates=True)
