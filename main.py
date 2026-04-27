import streamlit as st
import requests
import random
import time

# App Setup
st.set_page_config(page_title="Speed Mastermind", page_icon="⚡", layout="wide")

# API KEY
API_KEY = "07af93a1-ca72-4828-a7e0-f646ab4c9647"

# --- ADVANCED API CALLER ---
def fetch_api_data(endpoint):
    # Base URL ko direct use karne ke bajaye params mein todenge
    base_url = "https://api.cricketdata.org/v1/"
    full_url = f"{base_url}{endpoint}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    params = {"apikey": API_KEY}
    
    try:
        # Streamlit session ko use karke connection open rakhna
        with requests.Session() as s:
            response = s.get(full_url, params=params, headers=headers, timeout=20)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Server Status: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# --- LOGIC ---
st.title("⚡ SPEED MASTERMIND PRO")

# Sidebar for Match Selection
st.sidebar.header("📡 Live Connection")
if st.sidebar.button("Fetch Live Matches"):
    with st.spinner("Connecting to Cricket Server..."):
        data = fetch_api_data("currentMatches")
        if data and "data" in data:
            st.session_state['matches'] = {m["name"]: m["id"] for m in data["data"][:10]}
            st.sidebar.success("Matches Updated!")
        else:
            st.sidebar.error("Connection Reset. Try again in 10 seconds.")

# Main Display
if 'matches' in st.session_state:
    match_list = st.session_state['matches']
    selected_match = st.selectbox("🏏 Choose Live Match:", list(match_list.keys()))
    
    if st.button("Load Squads"):
        match_id = match_list[selected_match]
        squad_data = fetch_api_data(f"match_squad?id={match_id}")
        
        if squad_data and "data" in squad_data:
            players = []
            for team in squad_data["data"]:
                players.extend([p["name"] for p in team.get("players", [])])
            st.session_state['current_squad'] = sorted(list(set(players)))
            st.success("Squad Loaded!")

# --- TEAM GENERATOR (UI same as before) ---
if 'current_squad' in st.session_state:
    squad = st.session_state['current_squad']
    col1, col2 = st.columns(2)
    with col1:
        locks = st.multiselect("🔒 LOCKS:", squad)
    with col2:
        trumps = st.multiselect("🃏 TRUMPS:", squad)
        
    num = st.slider("Teams:", 1, 20, 11)
    if st.button("GENERATE TEAMS 🔥"):
        st.balloons()
        for i in range(num):
            pool = [p for p in squad if p not in locks]
            team = list(locks) + random.sample(pool, 11 - len(locks))
            with st.expander(f"📋 TEAM {i+1}"):
                st.write(", ".join(team))
else:
    st.info("Pehle Sidebar se 'Fetch Live Matches' button dabayein.")
    
