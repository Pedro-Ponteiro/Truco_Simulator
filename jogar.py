import pandas as pd

from classes_base import Jogo, Time
from jogadores import JogadorAleatorio, JogadorProbabilistico


def main():
    jogador1, jogador2 = JogadorProbabilistico("Pedro"), JogadorProbabilistico("Manu")
    jogador3, jogador4 = JogadorProbabilistico("Mari"), JogadorProbabilistico("Ariel")
    time1 = Time("PENU", jogador1, jogador2)
    time2 = Time("ARIMA", jogador3, jogador4)

    jogo = Jogo(12, 12, [jogador1, jogador3, jogador2, jogador4], time1, time2)

    jogos = []

    num_jogos = 10000
    for _ in range(num_jogos):
        vencedores = jogo.get_vencedor()
        jogos.append(vencedores.nome)
        vencedores = [jogador.nome for jogador in vencedores.jogadores]
        # print("\nEsses são os vencedores!")
        # print(vencedores)
        # print("--" * 50)
        # input()

    jogos = pd.Series(jogos)
    print(jogos.value_counts())

    df = pd.DataFrame(jogo.mesas_stats)
    df["cartas_medium_high"] = (
        df["high_carta"].astype(str).str.cat(df["medium_carta"].astype(str), sep=" + ")
    )
    df.to_excel("dados.xlsx", index=None)
    df.to_pickle("dados.pickle")

    # print("\nAo final da partida, temos:\n")
    # print(jogo)


if __name__ == "__main__":
    main()
