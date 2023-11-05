import pandas as pd
import msgpack
import json

# Датасет можно глянуть по ссылке https://www.kaggle.com/datasets/suraj520/car-sales-data

results = {}
data = pd.read_csv('car_sales_data.csv')
num_columns = ['Car Year', 'Sale Price', 'Commission Rate', 'Commission Earned']
freq_columns = ['Car Make', 'Car Model']

def calc_numeric_data(results, data, columns):
  for column in columns:
    results[f'{column}'] = {
      'MAX': data[column].max(),
      'MIN': data[column].min(),
      'AVG': data[column].mean(),
      'SUM': data[column].sum(),
      'STD': data[column].std(),
    }

def calc_freq_data(results, data, columns):
  for column in columns:
    results[f'{column}'] = {
      'FREQ': data[column].value_counts().to_dict()
    }

calc_numeric_data(results, data, num_columns)
calc_freq_data(results, data, freq_columns)

df = pd.DataFrame(results)
df.to_json('results.json')
df.to_csv('results.csv')

with open('results.msgpack', 'wb') as msg_file:
  msg_file.write(msgpack.packb(df.to_dict()))