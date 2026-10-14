
from pathlib import Path
import sqlite3

import joblib
import pandas as pd

BASE_DIR = Path(__file__).parent
MODEL_FILE = BASE_DIR / "breast_cancer_model.joblib"
PATIENTS_FILE = BASE_DIR / "breastcancer.db"

FEATURES = [
    "leeft",
    "diffgrad",
    "er_stat",
    "pr_stat",
    "her2_stat",
    "pos_lymf",
    "ct",
    "cn",
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
            "display_name", f"Patiënt {patient_id}"
        )

        patients[str(patient_id)] = {
            **patient,
            "demo_patient_id": str(patient_id),
            "display_name": display_name,
        }

    return patients


def make_input(patient):
    """Selecteer uitsluitend de kenmerken die het model verwacht."""
    ontbrekend = [
        feature for feature in FEATURES
        if feature not in patient
    ]

    if ontbrekend:
        raise ValueError(
            f"Deze kenmerken ontbreken in de database: {ontbrekend}"
        )

    return pd.DataFrame(
        [{feature: patient[feature] for feature in FEATURES}],
        columns=FEATURES,
    )


def get_prediction(model, patient):
    """Geef de geschatte kans op klasse 1."""
    X_patient = make_input(patient)
    probabilities = model.predict_proba(X_patient)[0]
    classes = list(model.classes_)

    return float(probabilities[classes.index(1)])