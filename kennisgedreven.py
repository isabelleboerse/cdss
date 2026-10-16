
import streamlit as st


BRON_NHG = (
    "https://www.henw.org/system/files/download/"
    "HW59-556.pdf"
)

BRON_NHG_ONDERZOEK = (
    "https://www.nhg.org/wp-content/uploads/2022/12/"
    "Werkbeschrijving-Mammae-lichamelijk-onderzoek_2022.pdf"
)

BRON_THUISARTS_CONTROLES = (
    "https://www.thuisarts.nl/borstkanker/"
    "behandeld-voor-borstkanker-welke-controles"
)

BRON_THUISARTS_KLACHTEN = (
    "https://www.thuisarts.nl/borstkanker/"
    "borstkanker-gehad-omgaan-met-klachten"
)


def maak_advies(titel, tekst, prioriteit, bronnen):
    return {
        "titel": titel,
        "tekst": tekst,
        "prioriteit": prioriteit,
        "bronnen": bronnen
    }


def beoordeel_klachten(gegevens):
    """
    Kennisgedreven regels op basis van ingevoerde
    klinische gegevens.

    Dit is een beslisondersteunend onderwijsprototype
    en geen volledige klinische triage.
    """

    adviezen = []

    nieuwe_klachten = gegevens["nieuwe_klachten"]
    rood_warm_pijnlijk = gegevens["rood_warm_pijnlijk"]
    verdachte_afwijking = gegevens["verdachte_afwijking"]
    lichamelijke_klachten = gegevens["lichamelijke_klachten"]
    psychosociale_klachten = gegevens["psychosociale_klachten"]

    
    # BESLISMOMENT 1 + 2
    # Nieuwe veranderingen en rood/warm/pijnlijk
    

    if nieuwe_klachten:

        if rood_warm_pijnlijk:
            adviezen.append(maak_advies(
                "Directe medische beoordeling",
                (
                    "Er is een nieuwe klacht waarbij de borst "
                    "rood, warm en pijnlijk is. Beoordeel "
                    "direct de klinische situatie, de urgentie "
                    "en mogelijke oorzaken zoals een ontsteking. "
                    "Bepaal op basis van de bevindingen of "
                    "aanvullend onderzoek of overleg nodig is."
                ),
                "hoog",
                [BRON_THUISARTS_CONTROLES, BRON_NHG]
            ))

        if verdachte_afwijking:
            adviezen.append(maak_advies(
                "Verdachte borstafwijking: verwijzing beoordelen",
                (
                    "Er zijn klinische aanwijzingen voor een "
                    "mogelijk maligne borstafwijking. Volgens "
                    "de NHG-Standaard is verwijzing naar de "
                    "mammapoli aangewezen bij klinische "
                    "aanwijzingen voor maligniteit. "
                    "Stem bij eerdere borstkanker af met het "
                    "bestaande oncologische behandelteam."
                ),
                "hoog",
                [BRON_NHG, BRON_NHG_ONDERZOEK]
            ))

        if not rood_warm_pijnlijk and not verdachte_afwijking:
            adviezen.append(maak_advies(
                "Nieuwe afwijking: verdere beoordeling",
                (
                    "De patiënt heeft nieuwe klachten of "
                    "veranderingen aan de borst, oksel of "
                    "het litteken. Voer gerichte anamnese "
                    "en lichamelijk borstonderzoek uit en "
                    "beoordeel of aanvullende diagnostiek "
                    "of overleg met het mammateam nodig is. "
                    "Wacht niet automatisch op de volgende "
                    "geplande controle."
                ),
                "middel",
                [
                    BRON_NHG,
                    BRON_NHG_ONDERZOEK,
                    BRON_THUISARTS_CONTROLES
                ]
            ))

    # Losse signalering: ook relevant als er niet
    # eerder 'nieuwe klachten' is aangevinkt.
    elif rood_warm_pijnlijk:
        adviezen.append(maak_advies(
            "Directe medische beoordeling",
            (
                "Een rode, warme en pijnlijke borst vraagt "
                "om directe klinische beoordeling. "
                "Beoordeel de urgentie en mogelijke oorzaken."
            ),
            "hoog",
            [BRON_THUISARTS_CONTROLES, BRON_NHG]
        ))

    elif verdachte_afwijking:
        adviezen.append(maak_advies(
            "Verdachte borstafwijking",
            (
                "Er zijn klinische aanwijzingen voor een "
                "verdachte borstafwijking. Beoordeel "
                "verwijzing naar de mammapoli volgens "
                "de NHG-Standaard en de afspraken met "
                "het behandelteam."
            ),
            "hoog",
            [BRON_NHG]
        ))

    
    # BESLISMOMENT 3
    # Aanhoudende lichamelijke klachten
    

    if lichamelijke_klachten:

        typen = gegevens["typen_lichamelijk"]

        if "Vermoeidheid" in typen:
            adviezen.append(maak_advies(
                "Aanhoudende vermoeidheid",
                (
                    "Bespreek de invloed van vermoeidheid "
                    "op het dagelijks functioneren. "
                    "Beoordeel mogelijke oorzaken en "
                    "overweeg passende begeleiding, "
                    "zoals oefentherapie, ergotherapie "
                    "of psychologische ondersteuning."
                ),
                "ondersteuning",
                [BRON_THUISARTS_KLACHTEN]
            ))

        if "Schouderbeperkingen" in typen:
            adviezen.append(maak_advies(
                "Schouderklachten",
                (
                    "Beoordeel pijn en beperkingen van de "
                    "schouderfunctie. Bespreek passende "
                    "oefeningen en overweeg begeleiding "
                    "door een fysiotherapeut."
                ),
                "ondersteuning",
                [BRON_THUISARTS_KLACHTEN]
            ))

        if "Langdurige pijn" in typen:
            adviezen.append(maak_advies(
                "Langdurige pijn",
                (
                    "Breng de aard, ernst en gevolgen "
                    "van de pijn in kaart. Beoordeel "
                    "mogelijke oorzaken en bespreek "
                    "passende pijnbehandeling of "
                    "eventueel overleg met een pijnpoli."
                ),
                "ondersteuning",
                [BRON_THUISARTS_KLACHTEN]
            ))

        if "Zwelling van arm of hand" in typen:
            adviezen.append(maak_advies(
                "Mogelijk lymfoedeem",
                (
                    "Beoordeel de zwelling en mogelijke "
                    "oorzaken. Als lymfoedeem passend is "
                    "bij het klinisch beeld, kan "
                    "begeleiding door een gespecialiseerde "
                    "fysiotherapeut of huidtherapeut "
                    "worden overwogen."
                ),
                "ondersteuning",
                [BRON_THUISARTS_KLACHTEN]
            ))

        if not typen:
            adviezen.append(maak_advies(
                "Lichamelijke klachten",
                (
                    "De patiënt heeft aanhoudende "
                    "lichamelijke klachten. Specificeer "
                    "de klachten en bespreek de invloed "
                    "op het dagelijks functioneren."
                ),
                "ondersteuning",
                [BRON_THUISARTS_KLACHTEN]
            ))

    
    # BESLISMOMENT 4
    # Aanhoudende psychosociale klachten
    

    if psychosociale_klachten:
        adviezen.append(maak_advies(
            "Psychosociale ondersteuning",
            (
                "Bespreek de aard en ernst van de "
                "psychosociale klachten en hun invloed "
                "op het dagelijks leven. Bespreek "
                "persoonlijke behoeften en overweeg "
                "ondersteuning via de POH-GGZ, "
                "een psycholoog of passende "
                "oncologische psychosociale zorg."
            ),
            "ondersteuning",
            [
                BRON_THUISARTS_KLACHTEN,
                BRON_THUISARTS_CONTROLES
            ]
        ))

    if not adviezen:
        adviezen.append(maak_advies(
            "Bestaande nazorg voortzetten",
            (
                "Op basis van de geselecteerde "
                "klachten is geen aanvullende regel "
                "geactiveerd. Bespreek het bestaande "
                "nazorgplan en blijf aandacht houden "
                "voor nieuwe klachten en zorgbehoeften. "
                "Dit sluit andere aandoeningen niet uit."
            ),
            "algemeen",
            [BRON_THUISARTS_CONTROLES]
        ))

    # Hoge prioriteit eerst
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
        "Beoordeel actuele klachten en gevolgen van "
        "borstkanker of de behandeling. De adviezen "
        "zijn gebaseerd op de NHG-Standaard Borstkanker "
        "en aanvullende Thuisarts-informatie."
    )

    with st.form("kennisgedreven_formulier"):

        st.subheader("Beslismoment 1")
        st.write(
            "**Zijn er nieuwe klachten of veranderingen "
            "aan borst, oksel of litteken?**"
        )

        nieuwe_klachten = st.radio(
            "Nieuwe klachten of veranderingen",
            ["Nee", "Ja"],
            horizontal=True
        ) == "Ja"

        st.subheader("Beslismoment 2")
        st.write(
            "**Zijn er alarmsignalen of verdachte "
            "bevindingen?**"
        )

        rood_warm_pijnlijk = st.checkbox(
            "De borst is rood, warm en pijnlijk"
        )

        verdachte_afwijking = st.checkbox(
            "Klinisch verdachte afwijking, zoals een "
            "verdachte massa, huid- of tepelintrekking "
            "of verdachte regionale lymfeklieren"
        )

        st.subheader("Beslismoment 3")
        st.write(
            "**Heeft de patiënt aanhoudende "
            "lichamelijke klachten na behandeling?**"
        )

        lichamelijke_klachten = st.radio(
            "Aanhoudende lichamelijke klachten",
            ["Nee", "Ja"],
            horizontal=True
        ) == "Ja"

        typen_lichamelijk = st.multiselect(
            "Welke lichamelijke klachten?",
            [
                "Vermoeidheid",
                "Schouderbeperkingen",
                "Langdurige pijn",
                "Zwelling van arm of hand"
            ]
        )

        st.subheader("Beslismoment 4")
        st.write(
            "**Heeft de patiënt aanhoudende "
            "psychosociale klachten na behandeling?**"
        )

        psychosociale_klachten = st.radio(
            "Psychosociale klachten",
            ["Nee", "Ja"],
            horizontal=True
        ) == "Ja"

        versturen = st.form_submit_button(
            "Genereer richtlijnadvies",
            type="primary"
        )

    if versturen:
        gegevens = {
            "nieuwe_klachten": nieuwe_klachten,
            "rood_warm_pijnlijk": rood_warm_pijnlijk,
            "verdachte_afwijking": verdachte_afwijking,
            "lichamelijke_klachten": (
                lichamelijke_klachten or bool(typen_lichamelijk)
            ),
            "typen_lichamelijk": typen_lichamelijk,
            "psychosociale_klachten": psychosociale_klachten
        }

        adviezen = beoordeel_klachten(gegevens)

        st.divider()
        st.subheader("Advies voor de huisarts")

        for advies in adviezen:
            toon_advies(advies)

        st.caption(
            "Deze module is een onderwijsprototype. "
            "De adviezen zijn vereenvoudigde "
            "richtlijnvertalingen en zijn niet volledig "
            "klinisch gevalideerd. De huisarts behoudt "
            "de verantwoordelijkheid voor diagnostiek, "
            "urgentie, verwijzing en behandeling."
        )


if __name__ == "__main__":
    kennisgedreven_cdss()
