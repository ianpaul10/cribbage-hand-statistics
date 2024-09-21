import pandas as pd

from plotly_app.points_by_hand import DealtHand


if __name__ == "__main__":
    df = pd.read_parquet("csv_outputs/crib_hands_sorted.parquet")
    hand = "2C,2H,3H,4H,7D,QC"

    hand_obj = DealtHand(hand, df)

    # print(hand_obj.to_dict())
    print(hand_obj.pretty_print())
    print(hand_obj.get_df())
