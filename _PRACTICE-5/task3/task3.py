import pickle
from pymongo import MongoClient


def get_collection(conUrl):
    client = MongoClient(conUrl)
    db = client["task1"]
    return db.person_data


def insert_data(data, collection):
    collection.insert_many(data)


def load_data(fileName):
    with open(fileName, "rb") as file:
        return pickle.load(file)


def delete_salary(collection):
    query = {"$or": [{"salary": {"$lt": 25000}},
                     {"salary": {"$gt": 175000}}]}

    collection.delete_many(query)


def increment_age(collection):
    collection.update_many({}, {"$inc": {"age": 1}})


def increase_salary_for_job(collection):
    collection.update_many({"job": {"$in": ["Учитель"]}},
                           {"$mul": {"salary": 1.05}})


def increase_salary_in_city(collection):
   collection.update_many({"city": {"$in": ["Вальядолид"]}},
                          {"$mul": {"salary": 1.07}})


def increase_salary_complex(collection):
    collection.update_many({"$and": [{"city": {"$in": ["Вальядолид"]}},
                                           {"job": {"$in": ["Вальядолид"]}}]},
                                 {"$mul": {"salary": 1.10}})

def delete_job(collection):
    collection.delete_many({"city": "Подгорица"})


data = load_data("task_3_item.pkl")
collection = get_collection("mongodb://localhost:27017")
insert_data(data, collection)

delete_salary(collection)
increment_age(collection)
increase_salary_for_job(collection)
increase_salary_in_city(collection)
increase_salary_complex(collection)
delete_job(collection)