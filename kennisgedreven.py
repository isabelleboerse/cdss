import streamlit as st

# KENNISBRONNEN


BRON_NHG = "https://richtlijnen.nhg.org/standaarden/borstkanker"

BRON_ONCOLOGIE = (
    "https://richtlijnen.nhg.org/files/2021-11/nhg-standpunt_oncologische_zorg.pdf"
)
BRON_NHG_VERMOEIDHEID = (
    "https://richtlijnen.nhg.org/standaarden/borstkanker"
    "#volledige-tekst-vermoeidheid"
)

BRON_THUISARTS = (
    "https://www.thuisarts.nl/borstkanker/behandeld-voor-borstkanker-welke-controles"
)


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
                    "De borst is rood, warm en pijnlijk. "
                    "Beoordeel direct de klinische situatie, "
                    "urgentie en mogelijke oorzaken, "
                    "zoals een ontsteking."
                ),
                "hoog",
                [BRON_THUISARTS, BRON_NHG],
            )
        )

    if verdachte_afwijking:
        adviezen.append(
            maak_advies(
                "Verdachte borstafwijking",
                (
                    "Er zijn klinische aanwijzingen voor "
                    "een mogelijk maligne borstafwijking. "
                    "Beoordeel verwijzing naar de mammapoli "
                    "of het behandelend mammateam volgens "
                    "de NHG-Standaard Borstkanker."
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

    # Voorkomt dubbel algemeen advies wanneer
    # al een acute of verdachte afwijking is herkend.

    if (
        gegevens["nieuwe_klachten"]
        and not gegevens["rood_warm_pijnlijk"]
        and not gegevens["verdachte_afwijking"]
    ):
        adviezen.append(
            maak_advies(
                "Nieuwe klachten of veranderingen",
                (
                    "Voer gerichte anamnese en lichamelijk "
                    "onderzoek uit. Beoordeel of aanvullende "
                    "diagnostiek of overleg met het mammateam "
                    "nodig is. Wacht bij een nieuwe afwijking "
                    "niet automatisch op de volgende controle."
                ),
                "middel",
                [BRON_NHG, BRON_THUISARTS],
            )
        )

    # BESLISMOMENT 3: LICHAMELIJKE KLACHTEN

    if gegevens["lichamelijke_klachten"]:
        klachten = gegevens["typen_lichamelijk"]

        lichamelijke_regels = {
            "Vermoeidheid": (
                "Aanhoudende vermoeidheid",
                (
                    "Breng de ernst en invloed op het "
                    "dagelijks functioneren in kaart. "
                    "Beoordeel mogelijke oorzaken en "
                    "bespreek zelfmanagement, belastbaarheid "
                    "en eventuele oncologische revalidatie."
                ),
                [BRON_NHG_VERMOEIDHEID],
            ),
            "Langdurige pijn": (
                "Langdurige pijn",
                (
                    "Beoordeel de aard, locatie, ernst en "
                    "gevolgen van de pijn. Onderzoek mogelijke "
                    "oorzaken en bespreek passende behandeling "
                    "of gespecialiseerde ondersteuning."
                ),
                [BRON_ONCOLOGIE],
            ),
            "Schouderbeperkingen": (
                "Schouderbeperkingen",
                (
                    "Beoordeel de bewegingsbeperking en "
                    "de invloed op dagelijkse activiteiten. "
                    "Overweeg passende fysiotherapeutische "
                    "begeleiding of oncologische revalidatie."
                ),
                [BRON_ONCOLOGIE],
            ),
            "Zwelling van arm of hand": (
                "Mogelijk lymfoedeem",
                (
                    "Beoordeel de zwelling en mogelijke "
                    "oorzaken. Overweeg bij passend "
                    "lymfoedeem gespecialiseerde "
                    "fysiotherapie of huidtherapie. "
                    "Sluit andere oorzaken niet automatisch uit."
                ),
                [BRON_NHG, BRON_ONCOLOGIE],
            ),
            "Concentratie- of geheugenproblemen": (
                "Cognitieve klachten",
                (
                    "Bespreek concentratie- en "
                    "geheugenproblemen en de invloed "
                    "op het dagelijks functioneren. "
                    "Beoordeel mogelijke oorzaken en "
                    "de behoefte aan aanvullende begeleiding."
                ),
                [BRON_ONCOLOGIE],
            ),
            "Slaapproblemen": (
                "Slaapproblemen",
                (
                    "Breng de aard en duur van de "
                    "slaapproblemen in kaart en beoordeel "
                    "mogelijke samenhang met lichamelijke "
                    "of psychosociale klachten. "
                    "Bespreek passende ondersteuning."
                ),
                [BRON_ONCOLOGIE],
            ),
            "Problemen met terugkeer naar werk": (
                "Werkhervatting",
                (
                    "Bespreek de mogelijkheden en "
                    "belemmeringen bij terugkeer naar werk. "
                    "Overweeg afstemming met de bedrijfsarts "
                    "en passende revalidatie of begeleiding."
                ),
                [BRON_ONCOLOGIE],
            ),
        }

        for klacht in klachten:
            if klacht in lichamelijke_regels:
                titel, tekst, bronnen = lichamelijke_regels[klacht]

                adviezen.append(maak_advies(titel, tekst, "ondersteuning", bronnen))

        # Wel lichamelijke klachten aangegeven,
        # maar geen specifieke klacht geselecteerd.

        if not klachten:
            adviezen.append(
                maak_advies(
                    "Lichamelijke klachten beoordelen",
                    (
                        "Breng de lichamelijke klachten en hun "
                        "invloed op het dagelijks functioneren "
                        "verder in kaart. Bespreek welke "
                        "ondersteuning de patiënt nodig heeft."
                    ),
                    "ondersteuning",
                    [BRON_ONCOLOGIE],
                )
            )

    # BESLISMOMENT 4: PSYCHOSOCIALE KLACHTEN

    if gegevens["psychosociale_klachten"]:
        klachten = gegevens["typen_psychosociaal"]

        # Eén algemeen psychosociaal advies.
        # Specifieke aanvullingen worden hieraan toegevoegd.

        tekst = (
            "Bespreek de aard en ernst van de "
            "psychosociale klachten, de invloed op "
            "het dagelijks functioneren en de "
            "ondersteuningsbehoefte van de patiënt. "
            "Overweeg begeleiding door de huisarts "
            "of POH-GGZ, gespecialiseerde psychosociale "
            "zorg of oncologische revalidatie."
        )

        if "Problemen in relaties of sociaal functioneren" in klachten:
            tekst += (
                " Bespreek daarnaast de gevolgen voor "
                "relaties, gezin en sociaal functioneren. "
                "Betrek waar passend het sociale netwerk "
                "of gespecialiseerde hulp."
            )

        if "Behoefte aan extra begeleiding" in klachten:
            tekst += (
                " Bespreek of een individueel nazorgplan "
                "wenselijk is, met daarin de zorgbehoeften, "
                "behandeldoelen, betrokken zorgverleners "
                "en afspraken over verdere begeleiding. "
                "Stem zo nodig af met het oncologisch team."
            )

        adviezen.append(
            maak_advies(
                "Psychosociale ondersteuning", tekst, "ondersteuning", [BRON_ONCOLOGIE]
            )
        )

    # GEEN KLACHTEN OF AFWIJKINGEN

    if not adviezen:
        adviezen.append(
            maak_advies(
                "Bestaande nazorg voortzetten",
                (
                    "Er zijn geen klachten geselecteerd "
                    "waarvoor deze beslisboom een aanvullend "
                    "advies geeft. Bespreek het bestaande "
                    "nazorgplan en blijf alert op veranderingen. "
                    "Andere aandoeningen zijn hiermee niet "
                    "uitgesloten."
                ),
                "algemeen",
                [BRON_NHG, BRON_ONCOLOGIE],
            )
        )

    # ADVIEZEN SORTEREN OP PRIORITEIT

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

    for nummer, bron in enumerate(advies["bronnen"], start=1):
        st.markdown(f"[Bekijk kennisbron {nummer}]({bron})")


# STREAMLIT APPLICATIE


def kennisgedreven_cdss():

    st.header("Kennisgedreven beslisondersteuning")

    st.write(
        "Deze module ondersteunt huisartsen bij "
        "het beoordelen van klachten en zorgbehoeften "
        "van patiënten die borstkanker hebben of "
        "hiervoor behandeld zijn."
    )

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

    # Waarschuwingen direct tonen.
    # Dezelfde waarschuwingen worden niet opnieuw
    # getoond bij het genereren van het eindadvies.

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

        # Acute waarschuwingen zijn al direct bij
        # beslismoment 2 getoond.
        # Daarom hier uitsluitend de overige adviezen.

        overige_adviezen = [
            advies for advies in adviezen if advies["prioriteit"] != "hoog"
        ]

        if any(advies["prioriteit"] == "hoog" for advies in adviezen):
            st.caption(
                "Het advies bij de acute of verdachte "
                "bevinding is hierboven al direct getoond. "
                "Hieronder staan alleen eventuele "
                "aanvullende adviezen."
            )

        if overige_adviezen:
            for advies in overige_adviezen:
                toon_advies(advies)

        else:
            st.info(
                "Er zijn geen aanvullende adviezen naast de waarschuwing hierboven."
            )

        st.caption(
            "Onderwijsprototype. De beslisregels "
            "zijn vereenvoudigde vertalingen van "
            "de kennisbronnen en zijn niet klinisch "
            "gevalideerd. Het NHG-Standpunt "
            "Oncologische zorg wordt als achtergrondbron "
            "gebruikt. De klinische besluitvorming "
            "blijft de verantwoordelijkheid van de huisarts."
        )
