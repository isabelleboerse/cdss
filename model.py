import joblib
import numpy as np
import pandas as pd

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

BASE_DIR = Path(__file__).parent
DATA_FILE = Path(r"C:\Users\isabe\cdss\borstkanker.csv")
MODEL_FILE = BASE_DIR / "breast_cancer_model.joblib"


def maak_uitkomstvariabele(df, jaren=5):
    df = df.copy()
    dagen = jaren * 365.25
    df["overleving"] = np.where(
        df["vit_stat_int"] >= dagen, 1, np.where(df["vit_stat"] == 1, 0, np.nan)
    )
    return df


def voorbereiden_data(df):
    df = df.copy()

    missing_codes = {
        "diffgrad": [9],
        "her2_stat": [4, 7, 9],
        "multifoc": [9],
        "ond_lymf": [98, 99],
        "pos_lymf": [99],
        "er_stat": [9],
        "pr_stat": [9],
        "swk": [8],
    }

    for k, codes in missing_codes.items():
        if k in df.columns:
            df[k] = df[k].replace(codes, np.nan)

    missings = df.isna().mean()
    df = df.drop(
        columns=[k for k in df.columns if missings[k] > 0.25 and k != "overleving"]
    )

    return df.dropna(subset=["overleving"]).copy()


def maak_X_y(df):
    y = df["overleving"].astype(int)

    gekozen_variabelen = [
        "leeft",
        "gesl",
        "diffgrad",
        "er_stat",
        "pr_stat",
        "her2_stat",
        "pos_lymf",
        "ct",
        "cn",
        "morf",
        "tumorsoort",
        "okd",
        "org_chir",
        "horm",
        "rt",
        "meta_rt",
        "meta_chir",
    ]

    X = df[[k for k in gekozen_variabelen if k in df.columns]].copy()

    categorical = [k for k in X.columns if k != "leeft"]
    numeric = [k for k in X.columns if k == "leeft"]

    return X, y, categorical, numeric


def data_splitsen(X, y):
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.4, random_state=42, stratify=y
    )
    X_tune, X_test, y_tune, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
    )
    return X_train, X_tune, X_test, y_train, y_tune, y_test


def pipeline_bouwen(categorical, numeric):
    transformers = []

    if numeric:
        transformers.append(
            (
                "numeric",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                numeric,
            )
        )

    if categorical:
        transformers.append(
            (
                "categorical",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical,
            )
        )

    return Pipeline(
        [
            ("preprocess", ColumnTransformer(transformers)),
            (
                "classifier",
                MLPClassifier(
                    hidden_layer_sizes=(400,),
                    max_iter=1000,
                    random_state=42,
                    early_stopping=True,
                ),
            ),
        ]
    )


def model_trainen(model, x_train, y_train):
    model.fit(x_train, y_train)


def model_voorspellen(model, x_test):
    return model.predict(x_test)


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


def model_tunen(X_train, y_train, X_tune, y_tune, categorical, numeric):
    beste_score = -1
    beste_model = None

    for neuronen in [50, 100, 200, 400]:
        for alpha in [0.0001, 0.001, 0.01]:
            model = pipeline_bouwen(categorical, numeric)
            model.set_params(
                classifier__hidden_layer_sizes=(neuronen,), classifier__alpha=alpha
            )
            model_trainen(model, X_train, y_train)
            score = accuracy_score(y_tune, model_voorspellen(model, X_tune))

            if score > beste_score:
                beste_score, beste_model = score, model
                beste_instellingen = {"neuronen": neuronen, "alpha": alpha}

    print("Beste tune accuracy:", round(beste_score, 3))
    print("Beste instellingen:", beste_instellingen)
    return beste_model


def main():
    df = pd.read_csv(DATA_FILE, sep=";")
    df = maak_uitkomstvariabele(df, jaren=5)
    df = voorbereiden_data(df)
    X, y, categorical, numeric = maak_X_y(df)
    print("Kolommen model:", X.columns.tolist())

    X_train, X_tune, X_test, y_train, y_tune, y_test = data_splitsen(X, y)

    print("Aantal patiënten:", len(df))
    print("Training:", len(X_train), "| Tune:", len(X_tune), "| Test:", len(X_test))

    model = model_tunen(X_train, y_train, X_tune, y_tune, categorical, numeric)

    X_train_tune = pd.concat([X_train, X_tune])
    y_train_tune = pd.concat([y_train, y_tune])
    model_trainen(model, X_train_tune, y_train_tune)

    voorspellingen = model_voorspellen(model, X_test)
    print("\nTestresultaten:")
    cf_matrix(voorspellingen, y_test)
    print(classification_report(y_test, voorspellingen, labels=[0, 1], zero_division=0))

    joblib.dump(model, MODEL_FILE)
    print("Model opgeslagen als:", MODEL_FILE)

    print(df["gesl"].value_counts())


if __name__ == "__main__":
    main()
