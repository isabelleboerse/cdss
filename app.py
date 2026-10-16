import pandas as pd
import streamlit as st
import prediction
from kennisgedreven import kennisgedreven_cdss

st.set_page_config(page_title="Borstkanker ML-demo")
st.title("Borstkanker: ML-demo")
st.caption(
    "Technische demo voor het voorspellen van vijfjaarsoverleving. "
    "Niet bedoeld voor klinische beslissingen."
)

tab1, tab2 = st.tabs(["Datagedreven", "Kennisgedreven"])

with tab1:

    if not prediction.MODEL_FILE.exists():
        st.error("Model ontbreekt. Voer eerst python model.py uit.")
        st.stop()

    if not prediction.PATIENTS_FILE.exists():
        st.error("Testpatiënten ontbreken. Voer eerst python model.py uit.")
        st.stop()


    @st.cache_resource
    def get_model(modified_time):
        return prediction.load_model()


    @st.cache_data
    def get_patients(modified_time):
        return prediction.load_patients()


    try:
        model = get_model(prediction.MODEL_FILE.stat().st_mtime)
        patients = get_patients(prediction.PATIENTS_FILE.stat().st_mtime)
    except Exception as error:
        st.error(f"Er ging iets mis bij het laden: {error}")
        st.stop()

    if not patients:
        st.warning("Er zijn geen testpatiënten beschikbaar.")
        st.stop()

    st.subheader("Selecteer een testpatiënt")

    patient_id = st.selectbox(
        "Patiënt",
        options=list(patients.keys())
    )
    current_patient = patients[patient_id]

    try:
        probability = prediction.get_prediction(model, current_patient)
    except Exception as error:
        st.error(f"De voorspelling is mislukt: {error}")
        st.stop()

    st.subheader("Modelvoorspelling")
    st.metric(
        "Voorspelde kans op minstens vijf jaar overleving",
        f"{probability:.1%}"
    )
    st.caption(
        "Dit is de kans die het model aan klasse 1 toekent. "
        "Deze waarde is niet automatisch een betrouwbaar gekalibreerde "
        "individuele overlevingskans."
    )

    with st.expander("Welke gegevens ontvangt het model?"):
        X_patient = prediction.make_input(current_patient)
        st.dataframe(
            X_patient.T.rename(columns={0: "Waarde"}),
            use_container_width=True
        )

    with st.expander("Werkelijke uitkomst in de testdata"):
        outcome = current_patient.get("werkelijke_overleving")

        if pd.notna(outcome):
            st.write("Werkelijke klasse:", int(outcome))
            st.caption(
                "Alleen bedoeld om de voorspelling achteraf te vergelijken "
                "met de bekende uitkomst in deze testdataset."
            )

with tab2:
    kennisgedreven_cdss()