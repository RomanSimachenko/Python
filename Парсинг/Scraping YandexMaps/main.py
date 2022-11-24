import requests
from pydantic import BaseModel, Field, parse_obj_as
from typing import List
from datetime import datetime
from fake_useragent import UserAgent
from pathlib import Path

COOKIES = {
    'yandexuid': '1617052961655386916',
    'skid': '5380125311655386918',
    'yuidss': '1617052961655386916',
    'ymex': '1686922918.yrts.1655386918',
    'is_gdpr': '0',
    '_ym_uid': '1655386920980143143',
    '_ym_d': '1655584475',
    'gdpr': '0',
    'Session_id': '3:1656017420.5.0.1656017420708:D4VuuQ:28.1.2:1|1592007087.0.2.0:2|3:254267.229459.1dIJzZtIf8YZmIOI2vT7IeQC84w',
    'sessionid2': '3:1656017420.5.0.1656017420708:D4VuuQ:28.1.2:1.499:1|1592007087.0.2.0:2|3:254267.386875.lsFsVwMn709dpjD6XKbfgyB2Lxg',
    'yp': '1971377420.udn.cDpyMG0xbVBM',
    'L': 'CVBSc2YMCHBXYk5xXn1lAEJ6XF9hYntBFV5fCQY0JQ==.1656017420.15017.365206.7f9ad844ce062d8005eecb941ea9efb0',
    'yandex_login': 'r0m1mPL',
    'i': 'IMQWR9sZOE7HXK6zsZB/PkEjo/ks4c4dx46LepTCNxkVZa7oFDRWZgs3zuE0XmbhKX1ndyqU8D+IWs98i6oPxnez1C0=',
    'is_gdpr_b': 'CN/1QxC3eigC',
    '_yasc': 'UsTCDOSlIRxdN/3hn6L51PTJKlY07HEoN/p+fTtMd1dXwht64kc3cw==',
    '_ym_isad': '2',
}

HEADERS = {
    'authority': 'yandex.ru',
    'accept': '*/*',
    'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6',
    'referer': 'https://yandex.ru/maps/org/kafe_pekarnya_lavka/1581539215/reviews/?ll=39.011003%2C45.069588&z=16',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': UserAgent().random,
    'x-retpath-y': 'https://yandex.ru/maps/org/kafe_pekarnya_lavka/1581539215/reviews/?ll=39.011003%2C45.069588&z=16',
}

RANKING_TYPES = {
    "by_relevance_org": "Стандартно",
    "by_time": "За новизною",
    "by_likes_count_desc": "За популярністю",
    "by_rating_asc": "У першу чергу негативні",
    "by_rating_desc": "У першу чергу позитивні"
}

# page = input("Page: ")
page = 1
try:
    if int(page) < 1:
        exit(1)
except ValueError:
    exit(1)

# page_size = input("Page size: ")
page_size = 50
try:
    if int(page_size) < 50:
        exit(1)
except ValueError:
    exit(1)

# ranking = input(f"Ranking({', '.join(RANKING_TYPES.keys())}): ")
ranking = "by_time"
try:
    RANKING_TYPES[ranking]
except KeyError:
    exit(1)

PARAMS = {
    'ajax': '1',
    'businessId': '1581539215',
    'csrfToken': '6280bbe9fa34399ac245748c84c71e93c587bf30:1656094595',
    'lang': 'uk',
    'page': page,
    'pageSize': page_size,
    'ranking': ranking,
    'reqId': '1656094595007388-1997497538-addrs-upper-yp-76',
    's': '4081253394',
    'sessionId': '1656094594984_602420',
}


PROXIES = {}


class Author(BaseModel):
    name: str
    profile_url: str = Field(alias="profileUrl")
    avatar_url: str = Field(alias="avatarUrl")
    profession_level: str = Field(alias="professionLevel")


class Reaction(BaseModel):
    likes: int
    dislikes: int
    user_reaction: str = Field(alias="userReaction")


class Review(BaseModel):
    id: str = Field(alias="reviewId")
    business_id: str = Field(alias="businessId")
    author: Author
    text: str
    rating: int
    updated_time: datetime = Field(alias="updatedTime")
    has_comments: bool = Field(alias="hasComments")
    reaction: Reaction = Field(alias="reactions")


class Param(BaseModel):
    offset: int
    limit: int
    count: int
    loaded_reviews_count: int = Field(alias="loadedReviewsCount")
    page: int
    total_pages: int = Field(alias="totalPages")
    reviews_remained: int = Field(alias="reviewsRemained")


class Tag(BaseModel):
    text: str
    count: int

class Aspect(BaseModel):
    text: str
    count: int
    positive: int
    negative: int


def _send_response(url: str) -> dict:
    """Sends request to the Yandex Maps API"""
    response = requests.get(url=url, params=PARAMS, cookies=COOKIES, headers=HEADERS, proxies=PROXIES)

    return response.json()['data']


def _fetch_reviews(reviews_json: dict) -> List[Review]:
    """Fetches reviews from given json"""
    reviews = parse_obj_as(List[Review], reviews_json)

    return reviews


def _fetch_params(params_json: dict) -> Param:
    """Fetches params from given json"""
    params = Param.parse_obj(params_json)

    return params


def _fetch_tags(tags_json: dict) -> List[Tag]:
    """Fetches tags from given json"""
    tags = parse_obj_as(List[Tag], tags_json)

    return tags


def _fetch_aspects(aspects_json: dict) -> List[Aspect]:
    """Fetches aspects from given json"""
    aspects = parse_obj_as(List[Aspect], aspects_json)

    return aspects


def main():
    url = "https://yandex.ru/maps/api/business/fetchReviews"

    response = _send_response(url)

    Path("data").mkdir(exist_ok=True)

    reviews = _fetch_reviews(response['reviews'])
    reviews_result_json = '{"reviews": [' + ", ".join(item.json() for item in reviews) + ']}'
    open("data/reviews.json", 'w').write(reviews_result_json)

    params = _fetch_params(response['params'])
    open("data/params.json", 'w').write(params.json())

    tags = _fetch_tags(response['tags'])
    tags_result_json = '{"tags": [' + ", ".join(item.json() for item in tags) + ']}'
    open("data/tags.json", 'w').write(tags_result_json)


    aspects = _fetch_aspects(response['aspects'])
    aspects_result_json = '{"aspects": [' + ", ".join(item.json() for item in aspects) + ']}'
    open("data/aspects.json", 'w').write(aspects_result_json)

if __name__ == "__main__":
    main()
