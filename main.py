#Dashboard com dados da covid no esgoto ETE Serraria

import pandas as pd
import streamlit as st
import plotly.express as px

# Configurações da página
st.set_page_config(
    page_title="Análise UP! Podcast",
    page_icon="	:up:",
    layout="wide",
    initial_sidebar_state='collapsed'
)

# Barra lateral para info
with st.sidebar:
    texto = """
# Sobre o painel
Este painel foi feito a partir de um estudo da biblioteca Spotipy, a qual facilita o consumo da API do Spotify. Selecionei o podcast UP! para avaliar seus dados, e deixá-los postos de uma maneira
que fosse fácil de entender.

# Sobre mim
            """
    st.markdown(texto)
    st.image('https://media.licdn.com/dms/image/D4D03AQEDuEud7TtpUw/profile-displayphoto-shrink_800_800/0/1664902362993?e=1704326400&v=beta&t=-FzZf4tS3p9l4KsfqoCMUAGDiaMUkmLcTHb6d6-UczA', width=100)

    texto = """

Me chamo André Jarenkow, entusiasta da linguagem Python e ouvinte fiel ao UP!.
            """
    st.markdown(texto)
    


# Título principal do painel
imagem, titulo  = st.columns([1, 6])
titulo.header("Análise Podcast UP - via API Spotify")
titulo.markdown('[Assine o UP! a partir de R$ 5,00](https://www.catarse.me/up)')
imagem.image('https://i.scdn.co/image/ab6765630000ba8a123f70dfa953d4707a9f2b59', width=100)

#Dados
dados = pd.read_table('https://docs.google.com/spreadsheets/d/e/2PACX-1vTviyi86G1qxhCZacjpN1v8ShugrnPn2Y-WwzcVjpEhNsZCWNcVQAMAOLXwYnj8g_1_IsPx7YMxKr2O/pub?output=tsv',  decimal=',')
dados = dados[['url_imagem','name','release_date', 'description','quem_esta','duration','link_spotify', 'nome_podcast', ]]
dados['duration'] = dados['duration'].astype(float)
dados['quem_esta'] = dados['quem_esta'].str.replace(', ',',')


#Participações
top_participacoes = (dados['quem_esta'].str.get_dummies(',').sum()).reset_index()
top_participacoes.columns = ['Nome', 'Participações']
top_participacoes['Porcentagem'] = top_participacoes['Participações']/len(dados)
top_participacoes['Linha'] = dados['quem_esta'].sort_index(ascending=False).str.get_dummies(',').T.values.tolist()
top_participacoes = top_participacoes.sort_values('Participações', ascending=False)
top_participacoes = top_participacoes.set_index('Nome')

#Métricas
tempo_total = dados['duration'].sum().round(1)

col1, col2, col3 = st.columns(3)
col1.metric("Total episódios", len(dados))
col2.metric("Tempo total em minutos", tempo_total)
col3.metric("Tempo total em horas", tempo_total/60)



#Gráficos
col1, col2, = st.columns([1.5,1])
grafico_duracao = px.scatter(dados, x='release_date', y='duration', color='nome_podcast', hover_data=['name','quem_esta'],
                             labels={
                     "release_date": "Data",
                     "duration": "Duração (minutos)",
                     "nome_podcast": "Fase do podcast",
                     'name':'Nome do episódio',
                     'quem_esta':'Participantes'
                 })


with col1:
    st.plotly_chart(grafico_duracao, theme="streamlit", use_container_width=True)

with col2:
    st.markdown('##### Ranking de participações')
    st.dataframe(top_participacoes,
                 column_config={
                    'Porcentagem': st.column_config.ProgressColumn('Total', help='Porcentagem de participação do total de episódios', min_value=0, max_value=1),
                    'Linha': st.column_config.BarChartColumn('Linha do tempo', )
                    })



#Tabela
st.markdown('##### Lista de Episódios')
st.dataframe(dados, 
                column_config={
                    'url_imagem': st.column_config.ImageColumn('Capa', help='Capa do episódio', width ='small'),
                    'release_date': st.column_config.DateColumn('Data', format="DD.MM.YYYY", help='Data de lançamento do episódio'),
                    'duration': st.column_config.NumberColumn("Duração (minutos)", format="%d", ),
                    'link_spotify': st.column_config.LinkColumn("Link"),
                    'description': st.column_config.Column("Descrição"),
                    'quem_esta': st.column_config.Column("Participantes"),
                    'name': st.column_config.Column("Nome do episódio")
                    

                })


