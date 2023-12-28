import csv
import pickle
import json
import pandas as pd

def insert_games(path, connection):
  pkl_data = pd.read_pickle(path)
  pkl_data.to_sql('games', connection, if_exists='replace', index=False)
  connection.commit()

def insert_players(path, connection):
  json_data = pd.read_json(path, lines=True)
  json_data.to_sql('players', connection, if_exists='replace', index=False)

def insert_teams(path, connection):
  csv_data = pd.read_csv(path)
  csv_data.to_sql('teams', connection, if_exists='replace', index=False)