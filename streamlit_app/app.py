import streamlit as st
import pandas as pd
import numpy as np

st.title("Uber pickups in NYC")


@st.cache_data
def load_data(nrows):
    # data = pd.read_csv(DATA_URL, nrows=nrows)
    # lowercase = lambda x: str(x).lower()
    # data.rename(lowercase, axis='columns', inplace=True)
    # data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    # return data

    # df = pd.read_parquet("../csv_outputs/crib_hands_sorted.parquet")
    df = pd.read_parquet("csv_outputs/crib_hands_sorted.parquet")
    return df


# Create a text element and let the reader know the data is loading.
data_load_state = st.text("Loading data...")
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache_data)")
