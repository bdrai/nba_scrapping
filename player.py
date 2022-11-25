import datetime
import requests
import pymysql.cursors
from env import Env
from bs4 import BeautifulSoup


class Player:
    _id: int
    team_id: str
    full_name: str
    height: str
    weight: str
    birth_date: datetime.date
    college: str

    def __init__(self, url):
        self._id = url.split("/")[-2]
        env = Env()
        connection = pymysql.connect(host=env.HOST_MYSQL, user=env.USER_MYSQL,
                                     password=env.PWD_MYSQL, database=env.DB_MYSQL)
        cursor = connection.cursor()
        if not self.is_in_db(cursor):
            self.scrap_player_info(url, cursor)
        connection.commit()
        cursor.close()
        connection.close()

    def is_in_db(self, cursor):
        """Tests if the Player is in the database."""
        cursor.execute(f"SELECT * FROM `Player` WHERE id = '{self._id}';")
        result = cursor.fetchone()
        if result:
            return True
        return False

    def write_in_db(self, cursor):
        """Writes Player data in MySQL database."""
        query_insert = """
            INSERT INTO `Player` (
                `id`,
                `team_id`,
                `full_name`, 
                `height`, 
                `weight`, 
                `birth_date`,
                `college`
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_insert, (self._id, self.team_id, self.full_name, self.height,
                                      self.weight, self.birth_date, self.college))

    def scrap_player_info(self, url, cursor):
        """Scraps Player data from ESPN."""
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        player_html = soup.find("div", class_="StickyContainer")
        player_name_html = player_html.find("div", class_="PlayerHeader__Main_Aside min-w-0 flex-grow flex-basis-0") \
            .find("h1", class_="PlayerHeader__Name flex flex-column ttu fw-bold pr4 h2").find_all("span")
        self.full_name = " ".join([p.text for p in player_name_html])

        player_team_html = player_html \
            .find("div", class_="PlayerHeader__Team n8 mt3 mb4 flex items-center mt3 mb4 clr-gray-01")
        try:
            self.team_id = player_team_html.find("a")["href"].split("/")[-2].lower()
        except TypeError:
            self.team_id = None
        player_bio_html = player_html.find("div", class_="PlayerHeader__Bio pv5")
        info_html = player_bio_html.find_all("li")
        self.height, self.weight, self.birth_date, self.college = None, None, None, None
        for info in info_html:
            title, result = info.find_all("div")[:2]
            if title.text == "HT/WT":
                self.height, self.weight = result.text.split(", ")
            elif title.text == "Birthdate":
                self.birth_date = datetime.datetime.strptime(result.text.split(' (')[0], "%m/%d/%Y")
            elif title.text == "College":
                self.college = result.text
        print(self.full_name, self.team_id, self.height, self.weight, self.birth_date, self.college, sep=', ')
        self.write_in_db(cursor)

    def __str__(self):
        return f"{self._id}: {self.full_name.title()} - {self.team_id.upper()}"


if __name__ == '__main__':
    winslow = Player("https://www.espn.co.uk/nba/player/_/id/3135047/justise-winslow")
    kuzma = Player("https://www.espn.co.uk/nba/player/_/id/3134907/kyle-kuzma")
