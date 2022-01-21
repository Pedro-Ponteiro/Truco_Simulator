import os

import pandas as pd

from modules.classes.classes_base import Jogo, Time
from modules.classes.jogadores import JogadorProbabilistico


def main(nr_maos: int) -> int:
    """Simulate games and output data to dados.csv and dados.pickle.

    Args:
        nr_maos (int): number of rows to be generated (each set of 3 rounds has 4 rows)

    Returns:
        int: number of hands generated
    """
    jogador1, jogador2 = JogadorProbabilistico("Pedro"), JogadorProbabilistico("Manu")
    jogador3, jogador4 = JogadorProbabilistico("Mari"), JogadorProbabilistico("Ariel")
    time1 = Time("PENU", jogador1, jogador2)
    time2 = Time("ARIMA", jogador3, jogador4)

    nr_mesas = nr_maos // 4

    # TODO: passar apenas o time1 e time2 como parametros
    jogo = Jogo(nr_mesas, [jogador1, jogador3, jogador2, jogador4], time1, time2)

    df = pd.DataFrame(jogo.mesas_stats)
    print(f"Quantidade de mãos geradas: {len(df)}")

    df.to_pickle(os.path.join(".", "dados.pickle"))
    df.to_csv(os.path.join(".", "dados.csv"))

    return len(df)
