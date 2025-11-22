import streamlit as st

# --------- PAGE CONFIG ---------
st.set_page_config(
    page_title="Trading Journal XAUUSD",
    page_icon="📒",
    layout="wide"
)

# --------- CUSTOM SIDEBAR ---------
with st.sidebar:
    st.title("📒 MUSAFXAU")
    st.markdown("---")
    st.page_link("app/pages/add_trade.py", label="+ Add Trade", icon="➕")
    st.page_link("app/pages/dashboard.py", label="Dashboard", icon="📊")
    st.page_link("app/pages/daily_journal.py", label="Daily Journal", icon="🗓️")
    st.page_link("app/pages/track_record.py", label="Track Record", icon="📈")
    st.markdown("---")
    st.caption("Trading Journal XAUUSD")

# --------- HOME PAGE ---------
st.title("📒 Trading Journal XAUUSD")
st.subheader("Bienvenue dans ton application de trading personnalisée.")

st.info("""
👉 Utilise la barre latérale pour naviguer :
- Ajouter un trade  
- Voir ton Dashboard  
- Compléter ton Daily Journal  
- Voir ton Track Record  
""")

st.markdown("---")
st.success("L'application est prête. Continue avec la création des pages 👇")
