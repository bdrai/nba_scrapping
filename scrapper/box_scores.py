import pymysql.cursors
import requests
import datetime
from typing import List
from bs4 import BeautifulSoup

from constants import *
from env import Env
from stats import Stats
from player_game_stats import PlayerGameStats


class ScrappingBoxScore:
    url: str
    game_id: str
    players_stats: List[PlayerGameStats]

    def __init__(self, game_id):
        self.game_id = game_id
        self.url = f"https://www.espn.com/nba/boxscore/_/gameId/{game_id}"
        self.players_stats = []

    def get_team_tabs_html(self):
        """Returns HTML object of the two teams' box score"""
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        teams_tab = soup.find("div", class_="StickyContainer").find_all("div", class_=BOXSCORE_KEY)
        return teams_tab

    @staticmethod
    def get_players_html(tab):
        """Returns list of players' HTML object"""
        return tab.find("table", class_=PLAYER).find("tbody", class_=TABLE_BODY).find_all("tr", class_=TABLE_CONTENT)

    @staticmethod
    def get_team_stats_data(tab):
        """Returns list of players data's HTML object"""
        return tab.find("div", class_="Table__ScrollerWrapper relative overflow-hidden") \
            .find("div", class_="Table__Scroller").find("table", class_="Table Table--align-right") \
            .find("tbody", class_=TABLE_BODY).find_all("tr", class_=TABLE_CONTENT)

    @staticmethod
    def get_player_info(player_html):
        """Returns player id, full_name and position"""
        player_name_div = player_html.find("a", PLAYER_NAME)
        if not player_name_div:
            return
        player_id = player_name_div["href"].split("/")[-2]
        player_position = player_html.find("span", class_=PLAYER_POSITION).text
        return player_id, player_position

    @staticmethod
    def get_player_stats(player_data_html):
        """Returns list of stats, either or not the player played the game (DNP),
         if not: the reason (DNP Reason)."""
        dnp_div = player_data_html.find("td", class_="tc td Table__TD")
        is_dnp = False
        dnp_reason = None
        if dnp_div:
            if 'dnp' in dnp_div.text.lower():
                is_dnp = True
                dnp_reason = dnp_div.text.split("-")[-1]
            stats = 17 * [0]
        else:
            stats = [elt.text for elt in player_data_html.find_all("td", class_="Table__TD Table__TD")]
        return stats, is_dnp, dnp_reason

    def scrap_box_scores(self):
        """Main scrapping function calling all sub-functions"""
        teams_tab = self.get_team_tabs_html()
        for team_number, team_tab in enumerate(teams_tab):
            # team_name = team_tab.find("div", class_=TEAM_NAME).text
            tab = team_tab.find("div", class_=TEAM_TAB).find("div", class_="flex")
            players = self.get_players_html(tab)
            datas = self.get_team_stats_data(tab)

            for player, data in zip(players, datas):
                player_info = self.get_player_info(player)
                if not player_info:
                    continue
                player_id, player_position = player_info

                stats, is_dnp, dnp_reason = self.get_player_stats(data)
                player_game_stats = PlayerGameStats(player_id, self.game_id, False, is_dnp,
                                                    dnp_reason, player_position, Stats(stats))
                print(player_game_stats)
                self.players_stats.append(player_game_stats)

    def save_in_db(self, env: Env):
        connection = pymysql.connect(host=env.HOST_MYSQL, user=env.USER_MYSQL,
                                     password=env.PWD_MYSQL, database=env.DB_MYSQL)
        cursor = connection.cursor()
        for player_stats in self.players_stats:
            player_stats.write_in_db(cursor)
        connection.commit()
        cursor.close()
        connection.close()
