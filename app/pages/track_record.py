import streamlit as st
import pandas as pd

st.title("📈 Track Record")

CSV_PATH = "trades.csv"

# Charger trades
def load_trades():
    try:
        return pd.read_csv(CSV_PATH)
    except:
        return pd.DataFrame()

df = load_trades()

if df.empty:
    st.warning("Aucun trade enregistré pour le moment.")
    st.stop()

# Convertir dates
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# ------------------ FILTRES ------------------
st.subheader("🔍 Filtres")

col1, col2, col3 = st.columns(3)

with col1:
    direction_filter = st.multiselect("Direction", df["direction"].unique())

with col2:
    session_filter = st.multiselect("Session", df["session"].unique())

with col3:
    tag_filter = st.multiselect("Stratégie / Tag", df["tag"].unique())

# Application des filtres
filtered_df = df.copy()

if direction_filter:
    filtered_df = filtered_df[filtered_df["direction"].isin(direction_filter)]

if session_filter:
    filtered_df = filtered_df[filtered_df["session"].isin(session_filter)]

if tag_filter:
    filtered_df = filtered_df[filtered_df["tag"].isin(tag_filter)]

st.markdown("---")

# ------------------ KPIs ------------------
st.subheader("📊 Statistiques")

colA, colB, colC = st.columns(3)

colA.metric("Total Trades", len(filtered_df))
colB.metric("Total P&L", f"${filtered_df['pnl'].sum():,.2f}")
colC.metric("Win Rate", f"{(filtered_df['pnl'] > 0).mean() * 100:.2f}%")

st.markdown("---")

# ------------------ TABLEAU COMPLET ------------------
st.subheader("📄 Historique complet")

st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")

# ------------------ TOP / FLOP TRADES ------------------
st.subheader("🏆 Top Trades & ❌ Worst Trades")

if len(filtered_df) > 0:
    top_trade = filtered_df.loc[filtered_df["pnl"].idxmax()]
    worst_trade = filtered_df.loc[filtered_df["pnl"].idxmin()]

    col1, col2 = st.columns(2)

    with col1:
        st.success("🏆 **Meilleur Trade**")
        st.write(top_trade)

    with col2:
        st.error("❌ **Pire Trade**")
        st.write(worst_trade)
else:
    st.info("Pas assez de données.")
