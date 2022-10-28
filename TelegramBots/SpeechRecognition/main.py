import speech_recognition as sr
from pydub import AudioSegment
import logging
from aiogram import Bot, Dispatcher, executor
from pathlib import Path
from aiogram.types import ContentType, Message
from aiogram.types.file import File
import os

API_TOKEN = os.getenv("API_TOKEN", "")
BASE_DIR = Path(__file__).resolve().parent

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def voice_recognition(voice_path: str) -> str:
    try:
        AudioSegment.from_file(f"{voice_path}.ogg").export(f"{voice_path}.wav", format="wav")

        sample_audio = sr.AudioFile(f"{voice_path}.wav")

        r = sr.Recognizer()

        with sample_audio as source:
            audio_data = r.record(source)

        os.remove(f"{voice_path}.ogg")
        os.remove(f"{voice_path}.wav")

        text_ua = r.recognize_google(audio_data, language="uk-UA")
        return text_ua.strip()
    except:
        return ""

async def save_voice(voice: File, voice_name: str):
    await bot.download_file(file_path=voice.file_path, destination=BASE_DIR / f"{voice_name}.ogg")

@dp.message_handler(content_types=[ContentType.VOICE])
async def voice_message_handler(message: Message):
    voice = await message.voice.get_file()

    await save_voice(voice, voice.file_id)

    recognition_text = await voice_recognition(str(BASE_DIR / voice.file_id))
    
    if recognition_text:
        await message.reply(recognition_text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
