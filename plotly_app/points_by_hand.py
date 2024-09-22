import statistics
import pandas as pd
from itertools import combinations
from pandas import DataFrame
from utils import Deck

hand_size = 4
dealt_hand_size = 6


class PlayedHand:
    def __init__(
        self, hand_cards: list[str], cut_card: str, hand_to_points_df: DataFrame
    ):
        self.hand_cards = hand_cards
        self.cut_card = cut_card
        self.points: int = self._get_points(hand_cards, cut_card, hand_to_points_df)

    def _get_points(
        self, hand_cards: list[str], cut_card: str, hand_to_points_df: DataFrame
    ):
        hand_list = list(hand_cards) + [cut_card]
        hand_list.sort()
        hand_list_str = ",".join(hand_list)
        row = hand_to_points_df.loc[hand_list_str]
        return int(row["points"].values[0])
        # return hand_to_points_df.loc[hand_list]["points"]

    def to_dict(self):
        return {
            "hand": self.hand_cards,
            "cut_card": self.cut_card,
            "points": self.points,
        }


class PossibleHand:
    def __init__(
        self,
        four_card_hand: list[str],
        possible_crib_cards: list[str],
        hand_to_points_df: DataFrame,
    ):
        print(f"four_card_hand: {four_card_hand}")
        self.hand = four_card_hand
        self.possible_crib_cards = possible_crib_cards

        # self.possible_played_hands: list[PlayedHand] = []
        self.possible_points: list[int] = []
        self.points_max: int = 0
        self.points_min: int = 29

        self.possible_hands = [
            self.hand + [cut_card] for cut_card in possible_crib_cards
        ]
        self.possible_hands_strs = []
        for hand in self.possible_hands:
            hand.sort()
            hand_str = ",".join(hand)
            self.possible_hands_strs.append(hand_str)

        self.posible_points = hand_to_points_df.loc[
            self.possible_hands_strs, "points"
        ].tolist()

        # for cut_card in possible_crib_cards:
        #     played_hand = PlayedHand(four_card_hand, cut_card, hand_to_points_df)
        #     self.possible_played_hands.append(played_hand)
        #     self.possible_points.append(played_hand.points)

        #     self.points_max = max(self.points_max, played_hand.points)
        #     self.points_min = min(self.points_min, played_hand.points)
        # self.points_ev = statistics.mean(self.possible_points)
        # self.points_stdev = statistics.stdev(self.possible_points)
        # self.points_median = statistics.median(self.possible_points)

    def to_dict(self):
        x = {}
        for i, point in enumerate(self.possible_points):
            x[self.possible_crib_cards[i]] = point

        return x


class DealtHand:
    def __init__(
        self, dealt_hand: str, hand_to_points_df: DataFrame, my_crib: bool = True
    ):
        self.my_crib = my_crib
        self.deck = Deck.boring_deck

        dealt_cards = dealt_hand.split(",")
        assert len(dealt_cards) == dealt_hand_size
        self.dealt_cards = dealt_cards

        # len == 46
        self.possible_cut_cards = [
            card for card in self.deck if card not in dealt_cards
        ]

        # len == 15
        self.hand_candidates = list(combinations(dealt_cards, r=hand_size))

        # self.possible_hands = [
        #     PossibleHand(list(hand), self.possible_cut_cards, hand_to_points_df)
        #     for hand in self.hand_candidates
        # ]

        # len == 690
        _hand_tuples = []
        self.possible_hands_strs = []
        for hand in self.hand_candidates:
            hcl = list(hand)
            hcl.sort()
            hcl_str = ",".join(hcl)
            for cut_card in self.possible_cut_cards:
                hand_list = hcl + [cut_card]
                hand_list_str = ",".join(hand_list)
                self.possible_hands_strs.append(hand_list_str)
                _hand_tuples.append((hand_list_str, hcl_str, cut_card))

        # print(f"{len(self.possible_hands_strs)=}")
        _sub_df = hand_to_points_df.loc[self.possible_hands_strs]

        # TODO: for me tm. Make sub_df add the hand and cut card as separate columns
        # then we'll be able to pivot the df and have it be rows of cut cards and columns of hands, and values should line up correctly
        # current way is a hack

        _sub_df.drop(
            columns=["hand_card_1", "hand_card_2", "hand_card_3", "hand_card_4"],
            inplace=True,
        )

        self.pivoted_df = _sub_df.pivot(
            columns="sorted_hand",
            index="cut_card",
            values="points",
        )
        self.pivoted_df = self.pivoted_df.reset_index()

        self.point_conjoined = _sub_df["points"].tolist()
        self.points = [
            self.point_conjoined[i : i + len(self.possible_cut_cards)]
            for i in range(0, len(self.point_conjoined), len(self.possible_cut_cards))
        ]

        # print("POINTS")
        # print(self.points)

        # self.ev_hand = max(self.possible_hands, key=lambda hand: hand.points_ev)
        # self.max_hand = max(self.possible_hands, key=lambda hand: hand.points_max)
        # self.median_hand = max(self.possible_hands, key=lambda hand: hand.points_median)

        # for hand in _possible_hands_tuples:
        #     hand_list = list(hand)
        #     for cut_card in self.possible_cut_cards:
        #         hand_list.append(cut_card)
        #         hand_list.sort()
        #         points = hand_to_points_df.loc[hand_list]["points"]

    # def to_dict(self):
    #     x = {}
    #     for i, possible_hand in enumerate(self.possible_hands):
    #         x[self.hand_candidates[i]] = possible_hand.to_dict()
    #     return x

    def to_dict(self):
        x = {}
        x["cut_card"] = self.possible_cut_cards
        for i, hand in enumerate(self.hand_candidates):
            hand_str = ",".join(hand)
            x[hand_str] = self.points[i]
        return x

    def get_df(self):
        return pd.DataFrame(self.to_dict())

    def get_table(self):
        columns = self.possible_cut_cards
        rows = self.hand_candidates

        sublist_len = len(columns)

        split_vals = [
            self.point_conjoined[i : i + sublist_len]
            for i in range(0, len(self.point_conjoined), sublist_len)
        ]

        # vals: list[int] = []
        # for hand in self.possible_hands:
        #     for played_hand in hand.possible_points:
        #         vals.append(played_hand)

        return rows, columns, split_vals

    def pretty_print(self):
        print(f"Dealt hand: {self.dealt_cards}")
        rows, columns, vals = self.get_table()
        print(rows)
        print(columns)
        print(vals)
