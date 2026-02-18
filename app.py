import streamlit as st

# Nastavení stránky - layout centered je lepší pro mobil
st.set_page_config(page_title="Anesteziologický asistent", layout="centered")

# --- CSS STYLOVÁNÍ (MOBILE FIRST) ---
st.markdown("""
    <style>
    /* Zarovnání nadpisu */
    h1 { text-align: center; color: #004a99; margin-bottom: 5px; }
    h3 { color: #333; font-size: 1.1rem; margin-top: 20px; }
    
    /* Design karet */
    .drug-card {
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        border-left: 6px solid #ccc;
        background-color: #f9f9f9;
        color: #1f1f1f;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Barvy */
    .border-red { border-left-color: #d93025; background-color: #fff0f0; }
    .border-green { border-left-color: #188038; background-color: #e6f4ea; }
    .border-blue { border-left-color: #1967d2; background-color: #e8f0fe; }
    .border-yellow { border-left-color: #f9ab00; background-color: #fef7e0; }

    /* Texty */
    .card-title { font-weight: 700; font-size: 1.15em; display: block; margin-bottom: 4px; }
    .card-generic { font-weight: 400; color: #555; font-size: 0.85em; }
    .card-rec { font-weight: 700; display: block; margin-top: 2px; font-size: 1.05em; }
    .card-info { font-size: 0.95em; font-style: italic; opacity: 0.9; display: block; margin-top: 2px; }
    </style>
    """, unsafe_allow_html=True)

# --- HLAVIČKA ---
st.markdown("<h1>🩺 Anesteziologický asistent</h1>", unsafe_allow_html=True)
st.caption("Verze 2026 | Kompletní databáze | Interní směrnice", unsafe_allow_html=True)
st.write("---")

# --- 1. VSTUPY (VŠE POD SEBOU) ---
st.subheader("1. Parametry výkonu")

# Žádné sloupce (st.columns), vše hezky pod sebou pro mobil
anestezie = st.radio("Typ anestezie:", ["Celková", "Neuroaxiální"], index=0)

st.write("") # Mezera
# Vráceno názvosloví "Rozsah výkonu"
rozsah = st.select_slider("Rozsah výkonu (Riziko krvácení):", ["Malý", "Střední", "Velký"], value="Střední")

st.divider()

st.subheader("2. Medikace")
med_text = st.text_area("Vložte text z NISu:", height=150, 
                       placeholder="Např.: Ventolin, Euthyrox, Anopyrin, Triplixam...").lower()

# --- 2. LABORKA (Podmíněná) ---
# Seznam spouštěčů pro laborku
lab_triggers = ["eliquis", "apixaban", "xarelto", "rivaroxaban", "pradaxa", "dabigatran", "jardiance", "forxiga", "synjardy", "metformin", "siofor", "glucophage"]
needs_lab = any(x in med_text for x in lab_triggers)
crcl = None

if needs_lab:
    st.info("⚠️ Nutný výpočet CrCl (DOAC / SGLT2 / Metformin)")
    with st.expander("Zadat parametry pacienta", expanded=True):
        # Tady necháme sloupce, protože čísla vedle se vejdou i na mobil
        l1, l2 = st.columns(2)
        vek = l1.number_input("Věk", 18, 100, 75)
        vaha = l2.number_input("Váha", 40, 150, 80)
        kreat = l1.number_input("Kreatinin", 40, 500, 110)
        pohl = l2.radio("Pohlaví", ["Muž", "Žena"], horizontal=True)
        
        k = 1.23 if pohl == "Muž" else 1.04
        crcl = ((140 - vek) * vaha * k) / kreat
        st.markdown(f"**CrCl: {crcl:.1f} ml/min**")

st.divider()

# --- 3. VELKÁ DATABÁZE (Sjednocená) ---
# Zde jsou všechny léky ze všech verzí
db = [
    # === RESPIRAČNÍ (Původní "běžné" léky) ===
    {"brands": ["ventolin", "salbutamol", "buventol", "ecosal"], "gen": "Salbutamol (SABA)", 
     "grp": "Inhalace", "act": "PONECHAT", "info": "Ráno i před sál prevence spasmu.", "col": "green"},
    {"brands": ["berodual", "ipratropium", "atrovent"], "gen": "Fenoterol/Ipratropium", 
     "grp": "Inhalace", "act": "PONECHAT", "info": "Nevysazovat.", "col": "green"},
    {"brands": ["spiriva", "braltus", "biskair"], "gen": "Tiotropium (LAMA)", 
     "grp": "Inhalace", "act": "PONECHAT", "info": "Udržet bronchodilataci.", "col": "green"},
    {"brands": ["seretide", "symbicort", "combair", "foster", "duoresp", "salmex", "trixeo", "trelegy"], "gen": "ICS/LABA/LAMA", 
     "grp": "Inhalace (Kombinace)", "act": "PONECHAT", "info": "Nevysazovat! Posílit dávku.", "col": "green"},
    {"brands": ["euphyllin", "tezeo", "theoplus"], "gen": "Teofylin", 
     "grp": "Methylxanthiny", "act": "PONECHAT", "info": "-", "col": "green"},

    # === ENDOKRINOLOGIE ===
    {"brands": ["euthyrox", "letrox", "thyrozol", "jodid", "eutyrox"], "gen": "Levothyroxin", 
     "grp": "Štítná žláza", "act": "PONECHAT", "info": "Substituce se nepřerušuje.", "col": "green"},
    {"brands": ["metformin", "stadamet", "siofor", "glucophage", "mulado"], "gen": "Metformin", 
     "grp": "Antidiabetikum", "act": "VYSADIT 48H", "info": "Riziko laktátové acidózy.", "col": "red"},
    {"brands": ["jardiance", "forxiga", "invokana", "synjardy"], "gen": "Gliflozin (SGLT2)", 
     "grp": "Antidiabetikum", "act": "VYSADIT 3 DNY", "info": "Riziko euglykemické ketoacidózy.", "col": "red"},
    {"brands": ["novorapid", "actrapid", "humalog", "apidra", "fiasp"], "gen": "Insulin (Bolus)", 
     "grp": "Diabetes", "act": "NEPODÁVAT", "info": "Při lačnění nepodávat.", "col": "red"},
    {"brands": ["tresiba", "lantus", "toujeo", "levemir", "abslaglar"], "gen": "Insulin (Bazál)", 
     "grp": "Diabetes", "act": "REDUKOVAT DÁVKU", "info": "Podat cca 75-80% dávky.", "col": "blue"},

    # === KARDIOVASKULÁRNÍ - BĚŽNÉ ===
    {"brands": ["anopyrin", "godasal", "stacyl", "stacly", "aspirin", "acylpyrin", "anp", "asketon"], "gen": "ASA", 
     "grp": "Antiagregace", "act": "PONECHAT", "info": "Benefit > Riziko (výjimka neurochirurgie).", "col": "green"},
    {"brands": ["trombex", "plavix", "clopidogrel", "zylagren", "zyllt"], "gen": "Clopidogrel", 
     "grp": "Antiagregace", "act": "VYSADIT 7 DNÍ", "info": "Vysoké riziko krvácení.", "col": "red"},
    {"brands": ["warfarin", "lawarin"], "gen": "Warfarin", 
     "grp": "Antikoagulace", "act": "VYSADIT 5 DNÍ", "info": "Nutný bridging LMWH (pokud INR < 1.5).", "col": "red"},
    
    {"brands": ["prestarium", "tritace", "ramipril", "perindopril", "prenessa", "telmisartan", "micardis", "lozap", "amprilan", "enap"], 
     "gen": "ACEI / Sartan", "grp": "Hypertenze", "act": "VYNECHAT V DEN OP", "info": "Riziko hypotenze.", "col": "red"},
    {"brands": ["bisoprolol", "concor", "betaloc", "egilok", "vasocardin", "nebilet", "lokren", "coryol"], 
     "gen": "Beta-blokátor", "grp": "Kardio", "act": "PONECHAT", "info": "Kardioprotekce.", "col": "green"},
    {"brands": ["agen", "amlodipin", "norvasc", "plendil", "lusopress", "isoptin", "verapamil"], 
     "gen": "BKK", "grp": "Kardio", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["furon", "furorese", "verospiron", "hydrochlorothiazid", "indapamid", "moduretic"], 
     "gen": "Diuretikum", "grp": "Hypertenze", "act": "VYNECHAT", "info": "Riziko hypovolemie.", "col": "red"},
    {"brands": ["cordarone", "sedacoron", "amiodaron", "ritmonorm", "digoxin"], 
     "gen": "Antiarytmikum", "grp": "Kardio", "act": "PONECHAT", "info": "-", "col": "green"},
     
    # === KARDIO - SLOŽITÉ (KOMBINACE) ===
    {"brands": ["entresto"], "gen": "Sacubitril/Valsartan", 
     "grp": "ARNI", "act": "RÁNO NEPODÁVAT", "info": "Riziko hypotenze.", "col": "red"},
    {"brands": ["triplixam", "tezefort", "twynsta", "amesos", "tonarssa", "lorista h", "lozap h"], "gen": "Kombinace (ACEI/Sartan/Diuret)", 
     "grp": "Kombinace", "act": "VYSADIT V DEN VÝKONU", "info": "Obsahuje ACEI/Sartan nebo diuretikum.", "col": "red"},

    # === DOAC ===
    {"brands": ["eliquis", "apixaban"], "gen": "Apixaban", "grp": "DOAC", "act": "DYNAMICKÉ", "info": "", "col": "red"},
    {"brands": ["xarelto", "rivaroxaban"], "gen": "Rivaroxaban", "grp": "DOAC", "act": "DYNAMICKÉ", "info": "", "col": "red"},
    {"brands": ["pradaxa", "dabigatran"], "gen": "Dabigatran", "grp": "DOAC", "act": "DYNAMICKÉ", "info": "", "col": "red"},

    # === NEURO / PSYCH / BOLEST ===
    {"brands": ["neurol", "xanax", "lexaurin", "diazepam", "rivotril", "frontin"], "gen": "Benzodiazepin", 
     "grp": "Anxiolytikum", "act": "PONECHAT", "info": "Prevence abstinenčního syndromu.", "col": "green"},
    {"brands": ["zolpidem", "stilnox", "hypnogen", "sanval", "adorma"], "gen": "Zolpidem", 
     "grp": "Hypnotikum", "act": "RÁNO NEPODÁVAT", "info": "Riziko sedace.", "col": "red"},
    {"brands": ["citalec", "cipralex", "zoloft", "trittico", "mirtazapin", "argofan", "elicea", "asentra"], "gen": "SSRI/SNRI", 
     "grp": "Antidepresivum", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["lyrica", "pregabalin", "gabapentin", "neurontin", "gabanox"], "gen": "Antiepileptikum", 
     "grp": "Neuro", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["nakom", "madopar", "isicom"], "gen": "L-Dopa", 
     "grp": "Antiparkinsonikum", "act": "PONECHAT", "info": "Přísně dodržet časování!", "col": "green"},

    # === ANALGETIKA & OPIÁTY ===
    {"brands": ["doreta", "zaldiar", "foxis", "palgotal", "ultracod"], "gen": "Tramadol/Paracetamol", 
     "grp": "Analgetikum (Opioid)", "act": "PONECHAT", "info": "⚠️ OPIÁT: Tolerance. Nevysazovat.", "col": "green"},
    {"brands": ["tramal", "mabron", "tramabene"], "gen": "Tramadol", 
     "grp": "Analgetikum (Opioid)", "act": "PONECHAT", "info": "⚠️ OPIÁT: Tolerance.", "col": "green"},
    {"brands": ["fentanyl", "matrifen", "durogesic", "transtec", "buprenorphin"], "gen": "Opioid (Náplast)", 
     "grp": "Analgetikum (TD)", "act": "PONECHAT - NEODLEPOVAT", "info": "⚠️ SILNÝ OPIÁT: Vysoká tolerance!", "col": "yellow"},
    {"brands": ["oxycontin", "targin", "dhc", "sevredol"], "gen": "Silný opioid (p.o.)", 
     "grp": "Analgetikum", "act": "PONECHAT", "info": "⚠️ SILNÝ OPIÁT: Nutno podat ranní dávku.", "col": "green"},

    # === OSTATNÍ (Žíly, GIT, Ionty) ===
    {"brands": ["detralex", "mobivenal", "diozen", "devenal", "cyclo 3 fort", "glyvenol"], "gen": "Venofarmaka", 
     "grp": "Cévy", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["pantoprazol", "controloc", "helides", "omeprazol", "helicid", "emanera", "nolpaza"], "gen": "PPI", 
     "grp": "GIT", "act": "PONECHAT", "info": "Prevence aspirace.", "col": "green"},
    {"brands": ["kreon", "pancreolan"], "gen": "Enzymy", 
     "grp": "GIT", "act": "VYNECHAT", "info": "Při lačnění.", "col": "red"},
    {"brands": ["kalnormin", "magnosolv", "magnesium", "vigantol"], "gen": "Suplementace", 
     "grp": "Ostatní", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["milurit", "purinol", "alopurinol"], "gen": "Allopurinol", 
     "grp": "Dna", "act": "PONECHAT", "info": "-", "col": "green"},
    {"brands": ["prednison", "medrol", "fortecortin", "dexamed"], "gen": "Kortikoid", 
     "grp": "Steroidy", "act": "SUBSTITUCE", "info": "", "col": "blue"},
     {"brands": ["betoptic", "timolol", "cosopt"], "gen": "Oční kapky", 
     "grp": "Oční", "act": "PONECHAT", "col": "green"},
]

# --- 4. LOGIKA A VÝSTUP ---
if st.button("🚀 VYHODNOTIT MEDIKACI", type="primary"):
    st.subheader("3. Doporučení pro sál")
    found_count = 0
    
    for item in db:
        # Hledáme, zda se nějaký "brand" nachází v zadaném textu
        match = next((b for b in item["brands"] if b in med_text), None)
        
        if match:
            found_count += 1
            rec = item["act"]
            info = item["info"]
            color = item["col"]
            
            # --- DYNAMICKÁ PRAVIDLA ---

            # A) KORTIKOIDY (Substituce)
            if item["act"] == "SUBSTITUCE":
                rec = "SUBSTITUCE NUTNÁ"
                if rozsah == "Malý": info = "+ 25mg Hydrocortison i.v."
                elif rozsah == "Střední": info = "+ 50-75mg Hydrocortison i.v."
                else: info = "+ 100mg Hydrocortison i.v."

            # B) DOAC (Výpočet hodin)
            # Dokument: Vysadit 1 den (24h) NEBO 2 dny (48h) u vysokého rizika
            elif item["grp"] == "DOAC":
                if rozsah == "Velký" or "Neuroaxiální" in anestezie:
                    rec = "VYSADIT 48h (2 dny)"
                    info = "Vysoké riziko krvácení / Neuroaxiální blokáda."
                else:
                    rec = "VYSADIT 24h (1 den)"
                    info = "Standardní riziko."
                
                # CrCl pojistka
                if crcl and crcl < 30:
                    info += " ⚠️ POZOR: CrCl < 30 ml/min -> Riziko akumulace! Konzultovat."

            # C) ASA (Anopyrin) u Spinálu
            elif item["grp"] == "Antiagregace" and item["act"] == "PONECHAT" and "Neuroaxiální" in anestezie:
                color = "yellow"
                info += " ⚠️ U spinální anestezie zvážit riziko (individuálně)."

            # D) SGLT2 (Jardiance) Renální
            elif "SGLT2" in item["gen"] and crcl and crcl < 30:
                 info = "Kontraindikováno při renálním selhání."

            # --- VYKRESLENÍ KARTY ---
            st.markdown(f"""
            <div class="drug-card border-{color}">
                <span class="card-title">{match.capitalize()} <span class="card-generic">({item['gen']})</span></span>
                <span class="card-rec">{rec}</span>
                <span class="card-info">{info}</span>
            </div>
            """, unsafe_allow_html=True)

    if found_count == 0:
        st.info("Žádná specifická riziková medikace nenalezena (nebo nebyla rozpoznána).")
        
    if "vysazeno" in med_text or "ex" in med_text:
        st.warning("⚠️ **Pozor:** Text obsahuje slovo 'vysazeno'/'ex'. Program nečte kontext, pouze detekuje názvy.")
