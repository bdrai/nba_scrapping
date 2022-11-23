import pymysql.cursors
from env import Env

HOST_MYSQL: str
PWD_MYSQL: str
USER_MYSQL: str


class NBADatabase:
    """Class to manage NBA database"""
    def __init__(self, env: Env):
        self.env = env

    def create_database(self):
        """Create database with the name configured in .env file"""
        connection = pymysql.connect(host=self.env.HOST_MYSQL, user=self.env.USER_MYSQL, password=self.env.PWD_MYSQL)
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.env.DB_MYSQL};")
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def create_table_team(cursor):
        """Creates table `Team`"""
        query = """
            CREATE TABLE IF NOT EXISTS Team (
                id VARCHAR(10) NOT NULL PRIMARY KEY, 
                name VARCHAR(250) NOT NULL, 
                division VARCHAR(250)
            );
        """
        cursor.execute(query)

    @staticmethod
    def create_table_player(cursor):
        """Creates table `Player`"""
        query = """
            CREATE TABLE IF NOT EXISTS Player (
                id BIGINT NOT NULL PRIMARY KEY,
                team_id VARCHAR(10) NOT NULL,
                full_name VARCHAR(250) NOT NULL,
                height FLOAT, 
                weight FLOAT,
                birth_date DATE,
                college VARCHAR(250),
                FOREIGN KEY (team_id) REFERENCES Team(id)
            );
        """
        cursor.execute(query)

    @staticmethod
    def create_table_game(cursor):
        """Creates table `Game`"""
        query = """
                CREATE TABLE IF NOT EXISTS Game (
                    id BIGINT NOT NULL PRIMARY KEY , 
                    date DATE NOT NULL, 
                    team_home_id VARCHAR(10) NOT NULL,
                    team_away_id VARCHAR(10) NOT NULL,
                    team_home_score INT NOT NULL, 
                    team_away_score INT NOT NULL, 
                    location VARCHAR(250), 
                    arena INT,
                    FOREIGN KEY (team_home_id) REFERENCES Team(id),
                    FOREIGN KEY (team_away_id) REFERENCES Team(id)
                );
            """
        cursor.execute(query)

    @staticmethod
    def create_table_player_game_stats(cursor):
        """Creates table `PlayerGameStats`"""
        query = """
            CREATE TABLE IF NOT EXISTS PlayerGameStats (
                id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                player_id BIGINT NOT NULL,
                game_id BIGINT NOT NULL,
                team_id VARCHAR(10) NOT NULL,
                position VARCHAR(250),
                is_starter BOOLEAN,
                is_dnp BOOLEAN,
                dnp_reason VARCHAR(250),
                min INT,
                fgm INT,
                fga INT,
                three_pts_m INT,
                three_pts_a INT,
                ftm INT,
                fta INT,
                oreb INT,
                drep INT,
                reb INT,
                ast INT,
                stl INT,
                blk INT,
                `to` INT,
                pf INT,
                plus_minus INT,
                pts INT,
                FOREIGN KEY (game_id) REFERENCES Game(id),
                FOREIGN KEY (team_id) REFERENCES Team(id),
                FOREIGN KEY (player_id) REFERENCES Player(id)
            );
        """
        cursor.execute(query)

    def create_tables(self, cursor):
        """Creates all tables in once"""
        self.create_table_team(cursor)
        self.create_table_player(cursor)
        self.create_table_game(cursor)
        self.create_table_player_game_stats(cursor)

    def initialize_database(self):
        """Initialize the database by creating it and the tables with."""
        self.create_database()
        connection = pymysql.connect(host=self.env.HOST_MYSQL, user=self.env.USER_MYSQL,
                                     password=self.env.PWD_MYSQL, database=self.env.DB_MYSQL)
        cursor = connection.cursor()
        self.create_tables(cursor)
        connection.commit()
        cursor.close()
        connection.close()


if __name__ == '__main__':
    db = NBADatabase(Env())
    db.initialize_database()
