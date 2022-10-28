"""
Crontab event:
    crontab -e
    0 4 * * * BASE_DIR/venv/bin/python3 BASE_DIR/tasks.py
"""

from config import BASE_DIR
import os
from datetime import datetime


def clean_tmp_folder() -> None:
    """Cleans tmp folder"""
    files = os.listdir(BASE_DIR / 'tmp')

    for file in files:
        file_path = BASE_DIR / 'tmp' / file

        last_file_modification = datetime.fromtimestamp(os.path.getmtime(file_path))
        day_now = datetime.now().day

        if last_file_modification.day != day_now:
            os.remove(file_path)


if __name__ == "__main__":
    clean_tmp_folder()
