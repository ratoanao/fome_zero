import plotly.express as px
import streamlit as st
from PIL import Image

from data_processing import load_data


st.set_page_config(page_title="Cuisines", page_icon="🍛", layout="wide")


df1 = load_data()


def best_restaurant_by_cuisine(df, cuisine):
    cuisine_df = df[df["cuisines"] == cuisine]

    if cuisine_df.empty:
        return None

    return (
        cuisine_df.sort_values(
            ["aggregate_rating", "restaurant_id"],
            ascending=[False, True],
        )
        .head(1)
        .iloc[0]
    )


def cuisine_metric(column, cuisine_label, cuisine_name):
    restaurant = best_restaurant_by_cuisine(df_filtrado, cuisine_name)

    if restaurant is None:
        column.metric(label=f"{cuisine_label}: Não encontrado", value="N/A")
        return

    column.metric(
        label=f"{cuisine_label}: {restaurant['restaurant_name']}",
        value=restaurant["aggregate_rating"],
        help=f"País: {restaurant['country']} | Cidade: {restaurant['city']}",
    )


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

num_restaurantes = st.sidebar.slider(
    label="Selecione a quantidade de restaurantes que deseja visualizar",
    min_value=1,
    max_value=20,
    value=10,
    step=1,
)

df_filtrado = df1.copy()

if paises:
    df_filtrado = df_filtrado[df_filtrado["country"].isin(paises)]

melhores_culinarias = (
    df_filtrado.groupby("cuisines", as_index=False)["aggregate_rating"]
    .mean()
    .sort_values(by="aggregate_rating", ascending=False)
    .head(num_restaurantes)
)

culinarias = st.sidebar.multiselect(
    label="Selecione os tipos de culinárias",
    options=melhores_culinarias["cuisines"].tolist(),
)

st.sidebar.markdown("""---""")

if culinarias:
    df_filtrado = df_filtrado[df_filtrado["cuisines"].isin(culinarias)]


# ============================================================
# Layout no Streamlit
# ============================================================

st.title("🍛 Cuisines")
st.markdown("Melhores Restaurantes dos Principais tipos Culinários")

col1, col2, col3, col4, col5 = st.columns(5)

cuisine_metric(col1, "Italiana", "Italian")
cuisine_metric(col2, "Americana", "American")
cuisine_metric(col3, "Árabe", "Arabian")
cuisine_metric(col4, "Japonesa", "Japanese")
cuisine_metric(col5, "Caseira", "Home-made")

st.markdown(f"### Top {num_restaurantes} melhores e mais antigos restaurantes")

melhores_restaurantes = df_filtrado.copy()

if melhores_restaurantes.empty:
    st.warning("Nenhum restaurante encontrado para os filtros selecionados.")
else:
    melhores_idx = melhores_restaurantes.groupby(["country", "cuisines"])[
        "aggregate_rating"
    ].idxmax()

    melhores_restaurantes = melhores_restaurantes.loc[melhores_idx]
    melhores_restaurantes = melhores_restaurantes.loc[
        :,
        [
            "restaurant_id",
            "restaurant_name",
            "city",
            "cuisines",
            "average_cost_for_two",
            "aggregate_rating",
            "country",
        ],
    ]
    melhores_restaurantes = melhores_restaurantes.sort_values(
        ["country", "aggregate_rating"],
        ascending=[True, False],
    ).head(num_restaurantes)

    st.dataframe(melhores_restaurantes, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    melhores_culinarias = (
        df_filtrado.groupby("cuisines", as_index=False)["aggregate_rating"]
        .mean()
        .sort_values(by="aggregate_rating", ascending=False)
        .head(num_restaurantes)
    )

    fig = px.bar(
        melhores_culinarias,
        x="cuisines",
        y="aggregate_rating",
        title=f"Top {num_restaurantes} melhores tipos de culinárias",
        labels={
            "cuisines": "Tipos de culinárias",
            "aggregate_rating": "Média de avaliação",
        },
        color="cuisines",
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    piores_culinarias = (
        df_filtrado.groupby("cuisines", as_index=False)["aggregate_rating"]
        .mean()
        .sort_values(by="aggregate_rating", ascending=True)
        .head(num_restaurantes)
    )

    fig = px.bar(
        piores_culinarias,
        x="cuisines",
        y="aggregate_rating",
        title=f"Top {num_restaurantes} piores tipos de culinárias",
        labels={
            "cuisines": "Tipos de culinárias",
            "aggregate_rating": "Média de avaliação",
        },
        color="cuisines",
    )
    st.plotly_chart(fig, use_container_width=True)
