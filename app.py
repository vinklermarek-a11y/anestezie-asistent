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
    {"brands": ["cordarone", "sedacoron", "amiodaron", "ritmonorm", "digoxin"], "gen": "Antiarytmikum", "grp": "Kardio", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["nitromint", "cardiket", "mono mack", "isoket"], "gen": "Nitráty", "grp": "Kardio", "act": "PONECHAT", "info": "-", "col": "green"},

    # === ANTIAGREGACE & ANTIKOAGULACE ===
    {"brands": ["anopyrin", "godasal", "stacyl", "stacly", "aspirin", "acylpyrin", "anp", "asketon"], "gen": "ASA", "grp": "Antiagregace", "act": "PONECHAT", "info": "Vysadit 7 dní předem jen u výkonů s vysokým rizikem krvácení nebo duální terapie.", "col": "green"},
    {"brands": ["trombex", "plavix", "clopidogrel", "zylagren", "zyllt", "iscover", "platel"], "gen": "Clopidogrel", "grp": "Antiagregace", "act": "VYSADIT 7 DNÍ PŘEDEM", "info": "Vysoké riziko krvácení.", "col": "red"},
    {"brands": ["warfarin", "lawarin"], "gen": "Warfarin", "grp": "Antikoagulace", "act": "VYSADIT 3-5 DNÍ PŘEDEM", "info": "Nutný bridging dle INR.", "col": "red"},
    {"brands": ["eliquis", "apixaban", "xarelto", "rivaroxaban", "pradaxa", "dabigatran", "lixiana", "edoxaban"], "gen": "NOAK", "grp": "NOAK", "act": "VYSADIT 1-2 DNY PŘEDEM", "info": "1 den předem (standard) nebo 2 dny (vysoké riziko). ⚠️ Pozor: Eliminaci léku může ovlivňovat funkce ledvin!", "col": "red"},

    # === ENDOKRINOLOGIE & DIABETES ===
    {"brands": ["euthyrox", "letrox", "thyrozol", "jodid", "eutyrox"], "gen": "Levothyroxin", "grp": "Štítná žláza", "act": "PONECHAT", "info": "Substituce se nepřerušuje.", "col": "green"},
    {"brands": ["metformin", "stadamet", "siofor", "glucophage", "mulado"], "gen": "Metformin", "grp": "Antidiabetikum", "act": "VYSADIT 48H", "info": "Riziko laktátové acidózy. ⚠️ Pozor: Eliminaci léku může ovlivňovat funkce ledvin!", "col": "red"},
    {"brands": ["jardiance", "forxiga", "invokana", "synjardy"], "gen": "Gliflozin (SGLT2)", "grp": "Antidiabetikum", "act": "VYSADIT 3 DNY PŘEDEM", "info": "Riziko euglykemické ketoacidózy. ⚠️ Pozor: Eliminaci léku může ovlivňovat funkce ledvin!", "col": "red"},
    {"brands": ["novorapid", "actrapid", "humalog", "apidra", "fiasp"], "gen": "Insulin (Bolus)", "grp": "Diabetes", "act": "NEPODÁVAT", "info": "Při lačnění nepodávat.", "col": "red"},
    {"brands": ["tresiba", "lantus", "toujeo", "levemir", "abslaglar"], "gen": "Insulin (Bazál)", "grp": "Diabetes", "act": "REDUKOVAT DÁVKU", "info": "Podat cca 75-80% dávky.", "col": "blue"},
    {"brands": ["oltar", "glimepirid", "gliklazid", "glyclada"], "gen": "Sulfonylurea", "grp": "Diabetes", "act": "NEPODÁVAT", "info": "Riziko hypoglykémie.", "col": "red"},
    {"brands": ["prednison", "medrol", "fortecortin", "dexamed"], "gen": "Kortikoid", "grp": "Steroidy", "act": "SUBSTITUCE NUTNÁ", "info": "Zajistit peri- a pooperační substituci dle rozsahu výkonu.", "col": "blue"},

    # === RESPIRAČNÍ ===
    {"brands": ["ventolin", "salbutamol", "buventol", "ecosal"], "gen": "Salbutamol (SABA)", "grp": "Inhalace", "act": "PONECHAT", "info": "Ráno i před sál prevence spasmu. Posílit dávku.", "col": "green"},
    {"brands": ["berodual", "ipratropium", "atrovent"], "gen": "Fenoterol/Ipratropium", "grp": "Inhalace", "act": "PONECHAT", "info": "Nevysazovat. Posílit dávku.", "col": "green"},
    {"brands": ["spiriva", "braltus", "biskair"], "gen": "Tiotropium (LAMA)", "grp": "Inhalace", "act": "PONECHAT", "info": "Udržet bronchodilataci. Posílit dávku.", "col": "green"},
    {"brands": ["seretide", "symbicort", "combair", "foster", "duoresp", "salmex", "trixeo", "trelegy"], "gen": "ICS/LABA/LAMA", "grp": "Inhalace (Kombinace)", "act": "PONECHAT", "info": "Nevysazovat! Posílit dávku (více vdechů).", "col": "green"},
    {"brands": ["euphyllin", "tezeo", "theoplus"], "gen": "Teofylin", "grp": "Methylxanthiny", "act": "PONECHAT", "info": "-", "col": "green"},

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
    {"brands": ["doreta", "zaldiar", "foxis", "palgotal", "ultracod", "tramal", "mabron", "tramabene"], "gen": "Tramadol/Paracetamol", "grp": "Analgetikum (Opioid)", "act": "PONECHAT", "info": "⚠️ OPIÁT: Tolerance. Nevysazovat.", "col": "green"},
    {"brands": ["fentanyl", "matrifen", "durogesic", "transtec", "buprenorphin"], "gen": "Opioid (Náplast)", "grp": "Analgetikum (TD)", "act": "PONECHAT - NEODLEPOVAT", "info": "⚠️ SILNÝ OPIÁT: Vysoká tolerance!", "col": "yellow"},
    {"brands": ["oxycontin", "targin", "dhc", "sevredol"], "gen": "Silný opioid (p.o.)", "grp": "Analgetikum", "act": "PONECHAT", "info": "⚠️ SILNÝ OPIÁT: Nutno podat ranní dávku.", "col": "green"},

    # === OSTATNÍ (Žíly, GIT, Ionty) ===
    {"brands": ["detralex", "mobivenal", "diozen", "devenal", "cyclo 3 fort", "glyvenol"], "gen": "Venofarmaka", "grp": "Cévy", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["pantoprazol", "controloc", "helides", "omeprazol", "helicid", "emanera", "nolpaza", "sulfasalazin", "pentasa", "asacol"], "gen": "PPI / Mesalazin", "grp": "GIT", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["kreon", "pancreolan"], "gen": "Enzymy", "grp": "GIT", "act": "VYNECHAT", "info": "Při lačnění nemají smysl.", "col": "red"},
    {"brands": ["kalnormin", "magnosolv", "magnesium", "vigantol", "novalgin"], "gen": "Suplementace / Analgetika", "grp": "Ostatní", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["milurit", "purinol", "alopurinol"], "gen": "Allopurinol", "grp": "Dna", "act": "PONECHAT", "info
