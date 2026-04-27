import streamlit as st
import requests
import random

# App Setup
st.set_page_config(page_title="Speed Mastermind", page_icon="⚡", layout="wide")

# Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background: linear-gradient(45deg, #00e676, #00c853); color: black; font-weight: bold; border: none; padding: 15px; }
    </style>
    """, unsafe_allow_html=True)

API_KEY = "07af93a1-ca72-4828-a7e0-f646ab4c9647"

# --- API FUNCTIONS ---
@st.cache_data(ttl=300)
def get_matches():
    url = f"https://api.cricketdata.org/v1/matches?apikey={API_KEY}&offset=0"
    try:
        data = requests.get(url).json()
        if data.get("status") == "success":
            return {m["name"]: m["id"] for m in data["data"][:10]}
    except: return {}
    return {}

@st.cache_data(ttl=300)
def get_players(match_id):
    url = f"https://api.cricketdata.org/v1/match_squad?apikey={API_KEY}&id={match_id}"
    try:
        data = requests.get(url).json()
        all_players = []
        if data.get("status") == "success":
            for team in data["data"]:
                for p in team.get("players", []):
                    all_players.append(p["name"])
        return sorted(list(set(all_players)))
    except: return []

# --- UI ---
st.title("⚡ SPEED MASTERMIND")
st.subheader("Mega GL Team Generator (Real-Time Squad)")

matches = get_matches()
if not matches:
    st.error("Matches load nahi ho rahe. API check karein.")
else:
    match_choice = st.selectbox("🏏 Match Choose Karein:", list(matches.keys()))
    squad = get_players(matches[match_choice])

    if not squad:
        st.warning("Squad abhi announce nahi hua. Neeche manual players daalein.")
        squad = st.text_area("Sabb players ke naam daalo (comma separated):").split(",")

    # --- STRATEGY SECTION ---
    col1, col2, col3 = st.columns(3)
    with col1:
        locks = st.multiselect("🔒 LOCKS (Hamesha rahenge):", squad)
    with col2:
        trumps = st.multiselect("🃏 TRUMPS (Gamble players):", squad)
    with col3:
        favs = st.multiselect("⭐ FAVOURITES:", squad)

    num_teams = st.slider("Kitni Teams Banani Hain?", 1, 20, 11)

    if st.button("GENERATE TEAMS NOW 🔥"):
        if len(squad) < 11:
            st.error("Kam se kam 11 players hone chahiye!")
        else:
            st.balloons()
            for i in range(num_teams):
                # Core Logic: Combine Locks + Random from remaining squad
                remaining_needed = 11 - len(locks)
                other_pool = [p for p in squad if p not in locks]
                
                # Mixing logic
                random.shuffle(other_pool)
                team = list(locks) + other_pool[:remaining_needed]
                
                # Show Team
                with st.expander(f"📋 TEAM {i+1}"):
                    st.write(", ".join(team))
                    st.caption(f"C: {random.choice(team)} | VC: {random.choice(team)}")

st.info("Note: Ek baar GitHub par Commit karne ke baad 30 seconds wait karein, Streamlit apne aap update ho jayega.")
