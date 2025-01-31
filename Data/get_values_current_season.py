import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from ClearData.add_data import AddData
from ClearData.save_to_csv import SaveToCsv


class GetValuesCurrentSeason:
    def __init__(self):
        self.download_service = Service()
        self.driver = webdriver.Chrome(service=self.download_service)
        self.driver.get(r"https://www.flashscore.com/football/england/premier-league/results/")
        self.accept_cookies()

    def accept_cookies(self):
        btn_allow = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
        )
        btn_allow.click()

    def button_load_all_rounds(self):
        btn_more_matches = self.driver.find_element(By.CSS_SELECTOR, '.event__more.event__more--static')
        btn_more_matches.click()

    def load_all_rounds(self):
        self.scroll_page(5500)
        time.sleep(1)
        self.button_load_all_rounds()
        time.sleep(1)
        self.scroll_page(4900)
        time.sleep(1)
        self.button_load_all_rounds()
        time.sleep(1)
        self.driver.execute_script(f"window.scrollTo(0, 0);")
        time.sleep(1)

    def fetch_results(self, match_element, current_season):

        first_team_name = WebDriverWait(match_element, 120).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'div.wcl-participant_7lPCX.event__homeParticipant'))
        )
        team_1_name = first_team_name.text
        print(team_1_name)

        second_team_name = WebDriverWait(match_element, 120).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'div.wcl-participant_7lPCX.event__awayParticipant'))
        )
        team_2_name = second_team_name.text
        print(team_2_name)

        btn_go_into_match = WebDriverWait(match_element, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'eventRowLink'))
        )
        btn_go_into_match.click()

        self.driver.switch_to.window(self.driver.window_handles[1])

        button_go_to_statistics = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#/match-summary/match-statistics"]'))
        )
        button_go_to_statistics.click()

        match_score = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, 'div.duelParticipant__score div.detailScore__matchInfo div.detailScore__wrapper'))
        )
        split_value = match_score.text.split("-")
        first_team_score = split_value[0].strip()
        second_team_score = split_value[1].strip()

        rows = WebDriverWait(self.driver, 10).until(
            ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.section div.wcl-row_OFViZ'))
        )

        descriptions = [
            "Expected Goals (xG)", "Ball Possession", "Goal Attempts", "Shots on Goal", "Shots off Goal",
            "Blocked Shots",
            "Big Chances", "Corner Kicks", "Shots inside the Box", "Shots outside the Box", "Hit the Woodwork",
            "Goalkeeper Saves", "Free Kicks", "Offsides", "Fouls", "Yellow Cards", "Red Cards", "Throw-ins",
            "Touches in the Opposition Box", "Passes", "Passes in the final third", "Crosses", "Tackles",
            "Clearances Total", "Interceptions"
        ]
        statistics_team_1 = [0] * len(descriptions)
        statistics_team_2 = [0] * len(descriptions)

        for row in rows:
            description = row.find_element(By.CSS_SELECTOR,
                                           'div.wcl-category_7qsgP strong[data-testid="wcl-scores-simpleText-01"]').text
            if description in descriptions:
                desc_index = descriptions.index(description)

                # Pobranie wartości dla drużyny 1
                team_1_value = row.find_element(By.CSS_SELECTOR,
                                                'div.wcl-value_IuyQw.wcl-homeValue_-iJBW strong[data-testid="wcl-scores-simpleText-01"]').text
                statistics_team_1[desc_index] = team_1_value

                # Pobranie wartości dla drużyny 2
                team_2_value = row.find_element(By.CSS_SELECTOR,
                                                'div.wcl-value_IuyQw.wcl-awayValue_rQvxs strong[data-testid="wcl-scores-simpleText-01"]').text
                statistics_team_2[desc_index] = team_2_value

        additional_fields = ["Opponent", "Goals scored", "Goals lost", "Result", "Season"]
        descriptions.extend(additional_fields)

        statistics_team_1_dict = dict(zip(descriptions, statistics_team_1))
        statistics_team_2_dict = dict(zip(descriptions, statistics_team_2))

        adding_data = AddData()
        adding_data.add_data(statistics_team_1_dict, statistics_team_2_dict, team_1_name, team_2_name, first_team_score,
                             second_team_score, current_season)

        csv_saver = SaveToCsv()
        csv_saver.save(team_1_name, statistics_team_1_dict, descriptions)
        csv_saver.save(team_2_name, statistics_team_2_dict, descriptions)

        self.driver.close()

        self.driver.switch_to.window(self.driver.window_handles[0])

        self.scroll_page(50)

    def current_season_check(self):
        current_season_element = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'div.heading__info'))
        )
        current_season = current_season_element.text.split('/')[1]
        return current_season

    def fetch_all_results(self):

        time.sleep(5)
        current_season = self.current_season_check()
        time.sleep(2)
        self.load_all_rounds()

        match_elements = self.driver.find_elements(By.CSS_SELECTOR,
                                                   'div.event__match.event__match--withRowLink.event__match--static.event__match--twoLine')
        if not match_elements:
            match_elements = self.driver.find_elements(By.CSS_SELECTOR,
                                                       'div.event__match.event__match--withRowLink.event__match--static.event__match--last.event__match--twoLine')
        for index, match_element in enumerate(match_elements):  # match_elements[10:]
            print(f"Processing element {index}: {match_element}")
            self.fetch_results(match_element, current_season)

    def scroll_page(self, scroll_distance):
        """Przewiń stronę w dół o ustaloną wartość."""
        self.driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
        time.sleep(5)
