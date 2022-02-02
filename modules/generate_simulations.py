"""Uses the players and game classes to simulate a given number of games."""

import os

import pandas as pd

from modules.classes.base_classes import Game, Team
from modules.classes.players import PlayerImplementation1


def main(hands_quantity: int) -> int:
    """Simulate games and output data to dados.csv and dados.pickle.

    Args:
        hands_quantity (int): number of rows to be generated
        (each set of 3 rounds has 4 rows)

    Returns:
        int: number of hands generated
    """
    player1, player2 = PlayerImplementation1("Pedro"), PlayerImplementation1("Manu")
    player3, player4 = PlayerImplementation1("Mari"), PlayerImplementation1("Ariel")
    team1 = Team("PENU", player1, player2)
    team2 = Team("ARIMA", player3, player4)

    table_quantity = hands_quantity // 4

    # TODO: only pass teams as parameters
    game = Game(table_quantity, [player1, player3, player2, player4], team1, team2)

    df = pd.DataFrame(game.table_stats)
    print(f"Number of hands generated: {len(df)}")

    df.to_pickle(os.path.join(".", "data.pickle"))
    df.to_csv(os.path.join(".", "data.csv"))

    print("Hands data saved to 'data.csv' and 'data.pickle'")

    return len(df)
