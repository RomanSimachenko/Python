import config
import services 
import exeptions
from dataclasses import dataclass
from dataclasses import field
from typing import Literal


@dataclass
class UniversityItem:
    name: str
    url: str
    k_all: int = 0
    k_higher: int = 0
    k_kv: int = 0
    k_k: int = 0
    entrants: tuple[services.EntrantItem, ...] = ()


@dataclass
class RequestItem:
    method: Literal['get', 'post']
    url: str = config.API_URL
    headers: dict = field(default_factory=dict)
    data: dict = field(default_factory=dict)
    params: dict = field(default_factory=dict)
    

async def process_un(university: str, k_bal: float) -> UniversityItem:
    """Processes all universities"""
    try:
        un_name, un_url = await services._form_un(university.strip().split('-'))
    except exeptions.CantFormUniversity:
        print("Couldn't form university data")
        exit(1)
    un = UniversityItem(un_name, un_url)
        
    try:
        DATA = await services._form_request_data(un.url.split('/'))
    except exeptions.CantFormRequestData:
        print("Couldn't form request data")
        exit(1)
        
    requestItem = RequestItem('post', config.API_URL, config.HEADERS, DATA)

    try:
        entrants = await services._send_request(requestItem)
    except exeptions.CantSendRequest:
        print("Couldn't send request")
        exit(1)

    try:
        return await services._process_entrants(k_bal, entrants, requestItem, un)
    except exeptions.CantProcessEntrants:
        print("Couldn't process entrants")
        exit(1)
