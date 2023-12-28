import sqlite3
from create_tables import *
from data_handler import *

connection = sqlite3.connect('task5.db')
cursor = connection.cursor()

create_tables_if_not_exist(cursor)
# insert_games("data/games.pkl", connection)
# insert_players("data/players.json", connection)
# insert_teams("data/teams.csv", connection)


# Выборка с условием, сортировкой и ограничением
query = """
    SELECT * FROM games
    WHERE SEASON = 2022 AND HOME_TEAM_WINS = 1
    ORDER BY PTS_home DESC
    LIMIT 5
"""
result = pd.read_sql_query(query, connection)
result.to_json('output/filtered_data.json', orient='records')


# Группировки по сезону и кол. игр
query = """
    SELECT SEASON, COUNT(*) AS game_count
    FROM games
    GROUP BY SEASON
"""

result = pd.read_sql_query(query, connection)
result.to_json('output/season_games_count.json', orient='records')


# Обновления данных
update_query = """
    UPDATE games
    SET PTS_home = 130
    WHERE GAME_ID = 22200477
"""
cursor.execute(update_query)
connection.commit()


# Информация о матчах в 2022 
query = """
    SELECT 
        games.GAME_DATE_EST,
        home_teams.NICKNAME AS home_team,
        away_teams.NICKNAME AS away_team,
        games.HOME_TEAM_WINS,
        games.PTS_home AS points_home,
        games.PTS_away AS points_away
    FROM games
    JOIN teams AS home_teams ON games.HOME_TEAM_ID = home_teams.TEAM_ID
    JOIN teams AS away_teams ON games.VISITOR_TEAM_ID = away_teams.TEAM_ID
    WHERE games.SEASON = 2022
"""
result = pd.read_sql_query(query, connection)
result.to_json('output/games_info_2022.json', orient='records')


# Выборки данных о матчах и командах
query = """
    SELECT games.*, teams.NICKNAME
    FROM games
    JOIN teams ON games.TEAM_ID_home = teams.TEAM_ID
    WHERE games.SEASON = 2022 AND games.HOME_TEAM_WINS = 1
"""

result = pd.read_sql_query(query, connection)
result.to_json('output/teams_season_2022.json', orient='records')


# Подсчет количества побед и поражений для каждой команды
query = """
    SELECT teams.NICKNAME, 
           SUM(CASE WHEN games.HOME_TEAM_WINS = 1 THEN 1 ELSE 0 END) AS wins,
           SUM(CASE WHEN games.HOME_TEAM_WINS = 0 THEN 1 ELSE 0 END) AS losses
    FROM teams
    LEFT JOIN games ON teams.TEAM_ID = games.TEAM_ID_home
    WHERE games.SEASON = 2022
    GROUP BY teams.NICKNAME
"""
result = pd.read_sql_query(query, connection)
result.to_json('output/wins_or_losses_by_teams.json', orient='records')

connection.close()