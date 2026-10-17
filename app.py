
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
        patients = get_patients(
            prediction.PATIENTS_FILE.stat().st_mtime
        )

    except Exception as error:
        st.error(f"Er ging iets mis bij het laden: {error}")
        st.stop()

    if not patients:
        st.warning("Er zijn geen testpatiënten beschikbaar.")
    else:
        st.subheader("Selecteer een testpatiënt")

        patient_id = st.selectbox(
        "Patiënt",
        options=list(patients.keys()),
        format_func=lambda pid: patients[pid]["display_name"],
        index=None,
        placeholder="Selecteer een patiënt..."
    )
        if patient_id is None:
            st.info(
                "Selecteer eerst een patiënt om de "
                "overlevingskans te bekijken."
            )

        else:
            current_patient = patients[patient_id]

            st.subheader("Selecteer een behandeling")

            behandelopties = {
                "Okselklierdissectie": "okd",
                "Orgaanchirurgie": "org_chir",
                "Hormoontherapie": "horm",
                "Radiotherapie bij metastasen": "meta_rt",
                "Chirurgie bij metastasen": "meta_chir",
            }

            behandeling = st.selectbox(
                "Behandeling",
                options=list(behandelopties.keys()),
                index=None,
                placeholder="Selecteer een behandeling..."
            )

            try:
                # Voorspelling op basis van de oorspronkelijke
                # patiëntgegevens, zonder aanpassingen.
                probability_origineel = prediction.get_prediction(
                    model,
                    current_patient
                )

                st.subheader("Modelvoorspelling")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Oorspronkelijke patiëntgegevens",
                        f"{probability_origineel:.1%}"
                    )

                if behandeling is None:
                    with col2:
                        st.metric(
                            "Met gekozen behandeling",
                            "—"
                        )

                    st.info(
                        "Selecteer een behandeling om de tweede "
                        "voorspelling te berekenen."
                    )

                else:
                    gekozen_variabele = behandelopties[behandeling]

                    # Voorlopige aanname: waarde 1 betekent dat
                    # de geselecteerde behandeling wordt toegepast.
                    overrides = {
                        gekozen_variabele: 1
                    }

                    probability_behandeling = (
                        prediction.get_prediction(
                            model,
                            current_patient,
                            overrides=overrides
                        )
                    )

                    verschil = (
                        probability_behandeling
                        - probability_origineel
                    ) * 100

                    with col2:
                        st.metric(
                            "Met gekozen behandeling",
                            f"{probability_behandeling:.1%}",
                            delta=f"{verschil:+.1f} procentpunt"
                        )

                    st.caption(
                        f"Geselecteerde behandeling: {behandeling}. "
                        "De tweede voorspelling gebruikt dezelfde "
                        "patiëntgegevens, met de gekozen "
                        "behandelvariabele aangepast."
                    )

                st.caption(
                    "Dit zijn modelvoorspellingen. De uitkomsten "
                    "zijn niet automatisch betrouwbaar gekalibreerde "
                    "individuele overlevingskansen en bewijzen geen "
                    "causaal effect van een behandeling."
                )

            except Exception as error:
                st.error(
                    f"De voorspelling is mislukt: {error}"
                )

            with st.expander("Welke gegevens ontvangt het model?"):
                try:
                    X_patient = prediction.make_input(
                        current_patient
                    )

                    st.write("Oorspronkelijke patiëntgegevens")

                    st.dataframe(
                        X_patient.T.rename(
                            columns={0: "Waarde"}
                        ),
                        use_container_width=True
                    )

                    if behandeling is not None:
                        X_behandeling = prediction.make_input(
                            current_patient,
                            overrides={
                                gekozen_variabele: 1
                            }
                        )

                        st.write(
                            "Patiëntgegevens met gekozen behandeling"
                        )

                        st.dataframe(
                            X_behandeling.T.rename(
                                columns={0: "Waarde"}
                            ),
                            use_container_width=True
                        )

                except Exception as error:
                    st.error(
                        f"De modelinvoer kon niet worden getoond: "
                        f"{error}"
                    )

with tab2:
    kennisgedreven_cdss()