import streamlit as st
import pandas as pd
import datetime as dt
from pathlib import Path

# -------------------------------------------------
# CONFIGURATION
# -------------------------------------------------
st.set_page_config(page_title="Trading Journal", layout="wide")
DATA_FILE = "trades.csv"

# Capital initial
STARTING_CAPITAL = 150.0  

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
def load_data():
    try:
        df = pd.read_csv(DATA_FILE)
        return df
    except:
        return pd.DataFrame(columns=[
            "date", "time", "direction", "entry", "exit", "taille",
            "pnl", "pct_capital", "capital", "strategy", "notes"
        ])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# -------------------------------------------------
# AUTOMATIC P&L CALCULATION XAUUSD
# -------------------------------------------------
# 1 lot = 100 oz
# value per $1 move = $100 per lot
def calculate_pnl(entry, exit, direction, taille):
    if direction == "Long":
        return (exit - entry) * 100 * taille
    else:  # Short
        return (entry - exit) * 100 * taille

# -------------------------------------------------
# FORM INPUT
# -------------------------------------------------
st.title("📒 Trading Journal XAUUSD")
st.write("Version automatique du P&L • Capitale initial: **150$**")

with st.form("add_trade"):
    col1, col2, col3 = st.columns(3)

    with col1:
        date = st.date_input("Date", dt.date.today())
        time = st.time_input("Heure", dt.datetime.now().time())
        direction = st.selectbox("Direction", ["Long", "Short"])

    with col2:
        entry = st.number_input("Entry", format="%.2f")
        exit = st.number_input("Exit", format="%.2f")
        taille = st.number_input("Taille (lots)", value=0.01, format="%.2f")

    with col3:
        strategy = st.text_input("Stratégie / Setup")
        notes = st.text_area("Notes")

    submitted = st.form_submit_button("Ajouter le trade")

    if submitted:
        if entry == 0 or exit == 0:
            st.error("Entry et Exit sont obligatoires.")
        else:
            pnl = calculate_pnl(entry, exit, direction, taille)

            # Calcul capital cumulé
            if df.empty:
                previous_capital = STARTING_CAPITAL
            else:
                previous_capital = df.iloc[-1]["capital"]

            new_capital = previous_capital + pnl
            pct_capital = (pnl / previous_capital) * 100

            new_row = {
                "date": str(date),
                "time": str(time),
                "direction": direction,
                "entry": entry,
                "exit": exit,
                "taille": taille,
                "pnl": pnl,
                "pct_capital": pct_capital,
                "capital": new_capital,
                "strategy": strategy,
                "notes": notes
            }

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            st.success("Trade ajouté ✔️")

# -------------------------------------------------
# DISPLAY TABLE
# -------------------------------------------------
st.subheader("📊 Historique des trades")
st.dataframe(df, use_container_width=True)

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------
if not df.empty:
    st.subheader("📈 Performance")

    total_pnl = df["pnl"].sum()
    winrate = (df["pnl"] > 0).mean() * 100
    last_capital = df.iloc[-1]["capital"]

    colA, colB, colC = st.columns(3)
    colA.metric("P&L Total", f"{total_pnl:.2f} $")
    colB.metric("Winrate", f"{winrate:.1f} %")
    colC.metric("Capital actuel", f"{last_capital:.2f} $")

    st.subheader("Courbe du capital")
    st.line_chart(df["capital"])
