import datetime
import pymysql.cursors
from env import Env
from scrapper.scrapper_object import ScrappingObject


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
            scrapper = ScrappingObject()
            self.full_name, self.team_id, self.height, self.weight, self.birth_date, self.college = scrapper.scrap_player(url)
            self.write_in_db(cursor)
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
                `full_name`,
                `team_id`,
                `height`, 
                `weight`, 
                `birth_date`,
                `college`
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_insert, (self._id, self.full_name, self.team_id, self.height,
                                      self.weight, self.birth_date, self.college))

    def __str__(self):
        return f"{self._id}: {self.full_name.title()} - {self.team_id.upper()}"
