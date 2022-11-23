import pymysql.cursors
import requests
from bs4 import BeautifulSoup

from env import Env
from team import Team
import datetime
from typing import List
from game import Game

"""
scrapper le scoreboard
Creer des games avec 
    l'id du game, la date les ids des equipes, le score
Parourir chaque game pour récupérer l'id et scrapper les box scores
"""


class ScrappingScoreboard:
    PLAYING_HOME_INDEX = 5

    url: str
    date: datetime.date
    games: List[Game]

    def __init__(self, date):
        self.url = 'https://www.espn.com/nba/scoreboard/_/date/' + str(date)
        self.date = date
        self.games = []

    def find_game_info(self, competitor):
        class_name = competitor["class"]
        is_playing_home = True if 'home' in class_name[self.PLAYING_HOME_INDEX] else False
        team_link = competitor.find("a", class_="AnchorLink truncate")["href"]
        team = Team(f"https://www.espn.com{team_link}")
        score = competitor.find("div", class_="ScoreCell__Score h4 clr-gray-01 fw-heavy tar ScoreCell_Score--scoreboard pl2").text
        return team, score, is_playing_home

    def find_games(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        games_html = soup.find(id="fitt-analytics").find(id="fittPageContainer").find_all(
            class_="Scoreboard bg-clr-white flex flex-auto justify-between")
        for game_html in games_html:
            game_id = game_html['id']
            competitors = game_html.find("ul", class_="ScoreboardScoreCell__Competitors").find_all("li")
            team_home_id, team_away_id, team_home_score, team_away_score = None, None, None, None
            for competitor in competitors:
                team, score, is_playing_home = self.find_game_info(competitor)
                if is_playing_home:
                    team_home_id = team._id
                    team_home_score = score
                else:
                    team_away_id = team._id
                    team_away_score = score
            if not team_home_id or not team_away_id or not team_home_score or not team_away_score:
                raise Exception(f"One of the game info of game {game_id} is missing!")
            game = Game(game_id, self.date, team_home_id, team_away_id, team_home_score, team_away_score)
            self.games.append(game)

    def save_in_db(self, env: Env):
        connection = pymysql.connect(host=env.HOST_MYSQL, user=env.USER_MYSQL,
                                     password=env.PWD_MYSQL, database=env.DB_MYSQL)
        cursor = connection.cursor()
        for game in self.games:
            game.write_game_in_db(cursor)
        connection.commit()
        cursor.close()
        connection.close()

