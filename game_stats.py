import requests
from bs4 import BeautifulSoup

from team_game_stats import TeamGameStats


class GameStats:
    game_id: str
    team1_stats: TeamGameStats
    team2_stats: TeamGameStats

    def __init__(self, game_id):
        self.game_id = game_id
        self.url_stats = f"https://www.espn.com/nba/boxscore/_/gameId/{game_id}"

    def scraping_stats(self):
        page = requests.get(self.url_stats)
        soup = BeautifulSoup(page.content, "html.parser")
        page_html = soup.find(id="espnfitt").find(id="DataWrapper")\
            .find(id="fitt-analytics").find("div", class_="StickyContainer")
        teams_tab = page_html.find_all("div", class_="Boxscore flex flex-column")

        for team_tab in teams_tab:
            team_name = team_tab.find("div", class_="BoxscoreItem__TeamName h5").text
            print(team_name)

    def __str__(self):
        pass

