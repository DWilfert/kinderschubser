import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Seiten-Konfiguration für mobiles Design und dunkles Thema
st.set_page_config(
    page_title="Sabines Kinderschubser App",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisierung des internen Speichers (Session State)
if "settings" not in st.session_state:
    st.session_state.settings = {"name": "", "personalnummer": "", "arbeitsstaette": "", "soll_stunden": ""}
if "entries" not in st.session_state:
    st.session_state.entries = {}

# Hilfsfunktion zur Berechnung der Arbeitszeit
def calculate_hours_str(kommen, gehn, pause):
    try:
        if not kommen or not gehn or pd.isna(kommen) or pd.isna(gehn): return ""
        k_h, k_m = map(int, str(kommen).replace(".", ":").split(":"))
        g_h, g_m = map(int, str(gehn).replace(".", ":").split(":"))
        p_m = 0
        if pause and not pd.isna(pause):
            if ":" in str(pause) or "." in str(pause):
                ph, pm = map(int, str(pause).replace(".", ":").split(":"))
                p_m = ph * 60 + pm
            else: p_m = int(pause)
        t_kommen, t_gehn = k_h * 60 + k_m, g_h * 60 + g_m
        if t_gehn <= t_kommen: t_gehn += 24 * 60
        total_minutes = t_gehn - t_kommen - p_m
        if total_minutes < 0: return "0:00h"
        return f"{total_minutes // 60}:{total_minutes % 60:02d}h"
    except: return ""

# --- SIDEBAR MENÜ (Anordnung der Navigation) ---
with st.sidebar:
    st.title("🧭 Navigation")
    # Das Logo wird geladen, wenn es existiert
    try:
        st.image("logox.png", width=100)
    except:
        pass
    st.subheader("Sabine´s Kinderschubser App")
    
    # Auswahl der Ansicht
    view = st.radio(
        "Gehe zu:",
        ["Einstellungen", "Zeiterfassung", "Übersicht & Druck", "Arbeitgeber-Bericht"]
    )
# --- 1. EINSTELLUNGEN ---
if view == "Einstellungen":
    st.header("⚙️ Einstellungen")
    
    # Eingabefelder genau wie in Kivy
    name = st.text_input("Name", st.session_state.settings["name"])
    pers_nr = st.text_input("Personalnummer", st.session_state.settings["personalnummer"])
    staette = st.text_input("Arbeitsstätte", st.session_state.settings["arbeitsstaette"])
    soll = st.text_input("Soll-Stunden", st.session_state.settings["soll_stunden"])
    
    if st.button("Speichern", type="primary"):
        st.session_state.settings = {
            "name": name,
            "personalnummer": pers_nr,
            "arbeitsstaette": staette,
            "soll_stunden": soll
        }
        st.success("Einstellungen im Sitzungsspeicher gesichert!")

# --- 2. ZEITERFASSUNG ---
elif view == "Zeiterfassung":
    st.header("📝 Zeiterfassung")
    
    # Monats- und Jahresauswahl über Dropdowns für einfache Bedienung am Handy
    col_m, col_j = st.columns(2)
    with col_m:
        monat = st.selectbox("Monat", ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"], index=datetime.now().month - 1)
    with col_j:
        jahr = st.number_input("Jahr", min_value=2000, max_value=2100, value=datetime.now().year)
    
    m_idx = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"].index(monat) + 1
    
    # Tage des Monats ermitteln
    next_m = datetime(jahr + 1, 1, 1) if m_idx == 12 else datetime(jahr, m_idx + 1, 1)
    last_day = (next_m - timedelta(days=1)).day
    wd_ger = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    
    # Tabelle für die Eingabe vorbereiten
    rows = []
    for day in range(1, last_day + 1):
        d_str = f"{jahr}-{m_idx:02d}-{day:02d}"
        wd_idx = datetime(jahr, m_idx, day).weekday()
        wochentag = wd_ger[wd_idx]
        
        # Bestehende Daten laden oder leere Zeile erstellen
        existing = st.session_state.entries.get(d_str, {"kommen": "", "gehn": "", "pause": "", "bemerkung": ""})
        
        # Berechnung der Stunden für die Anzeige
        stunden = calculate_hours_str(existing["kommen"], existing["gehn"], existing["pause"])
        if not stunden:
            stunden = "0:00h" if existing["kommen"] else ""
            
        rows.append({
            "Datum": f"{wochentag}, {day:02d}.{m_idx:02d}.",
            "Kommen": existing["kommen"],
            "Gehn": existing["gehn"],
            "Pause": existing["pause"],
            "Bemerkung": existing["bemerkung"],
            "Stunden": stunden,
            "_date_key": d_str
        })
    
    df = pd.DataFrame(rows)
    
    # Anzeige als interaktiver Daten-Editor (Smartphone-optimiert)
    st.write("Tippen Sie direkt in die Felder, um Ihre Zeiten einzutragen:")
    edited_df = st.data_editor(
        df,
        column_config={
            "Datum": st.column_config.TextColumn("Datum", disabled=True),
            "Kommen": st.column_config.TextColumn("Kommen (HH:MM)"),
            "Gehn": st.column_config.TextColumn("Gehn (HH:MM)"),
            "Pause": st.column_config.TextColumn("Pause"),
            "Bemerkung": st.column_config.TextColumn("Bemerkung"),
            "Stunden": st.column_config.TextColumn("Stunden", disabled=True),
            "_date_key": None # Versteckte Spalte für die Zuordnung
        },
        hide_index=True,
        use_container_width=True
    )
    
    if st.button("Monat Speichern", type="primary"):
        # Daten zurück in den Session State schreiben und Stunden neu berechnen
        for index, row in edited_df.iterrows():
            d_k = row["_date_key"]
            st.session_state.entries[d_k] = {
                "kommen": str(row["Kommen"]).strip() if not pd.isna(row["Kommen"]) else "",
                "gehn": str(row["Gehn"]).strip() if not pd.isna(row["Gehn"]) else "",
                "pause": str(row["Pause"]).strip() if not pd.isna(row["Pause"]) else "",
                "bemerkung": str(row["Bemerkung"]).strip() if not pd.isna(row["Bemerkung"]) else ""
            }
        st.success("Zeiten erfolgreich für diese Sitzung gespeichert! Wechseln Sie zur Übersicht zum Drucken.")
# --- 3. ÜBERSICHT & DRUCK ---
elif view == "Übersicht & Druck":
    st.header("📊 Übersicht & Druck")
    
    # Nutzerinfo anzeigen
    st.info(f"👤 Name: {st.session_state.settings['name'] or 'Unbekannt'} | ⏱️ Soll-Stunden: {st.session_state.settings['soll_stunden'] or '-'}")
    
    # Monatsfilter für den Bericht
    monat_rep = st.selectbox("Berichtsmonat wählen", ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"], index=datetime.now().month - 1)
    jahr_rep = st.number_input("Berichtsjahr wählen", min_value=2000, max_value=2100, value=datetime.now().year, key="ov_year")
    
    m_idx = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"].index(monat_rep) + 1
    next_m = datetime(jahr_rep + 1, 1, 1) if m_idx == 12 else datetime(jahr_rep, m_idx + 1, 1)
    last_day = (next_m - timedelta(days=1)).day
    
    # Daten für die schreibgeschützte Übersicht zusammenstellen
    report_rows = []
    for day in range(1, last_day + 1):
        d_str = f"{jahr_rep}-{m_idx:02d}-{day:02d}"
        day_data = st.session_state.entries.get(d_str, {"kommen": "", "gehn": "", "pause": "", "bemerkung": ""})
        ch = calculate_hours_str(day_data["kommen"], day_data["gehn"], day_data["pause"])
        disp_h = ch if ch else "0:00h" if day_data["kommen"] else ""
        
        report_rows.append({
            "Tag": f"{day:02d}.",
            "Kommen": day_data["kommen"],
            "Gehn": day_data["gehn"],
            "Pause": day_data["pause"],
            "Bemerkung": day_data["bemerkung"],
            "Stunden": disp_h
        })
    
    df_rep = pd.DataFrame(report_rows)
    
    # Saubere, schreibgeschützte Tabelle auf weißem/hellem Grund
    st.dataframe(df_rep, hide_index=True, use_container_width=True)
    
    # Daten-Sicherung als Excel-Download (Perfekt fürs Handy!)
    st.write("💾 Daten dauerhaft sichern:")
    try:
        import io
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_rep.to_excel(writer, sheet_name='Zeiterfassung', index=False)
        
        st.download_button(
            label="Als Excel-Datei (.xlsx) herunterladen",
            data=buffer.getvalue(),
            file_name=f"Zeiterfassung_{monat_rep}_{jahr_rep}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except:
        # Fallback zu CSV, falls xlsxwriter nicht installiert ist
        csv = df_rep.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Als CSV-Datei (.csv) herunterladen",
            data=csv,
            file_name=f"Zeiterfassung_{monat_rep}_{jahr_rep}.csv",
            mime="text/csv"
        )

# --- 4. ARBEITGEBER-BERICHT ---
elif view == "Arbeitgeber-Bericht":
    st.header("📋 Arbeitgeber-Bericht")
    
    # Arbeitgeber-relevante Infos oben platzieren
    st.info(f"👤 Name: {st.session_state.settings['name'] or 'Unbekannt'} | 🆔 Personalnummer: {st.session_state.settings['personalnummer'] or '-'}")
    
    monat_emp = st.selectbox("Monat für Arbeitgeber", ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"], index=datetime.now().month - 1)
    jahr_emp = st.number_input("Jahr für Arbeitgeber", min_value=2000, max_value=2100, value=datetime.now().year, key="emp_year")
    
    # Bemerkung EIN/AUS Schalter genau wie in Kivy (hier als komfortable Checkbox)
    show_remark = st.checkbox("Spalte 'Bemerkung' im Bericht anzeigen", value=True)
    
    m_idx = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"].index(monat_emp) + 1
    next_m = datetime(jahr_emp + 1, 1, 1) if m_idx == 12 else datetime(jahr_emp, m_idx + 1, 1)
    last_day = (next_m - timedelta(days=1)).day
    
    emp_rows = []
    for day in range(1, last_day + 1):
        d_str = f"{jahr_emp}-{m_idx:02d}-{day:02d}"
        day_data = st.session_state.entries.get(d_str, {"kommen": "", "gehn": "", "pause": "", "bemerkung": ""})
        ch = calculate_hours_str(day_data["kommen"], day_data["gehn"], day_data["pause"])
        disp_h = ch if ch else "0:00h" if day_data["kommen"] else ""
        
        row_entry = {
            "Tag": f"{day:02d}.",
            "Kommen": day_data["kommen"],
            "Gehn": day_data["gehn"],
            "Pause": day_data["pause"],
            "Stunden": disp_h
        }
        if show_remark:
            # Fügt Bemerkung an vorletzter Stelle ein, wenn aktiviert
            row_entry["Bemerkung"] = day_data["bemerkung"]
            
        emp_rows.append(row_entry)
        
    df_emp = pd.DataFrame(emp_rows)
    
    # Spaltenreihenfolge für saubere Anzeige korrigieren falls Bemerkung aktiv
    if show_remark and not df_emp.empty:
        df_emp = df_emp[["Tag", "Kommen", "Gehn", "Pause", "Bemerkung", "Stunden"]]
        
    st.dataframe(df_emp, hide_index=True, use_container_width=True)
    
    st.caption("💡 Tipp: Nutzen Sie die Druckfunktion Ihres Webbrowsers (Strg+P oder über das Browsermenü am Handy), um diese Ansicht direkt als sauberes PDF zu drucken.")
