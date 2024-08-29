# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

# df = pd.read_csv("csv_outputs/crib_hands_output.csv")
df = pd.read_csv("crib_hands_output_smol.csv")

df = df.head(20)

row_of_df = df.loc[df["dealt_hand"] == "2H,3H,4H,5H,6H,7H"]

# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
fig = px.bar(df, x="dealt_hand", y="max_hand_max_points")

app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash :D"),
        html.Div(
            children="""
        Dash: A web application framework for your data.
    """
        ),
        dcc.Graph(id="example-graph", figure=fig),
        html.Div(children=row_of_df["dealt_hand"]),
        html.Div(children=row_of_df["max_hand"]),
        html.Div(children=row_of_df["max_hand_max_points"]),
        html.Div(children=row_of_df["max_hand_ev_points"]),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
