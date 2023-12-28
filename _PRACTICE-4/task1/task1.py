import sqlite3
import json
import pickle

def get_data(path):
    with open(path, 'rb') as file:
      data = pickle.load(file)
    return data


def create_table_if_not_exist(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task1 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, street TEXT, city TEXT, zipcode INTEGER,
        floors INTEGER, year INTEGER, parking BOOLEAN,
        prob_price INTEGER, views INTEGER             
    )
    ''')


def insert_data(connection, data):
   cursor = connection.cursor()
   cursor.executemany('''
        INSERT INTO task1 (name, street, city,
            zipcode, floors, year, 
            parking, prob_price, views) 
        VALUES(
            :name, :street, :city,
            :zipcode, :floors, :year, 
            :parking, :prob_price, :views)
    ''', data)
   connection.commit()


def save_data(result, cursor, fileName):
    column_names = [description[0] for description in cursor.description]
    result_dict_list = [dict(zip(column_names, row)) for row in result]

    with open(fileName, 'w', encoding='utf-8') as json_file:
        json.dump(result_dict_list, json_file, ensure_ascii=False)


def save_first_35_rows(cursor):
    query = f'''
    SELECT * FROM task1
    ORDER BY views
    LIMIT {25 + 10}
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    save_data(result, cursor, "result_1.json")


def min_max_avg_by_floors(cursor):
    query_2 = '''
    SELECT SUM(floors) as sum_floors,
           MIN(floors) as min_floors,
           MAX(floors) as max_floors,
           AVG(floors) as avg_floors
    FROM task1
    '''
    cursor.execute(query_2)
    result_2 = cursor.fetchall()
    print("SUM<MIN<MAX<AVG BY FLOORS")
    print("SUM", result_2[0][0])
    print("MIN", result_2[0][1])
    print("MAX", result_2[0][2])
    print("AVG", result_2[0][3])
    save_data(result_2, cursor, "result_2.json")


def freq_by_city(cursor):
    query_3 = '''
    SELECT city, COUNT(*) as frequency
    FROM task1
    GROUP BY city
    '''
    cursor.execute(query_3)
    result_3 = cursor.fetchall()
    for (city, freq) in result_3:
        print(city, freq) 
    save_data(result_3, cursor, "result_3.json")


def save_first_35_filtered_data(cursor):
    query_4 = f'''
    SELECT * FROM task1
    WHERE YEAR >= 2000
    ORDER BY YEAR
    LIMIT {25 + 10}
    '''

    cursor.execute(query_4)
    result_4 = cursor.fetchall()
    save_data(result_4, cursor, "result_4.json")


connection = sqlite3.connect('task1.db')
cursor = connection.cursor()
create_table_if_not_exist(cursor)
# insert_data(connection, data=get_data("task_1_var_25_item.pkl"))

save_first_35_rows(cursor)
min_max_avg_by_floors(cursor)
freq_by_city(cursor)
save_first_35_filtered_data(cursor)
   
connection.close()