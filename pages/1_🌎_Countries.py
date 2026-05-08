import plotly.express as px
import streamlit as st
from PIL import Image

from data_processing import load_data


st.set_page_config(page_title="Countries", page_icon="🌎", layout="wide")


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

st.title("🌎 Countries")
st.markdown("Quantidade de restaurantes registrados por país")

df_grouped = (
    df_filtrado.groupby("country", as_index=False)["restaurant_id"]
    .count()
    .sort_values(by="restaurant_id", ascending=False)
)

fig = px.bar(
    df_grouped,
    x="country",
    y="restaurant_id",
    title="Quantidade de restaurantes por país",
    labels={"country": "País", "restaurant_id": "Quantidade de Restaurantes"},
    color="country",
)
st.plotly_chart(fig, use_container_width=True)

cidade_x_pais = (
    df_filtrado.groupby("country", as_index=False)["city"]
    .nunique()
    .sort_values(by="city", ascending=False)
)

fig = px.bar(
    cidade_x_pais,
    x="country",
    y="city",
    title="Quantidade de cidades registradas por país",
    labels={"country": "Países", "city": "Quantidade de cidades"},
    color="country",
)
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    media_avaliacoes = (
        df_filtrado.groupby("country", as_index=False)["votes"]
        .mean()
        .sort_values(by="votes", ascending=False)
    )

    fig = px.bar(
        media_avaliacoes,
        x="country",
        y="votes",
        title="Média de avaliações feitas por país",
        labels={"country": "Países", "votes": "Avaliações"},
        color="country",
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    media_2_pessoas = (
        df_filtrado.groupby("country", as_index=False)["average_cost_for_two"]
        .mean()
        .sort_values(by="average_cost_for_two", ascending=False)
    )

    fig = px.bar(
        media_2_pessoas,
        x="country",
        y="average_cost_for_two",
        title="Média de preço de um prato para duas pessoas",
        labels={
            "country": "Países",
            "average_cost_for_two": "Preço médio para duas pessoas",
        },
        color="country",
    )
    st.plotly_chart(fig, use_container_width=True)
