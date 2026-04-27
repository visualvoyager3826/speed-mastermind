import streamlit as st
import requests
import random

# App Setup
st.set_page_config(page_title="Speed Mastermind", page_icon="⚡", layout="wide")

API_KEY = "07af93a1-ca72-4828-a7e0-f646ab4c9647"

# --- API FUNCTIONS ---
@st.cache_data(ttl=60)
def get_matches():
    url = f"https://api.cricketdata.org/v1/currentMatches?apikey={API_KEY}&offset=0"
    # Headers add karne se 'Connection Reset' error khatam ho jata hai
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        match_list = {}
        if "data" in data:
            for m in data["data"]:
                name = f"{m.get('name', 'Unknown')} ({m.get('status', 'Live')})"
                match_list[name] = m.get("id")
        return match_list
    except Exception as e:
        return {"Error": str(e)}

@st.cache_data(ttl=60)
def get_players(match_id):
    url = f"https://api.cricketdata.org/v1/match_squad?apikey={API_KEY}&id={match_id}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        all_players = []
        if "data" in data:
            for team in data["data"]:
                players_list = team.get("players", [])
                for p in players_list:
                    all_players.append(p.get("name"))
        return sorted(list(set(all_players)))
    except:
        return []

# --- BAAKI UI CODE SAME RHEGA ---
st.title("⚡ SPEED MASTERMIND")
st.markdown("---")

matches = get_matches()

if not matches or "Error" in matches:
    st.error(f"API Error: {matches.get('Error')}")
    st.info("💡 Tip: Ek baar page refresh karein, Connection reset ho raha hai.")
else:
    match_choice = st.selectbox("🏏 Select Match:", list(matches.keys()))
    m_id = matches[match_choice]
    
    if m_id:
        squad = get_players(m_id)
        if squad:
            col1, col2 = st.columns(2)
            with col1:
                locks = st.multiselect("🔒 LOCKS:", squad)
                num_teams = st.number_input("Teams count", 1, 100, 11)
            with col2:
                trumps = st.multiselect("🃏 TRUMPS:", squad)
            
            if st.button("GENERATE TEAMS 🔥"):
                st.balloons()
                # Same generation logic...
                for i in range(num_teams):
                    pool = [p for p in squad if p not in locks]
                    needed = 11 - len(locks)
                    random.shuffle(pool)
                    final_team = list(locks) + pool[:needed]
                    with st.expander(f"📋 TEAM {i+1}"):
                        st.write(" , ".join(final_team))
                        
