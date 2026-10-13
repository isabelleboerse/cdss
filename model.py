import random
import numpy as np
import pandas as pd
import gdown
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier

df = pd.read_csv(r"C:\Users\isabe\cdss\borstkanker.csv", sep=';')

print(df.head())
print(df.shape)
print(df.describe())

def maak_uitkomstvariabele(df, jaren=5):
    dagen = jaren * 365.25

    # Nieuwe kolom: onbekend totdat uitkomst vaststaat
    df = df.copy()
    df["overleving"] = np.nan

    # Overleden vóór de gekozen termijn
    df.loc[
        (df["vit_stat"] == 1) &
        (df["vit_stat_int"] < dagen),
        "overleving"
    ] = 0

    # Minstens X jaar overleefd
    df.loc[
        (df["vit_stat_int"] >= dagen),
        "overleving"
    ] = 1

    return df

def verwijderen_missende_waarden(df):
    missing_vars = df.columns[df.isna().any()].tolist()
    print(f"Variabelen met missings: {missing_vars}")
    missing_percentages = (df.isna().mean() * 100)
    print("\nPercentages missings per variabele:")
    print(missing_percentages)
    # kolommen verwijderen met missende waarden perc boven 25%
    high_missing_vars = missing_percentages[missing_percentages > 25].index.tolist()
    print(f"\nVariabelen met > 25% missings: {high_missing_vars}")
    df.drop(columns=high_missing_vars, inplace=True)
    # rijen verwijderen met na
    df.dropna(inplace=True)


# functie om alles over te zetten naar numerieke variabelen

def trainset(df):
    train_size = int(2/3 * len(df))
    shuffled_indices = np.random.permutation(len(df))
    train_indices = shuffled_indices[:train_size]
    test_indices = shuffled_indices[train_size:]
    train = df.iloc[train_indices]
    test = df.iloc[test_indices]
    return train, test

def model_trainen(train):
    nn = MLPClassifier(hidden_layer_sizes=3, max_iter=1000, random_state=42)
    nn.fit(train.drop(columns='died'), train['died'])
    return nn

def model_voorspellen(test, nn):
    p_nn = nn.predict(test.drop('died', axis=1))

def cf_matrix(p, o, and_print=True):
    TP = sum((p == o) & (o == 1))  # True Positives
    TN = sum((p == o) & (o == 0))  # True Negatives
    FP = sum((p != o) & (o == 0))  # False Positives
    FN = sum((p != o) & (o == 1))  # False Negatives

    ER = (FP + FN) / (TP + FP + TN + FN)  # Error Rate
    AC = 1 - ER  # Accuracy

    if and_print:
        print('------------------------------')
        print('|            |Classified as: |')
        print('------------------------------')
        print('|True class: | Y*=p  | Y*=n  |')
        print('------------------------------')
        print(f'|       Y=p  |   {TP}   |   {FN}   |')
        print('------------------------------')
        print(f'|       Y=n  |   {FP}   |   {TN}   |')
        print('------------------------------')
        print(f'Error rate: {ER}')
        print(f'Accuracy: {AC}')

    return AC

def evaluatie(p_nn, test):
    p_nn_class = (p_nn > 0.5).astype(int)
    cf_matrix(p_nn_class, test['died'])

if __name__ == "__main__":
    df = maak_uitkomstvariabele(df, jaren=5)
    train, test = trainset(df)
    train, test = verwijderen_missende_waarden(train, test)
    nn = model_trainen(train, train)
    p_nn = model_voorspellen(test, nn)
    evaluatie(p_nn, test)