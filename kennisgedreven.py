import streamlit as st
import prediction


# KENNISBRONNEN


BRON_NHG = {
    "naam": "NHG-Standaard Borstkanker",
    "url": ("https://richtlijnen.nhg.org/standaarden/borstkanker"),
}

BRON_VERMOEIDHEID = {
    "naam": "NHG-Standaard Borstkanker - Vermoeidheid",
    "url": (
        "https://richtlijnen.nhg.org/standaarden/borstkanker"
        "#volledige-tekst-vermoeidheid"
    ),
}

BRON_WERKHERVATTING = {
    "naam": "NHG-Standaard Borstkanker - Werkhervatting",
    "url": (
        "https://richtlijnen.nhg.org/standaarden/borstkanker#volledige-tekst-terugkeer-naar-werk"
    ),
}

BRON_PIJN = {
    "naam": "NHG-Standaard Pijn",
    "url": ("https://richtlijnen.nhg.org/standaarden/pijn"),
}

BRON_SCHOUDER_KLACHTEN = {
    "naam": "Kanker.nl - Schouderklachten",
    "url": (
        "https://www.kanker.nl/kankersoorten/borstkanker/gevolgen/schouderklachten-na-borstkanker"
    ),
}

BRON_LYMFOEDEEM = {
    "naam": "NHG-Standaard Lymfoedeem",
    "url": (
        "https://richtlijnen.nhg.org/standaarden/borstkanker#volledige-tekst-lymfoedeem-en-schouderklachten"
    ),
}

BRON_LICHAMELIJKE_KLACHTEN = {
    "naam": "Richtlijnendatabase - Lichamelijke problemen",
    "url": (
        "https://richtlijnendatabase.nl/richtlijn/borstkanker/nazorg/lichamelijke_problemen.html"
    ),
}

BRON_COGNITIEVE_KLACHTEN = {
    "naam": "Richtlijnendatabase - Cognitieve en Psychosociale problemen",
    "url": (
        "https://richtlijnendatabase.nl/richtlijn/borstkanker/nazorg/vermoeidheid_cognitieve_en_psychosociale_problemen.html"
    ),
}

BRON_SLAAP = {
    "naam": "NHG-Standaard Slaapproblemen en slaapmiddelen",
    "url": ("https://richtlijnen.nhg.org/standaarden/slaapproblemen-en-slaapmiddelen"),
}

BRON_ANGST = {
    "naam": "NHG-Standaard Angst",
    "url": ("https://richtlijnen.nhg.org/standaarden/angst"),
}

BRON_DEPRESSIE = {
    "naam": "NHG-Standaard Depressie",
    "url": ("https://richtlijnen.nhg.org/standaarden/depressie"),
}

BRON_SOCIALE_PROBLEMEN = {
    "naam": "Richtlijnendatabase - Sociale problemen",
    "url": (
        "https://richtlijnendatabase.nl/richtlijn/borstkanker/nazorg/overige_gevolgen_van_borstkanker.html"
    ),
}

BRON_ONCOLOGIE = {
    "naam": "NHG-Standpunt Oncologische zorg (2014) - Nazorg, historische achtergrondbron",
    "url": (
        "https://richtlijnen.nhg.org/files/2021-11/nhg-standpunt_oncologische_zorg.pdf"
    ),
}

BRON_THUISARTS_CONTROLES = {
    "naam": "Thuisarts - Controles na borstkanker",
    "url": (
        "https://www.thuisarts.nl/borstkanker/"
        "behandeld-voor-borstkanker-welke-controles"
    ),
}

BRON_THUISARTS_KLACHTEN = {
    "naam": "Thuisarts - Klachten na borstkanker",
    "url": (
        "https://www.thuisarts.nl/borstkanker/borstkanker-gehad-omgaan-met-klachten"
    ),
}


# ADVIES AANMAKEN


def maak_advies(titel, tekst, prioriteit, bronnen):
    return {
        "titel": titel,
        "tekst": tekst,
        "prioriteit": prioriteit,
        "bronnen": bronnen,
    }


# BESLISMOMENT 2: ACUTE OF VERDACHTE KLACHTEN


def beoordeel_acute_klachten(rood_warm_pijnlijk, verdachte_afwijking):

    adviezen = []

    if rood_warm_pijnlijk:
        adviezen.append(
            maak_advies(
                "Directe medische beoordeling",
                (
                    "De patiënt heeft een rode, warme en "
                    "pijnlijke borst. Dit vraagt om directe "
                    "klinische beoordeling. Beoordeel "
                    "de ernst, bijkomende symptomen en "
                    "mogelijke oorzaken, waaronder een "
                    "ontsteking. Bepaal op basis van de "
                    "klinische bevindingen het verdere beleid."
                ),
                "hoog",
                [BRON_THUISARTS_CONTROLES],
            )
        )

    if verdachte_afwijking:
        adviezen.append(
            maak_advies(
                "Verdachte borstafwijking",
                (
                    "Er zijn klinische aanwijzingen voor "
                    "een mogelijk maligne borstafwijking. "
                    "Voer gericht lichamelijk onderzoek uit "
                    "en beoordeel verwijzing naar de "
                    "mammapoli volgens de NHG-Standaard "
                    "Borstkanker. Houd rekening met het "
                    "bestaande oncologische nazorgtraject."
                ),
                "hoog",
                [BRON_NHG],
            )
        )

    return adviezen


# KENNISGEDREVEN BESLISLOGICA


def beoordeel_klachten(gegevens):

    adviezen = beoordeel_acute_klachten(
        gegevens["rood_warm_pijnlijk"], gegevens["verdachte_afwijking"]
    )

    # BESLISMOMENT 1: NIEUWE KLACHTEN

    if (
        gegevens["nieuwe_klachten"]
        and not gegevens["rood_warm_pijnlijk"]
        and not gegevens["verdachte_afwijking"]
    ):
        adviezen.append(
            maak_advies(
                "Nieuwe klachten of veranderingen",
                (
                    "Bij nieuwe veranderingen aan de borst, "
                    "oksel of het litteken is gerichte "
                    "medische beoordeling nodig. "
                    "Vraag naar het ontstaan en beloop "
                    "van de afwijking en verricht gericht "
                    "lichamelijk onderzoek. Beoordeel "
                    "volgens de NHG-Standaard of "
                    "aanvullende diagnostiek of verwijzing "
                    "nodig is. Wacht bij een nieuwe "
                    "verdachte afwijking niet op de "
                    "volgende geplande controle."
                ),
                "middel",
                [BRON_NHG, BRON_THUISARTS_CONTROLES],
            )
        )

    # BESLISMOMENT 3: LICHAMELIJKE KLACHTEN

    if gegevens["lichamelijke_klachten"]:
        klachten = gegevens["typen_lichamelijk"]

        lichamelijke_regels = {
            "Vermoeidheid": (
                "Aanhoudende vermoeidheid",
                (
                    "Breng de vermoeidheid en de invloed "
                    "op het dagelijks functioneren in kaart. "
                    "Vraag naar het beloop en mogelijke "
                    "samenhang met de ziekte of behandeling. "
                    "Bespreek de klachten, de ervaren "
                    "beperkingen en de behoefte aan "
                    "verdere ondersteuning."
                ),
                [BRON_VERMOEIDHEID],
            ),
            "Langdurige pijn": (
                "Langdurige pijn",
                (
                    "Vraag naar de locatie, aard, ernst, "
                    "duur en het beloop van de pijn. "
                    "Breng de gevolgen voor het dagelijks "
                    "functioneren en eerdere behandelingen "
                    "in kaart. Beoordeel mogelijke "
                    "oorzaken en stel een passend "
                    "behandelplan op volgens de "
                    "NHG-Standaard Pijn. "
                    "Ga er niet automatisch van uit "
                    "dat de pijn een gevolg is van "
                    "de eerdere borstkankerbehandeling."
                ),
                [BRON_PIJN],
            ),
            "Schouderbeperkingen": (
                "Schouderbeperkingen",
                (
                    "Vraag naar pijn, stijfheid en "
                    "beperkingen bij het bewegen van "
                    "de arm of schouder. Bespreek "
                    "de invloed op dagelijkse activiteiten "
                    "en mogelijke gevolgen van de "
                    "borstkankerbehandeling. Beoordeel "
                    "of aanvullende begeleiding, "
                    "zoals fysiotherapie, passend is."
                ),
                [BRON_SCHOUDER_KLACHTEN],
            ),
            "Zwelling van arm of hand": (
                "Mogelijk lymfoedeem",
                (
                    "Zwelling van de arm of hand kan "
                    "voorkomen na een behandeling "
                    "van borstkanker waarbij lymfeklieren "
                    "zijn verwijderd of bestraald. "
                    "Beoordeel de zwelling en andere "
                    "mogelijke oorzaken. Als het "
                    "klinisch beeld past bij lymfoedeem, "
                    "kan gespecialiseerde behandeling "
                    "worden besproken. De historische "
                    "richtlijn Mammacarcinoom beschrijft "
                    "onder andere compressietherapie "
                    "en complexe decongestieve therapie. "
                    "Toets het behandelbeleid aan "
                    "actuele aanbevelingen."
                ),
                [BRON_LYMFOEDEEM],
            ),
            "Concentratie- of geheugenproblemen": (
                "Cognitieve klachten",
                (
                    "Bespreek concentratie- en "
                    "geheugenproblemen en de gevolgen "
                    "voor het dagelijks functioneren. "
                    "Vraag naar het ontstaan, het beloop "
                    "en mogelijke samenhang met "
                    "lichamelijke of psychosociale "
                    "problemen. Beoordeel of aanvullende "
                    "ondersteuning nodig is."
                ),
                [BRON_COGNITIEVE_KLACHTEN],
            ),
            "Slaapproblemen": (
                "Slaapproblemen",
                (
                    "Vraag naar het slaappatroon, "
                    "de duur van de klachten en "
                    "de gevolgen overdag. "
                    "Beoordeel mogelijke oorzaken "
                    "en factoren die de slaapproblemen "
                    "in stand houden. Bespreek "
                    "voorlichting en niet-medicamenteuze "
                    "behandeling volgens de "
                    "NHG-Standaard Slaapproblemen "
                    "en slaapmiddelen."
                ),
                [BRON_SLAAP],
            ),
            "Problemen met terugkeer naar werk": (
                "Problemen met werkhervatting",
                (
                    "Bespreek de gevolgen van kanker "
                    "en de behandeling voor het werk "
                    "en dagelijks functioneren. "
                    "Vraag naar ervaren beperkingen "
                    "en de behoefte aan begeleiding. "
                    "Overweeg afstemming met de "
                    "bedrijfsarts of betrokken "
                    "zorgverleners bij problemen "
                    "met terugkeer naar werk."
                ),
                [BRON_WERKHERVATTING],
            ),
        }

        for klacht in klachten:
            if klacht in lichamelijke_regels:
                titel, tekst, bronnen = lichamelijke_regels[klacht]

                adviezen.append(maak_advies(titel, tekst, "ondersteuning", bronnen))

        if not klachten:
            adviezen.append(
                maak_advies(
                    "Lichamelijke klachten beoordelen",
                    (
                        "Breng de aard en gevolgen "
                        "van de lichamelijke klachten "
                        "verder in kaart. Bespreek "
                        "de invloed op het dagelijks "
                        "functioneren en de behoefte "
                        "aan ondersteuning."
                    ),
                    "ondersteuning",
                    [BRON_LICHAMELIJKE_KLACHTEN],
                )
            )

    # BESLISMOMENT 4: PSYCHOSOCIALE KLACHTEN

    if gegevens["psychosociale_klachten"]:
        klachten = gegevens["typen_psychosociaal"]

        psychosociale_regels = {
            "Angst of onzekerheid": (
                "Angst of onzekerheid",
                (
                    "Breng de aard, ernst en duur "
                    "van de angstklachten in kaart. "
                    "Vraag naar de invloed op het "
                    "dagelijks functioneren en "
                    "eventueel vermijdingsgedrag. "
                    "Beoordeel of de klachten passen "
                    "bij een angststoornis en bespreek "
                    "passende begeleiding of behandeling "
                    "volgens de NHG-Standaard Angst."
                ),
                [BRON_ANGST],
            ),
            "Somberheid": (
                "Somberheid",
                (
                    "Vraag naar de duur en ernst "
                    "van de somberheid, verlies van "
                    "interesse of plezier en de gevolgen "
                    "voor het dagelijks functioneren. "
                    "Beoordeel of er aanwijzingen zijn "
                    "voor een depressie en besteed "
                    "aandacht aan eventuele suïcidaliteit. "
                    "Bepaal passende ondersteuning "
                    "of behandeling volgens de "
                    "NHG-Standaard Depressie."
                ),
                [BRON_DEPRESSIE],
            ),
            "Problemen met verwerking van de ziekte": (
                "Problemen met ziekteverwerking",
                (
                    "Bespreek de emotionele gevolgen "
                    "van de ziekte en behandeling. "
                    "Vraag welke problemen de patiënt "
                    "ervaart bij het omgaan met de "
                    "diagnose en de gevolgen ervan. "
                    "Bespreek de behoefte aan "
                    "psychosociale ondersteuning."
                ),
                [BRON_COGNITIEVE_KLACHTEN],
            ),
            "Problemen in relaties of sociaal functioneren": (
                "Sociaal functioneren",
                (
                    "Bespreek welke gevolgen de ziekte "
                    "en behandeling hebben voor relaties, "
                    "gezin en sociale activiteiten. "
                    "Vraag naar de ervaren belasting "
                    "en de beschikbare steun vanuit "
                    "de omgeving. Bespreek of "
                    "aanvullende psychosociale "
                    "ondersteuning gewenst is."
                ),
                [BRON_SOCIALE_PROBLEMEN],
            ),
            "Behoefte aan extra begeleiding": (
                "Aanvullende begeleiding en nazorg",
                (
                    "Bespreek de lichamelijke, psychische "
                    "en sociale zorgbehoeften van "
                    "de patiënt. Ga na welke zorgverleners "
                    "betrokken zijn en welke afspraken "
                    "over nazorg bestaan. Stem zo nodig "
                    "af met het oncologisch behandelteam "
                    "en bespreek passende aanvullende zorg."
                ),
                [BRON_ONCOLOGIE, BRON_NHG, BRON_THUISARTS_CONTROLES],
            ),
        }

        for klacht in klachten:
            if klacht in psychosociale_regels:
                titel, tekst, bronnen = psychosociale_regels[klacht]

                adviezen.append(maak_advies(titel, tekst, "ondersteuning", bronnen))

        if not klachten:
            adviezen.append(
                maak_advies(
                    "Psychosociale klachten beoordelen",
                    (
                        "Bespreek de aard en ernst "
                        "van de psychosociale klachten, "
                        "de gevolgen voor het dagelijks "
                        "functioneren en de gewenste "
                        "ondersteuning."
                    ),
                    "ondersteuning",
                    [BRON_COGNITIEVE_KLACHTEN],
                )
            )

    # GEEN KLACHTEN

    if not adviezen:
        adviezen.append(
            maak_advies(
                "Bestaande nazorg voortzetten",
                (
                    "Op basis van de geselecteerde "
                    "klachten geeft deze beslisboom "
                    "geen aanvullend advies. "
                    "Bespreek het bestaande nazorgplan "
                    "en blijf aandacht houden voor "
                    "nieuwe klachten en zorgbehoeften. "
                    "Dit sluit andere aandoeningen "
                    "of aanvullende zorgbehoeften niet uit."
                    "Verwijs de patiënt naar thuisarts om informatie bij de hand te hebben."
                ),
                "algemeen",
                [BRON_THUISARTS_CONTROLES],
            )
        )

    # ADVIEZEN SORTEREN

    volgorde = {"hoog": 0, "middel": 1, "ondersteuning": 2, "algemeen": 3}

    adviezen.sort(key=lambda advies: volgorde[advies["prioriteit"]])

    return adviezen


# ADVIEZEN TONEN


def toon_advies(advies):

    titel = advies["titel"]
    tekst = advies["tekst"]

    if advies["prioriteit"] == "hoog":
        st.error(f"**{titel}**\n\n{tekst}")

    elif advies["prioriteit"] == "middel":
        st.warning(f"**{titel}**\n\n{tekst}")

    else:
        st.info(f"**{titel}**\n\n{tekst}")

    st.markdown("**Gebruikte bron(nen):**")

    for bron in advies["bronnen"]:
        st.markdown(f"- [{bron['naam']}]({bron['url']})")


# STREAMLIT APPLICATIE


def kennisgedreven_cdss():

    st.header("Kennisgedreven beslisondersteuning")

    st.write(
        "Deze module ondersteunt huisartsen bij "
        "het beoordelen van klachten en zorgbehoeften "
        "van patiënten die borstkanker hebben of "
        "hiervoor behandeld zijn."
    )

    # patiënt selecteren

    st.subheader("Selecteer een patiënt")

    if not prediction.PATIENTS_FILE.exists():
        st.error("Testpatiënten ontbreken.")
        return

    @st.cache_data
    def get_kennisgedreven_patients(modified_time):
        return prediction.load_patients()

    try:
        patients = get_kennisgedreven_patients(prediction.PATIENTS_FILE.stat().st_mtime)
    except Exception as error:
        st.error(f"Er ging iets mis bij het laden: {error}")
        return

    if not patients:
        st.warning("Er zijn geen patiënten beschikbaar.")
        return

    patient_id = st.selectbox(
        "Patiënt",
        options=list(patients.keys()),
        format_func=lambda pid: patients[pid]["display_name"],
        index=None,
        placeholder="Selecteer een patiënt...",
        key="kennisgedreven_patient",
    )

    if patient_id is None:
        st.info(
            "Selecteer eerst een patiënt om de "
            "kennisgedreven beslisondersteuning te gebruiken."
        )
        return

    # BESLISMOMENT 1

    st.subheader("Beslismoment 1")

    st.write(
        "**Zijn er nieuwe klachten of veranderingen aan borst, oksel of litteken?**"
    )

    nieuwe_klachten = (
        st.radio(
            "Nieuwe klachten of veranderingen",
            ["Nee", "Ja"],
            horizontal=True,
            key="nieuwe_klachten",
        )
        == "Ja"
    )

    # BESLISMOMENT 2

    st.subheader("Beslismoment 2")

    st.write("**Zijn er acute of verdachte klachten?**")

    acute_klachten = st.radio(
        "Selecteer de bevinding:",
        [
            "Nee, geen acute of verdachte klachten",
            "Ja, rode, warme en pijnlijke borst",
            "Ja, klinisch verdachte borstafwijking",
            "Ja, beide bovenstaande klachten",
        ],
        index=0,
        key="acute_klachten",
    )

    rood_warm_pijnlijk = acute_klachten in [
        "Ja, rode, warme en pijnlijke borst",
        "Ja, beide bovenstaande klachten",
    ]

    verdachte_afwijking = acute_klachten in [
        "Ja, klinisch verdachte borstafwijking",
        "Ja, beide bovenstaande klachten",
    ]

    # Directe waarschuwingen
    acute_adviezen = beoordeel_acute_klachten(rood_warm_pijnlijk, verdachte_afwijking)

    for advies in acute_adviezen:
        toon_advies(advies)

    # BESLISMOMENT 3

    st.subheader("Beslismoment 3")

    st.write(
        "**Heeft de patiënt aanhoudende lichamelijke klachten na de behandeling?**"
    )

    lichamelijke_klachten = (
        st.radio(
            "Aanhoudende lichamelijke klachten",
            ["Nee", "Ja"],
            horizontal=True,
            key="lichamelijke_klachten",
        )
        == "Ja"
    )

    typen_lichamelijk = []

    if lichamelijke_klachten:
        typen_lichamelijk = st.multiselect(
            "Welke lichamelijke klachten?",
            [
                "Vermoeidheid",
                "Langdurige pijn",
                "Schouderbeperkingen",
                "Zwelling van arm of hand",
                "Concentratie- of geheugenproblemen",
                "Slaapproblemen",
                "Problemen met terugkeer naar werk",
            ],
            key="typen_lichamelijk",
        )

    # BESLISMOMENT 4

    st.subheader("Beslismoment 4")

    st.write(
        "**Heeft de patiënt aanhoudende psychosociale klachten na de behandeling?**"
    )

    psychosociale_klachten = (
        st.radio(
            "Psychosociale klachten",
            ["Nee", "Ja"],
            horizontal=True,
            key="psychosociale_klachten",
        )
        == "Ja"
    )

    typen_psychosociaal = []

    if psychosociale_klachten:
        typen_psychosociaal = st.multiselect(
            "Welke psychosociale klachten of behoeften?",
            [
                "Angst of onzekerheid",
                "Somberheid",
                "Problemen met verwerking van de ziekte",
                "Problemen in relaties of sociaal functioneren",
                "Behoefte aan extra begeleiding",
            ],
            key="typen_psychosociaal",
        )

    # ADVIES GENEREREN

    st.divider()

    if st.button("Genereer richtlijnadvies", type="primary", key="genereer_advies"):
        gegevens = {
            "nieuwe_klachten": nieuwe_klachten,
            "rood_warm_pijnlijk": rood_warm_pijnlijk,
            "verdachte_afwijking": verdachte_afwijking,
            "lichamelijke_klachten": lichamelijke_klachten,
            "typen_lichamelijk": typen_lichamelijk,
            "psychosociale_klachten": psychosociale_klachten,
            "typen_psychosociaal": typen_psychosociaal,
        }

        adviezen = beoordeel_klachten(gegevens)

        st.subheader("Richtlijngebaseerde adviezen")

        # Acute waarschuwingen zijn eerder al getoond
        overige_adviezen = [
            advies for advies in adviezen if advies["prioriteit"] != "hoog"
        ]

        if any(advies["prioriteit"] == "hoog" for advies in adviezen):
            st.caption(
                "De waarschuwing over de acute of "
                "verdachte afwijking is hierboven "
                "al direct weergegeven."
            )

        if overige_adviezen:
            for advies in overige_adviezen:
                toon_advies(advies)

        else:
            st.info(
                "Er zijn geen aanvullende adviezen "
                "naast de hierboven weergegeven waarschuwing."
            )

        st.caption(
            "Dit is een onderwijsprototype. "
            "De adviezen zijn vereenvoudigde "
            "vertalingen van richtlijninformatie "
            "en zijn niet klinisch gevalideerd. "
            "Oudere NHG-documenten worden "
            "uitsluitend als historische "
            "achtergrondbronnen gebruikt. "
            "De huisarts blijft verantwoordelijk "
            "voor de klinische besluitvorming."
        )
