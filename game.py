import requests
from bs4 import BeautifulSoup
from player_game_stats import PlayerGameStats
from stats import Stats
from team_game_stats import TeamGameStats
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

    def scraping_stats(self):
        page = requests.get(self.url_stats)
        soup = BeautifulSoup(page.content, "html.parser")
        page_html = soup.find(id="espnfitt").find(id="DataWrapper") \
            .find(id="fitt-analytics").find("div", class_="StickyContainer")
        teams_tab = page_html.find_all("div", class_="Boxscore flex flex-column")

        for team_number, team_tab in enumerate(teams_tab):
            team_name = team_tab.find("div", class_="BoxscoreItem__TeamName h5").text

            tab = team_tab.find("div", class_="ResponsiveTable ResponsiveTable--fixed-left Boxscore flex flex-column") \
                .find("div", class_="flex")
            players = tab.find("table", class_="Table Table--align-right Table--fixed Table--fixed-left") \
                .find("tbody", class_="Table__TBODY").find_all("tr", class_="Table__TR Table__TR--sm Table__even")
            datas = tab.find("div", class_="Table__ScrollerWrapper relative overflow-hidden") \
                .find("div", class_="Table__Scroller").find("table", class_="Table Table--align-right") \
                .find("tbody", class_="Table__TBODY").find_all("tr", class_="Table__TR Table__TR--sm Table__even")

            for player, data in zip(players, datas):
                player_name_div = player.find("a", "AnchorLink truncate db external Boxscore__AthleteName")
                if not player_name_div:
                    continue
                player_id, player_full_name = player_name_div["href"].split("/")[-2:]
                player_full_name = " ".join(map(lambda x: x.capitalize(), player_full_name.split("-")))
                player_position = player.find("span", class_="playerPosition pl2").text

                dnp_div = data.find("td", class_="tc td Table__TD")
                is_dnp = False
                dnp_reason = None
                if dnp_div:
                    if 'dnp' in dnp_div.text.lower():
                        is_dnp = True
                        dnp_reason = dnp_div.text.split("-")[-1]
                    stats = 17 * [0]
                else:
                    stats = [elt.text for elt in data.find_all("td", class_="Table__TD Table__TD")]

                player_stats = Stats(stats)
                player_game_stats = PlayerGameStats(player_id, self.game_id, player_full_name, False, is_dnp,
                                                    dnp_reason, player_position, player_stats)
                if team_number == 0:
                    self.team1_stats.set_team_name(team_name)
                    self.team1_stats.add_player_game_stats(player_game_stats)
                else:
                    self.team2_stats.set_team_name(team_name)
                    self.team2_stats.add_player_game_stats(player_game_stats)

    def print_game_stats(self):
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
