import folium
import streamlit as st
from folium.plugins import MarkerCluster
from PIL import Image
from streamlit_folium import st_folium

from data_processing import load_data


st.set_page_config(page_title="Home", page_icon="🍛", layout="wide")


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

st.title("🍛 Fome Zero")
st.subheader("O melhor lugar para encontrar seu mais novo restaurante favorito!")
st.subheader("Temos as seguintes marcas dentro da nossa plataforma:")

col1, col2, col3, col4, col5 = st.columns(5, gap="large")

with col1:
    restaurantes_unicos = df_filtrado["restaurant_id"].nunique()
    restaurantes_unicos_formatado = f"{restaurantes_unicos:,}"
    col1.metric("Restaurantes Cadastrados", value=restaurantes_unicos_formatado)

with col2:
    paises_unicos = df_filtrado["country"].nunique()
    col2.metric("Países Cadastrados", value=paises_unicos)

with col3:
    cidades_unicas = df_filtrado["city"].nunique()
    col3.metric("Cidades Cadastradas", value=cidades_unicas)

with col4:
    avaliacoes = df_filtrado["votes"].sum()
    avaliacoes_formatadas = f"{avaliacoes:,}"
    col4.metric("Avaliações na Plataforma", value=avaliacoes_formatadas)

with col5:
    tipos_culinaria = df_filtrado["cuisines"].nunique()
    col5.metric("Culinárias Registradas", value=tipos_culinaria)


# ==================================================================
# ======================= MAPA DOS RESTAURANTES ====================
# ==================================================================

st.title("Mapa dos Restaurantes")

if df_filtrado.empty:
    st.warning("Nenhum restaurante encontrado para os filtros selecionados.")
else:
    latitude_media = df_filtrado["latitude"].mean()
    longitude_media = df_filtrado["longitude"].mean()

    mapa = folium.Map(
        location=[latitude_media, longitude_media],
        zoom_start=1,
        control_scale=True,
    )
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
            location=[row["latitude"], row["longitude"]],
            popup=folium.Popup(html_popup, max_width=300),
        ).add_to(cluster)

    st_folium(mapa, width=None, height=500)

csv = df_filtrado.to_csv(index=False)
st.download_button(
    label="📥 Baixar Dados Filtrados (CSV)",
    data=csv,
    file_name="dados_filtrados.csv",
    mime="text/csv",
)
