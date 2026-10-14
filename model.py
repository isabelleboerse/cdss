import random
import numpy as np
import pandas as pd
import gdown
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier

np.random.seed(42)
               
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

def one_hot_encoding(y, num_classes):
    one_hot = np.zeros((len(y), num_classes))
    one_hot[np.arange(len(y)), y] = 1
    return one_hot

def verwijderen_missende_waarden(df):
    missing_percentages = df.isna().mean() * 100

    # Bekijk missende waarden
    print("Percentages missings per variabele:")
    print(missing_percentages)

    # Bepaal kolommen met > 25% missings,
    # maar behoud de uitkomstvariabele
    high_missing_vars = missing_percentages[
        (missing_percentages > 25) &
        (missing_percentages.index != "overleving")
    ].index.tolist()

    print("\nVariabelen met > 25% missings:")
    print(high_missing_vars)

    df = df.drop(columns=high_missing_vars)

    # Verwijder rijen zonder bekende uitkomst
    df = df.dropna(subset=["overleving"])

    # Verwijder rijen met missings in de overige variabelen
    
    df = df.dropna()
    df.drop(columns=['key_nkr'], inplace=True)
    df.drop(columns=['key_eid'], inplace=True)

    return df



# functie om alles over te zetten naar numerieke variabelen
def maak_one_hot(df, kolommen):
    for kol in kolommen:
        Y = df[kol].to_numpy()
        categorieen = np.unique(Y)
        Y_num = np.searchsorted(categorieen, Y)

        Y_onehot = one_hot_encoding(Y_num, len(categorieen))
        
        nieuwe_kolommen = [f"{kol}_{cat}" for cat in categorieen]
        
        df = df.drop(columns=[kol])
        df[nieuwe_kolommen] = Y_onehot
        
    return df
    
def variabelen_omzetten_numeriek(df):
    df.drop(columns='topo', inplace=True)
    df['gesl'] = df['gesl'] - 1
    df = maak_one_hot(df, ['ct','cn','pt','pn','diag_basis', 'diffgrad','gedrag','her2_stat','dcis_comp','okd','org_chir','dir_reconstr','meta_rt','meta_chir','multifoc','later','morf','ond_lymf','pos_lymf','er_stat','pr_stat','swk','chemo','target','horm','rt','topo_sublok','tumsoort', 'stadium', 'cstadium', 'pstadium', 'uitgebr_chir_code'])
    return df

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
    nn.fit(train.drop(columns='overleving'), train['overleving'])
    return nn

def model_voorspellen(test, nn):
    p_nn = nn.predict(test.drop('overleving', axis=1))
    return p_nn

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
    cf_matrix(p_nn_class, test['overleving'])

if __name__ == "__main__":
    df = pd.read_csv(r"C:\Users\romay\cdss\borstkanker.csv", sep=';')
    df = maak_uitkomstvariabele(df, jaren=5)
    print(df.columns.tolist())
    print(df.dtypes)
    print(df[["vit_stat", "vit_stat_int", "overleving"]].head(10))
    df = verwijderen_missende_waarden(df)
    df = variabelen_omzetten_numeriek(df)
    print(df.shape)
    print(df.head())
    train, test = trainset(df)
    nn = model_trainen(train)
    p_nn = model_voorspellen(test, nn)
    evaluatie(p_nn, test)
