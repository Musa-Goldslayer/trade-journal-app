import streamlit as st
import pandas as pd
import datetime

st.title("➕ Add Trade")

# ------------------ Base de données ------------------
CSV_PATH = "trades.csv"

# Charger ou créer fichier
def load_trades():
    try:
        return pd.read_csv(CSV_PATH)
    except:
        return pd.DataFrame(columns=[
            "date", "time", "direction", "setup", "entry", "stop_loss",
            "take_profit", "exit", "size", "pnl", "pct_capital",
            "r_multiple", "duration", "emotions", "notes",
            "screenshot_before", "screenshot_after",
            "session", "tag"
        ])

def save_trades(df):
    df.to_csv(CSV_PATH, index=False)

df = load_trades()

# ------------------ Formulaire ------------------
col1, col2, col3 = st.columns(3)

with col1:
    date = st.date_input("Date", datetime.date.today())
    time = st.time_input("Heure", datetime.datetime.now().time())
    direction = st.selectbox("Direction", ["Long", "Short"])
    setup = st.text_input("Setup / Stratégie")

with col2:
    entry = st.number_input("Entry", step=0.01, format="%.2f")
    stop_loss = st.number_input("Stop Loss", step=0.01, format="%.2f")
    take_profit = st.number_input("Take Profit", step=0.01, format="%.2f")
    exit_price = st.number_input("Exit", step=0.01, format="%.2f")

with col3:
    size = st.number_input("Taille (lots)", value=0.01, step=0.01)
    emotions = st.text_input("Émotions")
    notes = st.text_area("Notes")

colA, colB = st.columns(2)

with colA:
    screenshot_before = st.text_input("Screenshot avant (URL TradingView/Drive)")
with colB:
    screenshot_after = st.text_input("Screenshot après (URL TradingView/Drive)")

session = st.selectbox("Session", ["London", "NY", "Tokyo", "Asian", "Other"])
tag = st.text_input("Tag stratégie")

# ------------------ Calculs auto ------------------
if exit_price and entry:
    pnl = (exit_price - entry) * (100 * size) if direction == "Long" else (entry - exit_price) * (100 * size)
else:
    pnl = 0

capital_initial = 150  # Capital de départ (tu pourras modifier plus tard)
pct_capital = pnl / capital_initial * 100 if capital_initial else 0

if stop_loss:
    r_multiple = (exit_price - entry) / (entry - stop_loss) if direction == "Long" else (entry - exit_price) / (stop_loss - entry)
else:
    r_multiple = 0

duration = "À calculer plus tard"

# ------------------ Ajouter le trade ------------------
if st.button("💾 Ajouter le trade"):
    new_trade = {
        "date": date,
        "time": time,
        "direction": direction,
        "setup": setup,
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "exit": exit_price,
        "size": size,
        "pnl": pnl,
        "pct_capital": pct_capital,
        "r_multiple": r_multiple,
        "duration": duration,
        "emotions": emotions,
        "notes": notes,
        "screenshot_before": screenshot_before,
        "screenshot_after": screenshot_after,
        "session": session,
        "tag": tag,
    }

    df = df.append(new_trade, ignore_index=True)
    save_trades(df)
    st.success("Trade ajouté avec succès !")

# ------------------ Aperçu du fichier ------------------
st.subheader("Historique des trades")
st.dataframe(df, use_container_width=True)
