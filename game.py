import requests
from bs4 import BeautifulSoup
from player_game_stats import PlayerGameStats
from stats import Stats
from team_game_stats import TeamGameStats
from constants import *
import datetime


class Game:
    game_id: str
    game_date: datetime.datetime
    team1_stats: TeamGameStats
    team2_stats: TeamGameStats

    def __init__(self, game_id, game_date):
        self.game_id = game_id
        self.game_date = game_date
        self.url_stats = f"https://www.espn.com/nba/boxscore/_/gameId/{game_id}"
        self.team1_stats = TeamGameStats(game_id)
        self.team2_stats = TeamGameStats(game_id)

    def get_team_tabs_html(self):
        """Returns HTML object of the two teams' box score"""
        page = requests.get(self.url_stats)
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
    def store_data_in_team(team, team_name, player_game_stats):
        """Store data to the team specified in input"""
        team.set_team_name(team_name)
        team.add_player_game_stats(player_game_stats)

    @staticmethod
    def get_player_info(player_html):
        """Returns player id, full_name and position"""
        player_name_div = player_html.find("a", PLAYER_NAME)
        if not player_name_div:
            return
        player_id, player_full_name = player_name_div["href"].split("/")[-2:]
        player_full_name = " ".join(map(lambda x: x.capitalize(), player_full_name.split("-")))
        player_position = player_html.find("span", class_=PLAYER_POSITION).text
        return player_id, player_full_name, player_position

    @staticmethod
    def get_player_stats(player_data_html):
        """Returns list of stats, either or not the player played the game (DNP), if not why (DNP Reason)."""
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

    def scrapping_stats(self):
        """Main scrapping function calling all sub-functions"""
        teams_tab = self.get_team_tabs_html()
        for team_number, team_tab in enumerate(teams_tab):
            team_name = team_tab.find("div", class_=TEAM_NAME).text
            tab = team_tab.find("div", class_=TEAM_TAB).find("div", class_="flex")
            players = self.get_players_html(tab)
            datas = self.get_team_stats_data(tab)

            for player, data in zip(players, datas):
                player_info = self.get_player_info(player)
                if not player_info:
                    continue
                player_id, player_full_name, player_position = player_info

                stats, is_dnp, dnp_reason = self.get_player_stats(data)
                player_game_stats = PlayerGameStats(player_id, self.game_id, player_full_name,
                                                    False, is_dnp, dnp_reason, player_position,
                                                    Stats(stats))
                if team_number == 0:
                    self.store_data_in_team(self.team1_stats, team_name, player_game_stats)
                else:
                    self.store_data_in_team(self.team2_stats, team_name, player_game_stats)

    def print_game_stats(self):
        """Printing the games stats using a dataframe"""
        print("######################################################")
        print(f"{self.game_date}: {self.team1_stats.team_name} - {self.team2_stats.team_name} ({self.game_id})")
        print("######################################################")
        print(f'{self.team1_stats.team_name}:')
        self.team1_stats.print_dataframe()
        print("\n")
        print(f'{self.team2_stats.team_name}:')
        self.team2_stats.print_dataframe()
        print("\n")

    def __str__(self):
        return f"Game(id={self.game_id}, date={self.game_date})"

    def write_in_db(self):
        pass
