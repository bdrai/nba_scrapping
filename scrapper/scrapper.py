from env import Env
from scrapper.scoreboard import ScrappingScoreboard
from scrapper.box_scores import ScrappingBoxScore


class ScrapperDay:
    def __init__(self, date):
        self.date = date

    def scrapping(self, save_in_db=False):
        scoreboard_scrapper = ScrappingScoreboard(self.date)
        scoreboard_scrapper.find_games()
        env = Env()
        if save_in_db:
            scoreboard_scrapper.save_in_db(env)
        for game in scoreboard_scrapper.games:
            print(game)
            box_scores_scrapper = ScrappingBoxScore(game.game_id)
            box_scores_scrapper.scrap_box_scores()
            box_scores_scrapper.scrap_box_scores()
            if save_in_db:
                box_scores_scrapper.save_in_db(env)


if __name__ == '__main__':
    s = ScrapperDay(20221119)
    s.scrapping(save_in_db=True)
