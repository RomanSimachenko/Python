from bot import run_bot


def main():
    try:
        run_bot()
    except KeyboardInterrupt:
        exit(1)


if __name__ == "__main__":
    main()
