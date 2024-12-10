import streamlit as st
import pandas as pd
from io import StringIO, BytesIO
from itertools import combinations
import numpy as np
import duckdb
from code_editor import code_editor
from PIL import Image
import os
from groq import Groq
from groq.types import ImageBinary


@st.cache_resource
def get_db_connection():
    if "duck_conn" not in st.session_state:
        st.session_state["duck_conn"] = duckdb.connect(":memory:")

    return st.session_state["duck_conn"]


def main():
    conn = get_db_connection()
    create_side_bar(conn)
    create_page(conn)


def create_side_bar(conn: duckdb.DuckDBPyConnection):
    cur = conn.cursor()

    with st.sidebar:
        # Add Groq API Key input
        api_key = st.text_input("Groq API Key", type="password")
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key

        st.divider()
        st.button(
            "load sample data",
            on_click=load_sample_data,
            args=[conn],  # pyright: ignore[reportArgumentType]
        )
        files = st.file_uploader(
            "select one or more CSV or JSON files", accept_multiple_files=True
        )

        load_files(conn, files)  # pyright: ignore[reportArgumentType]

        st.divider()

        table_list = ""
        cur.execute("show all tables")
        recs = cur.fetchall()

        if len(recs) > 0:
            st.markdown("# tables")

        for rec in recs:
            table_name = rec[2]
            table_list += f"- {table_name}\n"
            cur.execute(f"describe {table_name}")

            for col in cur.fetchall():
                table_list += f"    - {col[0]} {col[1]}\n"

        st.markdown(table_list)


def load_sample_data(conn: duckdb.DuckDBPyConnection):
    conn.read_parquet("csv_outputs/crib_hands_sorted.parquet").to_table("posts")
    # conn.read_parquet("csv_outputs/crib_hands_output_big_boi.parquet").to_table("posts")
    # conn.read_parquet("csv_outputs/crib_hands_sorted.parquet").to_table("posts")


# should sort input string to make sure it matches one of the hands
def sort_hand(hand: str) -> str:
    cards = hand.replace(" ", "").split(",")
    cards.sort()
    return ",".join(cards)


def detect_cards_from_image(image):
    # Initialize Groq client
    if "GROQ_API_KEY" not in os.environ:
        raise ValueError("Please set your Groq API Key in the sidebar first")

    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    # Convert PIL Image to bytes
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()

    # Create the prompt for the vision model
    prompt = """
    Look at this image of playing cards and:
    1. Identify each playing card visible in the image. There should be 4-6 cards.
    2. List them in the format: [Value][Suit], where:
       - Values are: A,2,3,4,5,6,7,8,9,T,J,Q,K
       - Suits are: C (Clubs), D (Diamonds), H (Hearts), S (Spades)
    3. Return the cards as a comma-separated list
    Example format: "AC,2H,KD,TS"

    DO NOT HALUCINATE. DO NOT INCLUDE ANY OTHER TEXT.
    """

    # Make the API call
    response = client.chat.completions.create(
        model="llama2-70b-v2",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_binary", "image_binary": {"data": img_byte_arr}},
                ],
            }
        ],
    )

    # Extract the detected cards from the response
    detected_cards = response.choices[0].message.content.strip()

    # Basic validation that the format is correct
    cards = detected_cards.split(",")
    valid_cards = []
    for card in cards:
        card = card.strip()
        if len(card) == 2 and card[0] in "A23456789TJQK" and card[1] in "CDHS":
            valid_cards.append(card)

    return ",".join(valid_cards)


def get_hands(six_card_hand: str) -> list:
    cards = six_card_hand.replace(" ", "").split(",")
    if len(cards) not in {5, 6}:
        # TODO: check to make sure it's not less than 5 cards
        # only take first 5 or 6 cards
        cards = cards[:5]
    possible_hands_tuples = list(combinations(cards, r=4))

    sorted_hands = [sort_hand(",".join(hand)) for hand in possible_hands_tuples]
    return sorted_hands
    # "unique_hands_dealt = math.comb(len(deck), starting_hand_size)\n",


def create_page(conn: duckdb.DuckDBPyConnection):
    st.title("Welcome to my crib :duck:")
    st.write("Query your files with DuckDB")

    st.divider()

    cur = conn.cursor()

    st.write("Upload an image of your cards")
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Detect Cards"):
            with st.spinner("Analyzing image..."):
                try:
                    detected_hand = detect_cards_from_image(image)
                    st.success(f"Detected cards: {detected_hand}")
                    st.session_state["detected_hand"] = detected_hand
                except Exception as e:
                    st.error(f"Error detecting cards: {str(e)}")

    st.write(
        "Input 6 or 5 card hand, depending on whether you're playing a 2 or 3 person game. All possible 4 card hands + cut card will be calculated to determine the optimal hand to play."
    )
    six_card_hand = st.text_input("Add 5 or 6 card hand", "QC,TH,JD,4S,3H,2S")
    dix_card_calc_button = st.button("calculate all possibilities")

    if dix_card_calc_button:
        sorted_hands = get_hands(six_card_hand)
        sorted_hands = [f"'{hand}'" for hand in sorted_hands]
        sored_hands_str = ",".join(sorted_hands)
        cur.execute(f"select * from posts where sorted_hand in ({sored_hands_str})")
        df = cur.fetch_df()
        st.write(f"num of possible hands: {len(sorted_hands)}")
        st.write(f"num of possible outcomes with possible crib cards: {len(df)}")

        st.write(df)

    st.divider()

    # hand_str = st.text_input("6 card hand", "QC,10H,JD,4S,3H,2S")
    hand_str = st.text_input("5 card deal", "QC,TH,JD,5S,4D")
    # button to sort hand and then query db with sorted hand
    if st.button("sort hand"):
        sorted_hand = sort_hand(hand_str)
        # TODO: add a check to make sure the hand is valid
        cur.execute(f"select * from posts where sorted_hand = '{sorted_hand}'")
        df = cur.fetch_df()
        st.write(df)

    st.divider()

    st.write(
        "hint: you can write multiple queries as long as each one ends with a semicolon"
    )
    st.write("ctrl+enter to run the SQL")
    res = code_editor(code="", lang="sql", key="editor")

    for query in res["text"].split(";"):
        if query.strip() == "":
            continue

        try:
            cur.execute(query)
            df = cur.fetch_df()
            st.write(df)
        except Exception as e:
            st.error(e)

    if st.button("reset database"):
        st.cache_resource.clear()
        st.session_state["editor"]["text"] = ""
        st.rerun()


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
