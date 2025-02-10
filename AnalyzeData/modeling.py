from typing import TYPE_CHECKING
from typing import Any

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

if TYPE_CHECKING:
    from pandas import DataFrame

from ClearData.convert_data import ConvertData


class Modeling:
    def __init__(self, filename):
        self.filename = filename

    def modeling(self) -> None:
        # Wczytanie danych
        df: DataFrame = pd.read_csv(self.filename)

        convert_data = ConvertData()
        df: DataFrame = df.map(convert_data.convert_percentage)

        # Column for Manchater Utd we want to see the results vs this lcub
        df["Opponent_ManUtd"] = df["Opponent"].apply(lambda x: 1 if x == "Manchester Utd" else 0)

        train_df: DataFrame = df[df["Opponent"] != "Manchester Utd"]
        test_df: DataFrame = df[df["Opponent"] == "Manchester Utd"]

        features: list[str] = ["Ball Possession", "Goal Attempts", "Shots on Goal"]

        x_train: DataFrame = train_df[features]
        y_train: DataFrame = train_df["Result"].apply(lambda x: 1 if x == "Win" else 0)

        x_test: DataFrame = test_df[features]
        y_test: DataFrame = test_df["Result"].apply(lambda x: 1 if x == "Win" else 0)

        # Regresja logistyczna
        model: LogisticRegression = LogisticRegression()
        model.fit(x_train, y_train)

        # Predykcja wyników dla Manchester Utd
        y_pred: Any = model.predict(x_test)

        # Wyświetlenie raportu klasyfikacji
        print("Wyniki modelu dla meczów przeciwko Manchester Utd:\n")
        print(classification_report(y_test, y_pred))
