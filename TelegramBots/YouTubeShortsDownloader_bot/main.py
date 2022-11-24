from bot import start_telegram_bot
from exeptions import CantDownloadYouTubeVideo


def main():
    try:
        start_telegram_bot()
    except (KeyboardInterrupt, CantDownloadYouTubeVideo,):
        pass


if __name__ == "__main__":
    main()
