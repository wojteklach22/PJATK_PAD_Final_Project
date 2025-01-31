import pandas as pd
from scipy import stats

from ClearData.convert_data import ConvertData


class Tests:
    def __init__(self, filename):
        self.filename = filename

    def test_chi_square(self):

        df = pd.read_csv(self.filename)

        convert_data = ConvertData()

        df = df.map(convert_data.convert_percentage)

        # Odrzucenie wierszy, gdzie "Expected Goals (xG)" jest <= 0, ponieważ statystyka ta została wprowadzona
        # dopiero w drugiej połowie sezonu 2023
        df = df[df["Expected Goals (xG)"] > 0]

        # Tabela krzyżowa
        result_xg_crosstab = pd.crosstab(df['Ball Possession'], df['Result'])

        # Test chi-kwadrat
        chi2_stat, p_value, dof, expected = stats.chi2_contingency(result_xg_crosstab)

        print(f"Chi-kwadrat: {chi2_stat}, p-value: {p_value}")
        if p_value < 0.05:
            print("Istnieje zależność między Ball Possession a wynikiem meczu.")
        else:
            print("Brak zależności między Ball Possession a wynikiem meczu.")

        # Tabela krzyżowa
        result_xg_crosstab = pd.crosstab(df['Expected Goals (xG)'], df['Result'])

        # Test chi-kwadrat
        chi2_stat, p_value, dof, expected = stats.chi2_contingency(result_xg_crosstab)

        print(f"Chi-kwadrat: {chi2_stat}, p-value: {p_value}")
        if p_value < 0.05:
            print("Istnieje zależność między Expected Goals (xG) a wynikiem meczu.")
        else:
            print("Brak zależności między Expected Goals (xG) a wynikiem meczu.")

    def correlation_test(self):
        # Test korelacji między Expected Goals a Goals
        df = pd.read_csv(self.filename)

        convert_data = ConvertData()

        df = df.map(convert_data.convert_percentage)

        correlation, p_value = stats.pearsonr(df['Expected Goals (xG)'], df['Goals scored'])

        print(f"Pearson correlation: {correlation}, p-value: {p_value}")
        if p_value < 0.05:
            print("Istnieje istotna korelacja między Expected Goals a rzeczywistą liczbą bramek.")
        else:
            print("Brak istotnej korelacji między Expected Goals a rzeczywistą liczbą bramek.")
