
from pathlib import Path
import sqlite3

import joblib
import pandas as pd


BASE_DIR = Path(__file__).parent

MODEL_FILE = BASE_DIR / "breast_cancer_model.joblib"
PATIENTS_FILE = BASE_DIR / "breastcancer.db"


FEATURES = [
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


def load_model():
    """Laad het getrainde model."""
    return joblib.load(MODEL_FILE)


def load_patients():
    """Lees uitsluitend fictieve patiënten uit de SQLite-database."""
    with sqlite3.connect(PATIENTS_FILE) as conn:
        df = pd.read_sql_query(
            "SELECT * FROM patient ORDER BY id",
            conn,
        )

    patients = {}

    for _, row in df.iterrows():
        patient = row.to_dict()

        patient_id = patient["id"]

        display_name = patient.get(
            "display_name",
            f"Patiënt {patient_id}",
        )

        patients[str(patient_id)] = {
            **patient,
            "demo_patient_id": str(patient_id),
            "display_name": display_name,
        }

    return patients


def make_input(patient, overrides=None):
    """
    Maak een DataFrame met de kenmerken die het model verwacht.

    overrides is optioneel en bevat kenmerken die tijdelijk
    aangepast worden voor een behandelsscenario.
    """
    ontbrekend = [
        feature
        for feature in FEATURES
        if feature not in patient
    ]

    if ontbrekend:
        raise ValueError(
            "Deze kenmerken ontbreken in de database: "
            f"{ontbrekend}"
        )

    # Kopieer de oorspronkelijke waarden.
    gegevens = {
        feature: patient[feature]
        for feature in FEATURES
    }

    # Pas uitsluitend de opgegeven kenmerken aan.
    if overrides is not None:
        for feature, value in overrides.items():

            if feature not in FEATURES:
                raise ValueError(
                    f"Onbekend modelkenmerk: {feature}"
                )

            gegevens[feature] = value

    return pd.DataFrame(
        [gegevens],
        columns=FEATURES,
    )


def get_prediction(model, patient, overrides=None):
    """
    Geef de door het model geschatte kans op klasse 1.

    Zonder overrides:
        Gebruik de oorspronkelijke patiëntgegevens.

    Met overrides:
        Gebruik dezelfde patiëntgegevens, maar pas de opgegeven
        kenmerken tijdelijk aan voor een scenariovergelijking.
    """
    X_patient = make_input(
        patient,
        overrides=overrides,
    )

    probabilities = model.predict_proba(X_patient)[0]

    classes = list(model.classes_)

    if 1 not in classes:
        raise ValueError(
            "Klasse 1 ontbreekt in de klassen van het model. "
            f"Gevonden klassen: {classes}"
        )

    return float(
        probabilities[classes.index(1)]
    )