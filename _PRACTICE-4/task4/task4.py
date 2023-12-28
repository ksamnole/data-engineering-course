import sqlite3
import json
import pickle

def get_data_pkl(path):
    with open(path, 'rb') as file:
      data = pickle.load(file)
    return data


def get_data_json(path):
    with open(path, 'rb') as file:
      data = json.load(file)
    return data


def create_table_if_not_exist(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task4 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, price INTEGER, quantity INTEGER, category TEXT, fromCity TEXT,
        isAvailable BOOLEAN, views INTEGER, updCount INTEGER            
    )
    ''')


def apply_updates(cursor, updates):
    try:
        cursor.execute('BEGIN TRANSACTION')

        for update in updates:
            name = update['name']
            method = update['method']
            param = update['param']

            if method == 'quantity_sub':
                cursor.execute('''
                    UPDATE task4
                    SET quantity = quantity - ?, updCount = updCount + 1
                    WHERE name = ?
                ''', (param, name))
            elif method == 'price_percent':
                cursor.execute('''
                    UPDATE task4
                    SET price = price * (1 + ?), updCount = updCount + 1
                    WHERE name = ?
                ''', (param, name))
            elif method == 'price_abs':
                cursor.execute('''
                    UPDATE task4
                    SET price = price + ?, updCount = updCount + 1
                    WHERE name = ?
                ''', (param, name))
            elif method == 'available':
                cursor.execute('''
                    UPDATE task4
                    SET isAvailable = ?, updCount = updCount + 1
                    WHERE name = ?
                ''', (param, name))
            elif method == 'remove':
                cursor.execute('''
                    DELETE FROM task4
                    WHERE name = ?
                ''', (name,))

        # Проверка на корректность изменений (цена и остатки не могут быть отрицательными)
        cursor.execute('''SELECT COUNT(*) FROM task4 WHERE price < 0 OR quantity < 0''')
        count_invalid_changes = cursor.fetchone()[0]

        if count_invalid_changes != 0:
          cursor.execute('ROLLBACK')
        else:
          cursor.execute('COMMIT')
    except Exception as e:
        cursor.execute('ROLLBACK')
        print(f"Error applying updates: {e}")


def insert_data(connection, data):
   cursor = connection.cursor()
   for item in data:
    cursor.execute('''
          INSERT INTO task4 (name, price, quantity, category, fromCity, isAvailable, views, updCount)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      ''', (item['name'], item['price'], item['quantity'], item.get('category', ''), item['fromCity'], item['isAvailable'], item['views'], 0))
   connection.commit()


connection = sqlite3.connect('task4.db')
cursor = connection.cursor()
create_table_if_not_exist(cursor)

# data = get_data_json("task_4_var_25_product_data.json")
# insert_data(connection, data)

# upd_data = get_data_pkl("task_4_var_25_update_data.pkl")
# apply_updates(cursor, upd_data)

# Вывести топ-10 самых обновляемых товаров
query_1 = '''
    SELECT * FROM task4
    ORDER BY updCount DESC
    LIMIT 10
'''
cursor.execute(query_1)
result_1 = cursor.fetchall()
print("Топ-10 самых обновляемых товаров:")
print(result_1)

# Проанализировать цены товаров
query_2 = '''
    SELECT category,
           SUM(price) as total_price,
           MIN(price) as min_price,
           MAX(price) as max_price,
           AVG(price) as avg_price,
           COUNT(*) as num_products
    FROM task4
    GROUP BY category
'''
cursor.execute(query_2)
result_2 = cursor.fetchall()
print("\nАнализ цен товаров:")
print(result_2)

# Проанализировать остатки товаров
query_3 = '''
    SELECT category,
           SUM(quantity) as total_quantity,
           MIN(quantity) as min_quantity,
           MAX(quantity) as max_quantity,
           AVG(quantity) as avg_quantity,
           COUNT(*) as num_products
    FROM task4
    GROUP BY category
'''
cursor.execute(query_3)
result_3 = cursor.fetchall()
print("\nАнализ остатков товаров:")
print(result_3)

# Произвольный запрос
query_custom = '''
    SELECT name, price
    FROM task4
    WHERE isAvailable = 1
    ORDER BY price DESC
    LIMIT 5
'''
cursor.execute(query_custom)
result_custom = cursor.fetchall()
print("\nПроизвольный запрос:")
print(result_custom)