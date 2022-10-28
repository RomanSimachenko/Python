import os
import sqlite3
from PIL import Image
from random import randrange


# rename folders for button event
def rename_folders(file_path):
    try:
        # connect to database(if a database doesn't exist - it will create it)
        connection = sqlite3.connect('database.db')
        # from connection get object cursor
        cursor = connection.cursor()
        # Database - DB
        # create table in DB
        cursor.execute(
            "CREATE table if NOT EXISTS dependencies(FolderName TEXT, FolderKey TEXT);")
        # commit changes
        connection.commit()

        # get folder's names from path
        list_of_folders_name = [item for item in os.listdir(
            file_path) if os.path.isdir(os.path.join(file_path, item))]
        list_of_renamed_folders = []

        # rename every folder in loop
        for folder_name in list_of_folders_name:
            # choose unique random name for folder
            random_name = str(randrange(123456, 987655))
            while random_name in list_of_folders_name and random_name in list_of_renamed_folders:
                random_name = str(randrange(123456, 987655))
            # take all folder's names from DB
            cursor.execute("SELECT * FROM dependencies")
            folder_names = [item[1] for item in cursor.fetchall()]
            connection.commit()
            try:
                if folder_name in folder_names:
                    # update folder name if it's in DB
                    cursor.execute(
                        f"UPDATE dependencies SET FolderKey = {random_name} WHERE FolderKey = {folder_name};")
                    connection.commit()
                else:
                    # add new folder name if it's not in DB
                    cursor.execute(
                        f"INSERT INTO dependencies (FolderName, FolderKey) VALUES ('{folder_name}', '{random_name}');")
                    connection.commit()
            except:
                # add new folder name if it's not in DB
                cursor.execute(
                    f"INSERT INTO dependencies (FolderName, FolderKey) VALUES ('{folder_name}', '{random_name}');")
                connection.commit()
            # rename folder's names from our path
            os.rename(f"{file_path}/{folder_name}",
                      f"{file_path}/{random_name}")
            list_of_renamed_folders.append(random_name)
        return True
    except Exception as error:
        print(error)
    finally:
        if connection:
            # after all those operations close connection to DB
            connection.close()


# return folder's names on path from DB
def set_folders_name(file_path):
    try:
        # Database - DB
        # connect to DB
        connection = sqlite3.connect('database.db')
        # from connection get object cursor
        cursor = connection.cursor()
        # get folder's names from path
        list_of_folders_name = [item for item in os.listdir(
            file_path) if os.path.isdir(os.path.join(file_path, item))]
        # turn back names from DB
        for folder_name in list_of_folders_name:
            # take name from BD where name = now folder's name
            cursor.execute(
                f"SELECT FolderName FROM dependencies WHERE FolderKey = {folder_name};")
            new_name = cursor.fetchall()[0][0]
            # rename back to first folder's name
            os.rename(f"{file_path}/{folder_name}",
                      f"{file_path}/{new_name}")
            # commit all changes
            connection.commit()
        try:
            # remove DB - no need
            os.remove('database.db')
        except:
            pass
        return True
    except Exception as error:
        print(error)
    finally:
        # after all those operations close connection to DB
        if connection:
            connection.close()


# func for resize image for current screen width and height
def resize_image(width, height):
    try:
        img = Image.open(r'data/background.jpg')
        new_img = img.resize((width, height), Image.ANTIALIAS)
        new_img.save("data/background.jpg", "JPEG")
    except:
        img = Image.open(r'../data/background.jpg')
        new_img = img.resize((width, height), Image.ANTIALIAS)
        new_img.save("../data/background.jpg", "JPEG")

