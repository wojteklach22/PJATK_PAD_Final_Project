import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from ClearData.convert_data import ConvertData


class Modeling:
    def __init__(self, filename):
        self.filename = filename

    def modeling(self):
        df = pd.read_csv(self.filename)

        convert_data = ConvertData()

        df = df.map(convert_data.convert_percentage)

        # Przygotowanie danych
        x = df[["Expected Goals (xG)", "Ball Possession", "Goal Attempts", "Shots on Goal"]]
        y = df["Result"].apply(lambda x: 1 if x == "Win" else 0)

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        # Regresja logistyczna
        model = LogisticRegression()
        model.fit(x_train, y_train)

        # Ocena modelu
        y_pred = model.predict(x_test)
        print(classification_report(y_test, y_pred))
