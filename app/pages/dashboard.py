import streamlit as st
import pandas as pd
import numpy as np
import datetime

st.title("📊 Dashboard")

CSV_PATH = "trades.csv"

# Charger les trades
def load_trades():
    try:
        return pd.read_csv(CSV_PATH)
    except:
        return pd.DataFrame()

df = load_trades()

# ------------------ Vérification ------------------
if df.empty:
    st.warning("Aucun trade pour le moment. Ajoute ton premier trade dans ➕ Add Trade.")
    st.stop()

# Convertir dates
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# ------------------ KPIs ------------------

total_pnl = df["pnl"].sum()
account_balance = 150 + total_pnl  # capital initial + gain total

win_rate = (df["pnl"] > 0).mean() * 100
trade_count = len(df)
win_trades = (df["pnl"] > 0).sum()
lose_trades = (df["pnl"] <= 0).sum()

expectancy = df["pnl"].mean() if trade_count > 0 else 0

profit_factor = (
    df[df["pnl"] > 0]["pnl"].sum() /
    abs(df[df["pnl"] <= 0]["pnl"].sum())
) if lose_trades > 0 else np.nan

score = expectancy * win_rate  # Score simple (on pourra améliorer)

# ------------------ DISPLAY KPIs ------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Account Balance", f"${account_balance:,.2f}")
col2.metric("📈 Win Rate", f"{win_rate:.2f}%")
col3.metric("📊 Expectancy", f"${expectancy:.2f}")
col4.metric("⚖️ Profit Factor", f"{profit_factor:.2f}" if not np.isnan(profit_factor) else "N/A")

colA, colB = st.columns(2)
colA.metric("🏆 Trade Win %", f"{win_rate:.2f}%")
colB.metric("⭐ Score", f"{score:.2f}")

st.markdown("---")

# ------------------ Graph Performance ------------------
st.subheader("📉 Évolution du capital")

df_sorted = df.sort_values("date")
df_sorted["balance"] = 150 + df_sorted["pnl"].cumsum()

st.line_chart(df_sorted[["balance"]])

st.markdown("---")

# ------------------ Calendrier hebdo ------------------
st.subheader("🗓️ Calendrier Hebdomadaire")

df["weekday"] = df["date"].dt.day_name()
weekly_pnl = df.groupby("weekday")["pnl"].sum().reindex(
    ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
)

st.bar_chart(weekly_pnl)

st.markdown("---")

# ------------------ Calendrier mensuel ------------------
st.subheader("📅 Résultats Mensuels")

df["month"] = df["date"].dt.to_period("M")
monthly_pnl = df.groupby("month")["pnl"].sum()

st.bar_chart(monthly_pnl)

st.markdown("---")

# ------------------ Triangle zone ------------------
st.subheader("📐 Performance Triangle")

triangle_col1, triangle_col2 = st.columns([1, 3])

with triangle_col1:
    st.write("Win %")
    st.write("Profit Factor")
    st.write("Completeness (à définir)")

with triangle_col2:
    st.info("Triangle visuel à venir — on l’ajoute dès que ton design final est prêt.")
