from typing import TYPE_CHECKING
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

if TYPE_CHECKING:
    from pandas import DataFrame
    from numpy import numpy

from ClearData.convert_data import ConvertData


class CreatingGraphs:

    def __init__(self, filename):
        self.filename = filename

    def create_graphs(self) -> None:
        df = pd.read_csv(self.filename)

        convert_data: ConvertData = ConvertData()

        df: DataFrame = df.map(convert_data.convert_percentage)

        df_numeric: DataFrame = df.drop(columns=['Opponent', 'Result', 'Season'], errors='ignore')

        # Konwersja wszystkich kolumn do typu float
        df_numeric: DataFrame = df_numeric.apply(pd.to_numeric, errors='coerce')

        # Podstawowe statystyki:
        goals_expected: numpy.ndarray = np.array(df['Expected Goals (xG)'])
        filtered_goals_expected: numpy.ndarray = goals_expected[goals_expected > 0]
        # Niestety statystyka 'Goals expected' została wprowadzona
        # dopiero w drugiej połowie 2023 roku wcześniej brak danych
        print("Mean goals expected: ", filtered_goals_expected.mean())
        print("Minimum goals expected: ", filtered_goals_expected.min())
        print("Maximum goals expected: ", filtered_goals_expected.max())
        shots_on_goal: numpy.ndarray = np.array(df['Shots on Goal'])
        print("Mean shots on goal: ", shots_on_goal.mean())
        print("Minimum shots on goal: ", shots_on_goal.min())
        print("Maximum shots on goal: ", shots_on_goal.max())

        # Wyliczanie macierzy korelacji
        correlation_matrix: DataFrame = df_numeric.corr()

        # Wizualizacja korelacji
        plt.figure(figsize=(12, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
        plt.title("Macierz korelacji")
        plt.show()

        df_grouped_by_season: Any = df.groupby("Season")["Expected Goals (xG)"].mean()

        # Wizualizacja trendu dla Expected Goals (xG)
        plt.figure(figsize=(10, 6))
        sns.lineplot(x=df_grouped_by_season.index, y=df_grouped_by_season.values, marker='o')
        plt.title("Zmiana Expected Goals (xG) w sezonach")
        plt.xlabel("Sezon")
        plt.ylabel("Średnie Expected Goals (xG)")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.show()

        df_grouped_by_season: Any = df.groupby("Season")["Ball Possession"].mean()

        # Wizualizacja trendu dla Ball Possession
        plt.figure(figsize=(10, 6))
        sns.lineplot(x=df_grouped_by_season.index, y=df_grouped_by_season.values, marker='o')
        plt.title("Zmiana Ball Possession w sezonach")
        plt.xlabel("Sezon")
        plt.ylabel("Średnie Ball possesion")
        plt.grid(True)
        plt.xticks(rotation=45)  # Aby tekst na osi X był czytelny
        plt.show()

        df_grouped_by_season: Any = df.groupby("Season")["Goals scored"].mean()

        # Wizualizacja trendu dla Goals scored
        plt.figure(figsize=(10, 6))
        sns.lineplot(x=df_grouped_by_season.index, y=df_grouped_by_season.values, marker='o')
        plt.title("Zmiana Goals scored w sezonach")
        plt.xlabel("Sezon")
        plt.ylabel("Średnie Goals scored")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.show()

        df['xG_Category'] = pd.cut(df["Expected Goals (xG)"], bins=[-float('inf'), 0.5, 1.0, 1.5, 2.0, float('inf')],
                                   labels=["<0.5", "0.5-1.0", "1.0-1.5", "1.5-2.0", ">2.0"])

        result_xg_crosstab: DataFrame = pd.crosstab(df['xG_Category'], df['Result'], margins=True, margins_name="Total")

        result_xg_crosstab: DataFrame = result_xg_crosstab.drop(columns="Total")
        result_xg_crosstab: DataFrame = result_xg_crosstab.drop(index="Total", errors="ignore")

        # Tabela krzyżowa
        print(result_xg_crosstab)

        # Wizualizacja tabeli krzyżowej jako wykresu słupkowego
        result_xg_crosstab.plot(kind='bar', stacked=True, figsize=(10, 6))
        plt.title("Rozkład wyników meczu w zależności od kategorii Expected Goals (xG)")
        plt.xlabel("Kategoria Expected Goals (xG)")
        plt.ylabel("Liczba meczów")
        plt.xticks(rotation=45)
        plt.legend(title="Wynik meczu", bbox_to_anchor=(1, 1), loc="upper left")
        plt.tight_layout()
        plt.show()

        # Tabela krzyżowa z "Goals" w zależności od "Result"
        result_goals_crosstab: DataFrame = pd.crosstab(df['Goals scored'], df['Result'], margins=True, margins_name="Total")

        # Ignore "Total"
        result_goals_crosstab: DataFrame = result_goals_crosstab.drop(columns="Total")
        result_goals_crosstab: DataFrame = result_goals_crosstab.drop(index="Total", errors="ignore")

        # Tabela krzyżowa
        print(result_goals_crosstab)

        # Wizualizacja tabeli krzyżowej jako wykresu słupkowego
        result_goals_crosstab.plot(kind='bar', stacked=True, figsize=(10, 6))
        plt.title("Rozkład wyników meczu w zależności od liczby zdobytych bramek")
        plt.xlabel("Liczba bramek")
        plt.ylabel("Liczba meczów")
        plt.xticks(rotation=45)
        plt.legend(title="Wynik meczu", bbox_to_anchor=(1, 1), loc="upper left")
        plt.tight_layout()
        plt.show()

        # Liczba wystąpień różnych drużyn przeciwnych
        opponent_counts = df["Opponent"].value_counts()

        # Wizualizacja
        plt.figure(figsize=(12, 6))
        sns.barplot(x=opponent_counts.index, y=opponent_counts.values)
        plt.title("Liczba spotkań z różnymi przeciwnikami")
        plt.xlabel("Przeciwnik")
        plt.ylabel("Liczba meczów")
        plt.xticks(rotation=90)
        plt.show()
