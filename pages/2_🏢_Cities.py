import plotly.express as px
import streamlit as st
from PIL import Image

from data_processing import load_data


st.set_page_config(page_title="Cities", page_icon="🏢", layout="wide")


df1 = load_data()


# ============================================================
# Barra lateral no Streamlit
# ============================================================

image = Image.open("logo.png")
st.sidebar.image(image, width=120)

st.sidebar.markdown("# Filtros")

paises = st.sidebar.multiselect(
    "Escolha os países que deseja visualizar as informações",
    sorted(df1["country"].unique()),
)

st.sidebar.markdown("""---""")

if paises:
    df_filtrado = df1[df1["country"].isin(paises)]
else:
    df_filtrado = df1.copy()


# ============================================================
# Layout no Streamlit
# ============================================================

st.title("🏢 Cities")
st.markdown("Top 10 cidades com mais restaurantes registrados na base de dados")

top10_restaurantes = (
    df_filtrado.groupby("city", as_index=False)["restaurant_id"]
    .nunique()
    .sort_values(by="restaurant_id", ascending=False)
    .head(10)
)

fig = px.bar(
    top10_restaurantes,
    x="city",
    y="restaurant_id",
    title="Top 10 cidades com mais restaurantes registrados na base de dados",
    labels={"city": "Cidades", "restaurant_id": "Quantidade de Restaurantes"},
    color="city",
)
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    maior_4 = df_filtrado[df_filtrado["aggregate_rating"] > 4]
    top7_cidades = (
        maior_4.groupby("city", as_index=False)["restaurant_id"]
        .nunique()
        .sort_values(by="restaurant_id", ascending=False)
        .head(7)
    )

    fig = px.bar(
        top7_cidades,
        x="city",
        y="restaurant_id",
        title="Top 7 cidades com restaurantes com média de avaliação acima de 4",
        labels={"city": "Cidades", "restaurant_id": "Quantidade de restaurantes"},
        color="city",
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    menor_25 = df_filtrado[df_filtrado["aggregate_rating"] < 2.5]
    menor_25 = (
        menor_25.groupby("city", as_index=False)["restaurant_id"]
        .nunique()
        .sort_values(by="restaurant_id", ascending=False)
        .head(7)
    )

    fig = px.bar(
        menor_25,
        x="city",
        y="restaurant_id",
        title="Top 7 cidades com restaurantes com média de avaliação abaixo de 2.5",
        labels={"city": "Cidades", "restaurant_id": "Quantidade de restaurantes"},
        color="city",
    )
    st.plotly_chart(fig, use_container_width=True)

top10_culinarias = (
    df_filtrado.groupby("city", as_index=False)["cuisines"]
    .nunique()
    .sort_values(by="cuisines", ascending=False)
    .head(10)
)

fig = px.bar(
    top10_culinarias,
    x="city",
    y="cuisines",
    title="Top 10 cidades com mais restaurantes com tipos culinários distintos",
    labels={"city": "Cidades", "cuisines": "Tipos de culinárias distintas"},
    color="city",
)
st.plotly_chart(fig, use_container_width=True)
