import json
from pymongo import MongoClient
import csv


def get_collection(conUrl):
    client = MongoClient(conUrl)
    db = client["task4"]
    return db.happiness_2015


def insert_data(data, collection):
    collection.insert_many(data)


def load_data(fileName):
    with open(fileName, newline='') as file:
        data = list(csv.DictReader(file))
    for doc in data:
        for key in doc.keys():
            if key == "Country" or key== "Region":
                continue
            doc[key] = float(doc[key])
    return data


def save_data(fileName, data):
    with open(fileName, 'w', encoding="utf-8") as file:
        return file.write(json.dumps(data, ensure_ascii=False, default=str))


def sorted_happiness_score(collection):
    scores = list(collection.find({}).limit(10).sort({"Happiness Score": -1}))
    save_data("1_sorted_happiness_score.json", scores)


def sorted_country(collection):
    query = [{"$match": {"Country" : "Denmark"}}]
    save_data("1_sorted_country.json", list(collection.aggregate(query)))


def filtered_rank(collection):
    query = [{"$match": {"Happiness Rank": {"$gt": 5}}}]
    save_data("1_filtered_rank.json", list(collection.aggregate(query)))


def filtered_health(collection):
    query = [{"$match": {"Health (Life Expectancy)": {"$lt": 0.5}}}]
    save_data("1_filtered_health.json", list(collection.aggregate(query)))
    

def filtered_complex(collection):
    query = {
        "Family": {"$gt": 0.5, "$lt": 2},
        "Country": {"$in": ["Mexico", "Brazil", "United Arab Emirates"]},
        "$or": [{"Happiness Rank": {"$gt": 100}},
                {"Happiness Score": {"$gte": 6}}]
    }
    save_data("1_filtered_complex.json", list(collection.find(query)))


def aggregate_region_count(collection):
    query = [{"$group": {"_id": "$Region", "sum": {"$sum": 1}}}]
    save_data("2_aggregate_region_count.json", list(collection.aggregate(query)))


def aggregate_region_by_rank(collection):
    query = [{"$group": {"_id": "$Region", "Max Happiness Rank": {"$max": "$Happiness Rank"}}}]
    save_data("2_aggregate_region_by_rank.json", list(collection.aggregate(query)))


def aggregate_region_min_max_avg_family(collection):
    query = [{"$group": {"_id": "$Region",
                         "max": {"$max": "$Family"},
                         "min": {"$min": "$Family"},
                         "avg": {"$avg": "$Family"}}}]
    save_data("2_aggregate_region_min_max_avg_family.json", list(collection.aggregate(query)))


def aggregate_region_min_max_avg_economy(collection):
    query = [{"$group": {"_id": "$Region",
                         "max": {"$max": "$Economy (GDP per Capita)"},
                         "min": {"$min": "$Economy (GDP per Capita)"},
                         "avg": {"$avg": "$Economy (GDP per Capita)"}}}]
    save_data("2_aggregate_region_min_max_avg_economy.json", list(collection.aggregate(query)))


def aggregate_region_min_max_avg_economy(collection):
    query = [{"$group": {"_id": "$Region",
                         "max": {"$max": "$Economy (GDP per Capita)"},
                         "min": {"$min": "$Economy (GDP per Capita)"},
                         "avg": {"$avg": "$Economy (GDP per Capita)"}}}]
    save_data("2_aggregate_region_min_max_avg_economy.json", list(collection.aggregate(query)))


def max_health_min_family(collection):
    query = [
        {"$group": {"_id": "$Health (Life Expectancy)",
                    "max_family": {"$max": "$Family"}}
        }, {"$sort": {"_id": -1}}]
    save_data("2_max_health_min_family.json", list(collection.aggregate(query))[0])


def delete_region(collection):
    collection.delete_many({"Region": "Latin America and Caribbean"})


def increment_generosity(collection):
    collection.update_many({}, {"$inc": {"Generosity": 100}})


def delete_if_family_lt_1(collection):
    query = {"Family": {"$lt": 1}}
    collection.delete_many(query)


def increase_health_in_country(collection):
   collection.update_many({"Country": {"$in": ["Switzerland"]}},
                          {"$mul": {"Health (Life Expectancy)": 50}})


def delete_if_rank_more_15_in_western_europe(collection):
    collection.delete_many({"$and" : [
        {"Region": "Western Europe"},
        {"Happiness Rank" : {"$gt" : 15}}]})


data = load_data("happiness_2015.csv")
collection = get_collection("mongodb://localhost:27017")
if collection.count_documents({}) == 0:
    insert_data(data, collection)

sorted_happiness_score(collection)
sorted_country(collection)
filtered_rank(collection)
filtered_health(collection)
filtered_complex(collection)

aggregate_region_count(collection)
aggregate_region_by_rank(collection)
aggregate_region_min_max_avg_family(collection)
aggregate_region_min_max_avg_economy(collection)
max_health_min_family(collection)

delete_region(collection)
increment_generosity(collection)
delete_if_family_lt_1(collection)
increase_health_in_country(collection)
delete_if_rank_more_15_in_western_europe(collection)