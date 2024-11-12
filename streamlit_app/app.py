import streamlit as st
import pandas as pd
from io import StringIO
import numpy as np
import duckdb

st.title("Uber pickups in NYC")


# @st.cache_resource
def get_db_connection():
    if "duck_conn" not in st.session_state:
        st.session_state["duck_conn"] = duckdb.connect(":memory:")

    return st.session_state["duck_conn"]


def main():
    conn = get_db_connection()
    # create_side_bar(conn)
    create_page(conn)


def create_page(conn: duckdb.DuckDBPyConnection):

    # Create a text element and let the reader know the data is loading.
    data_load_state = st.text("Loading data...")
    # Load 10,000 rows of data into the dataframe.
    data = load_data(10000)
    # Notify the reader that the data was successfully loaded.
    data_load_state.text("Done! (using st.cache_data)")


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


def load_files(conn: duckdb.DuckDBPyConnection, files: list):
    for file in files:
        stringio = StringIO(file.getvalue().decode("utf-8"))

        if file.name.endswith(".csv"):
            conn.read_csv(stringio).to_table(file.name[:-4])


if __name__ == "__main__":
    main()

    # # Create a text element and let the reader know the data is loading.
    # data_load_state = st.text("Loading data...")
    # # Load 10,000 rows of data into the dataframe.
    # data = load_data(10000)
    # # Notify the reader that the data was successfully loaded.
    # data_load_state.text("Done! (using st.cache_data)")
