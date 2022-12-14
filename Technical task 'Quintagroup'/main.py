import requests
import json
from typing import List, Dict
from datetime import datetime

import config


def get_reports() -> List[Dict]:
    """Sends request to the API and gets all the reports"""
    response = requests.post(
        url=config.API_URL,
        headers=config.HEADERS,
        data=json.dumps(config.DATA)
    )

    # catch error
    if response.status_code != 200:
        print("Something went wrong!")
        print(response.text)
        exit(1)

    return response.json()['timeentries']


def print_reports(reports: List[Dict]) -> None:
    """Formats and prints reports"""
    total_time = 0

    for i, r in enumerate(reports[::-1]):
        r_desc = r['description']
        r_dur = round(r['timeInterval']['duration'] / 60, 1)
        total_time += r_dur
        r_start = datetime.fromisoformat(r['timeInterval']['start']).ctime()
        r_end = datetime.fromisoformat(r['timeInterval']['end']).ctime()

        print(f"{i + 1}. {r_desc} - {r_dur} хвилин (від {r_start} до {r_end})")

    print(f"\n Total spent time: {total_time} хвилин")


def main():
    reports = get_reports()
    print_reports(reports)


if __name__ == "__main__":
    main()