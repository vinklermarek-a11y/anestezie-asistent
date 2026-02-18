import streamlit as st

# Nastavení stránky
st.set_page_config(page_title="Anesteziologický asistent", layout="centered")

# --- CSS STYLOVÁNÍ ---
st.markdown("""
    <style>
    h1 { text-align: center; color: #004a99; margin-bottom: 0px; }
    div.block-container { padding-top: 1rem; }
    
    .drug-card {
        padding: 8px 12px;
        border-radius: 6px;
        margin-bottom: 6px;
        border-left: 6px solid #ccc;
        background-color: #f9f9f9;
        color: #1f1f1f;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    .border-red { border-left-color: #d93025; background-color: #fce8e6; }
    .border-green { border-left-color: #188038; background-color: #e6f4ea; }
    .border-blue { border-left-color: #1967d2; background-color: #e8f0fe; }
    .border-yellow { border-left-color: #f9ab00; background-color: #fef7e0; }

    .card-title { font-weight: 700; font-size: 1.1em; display: block; }
    .card-generic { font-weight: 400; color: #555; font-size: 0.85em; }
    .card-rec { font-weight: 700; display: block; margin-top: 2px; }
    .card-info { font-size: 0.9em; font-style: italic; opacity: 0.9; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- HLAVIČKA ---
st.markdown("<h1>🩺 Anesteziologický asistent</h1>", unsafe_allow_html=True)
st.caption("Verze 11.0 | Opioidy & Tolerance | Interní směrnice", unsafe_allow_html=True)

# --- 1. VSTUPY ---
st.write("---")
c1, c2 = st.columns([1, 1])
anestezie = c1.radio("Anestezie:", ["Celková", "Neuroaxiální"])
rozsah = c2.select_slider("Riziko krvácení:", ["Malé", "Střední", "Velké"], value="Střední")

med_text = st.text_area("Medikace (vložte i s překlepy):", height=150, 
                       placeholder="Např.: Doreta, Transtec, Zaldiar, Eliquis...").lower()

# --- 2. LABORKA ---
lab_triggers = ["eliquis", "apixaban", "xarelto", "rivaroxaban", "pradaxa", "dabigatran", "jardiance", "forxiga", "synjardy"]
needs_lab = any(x in med_text for x in lab_triggers)
crcl = None

if needs_lab:
    with st.expander("⚠️ Nutný výpočet CrCl (DOAC / SGLT2)", expanded=True):
        l1, l2 = st.columns(2)
        vek = l1.number_input("Věk", 18, 100, 75)
        vaha = l2.number_input("Váha", 40, 150, 80)
        kreat = l1.number_input("Kreatinin", 40, 500, 110)
        pohl = l2.radio("Pohlaví", ["Muž", "Žena"], horizontal=True)
        k = 1.23 if pohl == "Muž" else 1.04
        crcl = ((140 - vek) * vaha * k) / kreat
        st.markdown(f"**CrCl: {crcl:.1f} ml/min**")

st.write("---")

# --- 3. DATABÁZE LÉČIV ---
db = [
    # === NOVÉ: OPIÁTY & ANALGETIKA ===
    {"brands": ["doreta", "zaldiar", "foxis", "palgotal", "ultracod", "zillt"], "gen": "Tramadol/Paracetamol", 
     "grp": "Analgetikum (Opioid)", "act": "PONECHAT", "info": "⚠️ OPIÁT: Možný rozvoj tolerance. Nevysazovat (riziko withdrawal).", "col": "green"},
    
    {"brands": ["tramal", "mabron", "tramabene", "tramadol"], "gen": "Tramadol", 
     "grp": "Analgetikum (Opioid)", "act": "PONECHAT", "info": "⚠️ OPIÁT: Možný rozvoj tolerance.", "col": "green"},

    {"brands": ["fentanyl", "matrifen", "durogesic", "adamon", "victanyl"], "gen": "Fentanyl (Náplast)", 
     "grp": "Analgetikum (TD)", "act": "PONECHAT - NEODLEPOVAT", "info": "⚠️ SILNÝ OPIÁT: Vysoká tolerance! Při odlepení riziko krutých bolestí.", "col": "yellow"},

    {"brands": ["transtec", "buprenorphin", "buprenorfin"], "gen": "Buprenorfin (Náplast)", 
     "grp": "Analgetikum (TD)", "act": "PONECHAT - NEODLEPOVAT", "info": "⚠️ OPIÁT: Vysoká tolerance. Částečný agonista/antagonista.", "col": "yellow"},

    {"brands": ["oxycontin", "oxycodon", "targin", "dhc", "dhc continus", "sevredol", "mst continus"], "gen": "Silný opioid (p.o.)", 
     "grp": "Analgetikum", "act": "PONECHAT", "info": "⚠️ SILNÝ OPIÁT: Tolerance. Nutno podat ranní dávku.", "col": "green"},

    {"brands": ["doreta", "zaldiar", "foxis", "palgotal", "ultracod"], "gen": "Tramadol/Paracetamol", 
     "grp": "Analgetikum", "act": "PONECHAT", "info": "⚠️ OPIÁT: Tolerance.", "col": "green"},

    # === KARDIO ===
    {"brands": ["entresto"], "gen": "Sacubitril/Valsartan", "grp": "ARNI", "act": "RÁNO NEPODÁVAT", "info": "Riziko hypotenze.", "col": "red"},
    {"brands": ["triplixam", "tezefort", "twynsta", "amesos", "tonarssa"], "gen": "Kombinace (ACEI/Sartan)", 
     "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Obsahuje ACEI/Sartan nebo diuretikum.", "col": "red"},
    {"brands": ["lorista h", "lozap h", "moduretic", "furon", "furorese", "verospiron", "indapamid", "agen h"], 
     "gen": "Diuretikum", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypovolemie.", "col": "red"},
    {"brands": ["prestarium", "ramipril", "lozap", "lorista", "amprilan", "enap"], 
     "gen": "ACEI / Sartan", "grp": "Hypertenze", "act": "VYSADIT V DEN VÝKONU", "info": "Riziko hypotenze.", "col": "red"},
    
    {"brands": ["betaloc", "betaloc sr", "betaloc zok", "concor", "concor cor", "coryol", "nebilet", "egilok", "bisoprolol"], 
     "gen": "Beta-blokátor", "grp": "Kardio", "act": "PONECHAT", "info": "Kardioprotekce.", "col": "green"},
    {"brands": ["agen", "amlodipin", "sortis", "atoris", "torvacard", "tulip"], 
     "gen": "CCB / Statin", "grp": "Kardio", "act": "PONECHAT", "info": "-", "col": "green"},

    # === DIABETES ===
    {"brands": ["novorapid", "actrapid", "humalog", "apidra", "fiasp"], "gen": "Insulin (Bolus)", 
     "grp": "Diabetes", "act": "NEPODÁVAT", "info": "Riziko hypoglykemie.", "col": "red"},
    {"brands": ["tresiba", "lantus", "toujeo", "levemir"], "gen": "Insulin (Bazál)", 
     "grp": "Diabetes", "act": "REDUKOVAT DÁVKU", "info": "Podat cca 75-80% dávky.", "col": "blue"},
    {"brands": ["jardiance", "forxiga", "synjardy", "invokana"], "gen": "SGLT2 (Gliflozin)", 
     "grp": "Diabetes", "act": "VYSADIT 3 DNY", "info": "Riziko ketoacidózy.", "col": "red"},
    {"brands": ["oltar", "glimepirid", "gliklazid", "glyclada"], "gen": "Sulfonylurea", 
     "grp": "Diabetes", "act": "NEPODÁVAT", "info": "Riziko hypoglykémie.", "col": "red"},

    # === KRVÁCENÍ ===
    {"brands": ["anopyrin", "godasal", "stacyl", "stacly", "aspirin", "anp", "asketon"], "gen": "ASA", 
     "grp": "Antiagregace", "act": "PONECHAT", "info": "Benefit > Riziko.", "col": "green"},
    {"brands": ["zyllt", "trombex", "plavix", "clopidogrel"], "gen": "Clopidogrel", 
     "grp": "Antiagregace", "act": "VYSADIT 7 DNÍ", "info": "Vysoké riziko krvácení.", "col": "red"},
    {"brands": ["eliquis", "apixaban", "xarelto", "pradaxa"], "gen": "DOAC", 
     "grp": "Antikoagulace", "act": "DYNAMICKÉ", "info": "-", "col": "red"},

    # === OSTATNÍ ===
    {"brands": ["milurit", "purinol", "alopurinol"], "gen": "Allopurinol", "grp": "Dna", "act": "PONECHAT", "col": "green"},
    {"brands": ["detralex", "devenal", "mobivenal"], "gen": "Venofarmaka", "grp": "Cévy", "act": "PONECHAT", "col": "green"},
    {"brands": ["trixeo", "trelegy", "atrovent", "berodual", "ventolin"], "gen": "Inhalace", "grp": "Pneumo", "act": "PONECHAT", "info": "Posílit dávku.", "col": "green"},
    {"brands": ["betoptic", "timolol", "cosopt"], "gen": "Oční kapky", "grp": "Oční", "act": "PONECHAT", "col": "green"},
    {"brands": ["kreon", "pancreolan"], "gen": "Enzymy", "grp": "GIT", "act": "VYNECHAT", "info": "Při lačnění.", "col": "red"},
]

# --- 4. LOGIKA A VÝSTUP ---
if st.button("🚀 VYHODNOTIT SOUBOR LÉKŮ", type="primary"):
    st.subheader("3. Doporučení pro sál")
    found_count = 0
    
    for item in db:
        match = next((b for b in item["brands"] if b in med_text), None)
        
        if match:
            found_count += 1
            rec = item["act"]
            info = item["info"]
            color = item["col"]
            
            # A) DOAC
            if item["grp"] == "Antikoagulace" and item["act"] == "DYNAMICKÉ":
                if rozsah == "Velké" or "Neuroaxiální" in anestezie:
                    rec = "VYSADIT 48h (2 dny)"
                else:
                    rec = "VYSADIT 24h (1 den)"
                if crcl and crcl < 30: info = f"CrCl {crcl:.0f} ml/min -> Riziko akumulace! Konzultovat."

            # B) ASA u Spinálu
            if "ASA" in item["gen"] and "Neuroaxiální" in anestezie:
                color = "yellow"
                info += " ⚠️ U spinálu zvážit (individuální riziko)."

            # C) SGLT2 Renální
            if "SGLT2" in item["gen"] and crcl and crcl < 30:
                 info = "Kontraindikováno při renálním selhání."

            # Vykreslení
            st.markdown(f"""
            <div class="drug-card border-{color}">
                <span class="card-title">{match.capitalize()} <span class="card-generic">({item['gen']})</span></span>
                <span class="card-rec">{rec}</span>
                <span class="card-info">{info}</span>
            </div>
            """, unsafe_allow_html=True)
            
    if found_count == 0:
        st.info("Žádné specifické léky nebyly rozpoznány.")

    if "vysazeno" in med_text or "ex" in med_text:
        st.warning("⚠️ **Pozor:** Text obsahuje slovo 'vysazeno'/'ex'. Program nečte kontext, pouze detekuje názvy.")
