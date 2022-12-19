from modules.webdriver import WebDriver, ChromeDriver
from modules.auth import google, discord, crew3, twitter


def main():
    webdriver = WebDriver(ChromeDriver())

    twitter.login(webdriver)
    # google.login(webdriver)
    discord.login(webdriver)
    crew3.login(webdriver)

    # crew3.solve_discord_quest(webdriver)
    crew3.solve_quests(webdriver)


if __name__ == '__main__':
    main()
