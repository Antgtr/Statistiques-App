import streamlit as st
import pandas as pd

# Charger l’excel
df = pd.read_excel("Statistiques.xlsx")

df["Nominal"] = (
    df["Nominal"]
    .astype(str)
    .str.replace(" ", "")
    .str.replace(",", ".")
    .str.replace("€", "")
)

df["Nominal"] = pd.to_numeric(df["Nominal"], errors="coerce").fillna(0)

st.title("Statistiques par Issuer")

# Bouton
if st.button("Générer les statistiques"):

    nominal_sum = df.groupby("ISSUER")["Nominal"].sum()
    trade_count = df.groupby("ISSUER")["Nominal"].count()
    avg_nominal = nominal_sum / trade_count

    df_stats = pd.DataFrame({
        "Nominal_total": nominal_sum,
        "Trade_count": trade_count,
        "Nominal_par_trade": avg_nominal
    })

    df_stats = df_stats.sort_values("Nominal_total", ascending=False).head(10)

    # Formatage
    df_stats["Nominal_total_fmt"] = df_stats["Nominal_total"].apply(lambda x: f"{x:,.0f}".replace(",", " "))
    df_stats["Nominal_par_trade_fmt"] = df_stats["Nominal_par_trade"].apply(lambda x: f"{x:,.0f}".replace(",", " "))


    st.dataframe(df_stats[["Nominal_total_fmt", "Trade_count", "Nominal_par_trade_fmt"]])
