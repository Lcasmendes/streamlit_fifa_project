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


# Seletores na sidebar
clubes = df_data['Club'].unique()
club = st.sidebar.selectbox("Clube", clubes)

# Filtra jogadores por clube
df_players = df_data[df_data["Club"] == club]

players = df_players['Name'].unique()
player = st.sidebar.selectbox("Jogador", players)

# Tela

# Pega apenas a primeira aparição caso ele esteja repetido
player_stats = df_data[df_data["Name"] == player].iloc[0]

st.image(player_stats['Photo'])
st.title(player_stats['Name'])

st.markdown(f"**Clube:** {player_stats['Club']}")
st.markdown(f"**Posição:** {player_stats['Position']}")

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"**Idade:** {player_stats['Age']}")
col2.markdown(f"**Altura:** {player_stats['Height(cm.)']/100}m")
col3.markdown(f"**Peso:** {player_stats['Weight(lbs.)']*0.453:.2f}kg")

st.divider()

st.subheader(f"Overall: {player_stats['Overall']}")
st.progress(int(player_stats['Overall']))

col1, col2, col3, col4 = st.columns(4)

col1.metric(label='Valor de mercado', value=f'£{player_stats["Value(£)"]:,}')
col2.metric(label='Remuneração Semanal', value=f'£{player_stats["Wage(£)"]:,}')
col3.metric(label='Recisão', value=f'£{player_stats["Release Clause(£)"]:,}')
