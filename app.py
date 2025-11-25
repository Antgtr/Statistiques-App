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
df["TRADE DATE"] = pd.to_datetime(df["TRADE DATE"], errors="coerce")

# Filtrage business (MIFID + catégories)
df = df[df["Is Mifid"] == "Mifid"]

df_equity = df[df["Category product"] == "Equity"]
df_rate = df[df["Category product"] == "Rate"]
df_credit = df[df["Category product"] == "Credit"]

df_equity_fixdiv = df_equity[df_equity["Div Kind"] == "synthetic"]
df_equity_fixdiv_pts = df_equity[df_equity["type_div"] == "Absolute"]
df_equity_fixdiv_pourc = df_equity[df_equity["type_div"] == "Proportional"]

# Dictionnaire des datasets disponibles
DATASETS = {
    "All": df,
    "Equity": df_equity,
    "Rate": df_rate,
    "Credit": df_credit,
}

st.title("Statistiques")

# Choix By Issuer / By Underlying
data_filter = st.radio(
    "Filter by:",
    ["Issuer", "Underlying"]
)

if data_filter == "Issuer":
    group_col = "ISSUER" 
else: 
    group_col = "UNDERLYING"

# Choix du dataset
choice = st.selectbox("Choisir le dataset :", list(DATASETS.keys()))
df_selected = DATASETS[choice]

# Logique dynamique : options FixDiv seulement si Equity
fixdiv_filter = None
fixdiv_type = None

if choice == "Equity":
    fixdiv_filter = st.checkbox("Filtrer FixDiv")

    if fixdiv_filter:
        fixdiv_type = st.selectbox(
            "Choisir le type de dividende",
            ["Absolute", "Proportional"]
        )

        if fixdiv_type == "Absolute":
            df_selected = df_equity_fixdiv_pts

        if fixdiv_type == "Proportional":
            df_selected = df_equity_fixdiv_pourc

# Sélection des dates
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Date de début")
with col2:
    end_date = st.date_input("Date de fin")

# Bouton
if st.button("Générer les statistiques"):

    # Filtrer selon la période
    df_filtered = df_selected[
        (df_selected["TRADE DATE"] >= pd.to_datetime(start_date)) &
        (df_selected["TRADE DATE"] <= pd.to_datetime(end_date))
    ]

    if df_filtered.empty:
        st.warning("Aucun trade trouvé dans cette période.")
    else:
        # Aggregation
        df_stats = df_filtered.groupby(group_col).agg(
            Nominal_total=("Nominal", "sum"),
            Trade_count=("Nominal", "count")
        )
    
        # Nominal moyen
        df_stats["Nominal_par_trade"] = df_stats["Nominal_total"] / df_stats["Trade_count"]
    
        # Trier et prendre le top 10
        df_stats = df_stats.sort_values("Nominal_total", ascending=False).head(10)
    
        # Formatage
        df_stats["Nominal_total"] = df_stats["Nominal_total"].apply(lambda x: f"{x:,.0f}".replace(",", " "))
        df_stats["Nominal_par_trade"] = df_stats["Nominal_par_trade"].apply(lambda x: f"{x:,.0f}".replace(",", " "))
    
        # Affichage
        st.dataframe(df_stats)
















