import itertools
import requests
import csv
import utils


def run():
    possible_hands = list(itertools.combinations(utils.boring_deck, r=4))
    print(f"{len(possible_hands)=:,}")

    # write to csv
    with open("crib_hands.csv", "w") as csv_file:
        writer = csv.writer(csv_file)
        headers = [
            "points",
            "hand_card_1",
            "hand_card_2",
            "hand_card_3",
            "hand_card_4",
            "cut_card",
        ]
        writer.writerow(headers)

        for dealt_hand in possible_hands:
            dealt_hand = list(dealt_hand)

            remaining_deck = utils.boring_deck.copy()
            [remaining_deck.remove(card) for card in dealt_hand]

            for cut_card in remaining_deck:
                full_hand = dealt_hand + [cut_card]

                path_param = ",".join(full_hand)

                # Credit to https://github.com/dkackman/CribbageCounter.
                # You can run run the server locally so you don't spam his API.
                # url = f"https://cribbagecounter.kackman.net/api/score?hand={path_param}&isCrib=false"
                url = f"http://localhost:3000/api/score?hand={path_param}&isCrib=false"
                response = requests.get(url)
                val = response.text
                row = [val] + full_hand
                writer.writerow(row)


if __name__ == "__main__":
    run()
    print("Done!")
