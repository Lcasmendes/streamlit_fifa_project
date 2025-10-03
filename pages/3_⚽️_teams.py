import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(
    layout='wide',
)

if "data" in st.session_state:
    df_data = st.session_state["data"]
else:
    df_data = pd.read_csv("datasets/CLEAN_FIFA23_official_data.csv", index_col=0)
    # Filtrando jogadores com contratos ainda validos - data de fim de contrato maior que hoje
    df_data = df_data[df_data["Contract Valid Until"] >= datetime.today().year]
    # Apenas jogadors com valores registrados
    df_data = df_data[df_data["Value(£)"]>0]
    df_data = df_data.sort_values(by='Overall', ascending=False)
    st.session_state['data'] = df_data


# Seletor na sidebar
clubes = df_data['Club'].unique()
club = st.sidebar.selectbox("Clube", clubes)

df_filtered = df_data[df_data["Club"] == club].set_index("Name")

# Página
st.image(df_filtered.iloc[0]['Club Logo'])
st.markdown(f"## {club}")

# Tabela de jogadores
columns = ["Age", "Photo", "Flag", "Overall", 'Value(£)', 'Wage(£)', 'Joined', 
           'Height(cm.)', 'Weight(lbs.)',
           'Contract Valid Until', 'Release Clause(£)']

st.dataframe(df_filtered[columns],
             column_config={
                 "Overall": st.column_config.ProgressColumn(
                     "Overall", format="%d", min_value=0, max_value=100
                 ),
                 "Wage(£)": st.column_config.ProgressColumn("Weekly Wage", format="£%f", 
                                                    min_value=0, max_value=df_filtered["Wage(£)"].max()),
                "Photo": st.column_config.ImageColumn(),
                "Flag": st.column_config.ImageColumn("Country"),
             })