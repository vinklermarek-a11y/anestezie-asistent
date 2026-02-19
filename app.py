import streamlit as st

st.set_page_config(page_title="Anesteziologický asistent", layout="centered")

# --- CSS STYLOVÁNÍ ---
st.markdown("""
    <style>
    h1 { text-align: center; color: #004a99; margin-bottom: 5px; }
    .drug-card {
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        border-left: 6px solid #ccc;
        background-color: #f9f9f9;
        color: #1f1f1f;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .border-red { border-left-color: #d93025; background-color: #fff0f0; }
    .border-green { border-left-color: #188038; background-color: #e6f4ea; }
    .border-blue { border-left-color: #1967d2; background-color: #e8f0fe; }
    .border-yellow { border-left-color: #f9ab00; background-color: #fef7e0; }
    .card-title { font-weight: 700; font-size: 1.15em; display: block; margin-bottom: 4px; }
    .card-generic { font-weight: 400; color: #555; font-size: 0.85em; }
    .card-rec { font-weight: 700; display: block; margin-top: 2px; font-size: 1.05em; }
    .card-info { font-size: 0.95em; font-style: italic; opacity: 0.9; display: block; margin-top: 4px; }
    </style>
    """, unsafe_allow_html=True)

# --- HLAVIČKA ---
st.markdown("<h1>🩺 Anesteziologický asistent</h1>", unsafe_allow_html=True)
st.caption("Zdroj: Interní směrnice vč. nového dia managementu", unsafe_allow_html=True)
st.write("---")

# --- 1. VSTUP ---
st.subheader("Vložte chronickou medikaci pacienta:")
med_text = st.text_area("", height=200, placeholder="Např.: Prestarium, Eliquis, Metformin, Ozempic, Bydureon...").lower()
st.write("")

# --- 2. MEGA DATABÁZE LÉČIV ---
# Rozděleno na kratší řádky pro bezchybné zkopírování
db = [
    # === HYPERTENZE - KOMBINOVANÉ PREPARÁTY ===
    {
        "brands": ["accuzide", "amesos", "cazacombi", "egiramlon", "furorese", "hcht", "ifirmacombi", "lodoz", "loradur", "lozap h"], 
        "gen": "Kombinace (ACEI/Sartan/Diuretikum)", "grp": "Kombinace", "act": "VYSADIT V DEN VÝKONU", "info": "Obsahuje ACEI, Sartan nebo Diuretikum.", "col": "red"
    },
    {
        "brands": ["moduretic", "rasilez hct", "rhefluin", "stadapres", "tarka", "tonarsa", "triasyn", "tritazide", "valsacombi", "vidonorm"], 
        "gen": "Kombinace (ACEI/Sartan/Diuretikum)", "grp": "Kombinace", "act": "VYSADIT V DEN VÝKONU", "info": "Obsahuje ACEI, Sartan nebo Diuretikum.", "col": "red"
    },
    {
        "brands": ["triplixam", "tezefort", "twynsta", "tonarssa", "lorista h", "prestance", "lercaprel", "tonanda"], 
        "gen": "Kombinace (ACEI/Sartan/Diuretikum)", "grp": "Kombinace", "act": "VYSADIT V DEN VÝKONU", "info": "Obsahuje ACEI, Sartan nebo Diuretikum.", "col": "red"
    },

    # === HYPERTENZE - ACE INHIBITORY A SARTANY ===
    {
        "brands": ["accupro", "acesial", "almesa", "amprilan", "apo-enapril", "apo-perindo", "berlipril", "capoten", "cazaprol", "coverex"], 
        "gen": "ACE Inhibitor / Sartan", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypotenze. Zvážit ponechání jen u srdečního selhání.", "col": "red"
    },
    {
        "brands": ["dapril", "diroton", "ednyt", "enalapril", "enap", "enapril", "fosinogen", "fosinopril", "gleperil", "gopten"], 
        "gen": "ACE Inhibitor / Sartan", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypotenze. Zvážit ponechání jen u srdečního selhání.", "col": "red"
    },
    {
        "brands": ["hartil", "inhibace", "lisinopril", "medoram", "miril", "moex", "monace", "monopril", "perinalon", "perindopril"], 
        "gen": "ACE Inhibitor / Sartan", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypotenze. Zvážit ponechání jen u srdečního selhání.", "col": "red"
    },
    {
        "brands": ["perinpra", "pinbarix", "piramil", "prenesa", "prenewel", "prestarium", "pricoron", "ramicard", "ramigamma", "ramil"], 
        "gen": "ACE Inhibitor / Sartan", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypotenze. Zvážit ponechání jen u srdečního selhání.", "col": "red"
    },
    {
        "brands": ["ramipril", "rasilez", "renpres", "tanap", "tanatril", "tensiomin", "tritace", "vidotin", "arionex", "blessin"], 
        "gen": "ACE Inhibitor / Sartan", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypotenze. Zvážit ponechání jen u srdečního selhání.", "col": "red"
    },
    {
        "brands": ["canocord", "carzap", "giovax", "ifirmasta", "irbesartan", "kylotan", "lakea", "lorista", "losagen", "losartan"], 
        "gen": "ACE Inhibitor / Sartan", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypotenze. Zvážit ponechání jen u srdečního selhání.", "col": "red"
    },
    {
        "brands": ["losartic", "lozap", "micardis", "nopretens", "sangona", "telmark", "telmisartan", "teveten", "tezeo", "tolura"], 
        "gen": "ACE Inhibitor / Sartan", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypotenze. Zvážit ponechání jen u srdečního selhání.", "col": "red"
    },
    {
        "brands": ["valsacor", "valsap", "zanacodar", "caramlo", "entresto"], 
        "gen": "ACE Inhibitor / Sartan (ARNI)", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypotenze. Zvážit ponechání jen u srdečního selhání.", "col": "red"
    },
