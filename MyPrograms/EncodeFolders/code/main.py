from design import start_app
import os


def main():
    # start main app
    start_app()
    # if a database exists - remove it
    try:
        os.remove('database.db')
    except:
        pass


if __name__ == '__main__':
    main()
