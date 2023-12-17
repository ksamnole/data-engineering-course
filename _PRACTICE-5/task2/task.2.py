import json
from pymongo import MongoClient


def get_collection(conUrl):
    client = MongoClient(conUrl)
    db = client["task1"]
    return db.person_data


def insert_data(data, collection):
    collection.insert_many(data)


def load_data(fileName):
    with open(fileName, 'r', encoding="utf-8") as file:
        return json.load(file)
    

def save_data(fileName, data):
    with open(fileName, 'w', encoding="utf-8") as file:
        return file.write(json.dumps(data, ensure_ascii=False))


def aggregate_salary(collection):
    query = [
        {"$group": {"_id": "salary",
                    "max": {"$max": "$salary"},
                    "min": {"$min": "$salary"},
                    "avg": {"$avg": "$salary"}}}
    ]
    items = list(collection.aggregate(query))
    save_data("salary_aggregate.json", items)


def aggregate_job(collection):
    query = [{"$group": {"_id": "$job", "sum": {"$sum": 1}}}]
    items = list(collection.aggregate(query))
    save_data("aggregate_job.json", items)


def aggregate_info(groupBy, aggregateBy):
    query = \
        [{"$group":
              {"_id": f"${groupBy}",
               "max_salary": {"$max": f"${aggregateBy}"},
               "min_salary": {"$min": f"${aggregateBy}"},
               "avg_salary": {"$avg": f"${aggregateBy}"}
               }
          }]
    items = list(collection.aggregate(query))
    save_data(f"aggregate_{groupBy}_{aggregateBy}_info.json", items)


def max_salary_min_age(collection):
    query = [
        {"$group": {"_id": "$age",
                    "max_salary": {"$max": "$salary"}}
        },
        {"$sort": {"_id": 1}}]
    items = list(collection.aggregate(query))[0]
    save_data("max_salary_min_age.json", items)


def min_salary_max_age(collection):
    query = [
        {"$group": {"_id": "$age",
                    "min_salary": {"$min": "$salary"}}
         },
        {"$sort": {"_id": -1}}
    ]
    items = list(collection.aggregate(query))[0]
    save_data("min_salary_max_age.json", items)


def aggregate_city_filter_salary(collection):
    query = [
        {"$match": {"salary": {"$gt": 50000}}},
        {"$group": {"_id": "$city",
                    "max_age": {"$max": "$age"},
                    "min_age": {"$min": "$age"},
                    "avg_age": {"$avg": "$age"}}
         },
        {"$sort": {"_id": 1}}
    ]
    items = list(collection.aggregate(query))
    save_data("aggregate_city_filter_salary.json", items)


def aggregate_with_filter(collection, groupBy):
    query = [
        {"$match": {"$or": [{"age": {"$gt": 18, "$lte": 25}},
                            {"age": {"$gt": 50, "$lt": 65}}]}},
        {"$group": {"_id": f"${groupBy}",
                    "max_salary": {"$max": "$salary"},
                    "min_salary": {"$min": "$salary"},
                    "avg_salary": {"$avg": "$salary"}}
         },
        {"$sort": {"_id": 1}}
    ]
    items = list(collection.aggregate(query))
    save_data(f"aggregate_{groupBy}_with_filter.json", items)


def salary_by_city_teacher(collection):
    query = [
        {"$match": {"job": "Учитель"}},
        {"$group": {"_id": "$city",
                    "max_salary": {"$max": "$salary"},
                    "min_salary": {"$min": "$salary"},
                    "avg_salary": {"$avg": "$salary"}}
         },
        {"$sort": {"_id": 1}}
    ]
    items = list(collection.aggregate(query))
    save_data("salary_by_city_teacher.json", items)


data = load_data("task_2_item.json")
collection = get_collection("mongodb://localhost:27017")
insert_data(data, collection)

aggregate_salary(collection)
aggregate_job(collection)
aggregate_info("city", "salary")
aggregate_info("job", "salary")
aggregate_info("city", "age")
aggregate_info("job", "age")
max_salary_min_age(collection)
min_salary_max_age(collection)
aggregate_with_filter(collection, "city")
aggregate_with_filter(collection, "job")
aggregate_with_filter(collection, "age")
salary_by_city_teacher(collection)