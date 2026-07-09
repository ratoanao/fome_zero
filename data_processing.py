import inflection
import pandas as pd
import streamlit as st
from PIL import Image


COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zealand",
    162: "Philippines",
    166: "Qatar",
    184: "Singapore",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}


def country_name(country_id):
    return COUNTRIES.get(country_id, "Unknown")


def rename_columns(df):
    df = df.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")

    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new

    return df


@st.cache_data
def load_data(path="data/zomato.csv"):
    df = pd.read_csv(path)
    df = rename_columns(df)

    df["country"] = df["country_code"].apply(country_name)

    df = df[df["cuisines"].notna()].copy()
    df["cuisines"] = df["cuisines"].apply(lambda x: x.split(",")[0])
    df = df.drop_duplicates(subset="restaurant_id", keep="first")

    return df


def render_sidebar_logo(path="logo.png", width=120):
    image = Image.open(path)
    st.sidebar.image(image, width=width)


def country_multiselect(df):
    st.sidebar.markdown("# Filtros")
    return st.sidebar.multiselect(
        "Escolha os países que deseja visualizar as informações",
        sorted(df["country"].unique()),
    )


def filter_by_countries(df, paises):
    if paises:
        return df[df["country"].isin(paises)].copy()
    return df.copy()
