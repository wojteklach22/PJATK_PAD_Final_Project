class AddData:
    @staticmethod
    def add_data(statistics_team_1_dict, statistics_team_2_dict, team_1_name, team_2_name, first_team_score,
                 second_team_score, current_season):
        # Dodawanie przeciwnika
        statistics_team_1_dict["Opponent"] = team_2_name
        statistics_team_2_dict["Opponent"] = team_1_name

        # Dodawanie wyników
        statistics_team_1_dict["Goals scored"] = first_team_score
        statistics_team_2_dict["Goals scored"] = second_team_score

        statistics_team_1_dict["Goals lost"] = second_team_score
        statistics_team_2_dict["Goals lost"] = first_team_score

        # Dodawanie wyniku meczu
        if first_team_score > second_team_score:
            statistics_team_1_dict["Result"] = 'Win'
            statistics_team_2_dict["Result"] = 'Defeat'
        elif first_team_score < second_team_score:
            statistics_team_1_dict["Result"] = 'Defeat'
            statistics_team_2_dict["Result"] = 'Win'
        else:
            statistics_team_1_dict["Result"] = 'Draw'
            statistics_team_2_dict["Result"] = 'Draw'

        # Dodawanie sezonu
        statistics_team_1_dict["Season"] = current_season
        statistics_team_2_dict["Season"] = current_season

        return statistics_team_1_dict, statistics_team_2_dict
