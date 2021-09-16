from time import perf_counter

import pandas as pd

from modules.classes.classes_base import Jogo, Time
from modules.classes.jogadores import JogadorProbabilistico


def main() -> int:
    jogador1, jogador2 = JogadorProbabilistico("Pedro"), JogadorProbabilistico("Manu")
    jogador3, jogador4 = JogadorProbabilistico("Mari"), JogadorProbabilistico("Ariel")
    time1 = Time("PENU", jogador1, jogador2)
    time2 = Time("ARIMA", jogador3, jogador4)

    nr_maos = 1_000_000
    nr_mesas = nr_maos // 4

    jogo = Jogo(nr_mesas, [jogador1, jogador3, jogador2, jogador4], time1, time2)

    df = pd.DataFrame(jogo.mesas_stats)
    print(f"Quantidade de mãos geradas: {len(df)}")

    df.to_pickle(r".\modules\db\dados.pickle")

    return len(df)
