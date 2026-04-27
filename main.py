import streamlit as st
import requests
import random

# App Setup
st.set_page_config(page_title="Speed Mastermind", page_icon="⚡", layout="wide")

API_KEY = "07af93a1-ca72-4828-a7e0-f646ab4c9647"

# --- API FUNCTIONS ---
@st.cache_data(ttl=60)
def get_matches():
    # Try current matches endpoint
    url = f"https://api.cricketdata.org/v1/currentMatches?apikey={API_KEY}&offset=0"
    try:
        response = requests.get(url)
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
    try:
        response = requests.get(url)
        data = response.json()
        all_players = []
        if "data" in data:
            # Iterating through teams
            for team in data["data"]:
                players_list = team.get("players", [])
                for p in players_list:
                    all_players.append(p.get("name"))
        return sorted(list(set(all_players)))
    except:
        return []

# --- UI ---
st.title("⚡ SPEED MASTERMIND")
st.markdown("---")

matches = get_matches()

if not matches or "Error" in matches:
    st.error(f"API se data nahi aa raha. Check: {matches.get('Error', 'Unknown Error')}")
    st.info("💡 Tip: Agar live matches nahi hain, toh API empty list bhejti hai.")
else:
    match_choice = st.selectbox("🏏 Select Match:", list(matches.keys()))
    m_id = matches[match_choice]
    
    if m_id:
        squad = get_players(m_id)
        
        if not squad:
            st.warning("⚠️ Squad abhi tak announce nahi hua hai.")
            manual_input = st.text_area("Squad nahi mila? Yahan players ke naam comma (,) daal kar likhein:")
            if manual_input:
                squad = [name.strip() for name in manual_input.split(",")]
        
        if squad:
            col1, col2 = st.columns(2)
            with col1:
                locks = st.multiselect("🔒 LOCKS (Teams mein fix rahenge):", squad)
                num_teams = st.number_input("Kitni Teams Banani Hain?", 1, 100, 11)
            with col2:
                trumps = st.multiselect("🃏 TRUMPS (Risky players):", squad)
            
            if st.button("GENERATE TEAMS NOW 🔥"):
                if len(squad) < 11:
                    st.error("Kam se kam 11 players list mein hone chahiye!")
                else:
                    st.balloons()
                    for i in range(num_teams):
                        # Simple Random Logic with Locks
                        pool = [p for p in squad if p not in locks]
                        needed = 11 - len(locks)
                        random.shuffle(pool)
                        final_team = list(locks) + pool[:needed]
                        
                        with st.expander(f"📋 TEAM {i+1}"):
                            st.write(" , ".join(final_team))
                            st.caption(f"Capt: {random.choice(final_team)} | VC: {random.choice(final_team)}")
                            
