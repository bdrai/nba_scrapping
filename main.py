import sys
import time
import datetime
import argparse
import api_request
from env import Env
from constants import *
from database.nba_database import NBADatabase
from scrapper.scrapper import ScrapperDay


def string_to_date(string: str):
    """Convert string to date format"""
    string = string.replace('/', '-')
    string = list(map(int, string.split('-')))
    return datetime.date(string[0], string[1], string[2])


def get_all_dates(start_date="2022-10-18", end_date=str(date.today() - datetime.timedelta(days=1))):
    """Generate the statistics of all the games between start_date and end_date """
    all_days = []
    start_date = max(string_to_date(start_date), SEASON_START_DATE)
    end_date = min(string_to_date(end_date), date.today() - datetime.timedelta(days=1))
    delta = end_date - datetime.timedelta(days=1) - start_date  # returns timedelta
    for i in range(delta.days + 2):
        day = start_date + datetime.timedelta(days=i)
        all_days.append(day.strftime("%Y%m%d"))  # change date to espn format yyyymmdd
    return all_days


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
        result = get_all_dates(start_date=str(datetime.date.today() - datetime.timedelta(days=1)))
    elif len(dates['dates']) == 1:
        result = get_all_dates(start_date=sys.argv[1], end_date=sys.argv[1])
    elif len(dates['dates']) == 2:
        result = get_all_dates(start_date=sys.argv[1], end_date=sys.argv[2])
    else:
        sys.exit("Too many arguments were given")
    return result


def main(extract_bet=False):
    # Initialize database
    db = NBADatabase(Env())
    db.initialize_database()

    # Main Scrapping
    dates = get_args()
    for d in dates:
        scrapper = ScrapperDay(d)
        scrapper.scrapping(save_in_db=True)
        time.sleep(1)

    # Get bets
    if extract_bet:
        api_request.main_api()


if __name__ == '__main__':
    main(extract_bet=True)
