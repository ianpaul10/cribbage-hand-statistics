from itertools import combinations
from typing import Union
import pandas as pd

starting_hand_size = 6
hand_size = 4


_pretty_suits = ["♥", "♦", "♠", "♣"]
_boring_suits = ["H", "D", "S", "C"]

_values = list(range(2, 10))
_values.extend(["T", "J", "Q", "K", "A"])

deck = []
boring_deck = []
for i in range(len(_pretty_suits)):
    for value in _values:
        deck.append(f"{value}{_pretty_suits[i]}")
        boring_deck.append(f"{value}{_boring_suits[i]}")


class AllPossibleTotalHands:
    def __init__(self):
        df = pd.read_csv("crib_hands_smol.csv")


class Deck:
    _pretty_suits = ["♥", "♦", "♠", "♣"]
    _boring_suits = ["H", "D", "S", "C"]

    _values: list[Union[int, str]] = list(range(2, 10))
    _values.extend(["T", "J", "Q", "K", "A"])

    deck: list[str] = []
    boring_deck: list[str] = []
    for i in range(len(_pretty_suits)):
        for value in _values:
            deck.append(f"{value}{_pretty_suits[i]}")
            boring_deck.append(f"{value}{_boring_suits[i]}")


class TotalHand:
    def __init__(self, dealt_hand: list, cut_card: str):
        self.dealt_hand = dealt_hand
        self.cut_card = cut_card

        self.points = 0  # TODO pull from CSV/pandas


class DealtHand:

    def __init__(self, dealt_cards: list):
        remaining_deck = Deck.deck  # AKA possible cut cards
        for card in self.dealt_cards:
            remaining_deck.remove(card)

        self.possible_hands = list(combinations(dealt_cards, r=hand_size))

        possible_total_hands = []

        for hand in self.possible_hands:
            for cut_card in remaining_deck:
                possible_total_hands.append(TotalHand(hand, cut_card))
