from pymongo import MongoClient
import json


def get_collection(conUrl):
    client = MongoClient(conUrl)
    db = client["task1"]
    return db.person_data


def load_data(fileName):
    with open(fileName, "r", encoding="utf-8") as file:
       lines = file.readlines()
    data = []
    obj = {}
    for line in lines:
        if line.strip() != "=====":
            s = line.strip().split("::")
            obj[s[0]] = int(s[1]) if s[1].isdigit() else s[1]
        else:
            data.append(obj)
            obj = {}
    return data


def save_sorted_salary(collection):
    persons = list(collection.find({}).limit(10).sort({"salary": -1}))

    with open("sorted_by_salary.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(persons, ensure_ascii=False, default=str))


def save_filtered_age(collection):
    persons = list(collection.find({"age": {"$lt": 30}}, limit=15).sort({"salary": -1}))

    with open("filtered_by_age.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(persons, ensure_ascii=False, default=str))


def save_filtered_city(collection):
    query = {"city": "Вроцлав",
             "job": {"$in": ["Врач", "Бухгалтер", "Водитель"]}
             }
    persons = list(collection.find(query, limit=10).sort({"age": 1}))

    with open("filtered_by_city.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(persons, ensure_ascii=False, default=str))


def save_complex_filtered(collection):
    query = {
        "age": {"$gt": 18, "$lt": 35},
        "year": {"$in": [2019, 2020, 2021, 2022]},
        "$or": [{"salary": {"$gt": 50000, "$lte": 75000}},
                {"salary": {"$gt": 125000, "$lt": 150000}}]
    }
    _len = len(list(collection.find(query)))

    with open("complex_filter.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(_len, ensure_ascii=False, default=str))


data = load_data("task_1_item.text")
collection = get_collection("mongodb://localhost:27017")

if collection.count_documents({}) == 0:
    collection.insert_many(data)

save_sorted_salary(collection)
save_filtered_city(collection)
save_filtered_age(collection)
save_complex_filtered(collection)