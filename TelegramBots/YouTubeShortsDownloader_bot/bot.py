import logging
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, BASE_DIR, REPLACEABLE_SYMBOLS
from pytube import YouTube
from aiogram.utils.markdown import hlink
import os
from exeptions import CantDownloadYouTubeVideo
from dataclasses import dataclass
from pathlib import Path
import urllib.request


@dataclass
class Video:
    """Class for keeping information about YouTube video"""
    title: str
    link: str
    path: Path


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot)


async def _make_video_title(title: str) -> str:
    """Makes video title"""
    for item in REPLACEABLE_SYMBOLS:
        title = title.replace(item, '')

    return title


async def download_video(message: types.Message) -> None:
    "Downloads video from YouTube by given url"
    try:
        yt = YouTube(message.text.strip())
        yt_title = await _make_video_title(yt.title)

        video = Video(
                title=yt_title, 
                link=message.text.strip(), 
                path=BASE_DIR / f"tmp/{yt_title.replace('?', '')}.mp4", 
            )

        if not os.path.exists(video.path):
            streams = yt.streams
            yt_video = streams.filter(progressive=True, 
                    file_extension='mp4').get_highest_resolution()
            yt_video.download(BASE_DIR / "tmp")
    except:
        raise CantDownloadYouTubeVideo

    await send_video(video, message)


async def send_video(video: Video, message: types.Message) -> None:
    "Sends downloaded video"
    await bot.send_video(
            chat_id=message.chat.id,
            video=open(video.path, 'rb'),
            caption=hlink(video.title, video.link),
        )

    await bot.delete_message(message.chat.id, message.message_id)


async def check_if_shorts(message_text: str) -> bool:
    "Checks if it is an YouTube Shorts video"
    return True if "youtube.com/shorts" in message_text else False


@dp.message_handler(commands=['start', 'help'])
async def start_dialog(message: types.Message):
    await message.reply("Hey! This bot can download and send back YouTube Shorts videos. Just put the video link in the chat!")


@dp.message_handler()
async def echo(message: types.Message):
    if await check_if_shorts(message.text):
        await download_video(message)


def start_telegram_bot() -> None:
    os.makedirs(BASE_DIR / "tmp", exist_ok=True)
    executor.start_polling(dp, skip_updates=True)
