import streamlit as st
import pandas as pd

# Charger l’excel
df = pd.read_excel("Statistiques.xlsx")

# Nettoyage du Nominal
df["Nominal"] = (
    df["Nominal"]
    .astype(str)
    .str.replace(" ", "")
    .str.replace(",", ".")
    .str.replace("€", "")
)
df["Nominal"] = pd.to_numeric(df["Nominal"], errors="coerce").fillna(0)

# Conversion de la colonne Date
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

st.title("Statistiques par Issuer")

# Sélection des dates
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Date de début")
with col2:
    end_date = st.date_input("Date de fin")

# Bouton
if st.button("Générer les statistiques"):

    # Filtrer selon la période
    df_filtered = df[
        (df["Date"] >= pd.to_datetime(start_date)) &
        (df["Date"] <= pd.to_datetime(end_date))
    ]

    if df_filtered.empty:
        st.warning("Aucun trade trouvé dans cette période.")
    else:
        nominal_sum = df_filtered.groupby("ISSUER")["Nominal"].sum()
        trade_count = df_filtered.groupby("ISSUER")["Nominal"].count()
        avg_nominal = nominal_sum / trade_count

        df_stats = pd.DataFrame({
            "Nominal_total": nominal_sum,
            "Trade_count": trade_count,
            "Nominal_par_trade": avg_nominal
        })

        df_stats = df_stats.sort_values("Nominal_total", ascending=False).head(10)

        # Formatage
        df_stats["Nominal_total"] = df_stats["Nominal_total"].apply(lambda x: f"{x:,.0f}".replace(",", " "))
        df_stats["Nominal_par_trade"] = df_stats["Nominal_par_trade"].apply(lambda x: f"{x:,.0f}".replace(",", " "))

        st.dataframe(df_stats[["Nominal_total", "Trade_count", "Nominal_par_trade"]])
