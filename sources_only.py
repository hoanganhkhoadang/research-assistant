import warnings

warnings.filterwarnings("ignore", category=Warning)
import re
from urllib.parse import quote

import requests


# -------------------------
# Normalize human questions
# -------------------------
def normalize_topic(topic: str) -> str:
    topic = topic.lower()
    topic = re.sub(
        r"^(who is|what is|how does|why does|tell me about)\s+",
        "",
        topic
    )
    return topic.strip()

# -------------------------
# Reliable Institutional Sources
# -------------------------
def institutional_sources(topic):
    t = topic.lower()
    sources = []

    # Racism, discrimination, identity
    if any(w in t for w in ["racism", "race", "racial", "segregation", "apartheid", "discrimination"]):
        sources.extend([
            {"title": "UN CERD Committee Reports", "url": "https://www.ohchr.org/en/treaty-bodies/cerd"},
            {"title": "US DOJ Civil Rights Cases", "url": "https://www.justice.gov/crt/case-summaries"},
            {"title": "APA Race Guidelines PDF", "url": "https://www.apa.org/about/policy/guidelines-race-ethnicity.pdf"}
        ])

    # Inequality & economics
    if any(w in t for w in ["inequality", "poverty", "economy", "class"]):
        sources.extend([
            {"title": "World Bank Gini Data", "url": "https://data.worldbank.org/indicator/SI.POV.GINI"},
            {"title": "OECD Inequality Stats", "url": "https://stats.oecd.org/Index.aspx?DataSetCode=IDD"},
            {"title": "UNDP Inequality HDI", "url": "https://hdr.undp.org/data-center/inequality-adjusted-human-development-index"}
        ])

    # Migration & refugees
    if any(w in t for w in ["migration", "migrate", "immigration", "emigration", "refugee", "asylum", "border", "displacement"]):
        sources.extend([
            {"title": "UNHCR Refugee Data", "url": "https://www.unhcr.org/refugee-statistics/"},
            {"title": "IOM Migration Report 2024", "url": "https://worldmigrationreport.iom.int/"},
            {"title": "UN Migrant Stock Data", "url": "https://www.un.org/development/desa/pd/content/international-migrant-stock"}
        ])

    # Politics & governance
    if any(w in t for w in ["government", "policy", "politics", "democracy"]):
        sources.extend([
            {"title": "Freedom House 2025 Report", "url": "https://freedomhouse.org/report/freedom-world"},
            {"title": "World Bank Governance Data", "url": "https://www.worldbank.org/en/publication/worldwide-governance-indicators"},
            {"title": "V-Dem Democracy Dataset", "url": "https://v-dem.net/"}
        ])

    # Climate & environment
    if any(w in t for w in ["climate", "climate change", "climate crisis", "global warming", "environment", "carbon", "pollution"]):
        sources.extend([
            {"title": "IPCC AR6 Climate Report", "url": "https://www.ipcc.ch/report/ar6/syr/"},
            {"title": "World Bank Climate Data", "url": "https://climateknowledgeportal.worldbank.org/"},
            {"title": "UNEP Emissions Gap Report", "url": "https://www.unep.org/emissions-gap-report-2024"}
        ])

    # -------------------------
    # POLLUTION - NEW DEDICATED CATEGORY
    if any(w in t for w in ["pollution", "air pollution", "water pollution", "soil pollution", "pm2.5"]):
        sources.extend([
            {"title": "World Bank PM2.5 Pollution Data", "url": "https://data.worldbank.org/indicator/EN.ATM.PM25.MC.M3"},
            {"title": "WHO Air Quality Database", "url": "https://www.who.int/data/gho/data/themes/air-pollution"},
            {"title": "World Bank Pollution Management", "url": "https://ieg.worldbankgroup.org/evaluations/pollution"}
        ])

    # Population & demographics
    if any(w in t for w in ["population", "mortality", "fertility", "birth", "death", "aging"]):
        sources.extend([
            {"title": "UN Population Prospects CSV", "url": "https://population.un.org/wpp/Download/Standard/CSV_WPP/"},
            {"title": "World Bank Birth Rates", "url": "https://data.worldbank.org/indicator/SP.DYN.CBRT.IN"},
            {"title": "World Bank Death Rates", "url": "https://data.worldbank.org/indicator/SP.DYN.CDRT.IN"}
        ])

    # War & genocide
    if any(w in t for w in ["war", "genocide", "holocaust"]):
        sources.extend([
            {"title": "USHMM Document Archive", "url": "https://www.ushmm.org/online/hsv/source_view.php"},
            {"title": "Uppsala Conflict Database", "url": "https://ucdp.uu.se/downloads/index.html"},
            {"title": "UN Genocide Documents", "url": "https://www.un.org/en/genocideprevention/documents"}
        ])

    return sources

# -------------------------
# Academic Sources
# -------------------------

def academic_sources(topic):
    t = topic.lower()
    sources = []

    mapping = {
        # ANCIENT CIVILIZATIONS
        "ancient": [
            {"title": "Perseus Digital Library", "url": "http://www.perseus.tufts.edu/hopper/"},
            {"title": "Fordham Ancient Texts", "url": "https://sourcebooks.fordham.edu/ancient/asbook.asp"}
        ],
        "sumer": [
            {"title": "Electronic Text Corpus Sumerian", "url": "https://etcsl.orinst.ox.ac.uk/"},
            {"title": "CDLI Cuneiform Digital Library", "url": "https://cdli.ucla.edu/"}
        ],
        "1700s": [
            {"title": "Enlightenment Documents - Yale Avalon", "url": "https://avalon.law.yale.edu/subject_menus/18th.asp"},
            {"title": "French Revolution Primary Sources", "url": "https://revolution.chnm.org/"}
        ],
        "world war": [
            {"title": "US Army WWII Records", "url": "https://www.history.army.mil/html/reference/wwII/index.html"},
            {"title": "Imperial War Museum WWII", "url": "https://www.iwm.org.uk/history/second-world-war"}
        ],
        "cold war": [
            {"title": "Wilson Cold War Archive", "url": "https://digitalarchive.wilsoncenter.org/"},
            {"title": "Cold War History Project", "url": "https://www.wilsoncenter.org/program/cold-war-international-history-project"}
        ],
        "gulf war": [
            {"title": "Gulf War Documents - National Security Archive", "url": "https://nsarchive2.gwu.edu/project/gulf-war-files"},
            {"title": "British National Archives Gulf War", "url": "https://www.nationalarchives.gov.uk/education/resources/gulf-war/"},
            {"title": "US Army Gulf War Official History", "url": "https://history.army.mil/html/bookshelves/collect/72-29.html"}
        ]
    }

    for key, items in mapping.items():
        if key in t:
            sources.extend(items)

    return sources



# -------------------------
# Historical Figures
# -------------------------
def historical_figures(topic):
    t = topic.lower()
    figures = []

    mapping = {
        "racism": [
            {"title": "MLK Papers Project", "url": "https://kinginstitute.stanford.edu/papers"},
            {"title": "Du Bois Papers Edition", "url": "https://credo.library.harvard.edu/view/fulltext?doc=DuBois"}
        ],
        "inequality": [
            {"title": "Marx Collected Works", "url": "https://www.marxists.org/archive/marx/works/"},
            {"title": "Weber Economy Society", "url": "https://www.maxweberstiftung.de/en"}
        ],
        "psychology": [
            {"title": "Freud Complete Works", "url": "https://www.freud.org.uk/learn-discover/freud-online/"},
            {"title": "Jung Collected Works", "url": "https://press.princeton.edu/series/collected-works-of-c-g-jung"}
        ],
        "migration": [
            {"title": "Hannah Arendt Papers", "url": "https://hac.bard.edu/"}
        ]
    }

    for key, people in mapping.items():
        if key in t:
            figures.extend(people)

    return figures

# -------------------------
# Collect ALL sources
# -------------------------
def collect_sources(topic):
    sources = []
    sources.extend(institutional_sources(topic))
    sources.extend(academic_sources(topic))
    sources.extend(historical_figures(topic))

    # Remove duplicates
    seen = set()
    unique = []
    for s in sources:
        if s["url"] not in seen:
            seen.add(s["url"])
            unique.append(s)

    return unique

# -------------------------
# CLI Version
# -------------------------
if __name__ == "__main__":
    print("🌍 Reliable Research Sources - SPECIFIC LINKS")
    print("Background info only, no direct questions")
    print("-" * 70)

    while True:
        topic = input("\nEnter research topic (or 'exit'): ").strip()

        if topic.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break

        if not topic:
            continue

        results = collect_sources(topic)

        if not results:
            print("❌ No sources found. Try: rome, world war 2, cold war, birth, climate, migration")
        else:
            print(f"\n✅ {len(results)} RELIABLE SOURCES for '{topic.title()}':\n")
            for i, s in enumerate(results, 1):
                print(f"{i}. {s['title']}")
                print(f"   {s['url']}\n")

