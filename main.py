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
col3.metric("Tempo médio em minutos", dados['duration'].mean().round(1))

#Bolao The Game Awards
st.divider()
st.subheader('Bolão The Game Awards 2023!')
imagens_jogos = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vTviyi86G1qxhCZacjpN1v8ShugrnPn2Y-WwzcVjpEhNsZCWNcVQAMAOLXwYnj8g_1_IsPx7YMxKr2O/pub?gid=255129162&single=true&output=csv')
imagens_jogos = imagens_jogos.set_index('Jogo')
imagens_jogos = imagens_jogos.to_dict()['Imagem']

dados_game_awards = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vTviyi86G1qxhCZacjpN1v8ShugrnPn2Y-WwzcVjpEhNsZCWNcVQAMAOLXwYnj8g_1_IsPx7YMxKr2O/pub?gid=1743518019&single=true&output=csv')
dados_game_awards = dados_game_awards.replace(imagens_jogos)

st.dataframe(dados_game_awards, hide_index=True, use_container_width = True,
             column_config={
                 'Dan': st.column_config.ImageColumn(width='small'),
                 'Cardoso': st.column_config.ImageColumn(width='small'),
                 'Márcia': st.column_config.ImageColumn(width='small'),
                 'Marcellus': st.column_config.ImageColumn(width='small'),
                 'Vencedor': st.column_config.ImageColumn(width='small')
             }
            )
st.divider()

resultado = []

for i in ['Dan',	'Cardoso',	'Márcia',	'Marcellus'	]:

 resultado.append((i,(dados_game_awards[i]==dados_game_awards['Vencedor']).sum()))

resultado = pd.DataFrame(resultado, columns = ['Participante', 'Acertos']).sort_values('Acertos', ascending=False)
st.dataframe(resultado, hide_index=True, use_container_width = True,
             column_config={
                 'Acertos': st.column_config.ProgressColumn(min_value=0, max_value=23, format="%f"),})


#Gráficos
col1, col2, = st.columns([1.5,1])
grafico_duracao = px.scatter(dados, x='release_date', y='duration', color='nome_podcast', hover_data=['name','quem_esta'],
                             color_discrete_sequence=['#FFCB00','purple'],
                             labels={
                     "release_date": "Data",
                     "duration": "Duração (minutos)",
                     "nome_podcast": "Fase do podcast",
                     'name':'Nome do episódio',
                     'quem_esta':'Participantes'
                 })
grafico_duracao.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))

with col1:
    st.plotly_chart(grafico_duracao, theme="streamlit", use_container_width=True)

with col2:
    st.markdown('##### Ranking de participações')
    st.dataframe(top_participacoes,
                 column_config={
                    'Participações': st.column_config.Column("Nº", width='small'),
                    'Porcentagem': st.column_config.ProgressColumn('Total', help='Porcentagem de participação do total de episódios', min_value=0, max_value=1),
                    'Linha': st.column_config.BarChartColumn('Linha do tempo')
                    })



#Tabela
st.divider()
st.subheader('Lista de Episódios')
st.dataframe(dados.set_index('release_date'), 
                column_config={
                    'url_imagem': st.column_config.ImageColumn('Capa', help='Capa do episódio', width ='small'),
                    'release_date': st.column_config.DateColumn('Data', format="DD.MM.YYYY", help='Data de lançamento do episódio'),
                    'duration': st.column_config.NumberColumn("Duração (minutos)", format="%d", ),
                    'link_spotify': st.column_config.LinkColumn("Link"),
                    'description': st.column_config.Column("Descrição"),
                    'quem_esta': st.column_config.Column("Participantes"),
                    'name': st.column_config.Column("Nome do episódio")
                    

                })




