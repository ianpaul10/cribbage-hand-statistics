import pandas as pd


def sort_crib_hands_csv(csv_path: str, output_path: str):
    df = pd.read_csv(csv_path)

    df["sorted_hand"] = df[
        [
            "hand_card_1",
            "hand_card_2",
            "hand_card_3",
            "hand_card_4",
            "cut_card",
        ]
    ].apply(lambda row: sorted([str(item) for item in row]), axis=1)
    df["sorted_hand"] = df["sorted_hand"].apply(lambda x: ",".join(x))

    df = df.drop(
        columns=["hand_card_1", "hand_card_2", "hand_card_3", "hand_card_4", "cut_card"]
    )
    df.set_index("sorted_hand", inplace=True)

    df.to_csv(output_path, index=True)
    df.to_parquet(output_path.replace(".csv", ".parquet"))


if __name__ == "__main__":
    sort_crib_hands_csv(
        # "csv_outputs/crib_hands_smoler.csv", "csv_outputs/crib_hands_sorted_smoler.csv"
        "csv_outputs/crib_hands.csv",
        "csv_outputs/crib_hands_sorted.csv",
    )
