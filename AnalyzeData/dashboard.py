import re

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


def convert_percentage(value):
    if isinstance(value, str):
        value = value.strip()

        match = re.match(r"(\d+)% \((\d+)/(\d+)\)", value)
        if match:
            return float(match.group(1)) / 100

        elif "%" in value:
            return float(value.strip("%")) / 100

        elif "/" in value:
            num, denom = map(int, value.split("/"))
            return num / denom

    return value


@st.cache
def load_data():
    df = pd.read_csv("Output/Arsenal.csv")

    team_mapping = {
        "Arsenal": 1, "Aston Villa": 2, "Bournemouth": 3, "Brentford": 4, "Brighton": 5, "Burnley": 6, "Cardiff": 7,
        "Chelsea": 8,
        "Crystal Palace": 9, "Everton": 10, "Fulham": 11, "Huddersfield": 12, "Hull": 13, "Ipswich": 14, "Leeds": 15,
        "Leicester": 16,
        "Liverpool": 17, "Luton": 18, "Manchester City": 19, "Manchester Utd": 20, "Middlesbrough": 21, "Newcastle": 22,
        "Norwich": 23,
        "Nottingham": 24, "QPR": 25, "Sheffield Utd": 26, "Southampton": 27, "Stoke": 28, "Sunderland": 29,
        "Swansea": 30, "Tottenham": 31,
        "Watford": 32, "West Brom": 33, "West Ham": 34, "Wolves": 35
    }
    reverse_team_mapping = {v: k for k, v in team_mapping.items()}

    if 'Result' in df.columns:
        df['Result'] = df['Result'].map({'Win': 1, 'Draw': 0, 'Defeat': -1})

    if 'Opponent' in df.columns:
        df['Opponent'] = df['Opponent'].map(team_mapping)
    for column in df.columns:
        if df[column].dtype == 'object':
            df[column] = df[column].apply(convert_percentage)

    return df, reverse_team_mapping


df, reverse_team_mapping = load_data()

# Nagłówek
st.title("Analiza wyników drużyn piłkarskich")
st.write(
    "Interaktywny dashboard do analizy wyników drużyn piłkarskich, statystyk meczów oraz zależności między danymi.")

# Sekcja: Statystyki opisowe
st.header("1. Statystyki opisowe")
st.write("Analiza podstawowych statystyk dotyczących drużyn.")

# Statystyki opisowe
st.write(df.describe())

# 2. Korelacje między statystykami
st.header("2. Korelacje między statystykami")
st.write("Wykres przedstawiający korelacje między różnymi statystykami drużyn.")
corr_matrix = df.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
st.pyplot()

# 3. Analiza wyników drużyn
st.header("3. Analiza wyników drużyn")
st.write("Analiza rozkładu wyników drużyn na podstawie 'Expected Goals (xG)' oraz wyników meczów.")
plt.figure(figsize=(10, 6))
sns.boxplot(x='Result', y='Expected Goals (xG)', data=df, palette='coolwarm')
plt.xlabel("Wynik meczu")
plt.ylabel("Expected Goals (xG)")
plt.xticks(ticks=[0, 1, 2], labels=["Przegrana", "Remis", "Wygrana"])
plt.title("Analiza Expected Goals (xG) a wyniki meczów")
st.pyplot()

# 4. Trendy w czasie - Expected Goals (xG)
st.header("4. Trendy w czasie")
st.write("Analiza trendów 'Expected Goals (xG)' w różnych sezonach.")
fig = plt.figure(figsize=(10, 6))
sns.lineplot(x="Season", y="Expected Goals (xG)", data=df)
plt.title("Trendy Expected Goals (xG) w sezonach")
st.pyplot()

# 5. Trendy w czasie - Ball Possession
st.header("5. Trendy w czasie 2")
st.write("Analiza trendów 'Expected Goals (xG)' w różnych sezonach.")
fig_2 = plt.figure(figsize=(10, 6))
sns.lineplot(x="Season", y="Ball Possession", data=df)
plt.title("Trendy posiadanie piłki w sezonach")
st.pyplot()

# 6. Trendy w czasie - Shots on Goal
st.header("6. Trendy w czasie 3")
st.write("Analiza trendów 'Expected Goals (xG)' w różnych sezonach.")
fig_3 = plt.figure(figsize=(10, 6))
sns.lineplot(x="Season", y="Shots on Goal", data=df)
plt.title("Trendy strzały na bramkę w sezonach")
st.pyplot()

# 7. Rozkład wyników meczów względem xG
st.header("7. Rozkład wyników meczów względem xG")
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x="Expected Goals (xG)", hue="Result", multiple="stack", bins=20, palette="coolwarm")
plt.xlabel("Expected Goals (xG)")
plt.ylabel("Liczba meczów")
plt.title("Rozkład wyników meczów względem Expected Goals (xG)")
st.pyplot()

# 8. Rozkład wygranych na danego przeciwnika
st.header("8. Rozkład wygranych na danego przeciwnika")
st.write("Wykres przedstawiający liczbę wygranych meczów przeciwko poszczególnym drużynom.")
plt.figure(figsize=(12, 6))
win_counts = df[df['Result'] == 1]['Opponent'].value_counts().sort_index()
win_counts.index = win_counts.index.map(reverse_team_mapping)
sns.barplot(x=win_counts.index, y=win_counts.values, palette="coolwarm")
plt.xlabel("Przeciwnik")
plt.ylabel("Liczba wygranych")
plt.title("Liczba wygranych meczów przeciwko poszczególnym drużynom")
plt.xticks(rotation=90)
st.pyplot()
