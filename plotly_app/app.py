# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd

from points_by_hand import DealtHand

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

# df = pd.read_csv("csv_outputs/crib_hands_output.csv")
# df = pd.read_parquet("crib_hands_output_smol.parquet")
# df = pd.read_parquet("csv_outputs/crib_hands_output_big_boi.parquet")
# df = pd.read_csv("crib_hands_output_smol.csv")
df = pd.read_parquet("../csv_outputs/crib_hands_sorted.parquet")

# df = df.head(20)


# should sort input string to make sure it matches one of the hands
def sort_hand(hand: str) -> str:
    cards = hand.split(",")
    cards.sort()
    return ",".join(cards)


# hand = "2H,3H,4H,5H,6H,8H"
hand = "5S,3C,8D,5C,9H,AH"
hand_obj = DealtHand(hand, df)

# hand_df = hand_obj.get_df()
# row_of_hand_df = df.iloc[12]
# row_of_hand_df = df.loc[df["cut_card"] == "TD"]
# sorted_hand = sort_hand(hand)

# row_of_df = df.loc[df["dealt_hand_sorted_str"] == sorted_hand]

# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
# fig = px.bar(hand_obj.to_dict(), x="cut_card")

hand_obj_dict = hand_obj.to_dict()
hand_obj_dict_list = list(hand_obj_dict.items())

hand_records = hand_obj.get_df().to_dict("records")
print(hand_records)
print([{"name": i, "id": i} for i in hand_obj.to_dict().keys()])

dt = dash_table.DataTable(
    hand_records,
    [{"name": i, "id": i} for i in hand_obj_dict.keys()],
)

app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash :D"),
        html.Div(
            children="""
        Dash: A web application framework for your data.
    """
        ),
        # dcc.Graph(id="example-graph", figure=fig),
        # html.Div(children=row_of_hand_df),
        # html.Div(children=row_of_df["dealt_hand"]),
        # html.Div(children=row_of_df["max_hand"]),
        # html.Div(children=row_of_df["max_hand_max_points"]),
        # html.Div(children=row_of_df["max_hand_ev_points"]),
        html.Div(children=dt),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
