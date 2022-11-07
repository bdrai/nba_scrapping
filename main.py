import requests
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from game import Game


def find_url_from_date(day: datetime.date):
    """Find the url of all the games for a given date """
    return 'https://www.espn.com/nba/scoreboard/_/date/' + str(day)


def find_games_ids_from_url(url: str):
    """Finds all the ids of the games on a given day (using the url of the schedule of this day)"""
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    page_html = soup.find(id="fitt-analytics").find(id="fittPageContainer").find_all(
        class_="Scoreboard bg-clr-white flex flex-auto justify-between")
    ids = [elt['id'] for elt in page_html]
    return ids


def generate_games():
    """Find all the dates of the games since the beginning of the season"""
    all_games = []
    first_day_season = date(2022, 10, 18)  # first day of the season
    delta = date.today() - first_day_season  # returns timedelta

    for i in range(delta.days + 1):
        day = first_day_season + timedelta(days=i)
        print(f"###   LOADING THE: {day}   ###")
        formated_day = str(day).replace('-', '')  # change date to espn format yyyymmdd
        url_of_the_day = find_url_from_date(formated_day)  # find the url associated to the date
        all_ids = find_games_ids_from_url(url_of_the_day)  # scrapping all the ids of the games
        for id in all_ids:
            all_games.append(Game(id, day))
    return all_games


if __name__ == '__main__':
    # date_games = date(2022, 9, 30)
    # while date_games <= (date.today() - timedelta(days=1)):
    #     print("######################################")
    #     print(f"GAMES played the {str(date_games)}")
    #     print("######################################")
    #
    #     s = ScrappingGames(date_games)
    #     s.scrap_data()
    #     s.print_results()
    #     print("")
    #     date_games += timedelta(days=1)
    try:
        games = generate_games()
    except:

    print(games)
    [print(game) for game in games]
