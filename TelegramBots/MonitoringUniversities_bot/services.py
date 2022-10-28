import requests
import exeptions
from dataclasses import dataclass
from datetime import datetime


REQUEST_METHODS = {
    'get': requests.get,
    'post': requests.post
}


@dataclass
class EntrantItem:
    full_name: str
    k_bal: float
    priority: int
    b_or_k: str
    kvota: str


async def _form_un(un: list[str]) -> tuple[str, str]:
    """Forms university's data"""
    try:
        return un[0].strip(), un[1].strip()
    except:
        raise exeptions.CantFormUniversity


async def _form_request_data(un_url: list[str]) -> dict:
    """Forms data for request"""
    try:
        DATA = {
            'action': 'requests',
            'vcapcha': '1660646117',
            'ckm': 'ebebc.216',
            'y': un_url[3][1:],
            'uid': un_url[-2],
            'sid': un_url[-1],
            'last': 0,
        }
    except:
        raise exeptions.CantFormRequestData

    return DATA


async def _send_request(requestItem):
    """Sends request using given data"""
    try:
        response = REQUEST_METHODS[requestItem.method](
            url=requestItem.url,
            headers=requestItem.headers,
            data=requestItem.data,
            params=requestItem.params
        ).json()

        return response['requests']
    except:
        raise exeptions.CantSendRequest


async def _process_entrants(k_bal: float, entrants: dict, requestItem, un):
    """Processes all entrants"""
    try:
        k_last = len(entrants)

        while entrants:
            for person in entrants:
                un.k_all += 1
                if person[5] >= k_bal:
                    un.k_higher += 1
                    if person[7]: un.k_kv += 1
                    if person[2] == 0: un.k_k += 1

                    un.entrants += (EntrantItem(
                        person[4], 
                        float(person[5]),
                        int(person[2]),
                        "К" if int(person[2]) == 0 else "Б",
                        "+" if int(person[7]) == 1 else "-"
                    ),)

            requestItem.data['last'] += k_last
            entrants = await _send_request(requestItem)
        
        return un
    except:
        raise exeptions.CantProcessEntrants
