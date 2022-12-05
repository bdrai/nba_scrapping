import pymysql.cursors
from env import Env
from scrapper.scrapper_object import ScrappingObject


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
            scrapper = ScrappingObject()
            self.name, self.division = scrapper.scrap_team(url)
            self.write_in_db(cursor)
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

    def __str__(self):
        return f"{self.name.upper()} ({self._id}) - {self.division}"


