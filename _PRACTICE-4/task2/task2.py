import sqlite3
import json
import pickle

def get_data(path):
    with open(path, 'rb') as file:
      data = pickle.load(file)
    return data


def create_table_if_not_exist(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task2 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, rating INTEGER, convenience INTEGER, security INTEGER,
        functionality INTEGER, comment TEXT             
    )
    ''')


def insert_data(connection, data):
   cursor = connection.cursor()
   cursor.executemany('''
        INSERT INTO task2 (name, rating, convenience,
            security, functionality, comment) 
        VALUES(
            :name, :rating, :convenience,
            :security, :functionality, :comment)
    ''', data)
   connection.commit()


def save_data(result, cursor, fileName):
    column_names = [description[0] for description in cursor.description]
    result_dict_list = [dict(zip(column_names, row)) for row in result]

    with open(fileName, 'w', encoding='utf-8') as json_file:
        json.dump(result_dict_list, json_file, ensure_ascii=False)


def query1(cursor):
    query="""
    SELECT *
    FROM task1
    JOIN task2 ON task1.name = task2.name
    WHERE (parking == 1) AND rating >=3 
    ORDER BY rating DESC
    """
    cursor.execute(query)
    result = cursor.fetchall()


def query2(cursor):
    query="""
    SELECT *
    FROM task1
    JOIN task2 ON task1.name = task2.name
    WHERE (city == 'Камбадос') AND (SECURITY BETWEEN 3 AND 5) 
    ORDER BY security DESC
    """
    cursor.execute(query)
    result = cursor.fetchall()


def query3(cursor):
    query="""
    SELECT *
    FROM task1
    JOIN task2 ON task1.name = task2.name
    WHERE rating = (SELECT MAX(rating) FROM task2)
    ORDER BY rating DESC
    """
    cursor.execute(query)
    result = cursor.fetchall()


connection = sqlite3.connect('../task1/task1.db')
cursor = connection.cursor()
create_table_if_not_exist(cursor)
insert_data(connection, data=get_data("task_2_var_25_subitem.pkl"))

query1(cursor)
query2(cursor)
query3(cursor)