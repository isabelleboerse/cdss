
import streamlit as st


# Kennisbronnen
BRON_NHG = "https://richtlijnen.nhg.org/standaarden/borstkanker"

BRON_ONCOLOGIE = (
    "https://richtlijnen.nhg.org/files/2021-11/"
    "nhg-standpunt_oncologische_zorg.pdf"
)

BRON_THUISARTS = (
    "https://www.thuisarts.nl/borstkanker/"
    "behandeld-voor-borstkanker-welke-controles"
)


def maak_advies(titel, tekst, prioriteit, bronnen):
    return {
        "titel": titel,
        "tekst": tekst,
        "prioriteit": prioriteit,
        "bronnen": bronnen
    }


def beoordeel_klachten(gegevens):
    adviezen = []

    # Beslismoment 1 en 2
    if gegevens["rood_warm_pijnlijk"]:
        adviezen.append(maak_advies(
            "Directe medische beoordeling",
            (
                "De borst is rood, warm en pijnlijk. "
                "Beoordeel direct de klinische situatie, "
                "urgentie en mogelijke oorzaken, "
                "zoals een ontsteking."
            ),
            "hoog",
            [BRON_THUISARTS, BRON_NHG]
        ))

    if gegevens["verdachte_afwijking"]:
        adviezen.append(maak_advies(
            "Verdachte borstafwijking",
            (
                "Er zijn klinische aanwijzingen voor "
                "een mogelijk maligne borstafwijking. "
                "Beoordeel verwijzing naar de mammapoli "
                "of het behandelend mammateam volgens "
                "de NHG-Standaard Borstkanker."
            ),
            "hoog",
            [BRON_NHG]
        ))

    if (gegevens["nieuwe_klachten"]
            and not gegevens["verdachte_afwijking"]):
        adviezen.append(maak_advies(
            "Nieuwe klachten of veranderingen",
            (
                "Voer gerichte anamnese en lichamelijk "
                "onderzoek uit. Beoordeel of aanvullende "
                "diagnostiek of overleg met het mammateam "
                "nodig is. Wacht bij een nieuwe afwijking "
                "niet automatisch op de volgende controle."
            ),
            "middel",
            [BRON_NHG, BRON_THUISARTS]
        ))

    # Beslismoment 3: lichamelijke klachten
    if gegevens["lichamelijke_klachten"]:
        klachten = gegevens["typen_lichamelijk"]

        if "Vermoeidheid" in klachten:
            adviezen.append(maak_advies(
                "Aanhoudende vermoeidheid",
                (
                    "Breng de ernst en invloed op het "
                    "dagelijks functioneren in kaart. "
                    "Beoordeel mogelijke oorzaken en "
                    "bespreek zelfmanagement, belastbaarheid "
                    "en eventuele oncologische revalidatie."
                ),
                "ondersteuning",
                [BRON_ONCOLOGIE]
            ))

        if "Langdurige pijn" in klachten:
            adviezen.append(maak_advies(
                "Langdurige pijn",
                (
                    "Beoordeel de aard, locatie, ernst en "
                    "gevolgen van de pijn. Onderzoek mogelijke "
                    "oorzaken en bespreek passende behandeling "
                    "of gespecialiseerde ondersteuning."
                ),
                "ondersteuning",
                [BRON_ONCOLOGIE]
            ))

        if "Schouderbeperkingen" in klachten:
            adviezen.append(maak_advies(
                "Schouderbeperkingen",
                (
                    "Beoordeel de bewegingsbeperking en "
                    "de invloed op dagelijkse activiteiten. "
                    "Overweeg passende fysiotherapeutische "
                    "begeleiding of oncologische revalidatie."
                ),
                "ondersteuning",
                [BRON_ONCOLOGIE]
            ))

        if "Zwelling van arm of hand" in klachten:
            adviezen.append(maak_advies(
                "Mogelijk lymfoedeem",
                (
                    "Beoordeel de zwelling en mogelijke "
                    "oorzaken. Overweeg bij passend "
                    "lymfoedeem gespecialiseerde "
                    "fysiotherapie of huidtherapie. "
                    "Sluit andere oorzaken niet automatisch uit."
                ),
                "ondersteuning",
                [BRON_NHG, BRON_ONCOLOGIE]
            ))

        if "Concentratie- of geheugenproblemen" in klachten:
            adviezen.append(maak_advies(
                "Cognitieve klachten",
                (
                    "Bespreek concentratie- en "
                    "geheugenproblemen en de invloed "
                    "op het dagelijks functioneren. "
                    "Beoordeel mogelijke oorzaken en "
                    "de behoefte aan aanvullende begeleiding."
                ),
                "ondersteuning",
                [BRON_ONCOLOGIE]
            ))

        if "Slaapproblemen" in klachten:
            adviezen.append(maak_advies(
                "Slaapproblemen",
                (
                    "Breng de aard en duur van de "
                    "slaapproblemen in kaart en beoordeel "
                    "mogelijke samenhang met lichamelijke "
                    "of psychosociale klachten. "
                    "Bespreek passende ondersteuning."
                ),
                "ondersteuning",
                [BRON_ONCOLOGIE]
            ))

        if "Problemen met terugkeer naar werk" in klachten:
            adviezen.append(maak_advies(
                "Werkhervatting",
                (
                    "Bespreek de mogelijkheden en "
                    "belemmeringen bij terugkeer naar werk. "
                    "Overweeg afstemming met de bedrijfsarts "
                    "en passende revalidatie of begeleiding."
                ),
                "ondersteuning",
                [BRON_ONCOLOGIE]
            ))

        if not klachten:
            adviezen.append(maak_advies(
                "Lichamelijke klachten beoordelen",
                (
                    "Breng de lichamelijke klachten en hun "
                    "invloed op het dagelijks functioneren "
                    "verder in kaart. Bespreek welke "
                    "ondersteuning de patiënt nodig heeft."
                ),
                "ondersteuning",
                [BRON_ONCOLOGIE]
            ))

    # Beslismoment 4: psychosociale klachten
    if gegevens["psychosociale_klachten"]:

        klachten = gegevens["typen_psychosociaal"]

        adviezen.append(maak_advies(
            "Psychosociale ondersteuning",
            (
                "Bespreek de aard en ernst van de "
                "psychosociale klachten, de invloed "
                "op het dagelijks functioneren en "
                "de ondersteuningsbehoefte van de patiënt. "
                "Overweeg begeleiding door de huisarts "
                "of POH-GGZ, gespecialiseerde psychosociale "
                "zorg of oncologische revalidatie."
            ),
            "ondersteuning",
            [BRON_ONCOLOGIE]
        ))

        if "Problemen in relaties of sociaal functioneren" in klachten:
            adviezen.append(maak_advies(
                "Sociaal functioneren",
                (
                    "Bespreek gevolgen voor relaties, "
                    "gezin en sociaal functioneren. "
                    "Onderzoek de behoefte aan ondersteuning "
                    "en betrek waar passend het sociale "
                    "netwerk of gespecialiseerde hulp."
                ),
                "ondersteuning",
                [BRON_ONCOLOGIE]
            ))

        if "Behoefte aan extra begeleiding" in klachten:
            adviezen.append(maak_advies(
                "Individueel nazorgplan",
                (
                    "Bespreek of een individueel zorgplan "
                    "wenselijk is. Leg daarin de zorgbehoeften, "
                    "behandeldoelen, betrokken zorgverleners "
                    "en afspraken over verdere begeleiding vast. "
                    "Stem zo nodig af met het oncologisch team."
                ),
                "ondersteuning",
                [BRON_ONCOLOGIE]
            ))

    if not adviezen:
        adviezen.append(maak_advies(
            "Bestaande nazorg voortzetten",
            (
                "Er zijn geen klachten geselecteerd "
                "waarvoor deze beslisboom een aanvullend "
                "advies geeft. Bespreek het bestaande "
                "nazorgplan en blijf alert op veranderingen. "
                "Andere aandoeningen zijn hiermee niet uitgesloten."
            ),
            "algemeen",
            [BRON_NHG, BRON_ONCOLOGIE]
        ))

    volgorde = {
        "hoog": 0,
        "middel": 1,
        "ondersteuning": 2,
        "algemeen": 3
    }

    adviezen.sort(
        key=lambda advies: volgorde[advies["prioriteit"]]
    )

    return adviezen


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


def kennisgedreven_cdss():
    st.header("Kennisgedreven beslisondersteuning")

    st.write(
        "Deze module ondersteunt huisartsen bij "
        "het beoordelen van klachten en zorgbehoeften "
        "van patiënten die borstkanker hebben of "
        "hiervoor behandeld zijn."
    )

    # Beslismoment 1
    st.subheader("Beslismoment 1")
    st.write(
        "**Zijn er nieuwe klachten of veranderingen "
        "aan borst, oksel of litteken?**"
    )

    nieuwe_klachten = st.radio(
        "Nieuwe klachten of veranderingen",
        ["Nee", "Ja"],
        horizontal=True,
        key="nieuwe_klachten"
    ) == "Ja"

    # Beslismoment 2
    st.subheader("Beslismoment 2")
    st.write("**Zijn er acute of verdachte klachten?**")

    acute_klachten = st.radio(
        "Selecteer de bevinding:",
        [
            "Nee, geen acute of verdachte klachten",
            "Ja, rode, warme en pijnlijke borst",
            "Ja, klinisch verdachte borstafwijking",
            "Ja, beide bovenstaande klachten"
        ],
        index=0,
        key="acute_klachten"
    )

    rood_warm_pijnlijk = acute_klachten in [
        "Ja, rode, warme en pijnlijke borst",
        "Ja, beide bovenstaande klachten"
    ]

    verdachte_afwijking = acute_klachten in [
        "Ja, klinisch verdachte borstafwijking",
        "Ja, beide bovenstaande klachten"
    ]

    # Waarschuwing onmiddellijk zichtbaar
    if rood_warm_pijnlijk:
        st.error(
            "DIRECTE MEDISCHE BEOORDELING NODIG.\n\n"
            "Beoordeel de urgentie en mogelijke "
            "oorzaken van een rode, warme en "
            "pijnlijke borst."
        )

        st.markdown(
            f"[Bekijk de informatie over controles "
            f"na borstkanker]({BRON_THUISARTS})"
        )

    if verdachte_afwijking:
        st.warning(
            "VERDACHTE BORSTAFWIJKING.\n\n"
            "Beoordeel de noodzaak van verwijzing "
            "naar de mammapoli of het mammateam "
            "volgens de NHG-Standaard."
        )

        st.markdown(
            f"[Bekijk de NHG-Standaard "
            f"Borstkanker]({BRON_NHG})"
        )

    # Beslismoment 3
    st.subheader("Beslismoment 3")
    st.write(
        "**Heeft de patiënt aanhoudende "
        "lichamelijke klachten na de behandeling?**"
    )

    lichamelijke_klachten = st.radio(
        "Aanhoudende lichamelijke klachten",
        ["Nee", "Ja"],
        horizontal=True,
        key="lichamelijke_klachten"
    ) == "Ja"

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
                "Problemen met terugkeer naar werk"
            ],
            key="typen_lichamelijk"
        )

    # Beslismoment 4
    st.subheader("Beslismoment 4")
    st.write(
        "**Heeft de patiënt aanhoudende "
        "psychosociale klachten na de behandeling?**"
    )

    psychosociale_klachten = st.radio(
        "Psychosociale klachten",
        ["Nee", "Ja"],
        horizontal=True,
        key="psychosociale_klachten"
    ) == "Ja"

    typen_psychosociaal = []

    if psychosociale_klachten:
        typen_psychosociaal = st.multiselect(
            "Welke psychosociale klachten of behoeften?",
            [
                "Angst of onzekerheid",
                "Somberheid",
                "Problemen met verwerking van de ziekte",
                "Problemen in relaties of sociaal functioneren",
                "Behoefte aan extra begeleiding"
            ],
            key="typen_psychosociaal"
        )

    st.divider()

    if st.button(
        "Genereer richtlijnadvies",
        type="primary",
        key="genereer_advies"
    ):

        gegevens = {
            "nieuwe_klachten": nieuwe_klachten,
            "rood_warm_pijnlijk": rood_warm_pijnlijk,
            "verdachte_afwijking": verdachte_afwijking,
            "lichamelijke_klachten": lichamelijke_klachten,
            "typen_lichamelijk": typen_lichamelijk,
            "psychosociale_klachten": psychosociale_klachten,
            "typen_psychosociaal": typen_psychosociaal
        }

        adviezen = beoordeel_klachten(gegevens)

        st.subheader("Richtlijngebaseerde adviezen")

        for advies in adviezen:
            toon_advies(advies)

        st.caption(
            "Onderwijsprototype. De beslisregels "
            "zijn vereenvoudigde vertalingen van "
            "de kennisbronnen en zijn niet klinisch "
            "gevalideerd. Het NHG-Standpunt "
            "Oncologische zorg uit 2014 wordt "
            "uitsluitend als historische achtergrondbron "
            "gebruikt. De klinische besluitvorming "
            "blijft de verantwoordelijkheid van de huisarts."
        )
