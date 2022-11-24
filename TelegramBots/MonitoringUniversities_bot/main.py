#!/usr/bin/env python3
from bot import run_bot


def main():
    run_bot()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(1)
