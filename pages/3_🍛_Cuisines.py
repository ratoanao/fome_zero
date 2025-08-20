# Importando bibliotecas

import pandas as pd
import numpy as np
import plotly_express as px
import streamlit as st
import inflection
from PIL import Image
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title = 'Cuisines', page_icon = '🍛', layout = 'wide')

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


# filtros st.slider da quantidade de restaurantes que deseja visualizar

num_restaurantes = st.sidebar.slider(label = 'Selecione a quantidade de restaurantes que deseja visualizar', 
                                        min_value = 1, 
                                        max_value = 20, 
                                        step = 1)


# filtro por tipos de culinárias

melhores_culinarias = df1.groupby('cuisines', as_index = False)['aggregate_rating'].mean().sort_values(by = 'aggregate_rating', ascending = False).head(num_restaurantes)

culinarias = st.sidebar.multiselect(
    label = 'Selecione os tipos de culinárias',
    options = melhores_culinarias['cuisines'].tolist()
)

if culinarias:
    df_filtrado = df1[df1['cuisines'].isin(culinarias)]
else:
    df_filtrado = df1.copy()


# ============================================================
# Layout no Streamlit
# ============================================================

st.title('🍛 Cuisines')
st.markdown('Melhores Restaurantes dos Principais tipos Culinários')

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    comida_italiana = df_filtrado[df_filtrado['cuisines'] == 'Italian']
    if not comida_italiana.empty:
        nota_max = comida_italiana['aggregate_rating'].max()
        mais_antigo = comida_italiana[comida_italiana['aggregate_rating'] == nota_max].sort_values('restaurant_id')
        mais_antigo = mais_antigo.iloc[0]
        
        col1.metric(label=f"Italiana: {mais_antigo['restaurant_name']}",
                    value=mais_antigo['aggregate_rating'],
                    help=f"País: {mais_antigo['country']} | Cidade: {mais_antigo['city']}")
    else:
        col1.metric(label="Italiana: Não encontrado", value="N/A")

with col2:
    comida_americana = df_filtrado[df_filtrado['cuisines'] == 'American']
    if not comida_americana.empty:
        nota_max = comida_americana['aggregate_rating'].max()
        mais_antigo = comida_americana[comida_americana['aggregate_rating'] == nota_max].sort_values('restaurant_id', ascending=True)
        mais_antigo = mais_antigo.iloc[0]

        col2.metric(label=f"Americana: {mais_antigo['restaurant_name']}",
                    value=mais_antigo['aggregate_rating'],
                    help=f"País: {mais_antigo['country']} | Cidade: {mais_antigo['city']}")
    else:
        col2.metric(label="Americana: Não encontrado", value="N/A")

with col3:
    comida_arabe = df_filtrado[df_filtrado['cuisines'] == 'Arabian']
    if not comida_arabe.empty:
        nota_max = comida_arabe['aggregate_rating'].max()
        melhor_restaurante = comida_arabe[comida_arabe['aggregate_rating'] == nota_max]
        melhor_restaurante = melhor_restaurante.iloc[0]

        col3.metric(label=f"Árabe: {melhor_restaurante['restaurant_name']}",
                    value=melhor_restaurante['aggregate_rating'],
                    help=f"País: {melhor_restaurante['country']} | Cidade: {melhor_restaurante['city']}")
    else:
        col3.metric(label="Árabe: Não encontrado", value="N/A")

with col4:
    comida_japonesa = df_filtrado[df_filtrado['cuisines'] == 'Japanese']
    if not comida_japonesa.empty:
        nota_max = comida_japonesa['aggregate_rating'].max()
        top_restaurantes = comida_japonesa[comida_japonesa['aggregate_rating'] == nota_max]
        mais_antigo = top_restaurantes.sort_values('restaurant_id', ascending=True)
        mais_antigo = mais_antigo.iloc[0]

        col4.metric(label=f"Japonesa: {mais_antigo['restaurant_name']}",
                    value=mais_antigo['aggregate_rating'],
                    help=f"País: {mais_antigo['country']} | Cidade: {mais_antigo['city']}")
    else:
        col4.metric(label="Japonesa: Não encontrado", value="N/A")

with col5:
    comida_caseira = df_filtrado[df_filtrado['cuisines'] == 'Home-made']
    if not comida_caseira.empty:
        top_restaurante = comida_caseira.sort_values('aggregate_rating', ascending=False).head(1)
        nome_rest = top_restaurante.iloc[0]['restaurant_name']
        nota_rest = top_restaurante.iloc[0]['aggregate_rating']
        pais_rest = top_restaurante.iloc[0]['country']
        cidade_rest = top_restaurante.iloc[0]['city']
    else:
        nome_rest = "Não encontrado"
        nota_rest = "N/A"
        pais_rest = "-"
        cidade_rest = "-"

    col5.metric(label=f"Caseira: {nome_rest}",
                value=nota_rest,
                help=f"País: {pais_rest} | Cidade: {cidade_rest}")

st.markdown(f'### Top {num_restaurantes} melhores e mais antigos Restaurantes de cada país')
# DataFrame com os melhores restaurantes de cada país

# Filtra o DataFrame 'df1' para incluir apenas os países selecionados no multiselect
# e as culinárias selecionadas.
df_filtrado_paises_culinarias = df1.copy()

if paises:
    df_filtrado_paises_culinarias = df_filtrado_paises_culinarias[df_filtrado_paises_culinarias['country'].isin(paises)]

if culinarias:
    df_filtrado_paises_culinarias = df_filtrado_paises_culinarias[df_filtrado_paises_culinarias['cuisines'].isin(culinarias)]

# Encontra o restaurante com a maior avaliação para cada país e culinária,
# usando o DataFrame filtrado.
melhores_idx = df_filtrado_paises_culinarias.groupby(['country', 'cuisines'])['aggregate_rating'].idxmax()

melhores_restaurantes = df_filtrado_paises_culinarias.loc[melhores_idx]
melhores_restaurantes = melhores_restaurantes.loc[:, ['restaurant_id', 'restaurant_name', 'city', 'cuisines', 'average_cost_for_two', 'aggregate_rating', 'country']]
melhores_restaurantes = melhores_restaurantes.sort_values(['country', 'aggregate_rating'], ascending=[True, False])

# Limita o dataframe ao número de restaurantes selecionado pelo usuário.
melhores_restaurantes = melhores_restaurantes.head(num_restaurantes)

st.dataframe(melhores_restaurantes)

col1, col2 = st.columns(2)

with col1:
    # Gráfico Top melhores tipos de culinárias

    melhores_culinarias = df1.groupby('cuisines', as_index = False)['aggregate_rating'].mean().sort_values(by = 'aggregate_rating', ascending = False).head(num_restaurantes)

    fig = px.bar(
        melhores_culinarias,
        x = 'cuisines',
        y = 'aggregate_rating',
        title = f'Top {num_restaurantes} melhores tipos de culinárias',
        labels = {'cuisines':'Tipos de culinárias','aggregate_rating':'Média de avaliação média'},
        color = 'cuisines'
    )
    st.plotly_chart(fig)

with col2:

    # Gráfico Top piores tipos de culinárias
    piores_culinarias = df1.groupby('cuisines', as_index = False)['aggregate_rating'].mean().sort_values(by = 'aggregate_rating', ascending = True).head(num_restaurantes)

    fig = px.bar(
        piores_culinarias,
        x = 'cuisines',
        y = 'aggregate_rating',
        title = f'Top {num_restaurantes} piores tipos de culinárias',
        labels = {'cuisines':'Tipos de culinárias','aggregate_rating':'Média de avaliação média'},
        color = 'cuisines'
    )
    st.plotly_chart(fig)