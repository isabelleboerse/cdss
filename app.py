import pandas as pd
import streamlit as st
import prediction
from kennisgedreven import kennisgedreven_cdss


FIELD_LABELS = {
    "gesl": "Geslacht",
    "leeft": "Leeftijd bij diagnose (jaar)",
    "diffgrad": "Tumorgraad (diffgrad)",
    "er_stat": "ER-status",
    "pr_stat": "PR-status",
    "her2_stat": "HER2-status",
    "pos_lymf": "Aantal positieve lymfeklieren",
    "ct": "cT (TNM)",
    "cn": "cN (TNM)",
    "morf": "Morfologie",
    "tumorsoort": "Tumorsoort",
    "okd": "Okselklierdissectie",
    "org_chir": "Orgaanchirurgie",
    "horm": "Hormoontherapie",
    "rt": "Radiotherapie",
    "meta_rt": "Radiotherapie bij metastasen",
    "meta_chir": "Chirurgie bij metastasen",
}

JA_NEE = {
    "0": "Nee",
    "1": "Ja",
}

VALUE_LABELS = {
    "gesl": {"1": "Man", "2": "Vrouw"},
    "tumorsoort": {
        "501300": "Invasief mammacarcinoom",
        "502200": "Ductaal carcinoma in situ (DCIS)",
        "503200": "Lobulair carcinoma in situ (LCIS)",
    },
    "okd": JA_NEE,
    "org_chir": JA_NEE,
    "horm": JA_NEE,
    "rt": JA_NEE,
    "meta_rt": JA_NEE,
    "meta_chir": JA_NEE,
    "her2_stat": {
        "0": "0 — negatief",
        "1": "1+ — negatief",
        "3": "3+ — positief",
    },
    "diffgrad": {
        "1": "Graad 1 — goed gedifferentieerd",
        "2": "Graad 2 — matig gedifferentieerd",
        "3": "Graad 3 — slecht gedifferentieerd",
    },
    "er_stat": {
        "0": "Negatief",
        "1": "Positief",
    },
    "pr_stat": {
        "0": "Negatief",
        "1": "Positief",
    },
    "morf": {
        "8000": "Neoplasma, NNO",
        "8010": "Carcinoom, NNO",
        "8050": "Papillair carcinoom, NNO",
        "8140": "Adenocarcinoom, NNO",
        "8200": "Adenoïd cysteus carcinoom",
        "8201": "Cribriform carcinoom",
        "8211": "Tubulair adenocarcinoom",
        "8260": "Papillair adenocarcinoom, NNO",
        "8401": "Apocrien adenocarcinoom",
        "8480": "Mucineus adenocarcinoom",
        "8481": "Slijmvormend adenocarcinoom",
        "8500": "Ductaal carcinoom, NNO",
        "8501": "Comedocarcinoom, NNO",
        "8503": "Intraductaal papillair adenocarcinoom",
        "8504": "Omkapseld (intracysteus) papillair carcinoom",
        "8507": "Intraductaal micropapillair carcinoom",
        "8509": "Solide papillair carcinoom",
        "8510": "Medullair carcinoom, NNO",
        "8520": "Lobulair carcinoom, NNO",
        "8521": "Ductulair carcinoom",
        "8522": "Ductaal en lobulair carcinoom",
        "8523": "Ductaal carcinoom, gemengd met ander carcinoomtype",
        "8524": "Lobulair carcinoom gemengd met ander carcinoomtype",
        "8540": "Morbus Paget van mamma",
        "8541": "Morbus Paget en infiltrerend ductaal carcinoom",
        "8543": "Morbus Paget en intraductaal carcinoom (DCIS)",
        "8575": "Metaplastisch carcinoom, NNO",
        "8980": "Carcinosarcoom, NNO",
        "8982": "Myo-epitheliaal carcinoom",
        "8983": "Maligne adenomyo-epithelioom",
    },
    "horm": {
        "0": "Nee",
        "1": "Ja, alleen prechirurgisch",
        "2": "Ja, alleen postchirurgisch",
        "3": "Ja, zowel pre- als postchirurgisch",
        "4": "Ja, geen chirugie",
    },
    "rt": {
        "0": "Nee",
        "1": "Ja, alleen prechirurgisch",
        "2": "Ja, alleen postchirurgisch",
        "3": "Ja, zowel pre- als postchirurgisch",
        "4": "Ja, geen chirurgie",
    },
}



def invoer_voor_weergave(modelinvoer):
    tabel = modelinvoer.T.rename(columns={0: "Waarde"}).copy()

    # Alleen de weergave wordt tekst; de modelinvoer blijft ongewijzigd.
    tabel["Waarde"] = tabel["Waarde"].map(
        lambda waarde: "Onbekend" if pd.isna(waarde) else str(waarde)
    )

    for kenmerk, mapping in VALUE_LABELS.items():
        if kenmerk in tabel.index:
            waarde = tabel.loc[kenmerk, "Waarde"]
            code = waarde.removesuffix(".0")
            tabel.loc[kenmerk, "Waarde"] = mapping.get(code, waarde)

    return tabel.rename(index=FIELD_LABELS)


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

    else:
        st.subheader("Selecteer een testpatiënt")

        patient_id = st.selectbox(
            "Patiënt",
            options=list(patients.keys()),
            format_func=lambda pid: patients[pid]["display_name"],
            index=None,
            placeholder="Selecteer een patiënt...",
        )

        if patient_id is None:
            st.info("Selecteer eerst een patiënt om de overlevingskans te bekijken.")

        else:
            current_patient = patients[patient_id]

            behandelopties = {
                "Okselklierdissectie": "okd",
                "Orgaanchirurgie": "org_chir",
                "Hormoontherapie": "horm",
                "Radiotherapie bij metastasen": "meta_rt",
                "Chirurgie bij metastasen": "meta_chir",
            }

            try:
                # Voorspelling op basis van de oorspronkelijke
                # patiëntgegevens, zonder aanpassingen.
                probability_origineel = prediction.get_prediction(
                    model, current_patient
                )

                st.subheader("Modelvoorspelling")

                # De oorspronkelijke voorspelling staat nu
                # boven de behandelkeuze, met een nieuwe naam.
                st.metric(
                    "Vijfjaarsoverleving o.b.v. patiëntgegevens",
                    f"{probability_origineel:.1%}",
                )

                # onderdeel verplaatsen
                # naar onder de oorspronkelijke voorspelling.
                st.subheader("Selecteer een behandeling")

                behandeling = st.selectbox(
                    "Behandeling",
                    options=list(behandelopties.keys()),
                    index=None,
                    placeholder="Selecteer een behandeling...",
                )

                if behandeling is None:
                    st.info(
                        "Selecteer een behandeling om de tweede "
                        "voorspelling te berekenen."
                    )

                else:
                    gekozen_variabele = behandelopties[behandeling]

                    # Voorlopige aanname: waarde 1 betekent dat
                    # de geselecteerde behandeling wordt toegepast.
                    overrides = {gekozen_variabele: 1}

                    probability_behandeling = prediction.get_prediction(
                        model, current_patient, overrides=overrides
                    )

                    verschil = (probability_behandeling - probability_origineel) * 100

                    # De tweede voorspelling staat nu
                    # onder de behandelkeuze.
                    st.metric(
                        "Vijfjaarsoverleving met gekozen behandeling",
                        f"{probability_behandeling:.1%}",
                        delta=f"{verschil:+.1f} procentpunt",
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
                st.error(f"De voorspelling is mislukt: {error}")

            with st.expander("Welke gegevens ontvangt het model?"):
                try:
                    X_patient = prediction.make_input(current_patient)

                    st.write("Oorspronkelijke patiëntgegevens")

                    st.dataframe(
                        invoer_voor_weergave(X_patient), use_container_width=True
                    )

                    if behandeling is not None:
                        X_behandeling = prediction.make_input(
                            current_patient, overrides={gekozen_variabele: 1}
                        )

                        st.write("Patiëntgegevens met gekozen behandeling")

                        # waarden met elkaar te vergelijken.
                        originele_tabel = invoer_voor_weergave(X_patient)

                        aangepaste_tabel = invoer_voor_weergave(X_behandeling)

                        label = FIELD_LABELS.get(gekozen_variabele, gekozen_variabele)

                        oud = originele_tabel.loc[label, "Waarde"]

                        nieuw = aangepaste_tabel.loc[label, "Waarde"]

                        # Markeer de gewijzigde rij geel.
                        # Alleen als de waarde echt veranderd is.
                        if oud != nieuw:
                            gemarkeerde_tabel = aangepaste_tabel.style.apply(
                                lambda row: [
                                    "background-color: #FFF3B0; color: #000000"
                                    if row.name == label
                                    else ""
                                    for _ in row
                                ],
                                axis=1,
                            )

                            st.dataframe(gemarkeerde_tabel, use_container_width=True)

                            # NIEUW 6:
                            # Toon expliciet wat veranderd is.
                            st.info(
                                f"**Gewijzigde variabele:** {label}: {oud} → {nieuw}"
                            )

                        else:
                            # Geen highlight als de behandeling
                            # al in de oorspronkelijke data stond.
                            st.dataframe(aangepaste_tabel, use_container_width=True)

                            st.info(
                                f"{label} stond al op {nieuw}. "
                                "Er zijn geen patiëntgegevens gewijzigd."
                            )

                except Exception as error:
                    st.error(f"De modelinvoer kon niet worden getoond: {error}")


with tab2:
    kennisgedreven_cdss()
