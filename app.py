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
db = [
    # === HYPERTENZE - KOMBINOVANÉ PREPARÁTY ===
    {"brands": ["accuzide", "amesos", "cazacombi", "egiramlon", "furorese", "hcht", "ifirmacombi", "lodoz", "loradur", "lozap h"], "gen": "Kombinace (ACEI/Sartan/Diuretikum)", "grp": "Kombinace", "act": "VYSADIT V DEN VÝKONU", "info": "Obsahuje ACEI, Sartan nebo Diuretikum.", "col": "red"},
    {"brands": ["moduretic", "rasilez hct", "rhefluin", "stadapres", "tarka", "tonarsa", "triasyn", "tritazide", "valsacombi", "vidonorm"], "gen": "Kombinace (ACEI/Sartan/Diuretikum)", "grp": "Kombinace", "act": "VYSADIT V DEN VÝKONU", "info": "Obsahuje ACEI, Sartan nebo Diuretikum.", "col": "red"},
    {"brands": ["triplixam", "tezefort", "twynsta", "tonarssa", "lorista h", "prestance", "lercaprel", "tonanda"], "gen": "Kombinace (ACEI/Sartan/Diuretikum)", "grp": "Kombinace", "act": "VYSADIT V DEN VÝKONU", "info": "Obsahuje ACEI, Sartan nebo Diuretikum.", "col": "red"},

    # === HYPERTENZE - ACE INHIBITORY A SARTANY ===
    {"brands": ["accupro", "acesial", "almesa", "amprilan", "apo-enapril", "apo-perindo", "berlipril", "capoten", "cazaprol", "coverex"], "gen": "ACE Inhibitor / Sartan", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypotenze. Zvážit ponechání jen u srdečního selhání.", "col": "red"},
    {"brands": ["dapril", "diroton", "ednyt", "enalapril", "enap", "enapril", "fosinogen", "fosinopril", "gleperil", "gopten"], "gen": "ACE Inhibitor / Sartan", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypotenze. Zvážit ponechání jen u srdečního selhání.", "col": "red"},
    {"brands": ["hartil", "inhibace", "lisinopril", "medoram", "miril", "moex", "monace", "monopril", "perinalon", "perindopril"], "gen": "ACE Inhibitor / Sartan", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypotenze. Zvážit ponechání jen u srdečního selhání.", "col": "red"},
    {"brands": ["perinpra", "pinbarix", "piramil", "prenesa", "prenewel", "prestarium", "pricoron", "ramicard", "ramigamma", "ramil"], "gen": "ACE Inhibitor / Sartan", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypotenze. Zvážit ponechání jen u srdečního selhání.", "col": "red"},
    {"brands": ["ramipril", "rasilez", "renpres", "tanap", "tanatril", "tensiomin", "tritace", "vidotin", "arionex", "blessin"], "gen": "ACE Inhibitor / Sartan", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypotenze. Zvážit ponechání jen u srdečního selhání.", "col": "red"},
    {"brands": ["canocord", "carzap", "giovax", "ifirmasta", "irbesartan", "kylotan", "lakea", "lorista", "losagen", "losartan"], "gen": "ACE Inhibitor / Sartan", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypotenze. Zvážit ponechání jen u srdečního selhání.", "col": "red"},
    {"brands": ["losartic", "lozap", "micardis", "nopretens", "sangona", "telmark", "telmisartan", "teveten", "tezeo", "tolura"], "gen": "ACE Inhibitor / Sartan", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypotenze. Zvážit ponechání jen u srdečního selhání.", "col": "red"},
    {"brands": ["valsacor", "valsap", "zanacodar", "caramlo", "entresto"], "gen": "ACE Inhibitor / Sartan (ARNI)", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypotenze. Zvážit ponechání jen u srdečního selhání.", "col": "red"},

    # === HYPERTENZE - DIURETIKA ===
    {"brands": ["amiclaran", "amicloton", "apo-a1milzide", "furon", "hypotylin", "indap", "indapamid", "verospiron", "hydrochlorothiazid"], "gen": "Diuretikum", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypovolemie. Zvážit ponechání u srdečního selhání.", "col": "red"},

    # === HYPERTENZE - BETA BLOKÁTORY ===
    {"brands": ["acecor", "obsidan", "apo-acebutol", "pindol", "apo-metopro", "propranolol", "apo-nadol", "rivocor", "atehexal", "sandonorm"], "gen": "Beta-blokátor", "grp": "Kardio", "act": "PONECHAT", "info": "Kardioprotekce.", "col": "green"},
    {"brands": ["atenobene", "atenol", "sectral", "atenolol", "sobycir", "betaloc", "sotahexal", "betamed", "tenoloc", "betasyn"], "gen": "Beta-blokátor", "grp": "Kardio", "act": "PONECHAT", "info": "Kardioprotekce.", "col": "green"},
    {"brands": ["tenoretic", "betaxa", "tenormin", "bisocard", "trimepranol", "bisogamma", "tyrez", "bisoprolol", "vasocardin", "brevibloc"], "gen": "Beta-blokátor", "grp": "Kardio", "act": "PONECHAT", "info": "Kardioprotekce.", "col": "green"},
    {"brands": ["visken", "carvesan", "catenol", "bloxazoc", "celectol", "betaxolol", "combiso", "concor", "corotenol", "corvitol"], "gen": "Beta-blokátor", "grp": "Kardio", "act": "PONECHAT", "info": "Kardioprotekce.", "col": "green"},
    {"brands": ["egilok", "emzok", "lokren", "logimax", "metoprolol", "nebilet", "nebivolol", "apo-carve", "atram", "carvediol"], "gen": "Beta-blokátor", "grp": "Kardio", "act": "PONECHAT", "info": "Kardioprotekce.", "col": "green"},
    {"brands": ["coreton", "coryol", "dilatre", "dilatrend", "taliton", "trandate"], "gen": "Beta-blokátor", "grp": "Kardio", "act": "PONECHAT", "info": "Kardioprotekce.", "col": "green"},

    # === HYPERTENZE - BLOKÁTORY CA KANÁLŮ ===
    {"brands": ["adalat", "afiten", "agen", "amilostad", "amlator", "amlodipin", "amlop", "amloratio", "amlozek", "apo-amlo"], "gen": "Blokátor Ca kanálů", "grp": "Kardio", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["ardifen", "auronal", "caduet", "cardilopin", "cinarizin", "cordafen", "cordipin", "corinfar", "diacordin", "diltan"], "gen": "Blokátor Ca kanálů", "grp": "Kardio", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["felodipin", "hipres", "isoptin", "kapidin", "lacipil", "lekoptin", "lomir", "lusopress", "nifedipin", "nimotop"], "gen": "Blokátor Ca kanálů", "grp": "Kardio", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["nitrepress", "nitresan", "nitresdipin", "normodipine", "norvasc", "orcal", "plendil", "presid", "recotens", "sponit"], "gen": "Blokátor Ca kanálů", "grp": "Kardio", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["syocor", "tensigal", "torrela", "unipres", "vasexten", "verahexal", "verepamil", "verogalid", "zorem"], "gen": "Blokátor Ca kanálů", "grp": "Kardio", "act": "PONECHAT", "info": "-", "col": "green"},

    # === HYPERTENZE - CENTRÁLNÍ A ALFA BLOKÁTORY ===
    {"brands": ["cynt", "dopegyt", "moxogamma", "moxonidin", "moxostad", "rilmenidin", "tenaxum", "doxazosin", "ebrantil", "hytrin", "kamiren", "zoxon", "urapidil", "labetelol"], "gen": "Centrální / Alfa blokátory", "grp": "Kardio", "act": "PONECHAT", "info": "-", "col": "green"},
    
    # === HYPOLIPIDEMIKA ===
    {"brands": ["ezetrol", "ezetimib", "lipanthyl", "fenofibrat"], "gen": "Fibráty / Ezetrol", "grp": "Hypolipidemika", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko myopatie.", "col": "red"},
    {"brands": ["atorvastatin", "sorvasta", "tulip", "rosuvastatin", "torvacard", "atoris", "sortis"], "gen": "Statin", "grp": "Hypolipidemika", "act": "PONECHAT", "info": "Snižují riziko CMP, IM.", "col": "green"},

    # === ANTIARYTMIKA / NITRÁTY ===
    {"brands": ["cordarone", "sedacoron", "amiodaron", "ritmonorm", "digoxin"], "gen": "Antiarytmikum", "grp": "Kardio", "act": "PONECHAT", "info": "Amiodaron: CAVE na hypokalemii a hypomagnezémii.", "col": "green"},
    {"brands": ["nitromint", "cardiket", "mono mack", "isoket"], "gen": "Nitráty", "grp": "Kardio", "act": "PONECHAT", "info": "CAVE na hypovolemii.", "col": "green"},

    # === ANTIAGREGACE & ANTIKOAGULACE ===
    {"brands": ["anopyrin", "godasal", "stacyl", "stacly", "aspirin", "acylpyrin", "anp", "asketon"], "gen": "ASA", "grp": "Antiagregace", "act": "PONECHAT", "info": "Vysadit v den výkonu nebo 7 dní předem u výkonů s vysokým rizikem krvácení. Ponechat u duální terapie.", "col": "green"},
    {"brands": ["trombex", "plavix", "clopidogrel", "zylagren", "zyllt", "iscover", "platel"], "gen": "Clopidogrel", "grp": "Antiagregace", "act": "VYSADIT 7 DNÍ PŘEDEM", "info": "Vysoké riziko krvácení.", "col": "red"},
    {"brands": ["warfarin", "lawarin"], "gen": "Warfarin", "grp": "Antikoagulace", "act": "VYSADIT 3-5 DNÍ PŘEDEM", "info": "Nutný bridging dle INR.", "col": "red"},
    {"brands": ["eliquis", "apixaban", "xarelto", "rivaroxaban", "pradaxa", "dabigatran", "lixiana", "edoxaban"], "gen": "NOAK", "grp": "NOAK", "act": "VYSADIT 1 NEBO 2 DNY PŘEDEM", "info": "1 den předem (standard) nebo 2 dny (vysoké riziko). ⚠️ Eliminaci může ovlivňovat funkce ledvin!", "col": "red"},

    # === ENDOKRINOLOGIE & DIABETES ===
    {"brands": ["euthyrox", "letrox", "thyrozol", "jodid", "eutyrox"], "gen": "Levothyroxin", "grp": "Štítná žláza", "act": "PONECHAT", "info": "Substituce se nepřerušuje.", "col": "green"},
    {"brands": ["metformin", "stadamet", "siofor", "glucophage", "metfogamma", "mulado"], "gen": "Metformin", "grp": "Antidiabetikum", "act": "VYSADIT 24h PŘEDEM", "info": "Vysadit u středních/velkých výkonů. U malých lze ponechat. ⚠️ Eliminaci ovlivňují ledviny!", "col": "red"},
    {"brands": ["jardiance", "forxiga", "invokana", "synjardy", "xigduo"], "gen": "Glifloziny (SGLT2)", "grp": "Antidiabetikum", "act": "VYSADIT 3-4 DNY PŘEDEM", "info": "Riziko euglykemické ketoacidózy. ⚠️ Eliminaci ovlivňují ledviny!", "col": "red"},
    {"brands": ["bydureon", "byetta", "victoza", "ozempic", "trulicity", "rybelsus"], "gen": "GLP-1 agonisté", "grp": "Diabetes", "act": "VYSADIT V DEN VÝKONU", "info": "Kontroly glykémie á 4-6 hod.", "col": "red"},
    {"brands": ["januvia", "sitagliptin", "trajenta", "vipidia", "galvus", "pioglitazon", "actos"], "gen": "Gliptiny / Pioglitazon", "grp": "Diabetes", "act": "VYSADIT V DEN VÝKONU", "info": "-", "col": "red"},
    {"brands": ["amaryl", "glimepirid", "oltar", "diaprel", "gliklazid", "glyclada"], "gen": "Sulfonylurea", "grp": "Diabetes", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypoglykémie.", "col": "red"},
    {"brands": ["novorapid", "actrapid", "humalog", "apidra", "fiasp"], "gen": "Insulin (Bolus)", "grp": "Diabetes", "act": "NEPODÁVAT", "info": "Při lačnění nepodávat.", "col": "red"},
    {"brands": ["tresiba", "lantus", "toujeo", "levemir", "abslaglar"], "gen": "Insulin (Bazál)", "grp": "Diabetes", "act": "PONECHAT / REDUKOVAT", "info": "Ponechat jak nastaveno z předchozího dne, perioperačně bazální režim.", "col": "blue"},
    {"brands": ["prednison", "medrol", "fortecortin", "dexamed", "hydrocortison"], "gen": "Kortikoid p.o.", "grp": "Steroidy", "act": "SUBSTITUCE (PŘI DÁVCE > 5mg Prednisonu)", "info": "Do 5mg ponechat. Nad 5mg: střední výkon 50mg i.v., velký výkon 100mg i.v.", "col": "blue"},
    {"brands": ["tamoxifen", "raloxifen", "evista"], "gen": "SERM (Hormony)", "grp": "Endokrino", "act": "PONECHAT S LMWH", "info": "Vysadit POUZE u vysokého rizika TEN (Raloxifen 3 dny, Tamoxifen 2-3 týdny předem).", "col": "green"},

    # === BONE & OSTEOPORÓZA ===
    {"brands": ["alendronat", "ibandronat", "risedronat", "fosamax", "bonviva", "actonel"], "gen": "Bisfosfonáty", "grp": "Osteoporóza", "act": "VYSADIT V DEN VÝKONU", "info": "Zapíjí se velkým množstvím vody, riziko aspirace.", "col": "red"},

    # === RESPIRAČNÍ ===
    {"brands": ["ventolin", "salbutamol", "buventol", "ecosal"], "gen": "Salbutamol (SABA)", "grp": "Inhalace", "act": "PONECHAT A POSÍLIT", "info": "Ráno i před sál prevence spasmu. Posílit i pokud užívá jen dlp.", "col": "green"},
    {"brands": ["berodual", "ipratropium", "atrovent"], "gen": "Fenoterol/Ipratropium", "grp": "Inhalace", "act": "PONECHAT A POSÍLIT", "info": "Nevysazovat. Posílit více vdechy.", "col": "green"},
    {"brands": ["spiriva", "braltus", "biskair"], "gen": "Tiotropium (LAMA)", "grp": "Inhalace", "act": "PONECHAT A POSÍLIT", "info": "Udržet bronchodilataci. Posílit více vdechy.", "col": "green"},
    {"brands": ["seretide", "symbicort", "combair", "foster", "duoresp", "salmex", "trixeo", "trelegy"], "gen": "ICS/LABA/LAMA", "grp": "Inhalace", "act": "PONECHAT A POSÍLIT", "info": "Pokud > 2 vdechy denně: Hydrocortison 50/100mg i.v.", "col": "green"},
    {"brands": ["theofylin", "aminofylin", "syntophyllin", "euphyllin", "tezeo", "theoplus"], "gen": "Methylxanthiny", "grp": "Pneumo", "act": "VYSADIT", "info": "Riziko arytmií a neurotoxicity. NEPODÁVAT do premedikace!", "col": "red"},
    {"brands": ["montelukast", "castispir", "singulair", "asmen"], "gen": "Inhibitory leukotrienů", "grp": "Pneumo", "act": "PONECHAT", "info": "-", "col": "green"},

    # === PSYCHIATRIE / NEUROLOGIE / BOLEST ===
    {"brands": ["neurol", "xanax", "lexaurin", "diazepam", "rivotril", "frontin", "buspiron"], "gen": "Anxiolytika / BZD", "grp": "Psychofarmaka", "act": "PONECHAT", "info": "Nevysazovat ani u starších osob!", "col": "green"},
    {"brands": ["zolpidem", "stilnox", "hypnogen", "sanval", "adorma"], "gen": "Zolpidem", "grp": "Hypnotikum", "act": "RÁNO NEPODÁVAT", "info": "Riziko sedace.", "col": "red"},
    {"brands": ["citalec", "cipralex", "zoloft", "trittico", "mirtazapin", "argofan", "elicea", "asentra"], "gen": "Antidepresiva", "grp": "Psychofarmaka", "act": "PONECHAT", "info": "Pozor na iMAO (vysadit 2 týdny předem, absolutní KI ephedrin!).", "col": "green"},
    {"brands": ["lithium", "lithium carbonicum"], "gen": "Lithium", "grp": "Stabilizátor nálady", "act": "PONECHAT", "info": "Vysadit 3 dny předem POUZE u velkých operačních výkonů.", "col": "green"},
    {"brands": ["guanfacin", "intuniv"], "gen": "Guanfacin", "grp": "ADHD", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["ritalin", "concerta", "atomoxetin", "strattera", "bitinex"], "gen": "Methylfenidát/Atomoxetin", "grp": "ADHD", "act": "VYSADIT V DEN VÝKONU", "info": "-", "col": "red"},
    {"brands": ["zyprexa", "olanzapin", "tiaprid", "buronil", "quetiapin", "ketiapin", "risperdal"], "gen": "Antipsychotika", "grp": "Psychofarmaka", "act": "PONECHAT", "
