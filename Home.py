# Importando bibliotecas

import pandas as pd
import numpy as np
import plotly_express as px
import streamlit as st
import inflection
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from PIL import Image


st.set_page_config(page_title = 'Countries', page_icon = '🌆', layout = 'wide')


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

df = pd.read_csv('dashboard_fome_zero\data\zomato.csv')
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





# CONTINUAR DEPOIS A BARRA LATERAL


# ============================================================
# Layout no Streamlit
# ============================================================

st.title('🍛 Fome Zero')
st.subheader('O Melhor lugar para encontrar seu mais novo restaurante favorito!')
st.subheader('Temos as seguintes marcas dentro da nossa plataforma:')

col1, col2, col3, col4, col5 = st.columns(5, gap = 'Large')

with col1:
    restaurantes_unicos = df1['restaurant_id'].nunique()
    restaurantes_unicos_formatado = f'{restaurantes_unicos:,}'
    col1.metric('Restaurantes Cadastrados', value = restaurantes_unicos_formatado)

with col2:
    paises_unicos = len(df1['country'].unique())
    col2.metric('Países Cadastrados', value = paises_unicos)

with col3:
    cidades_unicas = len(df1['city'].unique())
    col3.metric('Cidades Cadastradas', value = cidades_unicas)

with col4:
    avaliacoes = df1['votes'].sum()
    avaliacoes_formatadas = f'{avaliacoes:,}'
    col4.metric('Avaliaçõesb na Plataforma', value = avaliacoes_formatadas)

with col5:
    tipos_culinaria = len(df1['cuisines'].unique())
    col5.metric('Culinárias Registradas', value = tipos_culinaria)



# ==================================================================
# ======================= MAPA DOS RESTAURANTES ====================
# ==================================================================

# criar medias para centralizar o mapa

latitude_media = df1['latitude'].mean()
longitude_media = df1['longitude'].mean()

# criando o mapa

mapa = folium.Map(location = [latitude_media, longitude_media], zoom_start = 1, control_scale = True)
cluster = MarkerCluster().add_to(mapa)

max_pontos = 2000 
df_plot = df_filtrado.head(max_pontos)


for _, row in df_plot.iterrows():
    html_popup = f"""
    <div style="width:250px; font-size:12px;">
        <b>Nome:</b> {row['restaurant_name']}<br>
        <b>Culinária:</b> {row['cuisines']}<br>
        <b>Custo médio para 2:</b> ${row['average_cost_for_two']}<br>
        <b>Nota:</b> {row['aggregate_rating']}
    </div>
    """
    
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=folium.Popup(html_popup, max_width=300)
    ).add_to(cluster)

st.title("Mapa dos Restaurantes")
st_folium(mapa, width = 800, height = 500)