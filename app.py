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
st.caption("Zdroj: Interní směrnice | Slovník antihypertenziv integrován", unsafe_allow_html=True)
st.write("---")

# --- 1. VSTUP ---
st.subheader("Vložte chronickou medikaci pacienta:")
med_text = st.text_area("", height=200, 
                       placeholder="Např.: Prestarium, Eliquis 5mg, Metformin, Euthyrox...").lower()

st.write("")

# --- 2. MEGA DATABÁZE LÉČIV (Pravidla pouze dle DOCX směrnice) ---
db = [
    # === HYPERTENZE - KOMBINOVANÉ PREPARÁTY (ACEI/SARTAN/DIURETIKUM) ===
    {"brands": ["accuzide", "amesos", "cazacombi", "egiramlon", "furorese", "hcht", "ifirmacombi", "lodoz", "loradur", "lozap h", "moduretic", "rasilez hct", "rhefluin", "stadapres", "tarka", "tonarsa", "triasyn", "tritazide", "valsacombi", "vidonorm", "triplixam", "tezefort", "twynsta", "tonarssa", "lorista h", "prestance", "lercaprel", "tonanda"], "gen": "Kombinace (ACEI/Sartan/Diuretikum)", "grp": "Kombinace", "act": "VYSADIT V DEN VÝKONU", "info": "Obsahuje ACEI, Sartan nebo Diuretikum. Zvážit ponechání u srdečního selhání.", "col": "red"},

    # === HYPERTENZE - ACE INHIBITORY A SARTANY ===
    {"brands": ["accupro", "acesial", "almesa", "amprilan", "apo-enapril", "apo-perindo", "berlipril", "capoten", "cazaprol", "coverex", "dapril", "diroton", "ednyt", "enalapril", "enap", "enapril", "fosinogen", "fosinopril", "gleperil", "gopten", "hartil", "inhibace", "lisinopril", "medoram", "miril", "moex", "monace", "monopril", "perinalon", "perindopril", "perinpra", "pinbarix", "piramil", "prenesa", "prenewel", "prestarium", "pricoron", "ramicard", "ramigamma", "ramil", "ramipril", "rasilez", "renpres", "tanap", "tanatril", "tensiomin", "tritace", "vidotin", "arionex", "blessin", "canocord", "carzap", "giovax", "ifirmasta", "irbesartan", "kylotan", "lakea", "lorista", "losagen", "losartan", "losartic", "lozap", "micardis", "nopretens", "sangona", "telmark", "telmisartan", "teveten", "tezeo", "tolura", "valsacor", "valsap", "zanacodar", "caramlo", "entresto"], "gen": "ACE Inhibitor / Sartan (ARNI)", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypotenze. Zvážit ponechání jen u srdečního selhání nebo špatně korigovatelné hypertenze.", "col": "red"},

    # === HYPERTENZE - DIURETIKA ===
    {"brands": ["amiclaran", "amicloton", "apo-a1milzide", "furon", "hypotylin", "indap", "indapamid", "verospiron", "hydrochlorothiazid"], "gen": "Diuretikum", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypovolemie. Zvážit ponechání u srdečního selhání.", "col": "red"},

    # === HYPERTENZE - BETA BLOKÁTORY (Vč. kombinovaných jako Carvedilol) ===
    {"brands": ["acecor", "obsidan", "apo-acebutol", "pindol", "apo-metopro", "propranolol", "apo-nadol", "rivocor", "atehexal", "sandonorm", "atenobene", "atenol", "sectral", "atenolol", "sobycir", "betaloc", "sotahexal", "betamed", "tenoloc", "betasyn", "tenoretic", "betaxa", "tenormin", "bisocard", "trimepranol", "bisogamma", "tyrez", "bisoprolol", "vasocardin", "brevibloc", "visken", "carvesan", "catenol", "bloxazoc", "celectol", "betaxolol", "combiso", "concor", "corotenol", "corvitol", "egilok", "emzok", "lokren", "logimax", "metoprolol", "nebilet", "nebivolol", "apo-carve", "atram", "carvediol", "coreton", "coryol", "dilatre", "dilatrend", "taliton", "trandate"], "gen": "Beta-blokátor", "grp": "Kardio", "act": "PONECHAT", "info": "Kardioprotekce.", "col": "green"},

    # === HYPERTENZE - BLOKÁTORY CA KANÁLŮ (BKK) ===
    {"brands": ["adalat", "afiten", "agen", "amilostad", "amlator", "amlodipin", "amlop", "amloratio", "amlozek", "apo-amlo", "ardifen", "auronal", "caduet", "cardilopin", "cinarizin", "cordafen", "cordipin", "corinfar", "diacordin", "diltan", "felodipin", "hipres", "isoptin", "kapidin", "lacipil", "lekoptin", "lomir", "lusopress", "nifedipin", "nimotop", "nitrepress", "nitresan", "nitresdipin", "normodipine", "norvasc", "orcal", "plendil", "presid", "recotens", "sponit", "syocor", "tensigal", "torrela", "unipres", "vasexten", "verahexal", "verepamil", "verogalid", "zorem"], "gen": "Blokátor Ca kanálů", "grp": "Kardio", "act": "PONECHAT", "info": "-", "col": "green"},

    # === HYPERTENZE - CENTRÁLNÍ A ALFA BLOKÁTORY ===
    {"brands": ["cynt", "dopegyt", "moxogamma", "moxonidin", "moxostad", "rilmenidin", "tenaxum", "doxazosin", "ebrantil", "hytrin", "kamiren", "zoxon", "urapidil", "labetelol"], "gen": "Centrální / Alfa blokátory", "grp": "Kardio", "act": "PONECHAT", "info": "-", "col": "green"},
    
    # === HYPOLIPIDEMIKA ===
    {"brands": ["ezetrol", "ezetimib", "lipanthyl", "fenofibrat"], "gen": "Fibráty / Ezetrol", "grp": "Hypolipidemika (Nestatinová)", "act": "VYSADIT V DEN VÝKONU", "info": "-", "col": "red"},
    {"brands": ["atorvastatin", "sorvasta", "tulip", "rosuvastatin", "torvacard", "atoris", "sortis"], "gen": "Statin", "grp": "Hypolipidemika", "act": "PONECHAT", "info": "-", "col": "green"},

    # === ANTIARYTMIKA / NITRÁTY ===
    {"brands": ["cordarone", "sedacoron", "amiodaron", "ritmonorm", "dig
