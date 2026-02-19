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
st.caption("Verze: Čistá farmakologie | Interní směrnice", unsafe_allow_html=True)
st.write("---")

# --- 1. VSTUP ---
st.subheader("Vložte chronickou medikaci pacienta:")
med_text = st.text_area("", height=200, 
                       placeholder="Např.: Triplixam 10mg, Eliquis 5mg, Metformin, Euthyrox...").lower()

st.write("")

# --- 2. DATABÁZE LÉČIV ---
db = [
    # === RESPIRAČNÍ ===
    {"brands": ["ventolin", "salbutamol", "buventol", "ecosal"], "gen": "Salbutamol (SABA)", "grp": "Inhalace", "act": "PONECHAT", "info": "Ráno i před sál prevence spasmu.", "col": "green"},
    {"brands": ["berodual", "ipratropium", "atrovent"], "gen": "Fenoterol/Ipratropium", "grp": "Inhalace", "act": "PONECHAT", "info": "Nevysazovat.", "col": "green"},
    {"brands": ["spiriva", "braltus", "biskair"], "gen": "Tiotropium (LAMA)", "grp": "Inhalace", "act": "PONECHAT", "info": "Udržet bronchodilataci.", "col": "green"},
    {"brands": ["seretide", "symbicort", "combair", "foster", "duoresp", "salmex", "trixeo", "trelegy"], "gen": "ICS/LABA/LAMA", "grp": "Inhalace (Kombinace)", "act": "PONECHAT", "info": "Nevysazovat! Posílit dávku (více vdechů).", "col": "green"},
    {"brands": ["euphyllin", "tezeo", "theoplus"], "gen": "Teofylin", "grp": "Methylxanthiny", "act": "PONECHAT", "info": "-", "col": "green"},

    # === ENDOKRINOLOGIE & DIABETES ===
    {"brands": ["euthyrox", "letrox", "thyrozol", "jodid", "eutyrox"], "gen": "Levothyroxin", "grp": "Štítná žláza", "act": "PONECHAT", "info": "Substituce se nepřerušuje.", "col": "green"},
    {"brands": ["metformin", "stadamet", "siofor", "glucophage", "mulado"], "gen": "Metformin", "grp": "Antidiabetikum", "act": "VYSADIT 48H", "info": "Riziko laktátové acidózy. ⚠️ Pozor: Eliminaci léku může ovlivňovat funkce ledvin!", "col": "red"},
    {"brands": ["jardiance", "forxiga", "invokana", "synjardy"], "gen": "Gliflozin (SGLT2)", "grp": "Antidiabetikum", "act": "VYSADIT 3 DNY PŘEDEM", "info": "Riziko euglykemické ketoacidózy. ⚠️ Pozor: Eliminaci léku může ovlivňovat funkce ledvin!", "col": "red"},
    {"brands": ["novorapid", "actrapid", "humalog", "apidra", "fiasp"], "gen": "Insulin (Bolus)", "grp": "Diabetes", "act": "NEPODÁVAT", "info": "Při lačnění nepodávat.", "col": "red"},
    {"brands": ["tresiba", "lantus", "toujeo", "levemir", "abslaglar"], "gen": "Insulin (Bazál)", "grp": "Diabetes", "act": "REDUKOVAT DÁVKU", "info": "Podat cca 75-80% dávky.", "col": "blue"},
    {"brands": ["oltar", "glimepirid", "gliklazid", "glyclada"], "gen": "Sulfonylurea", "grp": "Diabetes", "act": "NEPODÁVAT", "info": "Riziko hypoglykémie.", "col": "red"},

    # === KARDIOVASKULÁRNÍ ===
    {"brands": ["anopyrin", "godasal", "stacyl", "stacly", "aspirin", "acylpyrin", "anp", "asketon"], "gen": "ASA", "grp": "Antiagregace", "act": "PONECHAT", "info": "Vysadit 7 dní předem jen u výkonů s vysokým rizikem krvácení.", "col": "green"},
    {"brands": ["trombex", "plavix", "clopidogrel", "zylagren", "zyllt", "iscover", "platel"], "gen": "Clopidogrel", "grp": "Antiagregace", "act": "VYSADIT 7 DNÍ PŘEDEM", "info": "Vysoké riziko krvácení.", "col": "red"},
    {"brands": ["warfarin", "lawarin"], "gen": "Warfarin", "grp": "Antikoagulace", "act": "VYSADIT 3-5 DNÍ PŘEDEM", "info": "Nutný bridging dle INR.", "col": "red"},
    
    # NOAK s novým varováním na ledviny a obecným časováním
    {"brands": ["eliquis", "apixaban"], "gen": "Apixaban", "grp": "NOAK", "act": "VYSADIT 1-2 DNY PŘEDEM", "info": "1 den předem, nebo 2 dny u výkonů s vysokým rizikem krvácení. ⚠️ Pozor: Eliminaci léku může ovlivňovat funkce ledvin!", "col": "red"},
    {"brands": ["xarelto", "rivaroxaban"], "gen": "Rivaroxaban", "grp": "NOAK", "act": "VYSADIT 1-2 DNY PŘEDEM", "info": "1 den předem, nebo 2 dny u výkonů s vysokým rizikem krvácení. ⚠️ Pozor: Eliminaci léku může ovlivňovat funkce ledvin!", "col": "red"},
    {"brands": ["pradaxa", "dabigatran"], "gen": "Dabigatran", "grp": "NOAK", "act": "VYSADIT 1-2 DNY PŘEDEM", "info": "1 den předem, nebo 2 dny u výkonů s vysokým rizikem krvácení. ⚠️ Pozor: Eliminaci léku může ovlivňovat funkce ledvin!", "col": "red"},
    {"brands": ["lixiana", "edoxaban"], "gen": "Edoxaban", "grp": "NOAK", "act": "VYSADIT 1-2 DNY PŘEDEM", "info": "1 den předem, nebo 2 dny u výkonů s vysokým rizikem krvácení. ⚠️ Pozor: Eliminaci léku může ovlivňovat funkce ledvin!", "col": "red"},

    {"brands": ["prestarium", "tritace", "ramipril", "perindopril", "prenessa", "telmisartan", "micardis", "lozap", "amprilan", "enap"], "gen": "ACEI / Sartan", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Zvážit ponechání jen u srdečního selhání nebo špatně korigovatelné hypertenze.", "col": "red"},
    {"brands": ["bisoprolol", "concor", "betaloc", "egilok", "vasocardin", "nebilet", "lokren", "coryol"], "gen": "Beta-blokátor", "grp": "Kardio", "act": "PONECHAT", "info": "Kardioprotekce.", "col": "green"},
    {"brands": ["agen", "amlodipin", "norvasc", "plendil", "lusopress", "isoptin", "verapamil"], "gen": "BKK", "grp": "Kardio", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["furon", "furorese", "verospiron", "hydrochlorothiazid", "indapamid", "moduretic"], "gen": "Diuretikum", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Zvážit ponechání u srdečního selhání.", "col": "red"},
    {"brands": ["cordarone", "sedacoron", "amiodaron", "ritmonorm", "digoxin"], "gen": "Antiarytmikum", "grp": "Kardio", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["ezetrol", "ezetimib", "lipanthyl", "fenofibrat", "gopten"], "gen": "Fibráty / Ezetrol", "grp": "Hypolipidemika (Nestatinová)", "act": "VYSADIT V DEN VÝKONU", "info": "-", "col": "red"},
    {"brands": ["atorvastatin", "sorvasta", "tulip", "rosuvastatin", "torvacard", "atoris", "sortis"], "gen": "Statin", "grp": "Hypolipidemika", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["entresto"], "gen": "Sacubitril/Valsartan", "grp": "ARNI", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypotenze. Dle interní směrnice jako Sartany.", "col": "red"},
    {"brands": ["triplixam", "tezefort", "twynsta", "amesos", "tonarssa", "lorista h", "lozap h"], "gen": "Kombinace (ACEI/Sartan/Diuret)", "grp": "Kombinace", "act": "VYSADIT V DEN VÝKONU", "info": "Obsahuje ACEI/Sartan nebo diuretikum.", "col": "red"},
    {"brands": ["rilmenidin", "moxonidin", "cynt"], "gen": "Alfa2 agonista", "grp": "Kardio", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["nitromint", "cardiket", "mono mack", "isoket"], "gen": "Nitráty", "grp": "Kardio", "act": "PONECHAT", "info": "-", "col": "green"},

    # === PSYCHIATRIE / NEUROLOGIE / BOLEST ===
    {"brands": ["neurol", "xanax", "lexaurin", "diazepam", "rivotril", "frontin", "buspiron"], "gen": "Anxiolytika / BZD", "grp": "Psychofarmaka", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["zolpidem", "stilnox", "hypnogen", "sanval", "adorma"], "gen": "Zolpidem", "grp": "Hypnotikum", "act": "RÁNO NEPODÁVAT", "info": "Riziko sedace.", "col": "red"},
    {"brands": ["citalec", "cipralex", "zoloft", "trittico", "mirtazapin", "argofan", "elicea", "asentra"], "gen": "Antidepresiva", "grp": "Psychofarmaka", "act": "PONECHAT", "info": "Pozor na iMAO (vysadit 2 týdny předem).", "col": "green"},
    {"brands": ["lithium", "lithium carbonicum"], "gen": "Lithium", "grp": "Stabilizátor nálady", "act": "VYSADIT / PONECHAT", "info": "Vysadit 3 dny předem POUZE u velkých operačních výkonů, jinak ponechat.", "col": "yellow"},
    {"brands": ["guanfacin", "intuniv"], "gen": "Guanfacin", "grp": "ADHD", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["ritalin", "concerta", "atomoxetin", "strattera", "bitinex"], "gen": "Methylfenidát/Atomoxetin", "grp": "ADHD", "act": "VYSADIT V DEN VÝKONU", "info": "-", "col": "red"},
    {"brands": ["zyprexa", "olanzapin", "tiaprid", "buronil", "quetiapin", "ketiapin", "risperdal"], "gen": "Antipsychotika", "grp": "Psychofarmaka", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["lyrica", "pregabalin", "gabapentin", "neurontin", "gabanox", "depakine", "biston", "lamictal", "timonil"], "gen": "Antiepileptikum", "grp": "Neuro", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["nakom", "madopar", "isicom"], "gen": "L-Dopa", "grp": "Antiparkinsonikum", "act": "PONECHAT", "info": "Přísně dodržet časování!", "col": "green"},
    {"brands": ["doreta", "zaldiar", "foxis", "palgotal", "ultracod"], "gen": "Tramadol/Paracetamol", "grp": "Analgetikum (Opioid)", "act": "PONECHAT", "info": "⚠️ OPIÁT: Tolerance. Nevysazovat.", "col": "green"},
    {"brands": ["tramal", "mabron", "tramabene"], "gen": "Tramadol", "grp": "Analgetikum (Opioid)", "act": "PONECHAT", "info": "⚠️ OPIÁT: Tolerance.", "col": "green"},
    {"brands": ["fentanyl", "matrifen", "durogesic", "transtec", "buprenorphin"], "gen": "Opioid (Náplast)", "grp": "Analgetikum (TD)", "act": "PONECHAT - NEODLEPOVAT", "info": "⚠️ SILNÝ OPIÁT: Vysoká tolerance!", "col": "yellow"},
    {"brands": ["oxycontin", "targin", "dhc", "sevredol"], "gen": "Silný opioid (p.o.)", "grp": "Analgetikum", "act": "PONECHAT", "info": "⚠️ SILNÝ OPIÁT: Nutno podat ranní dávku.", "col": "green"},

    # === OSTATNÍ (Žíly, GIT, Ionty, Kortikoidy) ===
    {"brands": ["detralex", "mobivenal", "diozen", "devenal", "cyclo 3 fort", "glyvenol"], "gen": "Venofarmaka", "grp": "Cévy", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["pantoprazol", "controloc", "helides", "omeprazol", "helicid", "emanera", "nolpaza", "sulfasalazin", "pentasa", "asacol"], "gen": "PPI / Mesalazin", "grp": "GIT", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["kreon", "pancreolan"], "gen": "Enzymy", "grp": "GIT", "act": "VYNECHAT", "info": "Při lačnění nemají smysl.", "col": "red"},
    {"brands": ["kalnormin", "magnosolv", "magnesium", "vigantol", "novalgin"], "gen": "Suplementace / Analgetika", "grp": "Ostatní", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["milurit", "purinol", "alopurinol"], "gen": "Allopurinol", "grp": "Dna", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["prednison", "medrol", "fortecortin", "dexamed"], "gen": "Kortikoid", "grp": "Steroidy", "act": "SUBSTITUCE NUTNÁ", "info": "Zajistit peri- a pooperační substituci dle rozsahu výkonu a zvyklostí pracoviště.", "col": "blue"},
    {"brands": ["betoptic", "timolol", "cosopt", "carteol"], "gen": "Oční kapky", "grp": "Oční", "act": "PONECHAT", "info": "Nevysazovat!", "col": "green"},
]

# --- 3. VYHODNOCENÍ ---
if st.button("🚀 VYHODNOTIT MEDIKACI", type="primary"):
    st.subheader("Doporučení:")
    found_count = 0
    
    for item in db:
        match = next((b for b in item["brands"] if b in med_text), None)
        
        if match:
            found_count += 1
            
            st.markdown(f"""
            <div class="drug-card border-{item['col']}">
                <span class="card-title">{match.capitalize()} <span class="card-generic">({item['gen']})</span></span>
                <span class="card-rec">{item['act']}</span>
                <span class="card-info">{item['info']}</span>
            </div>
            """, unsafe_allow_html=True)

    if found_count == 0:
        st.info("Žádná riziková medikace nenalezena (nebo není v databázi).")
        
    if "vysazeno" in med_text or "ex" in med_text:
        st.warning("⚠️ **Pozor:** Text obsahuje slovo 'vysazeno'/'ex'. Pokud pacient lék neužívá, ignorujte pokyn k jeho vysazení.")
