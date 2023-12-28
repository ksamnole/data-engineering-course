import sqlite3
import json
import pickle
import csv


def insert_data_pkl(cursor, path):
    with open(path, 'rb') as file:
        data_pkl = pickle.load(file)
        for row in data_pkl:
            cursor.execute(f'''
            SELECT * FROM music_data 
            WHERE artist = ? AND song = ?
            ''', (row['artist'], row['song']))
            existing_record = cursor.fetchall()
            
            if len(existing_record) != 0:
                cursor.execute('''
                UPDATE music_data
                SET acousticness=?, popularity=?
                WHERE artist = ? AND song = ?
            ''', (
                float(row.get('acousticness', 0.0)),
                int(row.get('popularity', 0.0)),
                row['artist'],
                row['song']
            ))
            else:
                cursor.execute('''
                    INSERT INTO music_data (artist, song, duration_ms, year, tempo, genre, acousticness, energy, popularity)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row['artist'],
                    row['song'],
                    int(row['duration_ms']),
                    int(row['year']),
                    float(row['tempo']),
                    row['genre'],
                    float(row['acousticness']),
                    float(row['energy']),
                    int(row['popularity'])
                ))


def insert_data_csv(cursor, path):
    with open(path, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        for row in csv_reader:
            cursor.execute('''
                INSERT INTO music_data (artist, song, duration_ms, year, tempo, genre, energy, key, loudness)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['artist'],
                row['song'],
                int(row['duration_ms']),
                int(row['year']),
                float(row['tempo']),
                row['genre'],
                float(row['energy']),
                int(row['key']),
                float(row['loudness'])
            ))


def create_table_if_not_exist(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS music_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        artist TEXT,
        song TEXT,
        duration_ms INTEGER,
        year INTEGER,
        tempo REAL,
        genre TEXT,
        energy REAL,
        key INTEGER,
        loudness REAL,
        acousticness REAL,
        popularity INT
    )
''')


def save_data(result, cursor, fileName):
    column_names = [description[0] for description in cursor.description]
    result_dict_list = [dict(zip(column_names, row)) for row in result]

    with open(fileName, 'w', encoding='utf-8') as json_file:
        json.dump(result_dict_list, json_file, ensure_ascii=False)


def save_first_35_rows(cursor):
    query = f'''
    SELECT * FROM music_data
    ORDER BY year
    LIMIT {25 + 10}
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    save_data(result, cursor, "result_1.json")


def min_max_avg_by_duration(cursor):
    query_2 = '''
    SELECT SUM(duration_ms) as sum_duration,
           MIN(duration_ms) as min_duration,
           MAX(duration_ms) as max_duration,
           AVG(duration_ms) as avg_duration
    FROM music_data
    '''
    cursor.execute(query_2)
    result_2 = cursor.fetchall()
    print("SUM<MIN<MAX<AVG BY duration_ms")
    print("SUM", result_2[0][0])
    print("MIN", result_2[0][1])
    print("MAX", result_2[0][2])
    print("AVG", result_2[0][3])
    save_data(result_2, cursor, "result_2.json")


def freq_by_artist(cursor):
    query_3 = '''
    SELECT artist, COUNT(*) as frequency
    FROM music_data
    GROUP BY artist
    '''
    cursor.execute(query_3)
    result_3 = cursor.fetchall()
    for (artist, freq) in result_3:
        print(artist, freq) 
    save_data(result_3, cursor, "result_3.json")


def save_first_35_filtered_data(cursor):
    query_4 = f'''
    SELECT * FROM music_data
    WHERE popularity >= 30
    ORDER BY YEAR
    LIMIT {25 + 10}
    '''

    cursor.execute(query_4)
    result_4 = cursor.fetchall()
    save_data(result_4, cursor, "result_4.json")


connection = sqlite3.connect('task3.db')
cursor = connection.cursor()

create_table_if_not_exist(cursor)
# insert_data_csv(cursor, "task_3_var_25_part_1.csv")
# connection.commit()
# insert_data_pkl(cursor, "task_3_var_25_part_2.pkl")
# connection.commit()

save_first_35_rows(cursor)
min_max_avg_by_duration(cursor)
freq_by_artist(cursor)
save_first_35_filtered_data(cursor)