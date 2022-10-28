# https://www.youtube.com/watch?v=3bqcv8YmeQo&t=136s
import pymongo

try:
    db_client = pymongo.MongoClient("mongodb://localhost:27017/")
    current_db = db_client["Test"]
    collection = current_db["Persons"]
    person = {
        "Name": "TestName",
        "Nickname": "TestNickname",
        "Age": "TestAge",
        "Job": "TestJob",
    }
    confirm_person = collection.insert_one(person)
    print(confirm_person.inserted_id)
    # for db in db_client.list_databases():
    #     print(db)
    for person in collection.find():
        print(person)
except Exception as error:
    print(error)