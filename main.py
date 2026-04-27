import streamlit as st
import requests
import random

st.set_page_config(page_title="Speed Mastermind Pro", page_icon="⚡")

API_KEY = "07af93a1-ca72-4828-a7e0-f646ab4c9647"

def fetch_api(endpoint):
    # Bypass attempt using direct requests with extra headers
    url = f"https://api.cricketdata.org/v1/{endpoint}?apikey={API_KEY}"
    headers = {"User-Agent": "PostmanRuntime/7.28.4", "Accept": "*/*"}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        return r.json()
    except: return None

st.title("⚡ SPEED MASTERMIND PRO")

# Sidebar for Logic Toggle
mode = st.sidebar.radio("CHOOSE MODE:", ["📡 Live API (Auto)", "📝 Manual Entry (Reliable)"])

if mode == "📡 Live API (Auto)":
    if st.button("Fetch Live Matches 🏏"):
        data = fetch_api("currentMatches")
        if data and "data" in data:
            st.session_state['m_list'] = {m["name"]: m["id"] for m in data["data"][:10]}
        else:
            st.error("API Blocked by Streamlit Cloud. Use 'Manual Entry' Mode.")

    if 'm_list' in st.session_state:
        m_name = st.selectbox("Select Match:", list(st.session_state['m_list'].keys()))
        if st.button("Get Squad"):
            s_data = fetch_api(f"match_squad?id={st.session_state['m_list'][m_name]}")
            if s_data and "data" in s_data:
                players = []
                for t in s_data["data"]: players.extend([p["name"] for p in t.get("players", [])])
                st.session_state['squad'] = sorted(list(set(players)))

else: # MANUAL MODE
    st.subheader("📝 Manual Squad Entry")
    txt = st.text_area("Copy-Paste Players from Google/Cricbuzz (Comma separated):")
    if txt: st.session_state['squad'] = [p.strip() for p in txt.split(",")]

# --- COMMON GENERATOR LOGIC ---
if 'squad' in st.session_state:
    s = st.session_state['squad']
    col1, col2 = st.columns(2)
    with col1:
        locks = st.multiselect("🔒 LOCKS:", s)
        n = st.number_input("Teams:", 1, 20, 11)
    with col2:
        trumps = st.multiselect("🃏 TRUMPS:", s)
    
    if st.button("GENERATE TEAMS 🔥"):
        st.balloons()
        for i in range(n):
            pool = [p for p in s if p not in locks]
            team = list(locks) + random.sample(pool, 11 - len(locks))
            with st.expander(f"📋 TEAM {i+1}"):
                st.write(", ".join(team))
                st.caption(f"C: {random.choice(team)} | VC: {random.choice(team)}")
                
