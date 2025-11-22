import streamlit as st
import pandas as pd

st.title("📘 Daily Journal")

CSV_PATH = "trades.csv"

# Charger trades
def load_trades():
    try:
        return pd.read_csv(CSV_PATH)
    except:
        return pd.DataFrame()

df = load_trades()

if df.empty:
    st.warning("Aucun trade encore. Ajoute un trade dans ➕ Add Trade.")
    st.stop()

# Convertir dates
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["weekday"] = df["date"].dt.day_name()

# Ordre des jours
order_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
df["weekday"] = pd.Categorical(df["weekday"], categories=order_week, ordered=True)

# ---------------- WEEK VIEW ----------------
st.subheader("🗓️ Vue Hebdomadaire")

weekly_summary = df.groupby("weekday")["pnl"].sum().reindex(order_week)

st.bar_chart(weekly_summary)

st.markdown("---")

# ---------------- DAILY JOURNAL ----------------
st.subheader("📅 Journal du Jour")

selected_day = st.selectbox("Choisir un jour :", order_week)

day_df = df[df["weekday"] == selected_day]

if day_df.empty:
    st.info(f"Aucun trade ce jour-là ({selected_day}).")
else:
    for i, row in day_df.iterrows():
        st.write(f"### Trade {i+1}")
        st.write(f"**Direction :** {row['direction']}")
        st.write(f"**Setup :** {row['setup']}")
        st.write(f"**Entry :** {row['entry']}")
        st.write(f"**Exit :** {row['exit']}")
        st.write(f"**P&L :** {row['pnl']} $")
        st.write(f"**Émotions :** {row['emotions']}")
        st.write(f"**Notes :** {row['notes']}")

        if isinstance(row["screenshot_before"], str) and row["screenshot_before"].startswith("http"):
            st.write("📸 **Screenshot Avant :**")
            st.image(row["screenshot_before"])

        if isinstance(row["screenshot_after"], str) and row["screenshot_after"].startswith("http"):
            st.write("📸 **Screenshot Après :**")
            st.image(row["screenshot_after"])

        st.markdown("---")
