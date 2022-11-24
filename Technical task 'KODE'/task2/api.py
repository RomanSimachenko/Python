from typing import TypeAlias

from fastapi import FastAPI, Depends
from fastapi_cache import caches, close_caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend
from pydantic import BaseModel
import requests
import json

import config


Celsius: TypeAlias = float
mmHg: TypeAlias = int
mps: TypeAlias = float


class City(BaseModel):
    name: str
    temperature: Celsius
    pressure: mmHg
    wind_speed: mps


app = FastAPI()


def redis_cache():
    return caches.get(CACHE_KEY)


@app.get("/weather")
async def read_item(city_name: str, cache: RedisCacheBackend = Depends(redis_cache)):
    in_cache = await cache.get(city_name)
    if in_cache:
        return json.loads(in_cache)

    api_url = config.OPENWEATHER_API_URL % city_name
    response = requests.get(url=api_url).json()

    city = City(
        name=response['name'], 
        temperature=response['main']['temp'], 
        pressure=response['main']['pressure'],
        wind_speed=response['wind']['speed']
    )

    await cache.set(city_name, str(city.json()))

    return city


@app.on_event('startup')
async def on_startup() -> None:
    rc = RedisCacheBackend("redis://127.0.0.1:6379")
    caches.set(CACHE_KEY, rc)


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await close_caches()
