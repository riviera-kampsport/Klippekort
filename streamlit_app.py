import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# -----------------------------
# Streamlit setup
# -----------------------------
st.set_page_config(layout="wide")
st.title("🥋 Klippekort - Træning")

# -----------------------------
# Google Sheets forbindelse
# -----------------------------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["google"],
    scope
)

client = gspread.authorize(creds)

# 🔥 SKIFT TIL DIT SHEET NAVN
sheet = client.open("Medlemmer").sheet1

# -----------------------------
# Data loader
# -----------------------------
def load_data():
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # Sikrer at Klip altid er tal
    df["Klip"] = pd.to_numeric(df["Klip"], errors="coerce").fillna(0).astype(int)

    return df

# -----------------------------
# UI
# -----------------------------
st.subheader("🔎 Søg barn")

search = st.text_input("Skriv navn")

df = load_data()

if search:
    df = df[df["Navn"].str.contains(search, case=False, na=False)]

st.divider()

# -----------------------------
# Liste med klip-knapper
# -----------------------------
for index, row in df.iterrows():

    col1, col2, col3 = st.columns([3, 1, 1])

    col1.write(row["Navn"])

    col2.write(f"🎟️ Klip: {row['Klip']}")

    if col3.button("✂️ Klip", key=f"clip_{index}"):

        if row["Klip"] > 0:

            new_value = row["Klip"] - 1

            # +2 fordi Google Sheets starter efter header
            sheet.update_cell(index + 2, 3, new_value)

            st.success(f"Klip givet til {row['Navn']}")

            st.rerun()

        else:
            st.warning("Ingen klip tilbage")

st.info("Systemet bruger Google Sheet som database")