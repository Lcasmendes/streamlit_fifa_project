import streamlit as st
import pandas as pd
import webbrowser
from datetime import datetime

if "data" not in st.session_state:
    df_data = pd.read_csv("datasets/CLEAN_FIFA23_official_data.csv", index_col=0)
    # Filtrando jogadores com contratos ainda validos - data de fim de contrato maior que hoje
    df_data = df_data[df_data["Contract Valid Until"] >= datetime.today().year]
    # Apenas jogadors com valores registrados
    df_data = df_data[df_data["Value(£)"]>0]
    df_data = df_data.sort_values(by='Overall', ascending=False)
    st.session_state['data'] = df_data

df_data = st.session_state['data']

st.markdown("# FIFA 2023 - OFFICIAL DATASET!")
st.sidebar.markdown("Desenvolvido por [Lucas Mendes](link)")

btn = st.button("Acesse os dados no Kaggle")
if btn:
    webbrowser.open_new_tab("https://www.kaggle.com/datasets/bryanb/fifa-player-stats-database")

st.markdown(
    "" \
    "The dataset contains +17k unique players and more than 60 columns, " \
    "general information and all KPIs the famous videogame offers. As the " \
    "esport scene keeps rising espacially on FIFA, I thought it can be useful ]"
    "for the community (kagglers and/or gamers)"
)

st.write(st.session_state['data'])