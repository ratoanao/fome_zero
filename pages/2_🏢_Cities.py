# Importando bibliotecas

import pandas as pd
import numpy as np
import plotly_express as px
import streamlit as st
import inflection
from PIL import Image
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title = 'Cities', page_icon = '🏢', layout = 'wide')

# =================================================
# ================ Transformações =================
# =================================================


# Preenchimento do nome dos países
COUNTRIES = {
            1: "India",
            14: "Australia",
            30: "Brazil",
            37: "Canada",
            94: "Indonesia",
            148: "New Zeland",
            162: "Philippines",
            166: "Qatar",
            184: "Singapure",
            189: "South Africa",
            191: "Sri Lanka",
            208: "Turkey",
            214: "United Arab Emirates",
            215: "England",
            216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES[country_id]

# Criação do Tipo de Categoria de Comida

def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

# Criação do nome das Cores

COLORS = {
        "3F7E00": "darkgreen",
        "5BA829": "green",
        "9ACD32": "lightgreen",
        "CDD614": "orange",
        "FFBA00": "red",
        "CBCBC8": "darkred",
        "FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]

# Renomear as colunas do DataFrame

def rename_columns(df1):
    df1 = df1.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df1.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df1.columns = cols_new
    return df1

# Subindo os dados e analisando previamente

df = pd.read_csv('data/zomato.csv')
df1 = df.copy()


# ============================================
# ================== LIMPEZA =================
# ============================================

# renomeando colunas
df1 = rename_columns(df1)

# traduzindo o código do país para nome
df1['country'] = df1['country_code'].apply(country_name)

# criando os tipos de categorias de comidas
df1['price_type'] = df1['price_range'].apply(create_price_type)

# traduzindo código das cores para nomes
df1['color_name'] = df1['rating_color'].apply(color_name)

# removendo linhas "NaN"
df1 = df1[df1['cuisines'].notna()].copy()
df1["cuisines"] = df1.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

# removendo restaurant_id duplicados 
df1 = df1.drop_duplicates(subset = 'restaurant_id', keep = 'first')


# ============================================================
# Barra lateral no Streamlit
# ============================================================


image = Image.open('logo.png')
st.sidebar.image(image, width =  120)

st.sidebar.markdown('# Filtros')

paises = st.sidebar.multiselect(
    "Escolha os países que deseja visualizar as informações",
    df1['country'].unique()
) 

st.sidebar.markdown("""---""")

# filtro dos países

if paises:
    df_filtrado = df1[df1['country'].isin(paises)]
else:
    df_filtrado = df1.copy()


# ============================================================
# Layout no Streamlit
# ============================================================

st.title('🏢 Cities')
st.markdown('Top 10 cidades com mais restaurantes registrados na base de dados')

# gráfico dos Top 10 cidades com mais restaurantes registrados na base de dados 
top10_restaurantes = df_filtrado.groupby('city', as_index = False)['restaurant_id'].nunique().sort_values(by = 'restaurant_id', ascending = False).head(10)

fig = px.bar(
    top10_restaurantes,
    x = 'city',
    y = 'restaurant_id',
    title = 'Top 10 cidades com mais restaurantes registrados na base de dados',
    labels = {'city':'Cidades','restaurant_id':'Quantidade de Restaurantes'},
    color = 'city'
)
st.plotly_chart(fig)

col1, col2 = st.columns(2)

with col1:
    maior_4 = df_filtrado[df_filtrado['aggregate_rating'] > 4]

    top7_cidades = maior_4.groupby('city', as_index = False)['restaurant_id'].nunique().sort_values(by = 'restaurant_id', ascending = False).head(7)

    fig = px.bar(
        top7_cidades,
        x = 'city',
        y = 'restaurant_id',
        title = 'Top 7 cidades com restaurantes com média de avaliação acima de 4',
        labels = {'city':'Cidades','restaurant_id':'Quantidade de restaurantes'},
        color = 'city'
    )
    st.plotly_chart(fig)

# gráfico Top 7 cidades com restaurantes com média de avaliação abaixo de 2.5

with col2:
    menor_25 = df_filtrado[df_filtrado['aggregate_rating'] < 2.5]

    menor_25 = menor_25.groupby('city', as_index = False)['restaurant_id'].nunique().sort_values(by = 'restaurant_id', ascending = False).head(7)

    fig = px.bar(
        menor_25,
        x = 'city',
        y = 'restaurant_id',
        title = 'Top 7 cidades com restaurantes com média de avaliação abaixo de 2.5',
        labels = {'city':'Cidades','restaurant_id':'Quantidade de restaurantes'},
        color = 'city'
    )
    st.plotly_chart(fig)


# gráfico top 10 cidades com mais restaurantes com tipos culinários distintos

top10_culinarias = df_filtrado.groupby('city', as_index = False)['cuisines'].nunique().sort_values(by = 'cuisines', ascending = False).head(10)

fig = px.bar(
    top10_culinarias,
    x = 'city',
    y = 'cuisines',
    title = 'Top 10 cidades com mais restaurantes com tipos culinários distintos',
    labels = {'city':'Cidades','cuisines':'Tipos de culinárias distintas'},
    color = 'city'
)

st.plotly_chart(fig)

