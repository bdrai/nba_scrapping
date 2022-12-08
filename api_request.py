import datetime
import requests
from constants import *
import pandas as pd
import pymysql.cursors
from env import Env
from sqlalchemy import create_engine

convert_teams = {
    "Los Angeles Clippers": "LA Clippers"
}

replacer_columns = {
    "home_team": convert_teams,
    "away_team": convert_teams
}


def get_odds():
    """Get odds from API"""
    odds_response = requests.get(
        f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
        params={
            'api_key': API_KEY,
            'regions': REGIONS,
            'markets': MARKETS,
            'oddsFormat': ODDS_FORMAT,
            'dateFormat': DATE_FORMAT,
        }
    )

    if odds_response.status_code != 200:
        print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')
        return

    else:
        odds_json = odds_response.json()
        print('Remaining requests', odds_response.headers['x-requests-remaining'])
        return odds_json


def unpack_bookmakers(dict_apps_odds):
    """Processes bookmakers columns to extract a cleaner dictionary with useful data."""
    final_dic = {}
    for app in dict_apps_odds:
        app_name = app['title']
        dic_team_odd = []
        for team_odd in app['markets'][0]['outcomes']:
            dic_team_odd.append(team_odd['price'])
        final_dic[app_name] = dic_team_odd
    return final_dic


def find_best_bookmaker(dict_apps_odds):
    """Finds best bookmaker according to the best odds for each game"""
    min_avg = sum(dict_apps_odds[list(dict_apps_odds.keys())[0]]) / 2
    best_bookmaker = list(dict_apps_odds.keys())[0]
    for key in dict_apps_odds.keys():
        avg = sum(dict_apps_odds[key]) / 2
        if avg < min_avg:
            min_avg = avg
            best_bookmaker = key
    return best_bookmaker, dict_apps_odds[key][0], dict_apps_odds[key][1]


def process_odds_json(odds_json):
    """Process the API's response into a dataframe"""
    df = pd.DataFrame(odds_json)
    df = df[['home_team', 'away_team', 'bookmakers']]
    df["date"] = datetime.date.today()
    df['bookmakers'] = df.bookmakers.apply(lambda x: unpack_bookmakers(x))
    df['bookmaker'], df['odd_home'], df['odd_away'] = zip(*df.bookmakers.apply(find_best_bookmaker))
    df = df.drop(columns='bookmakers').replace(replacer_columns)
    return df


def get_teams_dataframe():
    """Read Team table from database into dataframe."""
    env = Env()
    connection = pymysql.connect(host=env.HOST_MYSQL, user=env.USER_MYSQL, password=env.PWD_MYSQL,
                                 database=env.DB_MYSQL)
    query = """SELECT `id`, `name`  FROM Team;"""
    df_teams = pd.read_sql(query, connection)
    connection.close()
    return df_teams


def merge_odds_teams(df_odds, df_teams):
    """Merge odds dataframe with teams one for getting teams' id."""
    df_merge = df_odds.merge(df_teams, left_on="home_team", right_on="name", how='left') \
        .drop(["name", "home_team"], axis=1).rename(columns={"id": "home_id"})
    df_merge = df_merge.merge(df_teams, left_on="away_team", right_on="name", how='left') \
        .drop(["name", "away_team"], axis=1).rename(columns={"id": "away_id"})
    return df_merge[["date", "home_id", "away_id", "odd_home", "odd_away", "bookmaker"]]


def write_in_db(df):
    """Write the Bet dataframe into Bet table in database"""
    env = Env()
    engine = create_engine(f'mysql+pymysql://{env.USER_MYSQL}:{env.PWD_MYSQL}@{env.HOST_MYSQL}/{env.DB_MYSQL}')
    df.to_sql('Bet', engine, if_exists='append', index=False)


def main_api():
    """Main script"""
    odds_json = get_odds()
    df_odds = process_odds_json(odds_json)
    df_teams = get_teams_dataframe()
    df_merge = merge_odds_teams(df_odds, df_teams)
    write_in_db(df_merge)
