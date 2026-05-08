import inflection
import pandas as pd
import streamlit as st


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

COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}


def country_name(country_id):
    return COUNTRIES.get(country_id, "Unknown")


def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    if price_range == 2:
        return "normal"
    if price_range == 3:
        return "expensive"
    return "gourmet"


def color_name(color_code):
    return COLORS.get(color_code, "unknown")


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
    df["price_type"] = df["price_range"].apply(create_price_type)
    df["color_name"] = df["rating_color"].apply(color_name)

    df = df[df["cuisines"].notna()].copy()
    df["cuisines"] = df["cuisines"].apply(lambda x: x.split(",")[0])
    df = df.drop_duplicates(subset="restaurant_id", keep="first")

    return df
