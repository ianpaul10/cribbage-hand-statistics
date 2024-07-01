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
