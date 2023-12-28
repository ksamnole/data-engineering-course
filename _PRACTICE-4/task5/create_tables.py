def create_tables_if_not_exist(cursor):
   # teams
   cursor.execute('''
    CREATE TABLE IF NOT EXISTS teams (
    LEAGUE_ID TEXT,
    TEAM_ID INTEGER,
    MIN_YEAR INTEGER,
    MAX_YEAR INTEGER,
    ABBREVIATION TEXT,
    NICKNAME TEXT,
    YEARFOUNDED INTEGER,
    CITY TEXT,
    ARENA TEXT,
    ARENACAPACITY INTEGER,
    OWNER TEXT,
    GENERALMANAGER TEXT,
    HEADCOACH TEXT,
    DLEAGUEAFFILIATION TEXT
  );
  ''')
   
   # games
   cursor.execute('''
    CREATE TABLE IF NOT EXISTS games (
    GAME_DATE_EST TEXT,
    GAME_ID INTEGER,
    GAME_STATUS_TEXT TEXT,
    HOME_TEAM_ID INTEGER,
    VISITOR_TEAM_ID INTEGER,
    SEASON INTEGER,
    TEAM_ID_home INTEGER,
    PTS_home INTEGER,
    FG_PCT_home REAL,
    FT_PCT_home REAL,
    FG3_PCT_home REAL,
    AST_home INTEGER,
    REB_home INTEGER,
    TEAM_ID_away INTEGER,
    PTS_away INTEGER,
    FG_PCT_away REAL,
    FT_PCT_away REAL,
    FG3_PCT_away REAL,
    AST_away INTEGER,
    REB_away INTEGER,
    HOME_TEAM_WINS INTEGER
);
''')
   
   # players
   cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
    PLAYER_NAME TEXT,
    TEAM_ID INTEGER,
    PLAYER_ID INTEGER,
    SEASON INTEGER
);
''')