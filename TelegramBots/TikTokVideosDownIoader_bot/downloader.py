import requests
from bs4 import BeautifulSoup
from pathlib import Path
import urllib.request
from dataclasses import dataclass
import config
from typing import Literal, Union
import os


@dataclass
class RequestItem:
    """Class for keeping request settings"""
    method: Literal['get', 'post']
    url: str
    params: dict[str, str]
    cookies: dict[str, str]
    headers: dict[str, str]
    data: dict[str, str]


    def __init__(self, 
        method: Literal['get', 'post'],
        url: str,
        params: dict[str, str],
        cookies: dict[str, str],
        headers: dict[str, str],
        data: dict[str, str]
                 ):
        self.method = method
        self.url = url
        self.params = params
        self.cookies = cookies
        self.headers = headers
        self.data = data


    async def send_request(self) -> requests.Response:
        return config.REQUEST_METHODS['post'](
            url=self.url,
            params=self.params,
            cookies=self.cookies,
            headers=self.headers,
            data=self.data
                )


@dataclass
class VideoItem:
    """Class for keeping track of a video"""
    url: str
    title: str = ""
    path: Path = Path()


async def _remove_hashtags(string: str) -> str:
    """Removes hashtags from the string"""
    hashtags = string.split('#')
    result_string, hashtags = hashtags[0].strip(), hashtags[1:]
    for tag in hashtags:
        result_string += ' ' + ' '.join(tag.strip().split()[1:])
    return result_string.strip()


async def download_video(url: str) -> Union[VideoItem, None]:
    """Downloads video by given url"""
    os.makedirs(config.BASE_DIR / 'videos', exist_ok=True)

    video = VideoItem(url=url)

    response = requests.get(url=config.URL, headers=config.HEADERS)
    COOKIES = response.cookies.get_dict()

    DATA = {'id': video.url}
    DATA.update(config.DATA)

    request = RequestItem('post', config.URL, config.PARAMS, 
                          COOKIES, config.HEADERS, DATA)
    response = await request.send_request()
    
    soup = BeautifulSoup(response.text, 'lxml')
    
    try:
        video.title = await _remove_hashtags(soup.find('p', class_="maintext").text.strip())
    except AttributeError:
        return None
    video.path = config.BASE_DIR / f"videos/{video.title}.mp4"

    if os.path.exists(video.path):
        os.remove(video.path)
    try:
        download_url = soup.find('a', class_="without_watermark_hd").get('href').strip()
    except AttributeError:
        try:
            download_url = soup.find('a', class_="without_watermark").get('href').strip()
        except AttributeError:
            try:
                download_url = soup.find('a', class_="without_watermark_direct").get('href').strip()
            except AttributeError:
                try:
                    download_url = soup.find('a', class_="download_link").get('href').strip()
                except AttributeError:
                    return None
    urllib.request.urlretrieve(download_url, video.path)

    return video
