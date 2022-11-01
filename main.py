from datetime import date, timedelta

from scraping_games import ScrappingGames

if __name__ == '__main__':
    date_games = date(2022, 9, 30)
    while date_games <= (date.today() - timedelta(days=1)):
        print("######################################")
        print(f"GAMES played the {str(date_games)}")
        print("######################################")

        s = ScrappingGames(date_games)
        s.scrap_data()
        s.print_results()
        print("")
        date_games += timedelta(days=1)

