import requests
from bs4 import BeautifulSoup
from datetime import date
from typing import List
from game import Game


class ScrappingGames:
    url: str
    date: date
    games: List[Game]

    def __init__(self, date):
        self.url = f"https://www.nba.com/games?date={str(date)}"
        self.date = date
        self.games = []

    @staticmethod
    def get_stats_url(bs4_obj):
        for elt in bs4_obj:
            if elt['data-text'] == "BOX SCORE":
                return elt['href']
        return None

    def scrap_data(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        page = soup.find(id="__next")
        games_html = page.find_all("div", class_="GameCard_gc__UCI46 GameCardsMapper_gamecard__pz1rg")
        for tab in games_html:
            teams = tab.find_all("span", class_="MatchupCardTeamName_teamName__9YaBA")
            scores = tab.find_all("p", class_="MatchupCardScore_p__dfNvc GameCardMatchup_matchupScoreCard__owb6w")
            records = tab.find_all("p", class_="MatchupCardTeamRecord_record__20YHe")
            stats_url = self.get_stats_url(tab.find_all("a", class_="Anchor_anchor__cSc3P TabLink_link__f_15h"))
            self.games.append(Game(teams[0].text, teams[1].text, scores[0].text, scores[1].text,
                                   records[0].text, records[1].text, stats_url, str(self.date)))

    def print_results(self):
        for game in self.games:
            print(game)

    def write_in_db(self):
        pass
