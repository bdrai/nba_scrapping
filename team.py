import requests
import pymysql.cursors
from bs4 import BeautifulSoup

from env import Env


class Team:
    _id: str
    name: str
    division: str

    def __init__(self, url):
        self._id = url.split('/')[-2]
        env = Env()
        connection = pymysql.connect(host=env.HOST_MYSQL, user=env.USER_MYSQL,
                                     password=env.PWD_MYSQL, database=env.DB_MYSQL)
        cursor = connection.cursor()
        if not self.is_in_db(cursor):
            self.scrap_team_info(url, cursor)
        connection.commit()
        cursor.close()
        connection.close()

    def is_in_db(self, cursor):
        """Tests if the Team is in the database."""
        cursor.execute(f"SELECT * FROM `Team` WHERE id = '{self._id}';")
        result = cursor.fetchone()
        if result:
            self.name = result[1]
            self.division = result[2]
            return True
        return False

    def write_in_db(self, cursor):
        """Writes Team data in MySQL database."""
        query_insert = """
            INSERT INTO `Team` (
                `id`,
                `name`,
                `division`
            ) VALUES (%s, %s, %s)
        """
        cursor.execute(query_insert, (self._id, self.name, self.division))

    def scrap_team_info(self, url, cursor):
        """Scraps Team data from ESPN."""
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        page_html = soup.find(id="fitt-analytics").find(id="fittPageContainer")
        name_html = page_html.find("h1", class_="ClubhouseHeader__Name ttu flex items-start n2").find("span")
        self.name = ' '.join([span.text for span in name_html.find_all("span")])
        division_html = page_html.find("ul", class_="list flex ClubhouseHeader__Record n8 ml4").find_all("li")[-1]
        self.division = division_html.text.split("in ")[-1]
        self.write_in_db(cursor)

    def __str__(self):
        return f"{self.name.upper()} ({self._id}) - {self.division}"


if __name__ == '__main__':
    t = Team('https://www.espn.com/nba/team/_/name/tor/toronto-raptors')
    print(t)
