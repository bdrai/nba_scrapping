import sys
import time
import requests
from bs4 import BeautifulSoup
import datetime

from env import Env
from game import Game
from database.nba_database import NBADatabase
from scrapper.scrapper import ScrapperDay
import argparse
from constants import *


def find_url_from_date(day: datetime.date):
    """Find the url of all the games for a given date """
    return DOMAIN_URL_FROM_DATE + str(day)


def find_games_ids_from_url(url: str):
    """Finds all the ids of the games on a given day (using the url of the schedule of this day)"""
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    page_html = soup.find(id="fittPageContainer").find_all(
        class_="Scoreboard bg-clr-white flex flex-auto justify-between")
    ids = [elt['id'] for elt in page_html]
    return ids


def string_to_date(string: str):
    """Convert string to date format"""
    string = string.replace('/', '-')
    string = list(map(int, string.split('-')))
    return datetime.date(string[0], string[1], string[2])


def generate_games(start_date="2022-10-18", end_date=str(date.today() - timedelta(days=1))):
    """Generate the statistics of all the games between start_date and end_date """
    all_games = []
    start_date = max(string_to_date(start_date), SEASON_START_DATE)
    end_date = min(string_to_date(end_date), date.today() - timedelta(days=1))
    delta = end_date - timedelta(days=1) - start_date  # returns timedelta
    
    for i in range(delta.days + 2):
        day = start_date + datetime.timedelta(days=i)
        print(f"###   LOADING THE: {day}   ###")
        formated_day = str(day).replace('-', '')  # change date to espn format yyyymmdd
        url_of_the_day = find_url_from_date(formated_day)  # find the url associated to the date
        all_ids = find_games_ids_from_url(url_of_the_day)  # scrapping all the ids of the games
        for _id in all_ids:
            all_games.append(Game(_id, day))
    return all_games



def get_all_dates(start_date=datetime.date(2022, 10, 18), end_date=datetime.date.today() - datetime.timedelta(days=1)):
    d = start_date
    dates = [d.strftime("%Y%m%d")]
    while d < end_date:
        d += datetime.timedelta(days=1)
        dates.append(d.strftime("%Y%m%d"))
    return dates



def get_args():
    """
    Generate stats from certain dates
    :return: Scrapping from the start date and the end date given
    """
    parser = argparse.ArgumentParser()  # create the parser
    parser.add_argument("dates", nargs="*", type=str)
    args = parser.parse_args()  # gets the argument
    dates = vars(args)
    if not len(dates['dates']):
        games = generate_games()
    elif len(dates['dates']) == 1:
        games = generate_games(start_date=sys.argv[1], end_date=sys.argv[1])
    elif len(dates['dates']) == 2:
        games = generate_games(start_date=sys.argv[1], end_date=sys.argv[2])
    else:
        sys.exit("Too many arguments were given")
    for game in games:
        game.scrapping_stats()
        game.print_game_stats()


def main():
    db = NBADatabase(Env())
    db.initialize_database()
    dates = get_all_dates()
    for d in dates:
        scrapper = ScrapperDay(d)
        scrapper.scrapping(save_in_db=True)
        time.sleep(1)

if __name__ == '__main__':
    main()
