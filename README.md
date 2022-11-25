# Data mining project : NBA
 - [Benjamin Drai](https://www.linkedin.com/in/benjamin-d-838919127)
 - [Kevin Jerusalmi](https://www.linkedin.com/in/kevin-jerusalmi-151a74188)

## Introduction
The goal of this project is to create dashboards about NBA players' statistics during the season. 

This project is composed of three parts:
* Scrap the data from a website.
* Design and implement a database to store them.
* Run the code in production on AWS server.
* Create dashboards to analyse the data.


## Data scraping
The website we decided to scrap to get our data is [ESPN](https://www.espn.com/nba).
Our scrapping is divided in two parts:
* Get all games id according to the dates we want to scrap from the [Scoreboard](https://www.espn.com/nba/scoreboard/_/date/20221109) page.
* Once we get the ids, we can go throw the [Box Score](https://www.espn.com/nba/boxscore/_/gameId/401468316) of each game and scrap the stat tables of each team.

To run the scrapper, we must execute the following command: ```python3 main.py```.
