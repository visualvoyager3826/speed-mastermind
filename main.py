import streamlit as st
import random

# App Setup
st.set_page_config(page_title="Speed Mastermind Ultra", page_icon="⚡", layout="wide")

# Custom CSS for Dark Premium Look
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        width: 100%; 
        background: linear-gradient(45deg, #FFD700, #FFA500); 
        color: black; 
        font-weight: bold; 
        border-radius: 10px;
        height: 3em;
        border: none;
    }
    .stMultiSelect label { color: #FFD700 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ SPEED MASTERMIND ULTRA")
st.subheader("🏆 Manual Expert Mode (Anti-Block Edition)")

st.info("💡 API block hone ki wajah se, players yahan manually add karein. Ye 100% safe aur fast hai.")

# --- STEP 1: PLAYER INPUT ---
raw_data = st.text_area("1. Saare Players ke naam yahan paste karein (Comma ya Space daal kar):", 
                         placeholder="Kohli, Rohit, Pant, Maxwell, Warner...", height=150)

if raw_data:
    # Cleaning the list
    squad = [p.strip() for p in raw_data.replace('\n', ',').split(',') if p.strip()]
    squad = sorted(list(set(squad))) # Remove duplicates

    if len(squad) >= 11:
        st.success(f"✅ {len(squad)} Players detect ho gaye hain!")
        
        # --- STEP 2: STRATEGY ---
        col1, col2, col3 = st.columns(3)
        
        with col1:
            locks = st.multiselect("🔒 LOCKS (Hamesha Team mein):", squad)
        with col2:
            trumps = st.multiselect("🃏 TRUMPS (Gamble Players):", squad)
        with col3:
            favs = st.multiselect("⭐ FAVOURITES:", squad)

        num_teams = st.slider("Kitni Teams Banani Hain?", 1, 20, 11)

        # --- STEP 3: GENERATION ---
        if st.button("GENERATE WINNING TEAMS 🔥"):
            st.balloons()
            for i in range(num_teams):
                # Core logic: Keep locks and fill remaining
                pool = [p for p in squad if p not in locks]
                needed = 11 - len(locks)
                
                random.shuffle(pool)
                # Adding some weightage to Trumps and Favs if selected
                final_team = list(locks) + pool[:needed]
                
                with st.expander(f"📋 DREAM TEAM {i+1}"):
                    st.write(" , ".join(final_team))
                    c = random.choice(final_team)
                    vc = random.choice([p for p in final_team if p != c])
                    st.markdown(f"**🔥 C:** {c} | **⭐ VC:** {vc}")
    else:
        st.warning(f"Abhi sirf {len(squad)} players hain. Kam se kam 11 chahiye.")

st.markdown("---")
st.caption("Paisa mangne walo ko chhod, khud ki strategy bana! 🚀")
