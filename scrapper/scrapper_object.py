import requests
from bs4 import BeautifulSoup
import datetime


class ScrappingObject:
    
    @staticmethod
    def scrap_player(url):
        """Scraps Player data from ESPN."""
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        player_html = soup.find("div", class_="StickyContainer")
        player_name_html = player_html.find("div", class_="PlayerHeader__Main_Aside min-w-0 flex-grow flex-basis-0") \
            .find("h1", class_="PlayerHeader__Name flex flex-column ttu fw-bold pr4 h2").find_all("span")
        full_name = " ".join([p.text for p in player_name_html])

        player_team_html = player_html \
            .find("div", class_="PlayerHeader__Team n8 mt3 mb4 flex items-center mt3 mb4 clr-gray-01")
        try:
            team_id = player_team_html.find("a")["href"].split("/")[-2].lower()
        except TypeError:
            team_id = None
        player_bio_html = player_html.find("div", class_="PlayerHeader__Bio pv5")
        info_html = player_bio_html.find_all("li")
        height, weight, birth_date, college = None, None, None, None
        for info in info_html:
            title, result = info.find_all("div")[:2]
            if title.text == "HT/WT":
                height, weight = result.text.split(", ")
            elif title.text == "Birthdate":
                birth_date = datetime.datetime.strptime(result.text.split(' (')[0], "%m/%d/%Y")
            elif title.text == "College":
                college = result.text
        print(full_name, team_id, height, weight, birth_date, college, sep=', ')
        return full_name, team_id, height, weight, birth_date, college

    @staticmethod
    def scrap_team(url):
        """Scraps Team data from ESPN."""
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        page_html = soup.find(id="fitt-analytics").find(id="fittPageContainer")
        name_html = page_html.find("h1", class_="ClubhouseHeader__Name ttu flex items-start n2").find("span")
        name = ' '.join([span.text for span in name_html.find_all("span")])
        division_html = page_html.find("ul", class_="list flex ClubhouseHeader__Record n8 ml4").find_all("li")[-1]
        division = division_html.text.split("in ")[-1]
        print(f"{name.upper()} - {division}")
        return name, division