import pandas as pd
import numpy as np
import os
from metrics import *

paths = ['data\[1]game_logs.csv'
         'data\[3]flights.csv', 
         'data\CIS_Automotive_Kaggle_Sample.csv', 
         'data\dataset.csv', 
         'data\\vacancies_2020.csv']

optimized_paths = [
         'optimized_data\[3]flights.csv', 
         'optimized_data\CIS_Automotive_Kaggle_Sample.csv', 
         'optimized_data\dataset.csv', 
         'optimized_data\\vacancies_2020.csv']

def analyze_memory(fileName, savePath):
    # Объем памяти на диске
    file_size = os.path.getsize(fileName) / (1024 * 1024)  # в МБ

    # Объем памяти в памяти
    df = pd.read_csv(fileName)
    memory_usage_memory = df.memory_usage(deep=True, index=False).sum() / (1024 * 1024)  # в МБ

    # Статистика по памяти
    stats = df.memory_usage(deep=True, index=False).sort_values(ascending=False)
    stats = pd.DataFrame({
        'Column': stats.index,
        'Memory Usage': stats.values,
        'Memory Share': stats.values / memory_usage_memory, # Доля от общего объема
        'Data Type': df.dtypes[stats.index].astype(str)
    })

    name = path.split('\\')[1].split('.')[0]
    stats.to_json(f"{savePath}\{name}.json")

    # Вывод результатов
    print(f"File Size on Disk ({fileName}): {file_size:.2f} MB")
    print(f"Memory Usage in Memory: {memory_usage_memory:.2f} MB")
    print(stats)


def optimize_data(fileName, savePath):
    df = pd.read_csv(fileName)

    # object -> Категориальные
    for column in df.columns:
      if df[column].dtype == 'object':
          unique_values_count = len(df[column].unique())
          total_values_count = len(df[column])
          if unique_values_count / total_values_count < 0.5:
              df[column] = df[column].astype('category')

      # Понижающее преобразование типов для int-колонок
      int_columns = df.select_dtypes(include='int').columns
      df[int_columns] = df[int_columns].apply(pd.to_numeric, downcast='integer')

      # Понижающее преобразование типов для float-колонок
      float_columns = df.select_dtypes(include='float').columns
      df[float_columns] = df[float_columns].apply(pd.to_numeric, downcast='float')
    
    name = fileName.split('\\')[1]
    df.to_csv(f'{savePath}\{name}', index=False)


def create_metrics(path, selected_columns):
    chunk_size = 1000
    name = path.split('\\')[1].split('.')[0]
    output_file = f'chunks\{name}.subset_data.csv'
    chunk_iter = pd.read_csv(path, usecols=selected_columns, chunksize=chunk_size)
    result_df = pd.DataFrame()
    for i, chunk in enumerate(chunk_iter):
      result_df = pd.concat([result_df, chunk], ignore_index=True)
    result_df.to_csv(output_file, index=False)

    optimized_data = pd.read_csv(output_file)
    plot_linear(optimized_data, selected_columns[1], selected_columns[0], f"{name}.1")


columns = [
        ["h_score", "v_score", "day_of_week", "h_name", "length_outs", "v_hits", "v_doubles", "v_triples",
         "v_homeruns", "v_rbi"],
        ["FLIGHT_NUMBER", "ORIGIN_AIRPORT", "DAY_OF_WEEK", "DESTINATION_AIRPORT", "DISTANCE", "AIR_TIME",
         "TAXI_OUT", "ARRIVAL_DELAY", "AIRLINE", "TAXI_IN"],
        ["vf_Make", "stockNum", "vf_EngineCylinders", "vf_EngineKW", "vf_EngineModel", "vf_EntertainmentSystem",
         "vf_ForwardCollisionWarning", "vf_FuelInjectionType", "vf_FuelTypePrimary", "vf_FuelTypeSecondary"],
        ["name", "spkid", "class", "diameter", "albedo", "diameter_sigma", "epoch", "epoch_cal", "om", "w"],
        ["id", "key_skills", "schedule_name", "experience_id", "experience_name", "salary_from", "salary_to",
         "employer_name", "employer_industries", "schedule_id"],
    ]


# for path in paths:
    # analyze_memory(path, "unoptimazed_analyze_memory")
    # optimize_data(path, "optimized_data")

for i, path in enumerate(optimized_paths):
    # analyze_memory(path, "optimized_analyze_memory")
    create_metrics(path, columns[i+1])
