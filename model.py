import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

np.random.seed(42)

df = pd.read_csv(r"C:\Users\isabe\cdss\borstkanker.csv", sep=';')

def normalize(x):
    if min(x) < max(x):
        z = (x - min(x)) / (max(x) - min(x))
    elif min(x) == max(x):
        z = 1
    return z

def normaliseren_data(df):
    numerieke_kolommen = df.select_dtypes(include=[np.number]).columns
    df[numerieke_kolommen] = df[numerieke_kolommen].apply(normalize)
    print("\nData na normalisatie:")
    print(df.head())
    return df

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

    # Zet gecodeerde missende waarden om naar NaN.
    # Controleer deze codes aan de hand van het codeboek.
    missing_codes = {
            "diffgrad": [9],
            "her2_stat": [4, 7, 9],
            "multifoc": [9],
            "ond_lymf": [98, 99],
            "pos_lymf": [99],
            "er_stat": [9],
            "pr_stat": [9],
            "swk": [8]
        }

    for kolom, codes in missing_codes.items():
        if kolom in df.columns:
            df[kolom] = df[kolom].replace(codes, np.nan)

    # Bepaal kolommen met > 25% missings,
    # maar behoud de uitkomstvariabele
    high_missing_vars = missing_percentages[
        (missing_percentages > 25) &
        (missing_percentages.index != "overleving")
    ].index.tolist()

    df = df.drop(columns=high_missing_vars)

    # Verwijder rijen zonder bekende uitkomst
    df = df.dropna(subset=["overleving"])

    # imputeer na met de meest voorkomende waarden
    # kolommen = df.columns.drop('overleving')
    # imputer = SimpleImputer(strategy='most_frequent')
    # df[kolommen] = imputer.fit_transform(df[kolommen])

    df = df.dropna()

    # verwijderen van unieke kolommen
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

def maak_X_y(df):
    X = df.drop(
        columns=[
            "overleving",
            "vit_stat",
            "vit_stat_int",
            "topo"
        ],
        errors="ignore"
    )

    y = df["overleving"].astype(int)

    # Categorische variabelen
    categorical_kandidaten = [
        "ct", "cn", "pt", "pn", "diag_basis", "diffgrad",
        "gedrag", "her2_stat", "dcis_comp", "okd",
        "org_chir", "dir_reconstr", "meta_rt", "meta_chir",
        "multifoc", "later", "morf", "ond_lymf",
        "pos_lymf", "er_stat", "pr_stat", "swk",
        "chemo", "target", "horm", "rt", "topo_sublok",
        "tumsoort", "stadium", "cstadium", "pstadium",
        "uitgebr_chir_code"
    ]

    categorical = [
        kolom for kolom in categorical_kandidaten
        if kolom in X.columns
    ]

    # Andere tekstkolommen ook als categorisch behandelen
    for kolom in X.select_dtypes(
        include=["object", "category", "string"]
    ).columns:
        if kolom not in categorical:
            categorical.append(kolom)

    # Alle overige kenmerken numeriek verwerken
    numeric = [
        kolom for kolom in X.columns
        if kolom not in categorical
    ]

    print("\nCategorische variabelen:", categorical)
    print("\nNumerieke variabelen:", numeric)

    return X, y, categorical, numeric

def trainset(df):
    np.random.seed(42)
    train_size = int(2/3 * len(df))
    shuffled_indices = np.random.permutation(len(df))
    train_indices = shuffled_indices[:train_size]
    test_indices = shuffled_indices[train_size:]
    train = df.iloc[train_indices]
    test = df.iloc[test_indices]
    return train, test

def pipeline_bouwen(categorical, numeric):
    transformers = []

    # Numerieke variabelen: mediaan imputeren en schalen
    if numeric:
        transformers.append((
            "numeric",
            Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
            ]),
            numeric
        ))

    # Categorische variabelen: meest voorkomende waarde imputeren
    # en daarna one-hot encoden
    if categorical:
        transformers.append((
            "categorical",
            Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore"))
            ]),
            categorical
        ))

    preprocessor = ColumnTransformer(
        transformers=transformers,
        remainder="drop"
    )

    model = Pipeline([
        ("preprocess", preprocessor),
        ("classifier", MLPClassifier(
            hidden_layer_sizes=(400,),
            max_iter=1000,
            random_state=42,
            early_stopping=True
        ))
    ])

    return model

def model_trainen(model, train):
    model.fit(train.drop(columns=['overleving', 'vit_stat', 'vit_stat_int']), train['overleving'])

def model_voorspellen(test, model):
    p_nn = model.predict(test.drop(columns=['overleving', 'vit_stat', 'vit_stat_int']))
    return p_nn

def cf_matrix(p, o):
    cm = confusion_matrix(o, p, labels=[1, 0])

    # Volgorde: werkelijke klasse 1, daarna 0
    TP, FN = cm[0]
    FP, TN = cm[1]

    accuracy = accuracy_score(o, p)

    print("\nConfusion matrix:")
    print("                    Voorspeld 1   Voorspeld 0")
    print(f"Werkelijk 1             {TP}             {FN}")
    print(f"Werkelijk 0             {FP}             {TN}")

    print(f"\nAccuracy: {accuracy:.3f}")
    print(f"Error rate: {1 - accuracy:.3f}")

    return accuracy

def evaluatie(p_nn, test):
    p_nn_class = (p_nn > 0.5).astype(int)
    cf_matrix(p_nn_class, test['overleving'])

if __name__ == "__main__":
    df = maak_uitkomstvariabele(df, jaren=5)
    print(df.columns.tolist())
    print(df.dtypes)
    print(df[["vit_stat", "vit_stat_int", "overleving"]].head(10))
    df = verwijderen_missende_waarden(df)
    df = variabelen_omzetten_numeriek(df)
    print(df.shape)
    print(df.head())
    df = normaliseren_data(df)
    train, test = trainset(df)
    x, y, categorical, numeric = maak_X_y(df)
    model = pipeline_bouwen(categorical, numeric)
    model_trainen(model, train)
    p_nn = model_voorspellen(test, model)
    evaluatie(p_nn, test)
    print(pd.crosstab(df["overleving"], columns="Aantal patiënten"))
    print(df.shape)
