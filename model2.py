
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


def maak_uitkomstvariabele(df, jaren=5):
    dagen = jaren * 365.25
    df = df.copy()

    # Uitkomst is onbekend totdat deze kan worden vastgesteld
    df["overleving"] = np.nan

    # Overleden vóór de gekozen termijn
    df.loc[
        (df["vit_stat"] == 1) &
        (df["vit_stat_int"] < dagen),
        "overleving"
    ] = 0

    # Follow-upduur van minstens de gekozen termijn
    df.loc[
        df["vit_stat_int"] >= dagen,
        "overleving"
    ] = 1

    return df


def verwijderen_missende_waarden(df):
    df = df.copy()

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

    # Bereken missings nadat de speciale codes zijn omgezet
    missing_percentages = df.isna().mean() * 100

    print("\nPercentage missings per variabele:")
    print(missing_percentages.sort_values(ascending=False))

    # Verwijder kolommen met >25% missings,
    # maar behoud de uitkomstvariabele
    high_missing_vars = missing_percentages[
        (missing_percentages > 25) &
        (missing_percentages.index != "overleving")
    ].index.tolist()

    print("\nKolommen verwijderd wegens >25% missings:")
    print(high_missing_vars)

    df = df.drop(columns=high_missing_vars)

    # Verwijder identificatiekolommen
    df = df.drop(
        columns=["key_nkr", "key_eid"],
        errors="ignore"
    )

    # Verwijder alleen patiënten zonder bekende uitkomst
    df = df.dropna(subset=["overleving"])

    return df


def build_pipeline(categorical, numeric):
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


if __name__ == "__main__":

    # 1. Dataset inlezen
    df = pd.read_csv(r"C:\Users\isabe\cdss\borstkanker.csv", sep=";")

    print("Oorspronkelijke dataset:", df.shape)

    # 2. Uitkomstvariabele maken
    df = maak_uitkomstvariabele(df, jaren=5)

    print("\nVerdeling van de uitkomst vóór filtering:")
    print(df["overleving"].value_counts(dropna=False))

    # 3. Speciale missingscodes verwerken en kolommen selecteren
    df = verwijderen_missende_waarden(df)

    print("\nDataset na selectie:", df.shape)
    print("\nVerdeling van de uitkomst:")
    print(df["overleving"].value_counts())

    # 4. X en y maken
    kolommen_verwijderen = [
        "overleving",
        "vit_stat",
        "vit_stat_int",
        "topo",
        "key_nkr",
        "key_eid"
    ]

    X = df.drop(
        columns=kolommen_verwijderen,
        errors="ignore"
    )

    y = df["overleving"].astype(int)

    # 5. Categorische variabelen definiëren
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

    # Voeg overige tekstkolommen toe als categorisch
    for kolom in X.select_dtypes(
        include=["object", "category"]
    ).columns:
        if kolom not in categorical:
            categorical.append(kolom)

    # Overige numerieke kolommen
    numeric = [
        kolom for kolom in X.select_dtypes(
            include=[np.number]
        ).columns
        if kolom not in categorical
    ]

    print("\nCategorische variabelen:")
    print(categorical)

    print("\nNumerieke variabelen:")
    print(numeric)

    # 6. Train-test-split vóór imputatie en encoding
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=1/3,
        random_state=42,
        stratify=y
    )

    # 7. Pipeline bouwen en trainen
    nn = build_pipeline(categorical, numeric)
    nn.fit(X_train, y_train)

    # 8. Voorspellen
    p_nn = nn.predict(X_test)

    # 9. Evalueren
    cf_matrix(p_nn, y_test.to_numpy())

    print("\nClassification report:")
    print(classification_report(
        y_test,
        p_nn,
        zero_division=0
    ))
