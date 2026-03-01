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
    .nis-box {
        background-color: #e0e0e0;
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
        color: #333;
        font-family: monospace;
        font-size: 1.05em;
        border-left: 6px solid #888;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HLAVIČKA ---
st.markdown("<h1>🩺 Anesteziologický asistent</h1>", unsafe_allow_html=True)
st.caption("Zdroj: Interní směrnice + Prezentace + Dia protokol + Nová farmaka", unsafe_allow_html=True)
st.write("---")

# --- 1. VSTUP ---
st.subheader("Vložte chronickou medikaci pacienta:")
med_text = st.text_area(
    "", 
    height=200, 
    placeholder="Např.: Cosyrel 5/10mg tbl., Palexia, Ylpio, Zyrtec, Xanirva..."
).lower()
st.write("")

# --- 2. DATABÁZE LÉČIV ---
db = [
    {
        "brands": [
            "accuzide", "amesos", "cazacombi", "egiramlon", "furorese", 
            "hcht", "ifirmacombi", "lodoz", "loradur", "lozap h", 
            "moduretic", "rasilez hct", "rhefluin", "stadapres", "tarka", 
            "tonarsa", "triasyn", "tritazide", "valsacombi", "vidonorm", 
            "triplixam", "tezefort", "twynsta", "tonarssa", "lorista h", 
            "prestance", "lercaprel", "tonanda", "ylpio", "cosyrel"
        ], 
        "gen": "Kombinace (obsahuje ACEI/Sartan/Diur)", 
        "grp": "Kombinace", 
        "act": "VYSADIT V DEN VÝKONU", 
        "info": "Obsahuje ACEI, Sartan nebo Diuretikum (u Cosyrelu převáží riziko ACEI nad BB).", 
        "col": "red"
    },
    {
        "brands": [
            "accupro", "acesial", "almesa", "amprilan", "apo-enapril", 
            "apo-perindo", "berlipril", "capoten", "cazaprol", "coverex", 
            "dapril", "diroton", "ednyt", "enalapril", "enap", "enapril", 
            "fosinogen", "fosinopril", "gleperil", "gopten", "hartil", 
            "inhibace", "lisinopril", "medoram", "miril", "moex", "monace", 
            "monopril", "perinalon", "perindopril", "perinpra", "pinbarix", 
            "piramil", "prenesa", "prenewel", "prestarium", "pricoron", 
            "ramicard", "ramigamma", "ramil", "ramipril", "rasilez", 
            "renpres", "tanap", "tanatril", "tensiomin", "tritace", 
            "vidotin", "arionex", "blessin", "canocord", "carzap", "giovax", 
            "ifirmasta", "irbesartan", "kylotan", "lakea", "lorista", 
            "losagen", "losartan", "losartic", "lozap", "micardis", 
            "nopretens", "sangona", "telmark", "telmisartan", "teveten", 
            "tezeo", "tolura", "valsacor", "valsap", "zanacodar", "caramlo", 
            "entresto"
        ], 
        "gen": "ACE Inhibitor / Sartan", 
        "grp": "Hypertenze", 
        "act": "VYSADIT V DEN VÝKONU", 
        "info": "Zvážit ponechání jen u srdečního selhání.", 
        "col": "red"
    },
    {
        "brands": [
            "amiclaran", "amicloton", "apo-a1milzide", "furon", "hypotylin", 
            "indap", "indapamid", "verospiron", "hydrochlorothiazid"
        ], 
        "gen": "Diuretikum", 
        "grp": "Hypertenze", 
        "act": "VYSADIT V DEN VÝKONU", 
        "info": "Riziko hypovolemie. Zvážit ponechání u srdečního selhání.", 
        "col": "red"
    },
    {
        "brands": [
            "acecor", "obsidan", "apo-acebutol", "pindol", "apo-metopro", 
            "propranolol", "apo-nadol", "rivocor", "atehexal", "sandonorm", 
            "atenobene", "atenol", "sectral", "atenolol", "sobycir", "betaloc", 
            "sotahexal", "betamed", "tenoloc", "betasyn", "tenoretic", "betaxa", 
            "tenormin", "bisocard", "trimepranol", "bisogamma", "tyrez", 
            "bisoprolol", "vasocardin", "brevibloc", "visken", "carvesan", 
            "catenol", "bloxazoc", "celectol", "betaxolol", "combiso", "concor", 
            "corotenol", "corvitol", "egilok", "emzok", "lokren", "logimax", 
            "metoprolol", "nebilet", "nebivolol", "apo-carve", "atram", 
            "carvediol", "coreton", "coryol", "dilatre", "dilatrend", "taliton", 
            "trandate"
        ], 
        "gen": "Beta-blokátor", 
        "grp": "Kardio", 
        "act": "PONECHAT", 
        "info": "Kardioprotekce.", 
        "col": "green"
    },
    {
        "brands": [
            "adalat", "afiten", "agen", "amilostad", "amlator", "amlodipin", 
            "amlop", "amloratio", "amlozek", "apo-amlo", "ardifen", "auronal", 
            "caduet", "cardilopin", "cinarizin", "cordafen", "cordipin", 
            "corinfar", "diacordin", "diltan", "felodipin", "hipres", "isoptin", 
            "kapidin", "lacipil", "lekoptin", "lomir", "lusopress", "nifedipin", 
            "nimotop", "nitrepress", "nitresan", "nitresdipin", "normodipine", 
            "norvasc", "orcal", "plendil", "presid", "recotens", "sponit", 
            "syocor", "tensigal", "torrela", "unipres", "vasexten", "verahexal", 
            "verepamil", "verogalid", "zorem"
        ], 
        "gen": "Blokátor Ca kanálů", 
        "grp": "Kardio", 
        "act": "PONECHAT", 
        "info": "-", 
        "col": "green"
    },
    {
        "brands": [
            "cynt", "dopegyt", "moxogamma", "moxonidin", "moxostad", "rilmenidin", 
            "tenaxum", "doxazosin", "ebrantil", "hytrin", "kamiren", "zoxon", 
            "urapidil", "labetelol"
        ], 
        "gen": "Centrální / Alfa blokátory", 
        "grp": "Kardio", 
        "act": "PONECHAT", 
        "info": "-", 
        "col": "green"
    },
    {
        "brands": ["ezetrol", "ezetimib", "lipanthyl", "fenofibrat", "ezen", "delipid plus"], 
        "gen": "Fibráty / Ezetimib", 
        "grp": "Hypolipidemika", 
        "act": "VYSADIT V DEN VÝKONU", 
        "info": "U kombinací (Delipid Plus) převažuje nutnost vysazení Ezetimibu.", 
        "col": "red"
    },
    {
        "brands": ["atorvastatin", "sorvasta", "tulip", "rosuvastatin", "torvacard", "atoris", "sortis", "rosucard", "rosumop"], 
        "gen": "Statin", 
        "grp": "Hypolipidemika", 
        "act": "PONECHAT", 
        "info": "Snižují riziko CMP, IM.", 
        "col": "green"
    },
    {
        "brands": ["cordarone", "sedacoron", "amiodaron", "ritmonorm", "digoxin", "rivodaron"], 
        "gen": "Antiarytmikum", 
        "grp": "Kardio", 
        "act": "PONECHAT", 
        "info": "Amiodaron: CAVE na hypokalemii a hypomagnezémii.", 
        "col": "green"
    },
    {
        "brands": ["nitromint", "cardiket", "mono mack", "isoket"], 
        "gen": "Nitráty", 
        "grp": "Kardio", 
        "act": "PONECHAT", 
        "info": "CAVE na hypovolemii.", 
        "col": "green"
    },
    {
        "brands": ["anopyrin", "godasal", "stacyl", "stacly", "aspirin", "acylpyrin", "anp", "asketon"], 
        "gen": "ASA", 
        "grp": "Antiagregace", 
        "act": "PONECHAT", 
        "info": "Vysadit v den výkonu nebo 7 dní předem u vysokého rizika krvácení. Ponechat u duální terapie.", 
        "col": "green"
    },
    {
        "brands": ["trombex", "plavix", "clopidogrel", "zylagren", "zyllt", "iscover", "platel"], 
        "gen": "Clopidogrel", 
        "grp": "Antiagregace", 
        "act": "VYSADIT 7 DNÍ PŘEDEM", 
        "info": "Vysoké riziko krvácení.", 
        "col": "red"
    },
    {
        "brands": ["warfarin", "lawarin"], 
        "gen": "Warfarin", 
        "grp": "Antikoagulace", 
        "act": "VYSADIT 3-5 DNÍ PŘEDEM", 
        "info": "Nutný bridging dle INR.", 
        "col": "red"
    },
    {
        "brands": ["eliquis", "apixaban", "xarelto", "rivaroxaban", "pradaxa", "dabigatran", "lixiana", "edoxaban", "xanirva"], 
        "gen": "NOAK", 
        "grp": "NOAK", 
        "act": "VYSADIT 1 NEBO 2 DNY PŘEDEM", 
        "info": "1 den (standard) nebo 2 dny (vysoké riziko). ⚠️ Eliminaci ovlivňují ledviny!", 
        "col": "red"
    },
    {
        "brands": ["euthyrox", "letrox", "thyrozol", "jodid", "eutyrox"], 
        "gen": "Levothyroxin", 
        "grp": "Štítná žláza", 
        "act": "PONECHAT", 
        "info": "Substituce se nepřerušuje.", 
        "col": "green"
    },
    {
        "brands": ["metformin", "stadamet", "siofor", "glucophage", "metfogamma", "mulado"], 
        "gen": "Metformin", 
        "grp": "Antidiabetikum", 
        "act": "VYSADIT 24h PŘEDEM", 
        "info": "Vysadit u středních/velkých výkonů. U malých lze ponechat. ⚠️ Eliminaci ovlivňují ledviny!", 
        "col": "red"
    },
    {
        "brands": ["jardiance", "forxiga", "invokana", "synjardy", "xigduo"], 
        "gen": "Glifloziny (SGLT2)", 
        "grp": "Antidiabetikum", 
        "act": "VYSADIT 3-4 DNY PŘEDEM", 
        "info": "Riziko euglykemické ketoacidózy. ⚠️ Eliminaci ovlivňují ledviny!", 
        "col": "red"
    },
    {
        "brands": ["bydureon", "byetta", "victoza", "ozempic", "trulicity", "rybelsus"], 
        "gen": "GLP-1 agonisté", 
        "grp": "Diabetes", 
        "act": "VYSADIT V DEN VÝKONU", 
        "info": "Kontroly glykémie á 4-6 hod.", 
        "col": "red"
    },
    {
        "brands": ["januvia", "sitagliptin", "trajenta", "vipidia", "galvus", "pioglitazon", "actos"], 
        "gen": "Gliptiny / Pioglitazon", 
        "grp": "Diabetes", 
        "act": "VYSADIT V DEN VÝKONU", 
        "info": "-", 
        "col": "red"
    },
    {
        "brands": ["amaryl", "glimepirid", "oltar", "diaprel", "gliklazid", "glyclada"], 
        "gen": "Sulfonylurea", 
        "grp": "Diabetes", 
        "act": "VYSADIT V DEN VÝKONU", 
        "info": "Riziko hypoglykémie.", 
        "col": "red"
    },
    {
        "brands": ["novorapid", "actrapid", "humalog", "apidra", "fiasp"], 
        "gen": "Insulin (Bolus)", 
        "grp": "Diabetes", 
        "act": "NEPODÁVAT", 
        "info": "Při lačnění nepodávat.", 
        "col": "red"
    },
    {
        "brands": ["tresiba", "lantus", "toujeo", "levemir", "abslaglar"], 
        "gen": "Insulin (Bazál)", 
        "grp": "Diabetes", 
        "act": "PONECHAT / REDUKOVAT", 
        "info": "Ponechat jak nastaveno z předchozího dne, perioperačně bazální režim.", 
        "col": "blue"
    },
    {
        "brands": ["prednison", "medrol", "fortecortin", "dexamed", "hydrocortison"], 
        "gen": "Kortikoid p.o.", 
        "grp": "Steroidy", 
        "act": "SUBSTITUCE (> 5mg)", 
        "info": "Do 5mg ponechat. Nad 5mg: střední výkon 50mg i.v., velký 100mg i.v.", 
        "col": "blue"
    },
    {
        "brands": ["tamoxifen", "raloxifen", "evista"], 
        "gen": "SERM (Hormony)", 
        "grp": "Endokrino", 
        "act": "PONECHAT S LMWH", 
        "info": "Vysadit POUZE u vysokého rizika TEN.", 
        "col": "green"
    },
    {
        "brands": ["alendronat", "ibandronat", "risedronat", "fosamax", "bonviva", "actonel"], 
        "gen": "Bisfosfonáty", 
        "grp": "Osteoporóza", 
        "act": "VYSADIT V DEN VÝKONU", 
        "info": "Zapíjí se velkým množstvím vody, riziko aspirace.", 
        "col": "red"
    },
    {
        "brands": ["ventolin", "salbutamol", "buventol", "ecosal", "berodual", "ipratropium", "atrovent", "spiriva", "braltus", "biskair"], 
        "gen": "Inhalace (SABA/SAMA/LAMA)", 
        "grp": "Inhalace", 
        "act": "PONECHAT A POSÍLIT", 
        "info": "Posílit více vdechy. Ráno i před sál prevence spasmu.", 
        "col": "green"
    },
    {
        "brands": ["seretide", "symbicort", "combair", "foster", "duoresp", "salmex", "trixeo", "trelegy"], 
        "gen": "ICS/LABA/LAMA", 
        "grp": "Inhalace", 
        "act": "PONECHAT A POSÍLIT", 
        "info": "Pokud > 2 vdechy denně: Hydrocortison 50/100mg i.v.", 
        "col": "green"
    },
    {
        "brands": ["theofylin", "aminofylin", "syntophyllin", "euphyllin", "tezeo", "theoplus"], 
        "gen": "Methylxanthiny", 
        "grp": "Pneumo", 
        "act": "VYSADIT", 
        "info": "Riziko arytmií a neurotoxicity. NEPODÁVAT do premedikace!", 
        "col": "red"
    },
    {
        "brands": ["montelukast", "castispir", "singulair", "asmen"], 
        "gen": "Inhibitory leukotrienů", 
        "grp": "Pneumo", 
        "act": "PONECHAT", 
        "info": "-", 
        "col": "green"
    },
    {
        "brands": ["neurol", "xanax", "lexaurin", "diazepam", "rivotril", "frontin", "buspiron"], 
        "gen": "Anxiolytika / BZD", 
        "grp": "Psychofarmaka", 
        "act": "PONECHAT", 
        "info": "Nevysazovat ani u starších osob!", 
        "col": "green"
    },
    {
        "brands": ["zolpidem", "stilnox", "hypnogen", "sanval", "adorma"], 
        "gen": "Zolpidem", 
        "grp": "Hypnotikum", 
        "act": "RÁNO NEPODÁVAT", 
        "info": "Riziko sedace.", 
        "col": "red"
    },
    {
        "brands": ["citalec", "cipralex", "zoloft", "trittico", "mirtazapin", "argofan", "elicea", "asentra"], 
        "gen": "Antidepresiva", 
        "grp": "Psychofarmaka", 
        "act": "PONECHAT", 
        "info": "Pozor na iMAO (vysadit 2 týdny předem, absolutní KI ephedrin!).", 
        "col": "green"
    },
    {
        "brands": ["lithium", "lithium carbonicum"], 
        "gen": "Lithium", 
        "grp": "Stabilizátor nálady", 
        "act": "PONECHAT", 
        "info": "Vysadit 3 dny předem POUZE u velkých operačních výkonů.", 
        "col": "green"
    },
    {
        "brands": ["guanfacin", "intuniv"], 
        "gen": "Guanfacin", 
        "grp": "ADHD", 
        "act": "PONECHAT", 
        "info": "-", 
        "col": "green"
    },
    {
        "brands": ["ritalin", "concerta", "atomoxetin", "strattera", "bitinex"], 
        "gen": "Methylfenidát/Atomoxetin", 
        "grp": "ADHD", 
        "act": "VYSADIT V DEN VÝKONU", 
        "info": "-", 
        "col": "red"
    },
    {
        "brands": ["zyprexa", "olanzapin", "tiaprid", "buronil", "quetiapin", "ketiapin", "risperdal"], 
        "gen": "Antipsychotika", 
        "grp": "Psychofarmaka", 
        "act": "PONECHAT", 
        "info": "-", 
        "col": "green"
    },
    {
        "brands": ["lyrica", "pregabalin", "gabapentin", "neurontin", "gabanox", "depakine", "biston", "lamictal", "timonil"], 
        "gen": "Antiepileptikum", 
        "grp": "Neuro", 
        "act": "PONECHAT", 
        "info": "-", 
        "col": "green"
    },
    {
        "brands": ["nakom", "madopar", "isicom"], 
        "gen": "L-Dopa", 
        "grp": "Antiparkinsonikum", 
        "act": "PONECHAT", 
        "info": "Přísně dodržet časování i v den výkonu (riziko hypertermie a rigidity)!", 
        "col": "green"
    },
    {
        "brands": ["biperiden", "akineton", "orfendrin"], 
        "gen": "Centrální anticholinergika", 
        "grp": "Antiparkinsonikum", 
        "act": "VYSADIT V DEN VÝKONU", 
        "info": "Riziko zmatenosti.", 
        "col": "red"
    },
    {
        "brands": ["naltrexon", "adepend", "mysimba"], 
        "gen": "Naltrexon", 
        "grp": "Závislost", 
        "act": "VYSADIT V DEN VÝKONU", 
        "info": "Blokuje opiátové receptory.", 
        "col": "red"
    },
    {
        "brands": ["donepezil", "aricept", "yasnal", "memantin", "ebixa", "kognityl", "rivastigmin", "exelon"], 
        "gen": "Kognitiva (Inh. ACHE)", 
        "grp": "Neuro", 
        "act": "PONECHAT", 
        "info": "Nevysazovat (riziko zhoršení kognice/zmatenosti).", 
        "col": "green"
    },
    {
        "brands": ["doreta", "zaldiar", "foxis", "palgotal", "ultracod", "tramal", "mabron", "tramabene"], 
        "gen": "Tramadol/Paracetamol", 
        "grp": "Analgetikum (Opioid)", 
        "act": "PONECHAT", 
        "info": "⚠️ OPIÁT: Tolerance. Nevysazovat.", 
        "col": "green"
    },
    {
        "brands": ["fentanyl", "matrifen", "durogesic", "transtec", "buprenorphin"], 
        "gen": "Opioid (Náplast)", 
        "grp": "Analgetikum (TD)", 
        "act": "PONECHAT - NEODLEPOVAT", 
        "info": "⚠️ SILNÝ OPIÁT: Vysoká tolerance!", 
        "col": "yellow"
    },
    {
        "brands": ["oxycontin", "targin", "dhc", "sevredol", "palexia", "tapentadol"], 
        "gen": "Silný opioid (p.o.)", 
        "grp": "Analgetikum", 
        "act": "PONECHAT", 
        "info": "⚠️ SILNÝ OPIÁT: Nutno podat ranní dávku.", 
        "col": "green"
    },
    {
        "brands": ["detralex", "mobivenal", "diozen", "devenal", "cyclo 3 fort", "glyvenol"], 
        "gen": "Venofarmaka", 
        "grp": "Cévy", 
        "act": "PONECHAT", 
        "info": "-", 
        "col": "green"
    },
    {
        "brands": ["pantoprazol", "controloc", "helides", "omeprazol", "helicid", "emanera", "nolpaza", "sulfasalazin", "pentasa", "asacol"], 
        "gen": "PPI / Mesalazin", 
        "grp": "GIT", 
        "act": "PONECHAT", 
        "info": "Prevence chemické pneumonie / exacerbace IBD.", 
        "col": "green"
    },
    {
        "brands": ["kreon", "pancreolan"], 
        "gen": "Enzymy", 
        "grp": "GIT", 
        "act": "VYNECHAT", 
        "info": "Při lačnění nemají smysl.", 
        "col": "red"
    },
    {
        "brands": ["ursosan", "ursofalk"], 
        "gen": "Kys. ursodeoxycholová", 
        "grp": "GIT", 
        "act": "PONECHAT", 
        "info": "-", 
        "col": "green"
    },
    {
        "brands": ["kalnormin", "magnosolv", "magnesium", "vigantol", "novalgin"], 
        "gen": "Suplementace / Analgetika", 
        "grp": "Ostatní", 
        "act": "PONECHAT", 
        "info": "-", 
        "col": "green"
    },
    {
        "brands": ["zyrtec", "analergin", "xalerg", "zenaro", "cezera", "desloratadin", "cetirizin", "levocetirizin", "aerius"], 
        "gen": "Antihistaminika", 
        "grp": "Alergie", 
        "act": "PONECHAT", 
        "info": "-", 
        "col": "green"
    },
    {
        "brands": ["milurit", "purinol", "alopurinol", "kolchicin"], 
        "gen": "Léčba Dny", 
        "grp": "Dna", 
        "act": "PONECHAT", 
        "info": "-", 
        "col": "green"
    },
    {
        "brands": ["tamsulosin", "omnic", "penester", "fokusin", "uprox"], 
        "gen": "Alfa1-blokátor", 
        "grp": "BHP", 
        "act": "PONECHAT", 
        "info": "-", 
        "col": "green"
    },
    {
        "brands": ["betoptic", "timolol", "cosopt", "carteol"], 
        "gen": "Oční kapky", 
        "grp": "Oční", 
        "act": "PONECHAT", 
        "info": "Nevysazovat!", 
        "col": "green"
    }
]

# --- 3. VYHODNOCENÍ ---
if st.button("🚀 VYHODNOTIT MEDIKACI", type="primary"):
    
    kept_drugs = []
    stopped_drugs = []
    diabetik_nalezen = False
    
    # Roztřídění léků do dvou skupin
    for item in db:
        match = next((b for b in item["brands"] if b in med_text), None)
        if match:
            if item["grp"] in ["Diabetes", "Antidiabetikum"]:
                diabetik_nalezen = True
                
            # Pokud je akce "PONECHAT" (vč. Ponechat s LMWH atd.), jde do zelené skupiny
            if "PONECHAT" in item["act"]:
                kept_drugs.append((match.capitalize(), item))
            else:
                # Vše k vysazení, redukci nebo vynechání jde do červené skupiny
                stopped_drugs.append((match.capitalize(), item))

    # --- ZOBRAZENÍ VÝSLEDKŮ ---
    if not kept_drugs and not stopped_drugs:
        st.info("Žádná riziková medikace nenalezena (nebo není v databázi).")
    else:
        # 1. Skupina: LÉKY K PONECHÁNÍ
        if kept_drugs:
            st.subheader("✅ Léky k ponechání v den výkonu:")
            for drug_name, item in kept_drugs:
                st.markdown(f"""
                <div class="drug-card border-{item['col']}">
                    <span class="card-title">{drug_name} <span class="card-generic">({item['gen']})</span></span>
                    <span class="card-rec">{item['act']}</span>
                    <span class="card-info">{item['info']}</span>
                </div>
                """, unsafe_allow_html=True)

        # 2. Skupina: LÉKY K VYSAZENÍ/ÚPRAVĚ
        if stopped_drugs:
            st.subheader("🛑 Léky k vysazení nebo úpravě dávky:")
            for drug_name, item in stopped_drugs:
                st.markdown(f"""
                <div class="drug-card border-{item['col']}">
                    <span class="card-title">{drug_name} <span class="card-generic">({item['gen']})</span></span>
                    <span class="card-rec">{item['act']}</span>
                    <span class="card-info">{item['info']}</span>
                </div>
                """, unsafe_allow_html=True)
                
        # 3. Skupina: TEXT DO NISu (Informační systém)
        st.markdown(f"""
        <div class="nis-box">
            <strong>📝 Text do informačního systému (NIS):</strong><br><br>
            V den výkonu podat: {', '.join([drug[0] for drug in kept_drugs]) if kept_drugs else 'nic (vše vysazeno)'}
        </div>
        """, unsafe_allow_html=True)

    # --- VAROVÁNÍ A DIA PROTOKOL ---
    if "vysazeno" in med_text or "ex" in med_text:
        st.warning("⚠️ **Pozor:** Text obsahuje slovo 'vysazeno'/'ex'. Pokud pacient lék neužívá, ignorujte pokyn k jeho vysazení.")
        
    if diabetik_nalezen:
        st.write("---")
        st.error("🩸 **Diabetický management pro sál:**\n\n"
                 "• **Cílová glykémie:** 6,1 – 10,0 mmol/l.\n"
                 "• **Malé výkony:** Při užití PAD ráno výkon nerušit, lze provést s kontrolami á 2-4h + G10% s Inzulinem.\n"
                 "• **Střední/Velké výkony (> 2 hod):** Nutná hospitalizace den před
