from typing import List, Tuple

from modules.classes.baralho import Carta
from modules.classes.classes_base import Jogada, Jogador, Mesa


class JogadorProbabilistico(Jogador):
    def analisar_cartas_mao(self, mesa: Mesa) -> None:

        pontuacao = int
        self.mao_analisada: List[Tuple[mesa.baralho.tipo_carta, pontuacao]] = []

        cartas_conhecidas = [carta.num for carta in self.mao] + [mesa.vira]

        for carta in self.mao:

            qtd_abaixo = mesa.baralho.calc_qtd_cartas_abaixo(
                carta.num, cartas_conhecidas, mesa.manilha
            )
            self.mao_analisada.append((carta, qtd_abaixo))
        self.mao_analisada.sort(key=lambda t: t[1])
        self.mao_analisada = [tupl[0] for tupl in self.mao_analisada]

    def get_maior_carta_mao(self) -> Carta:
        return self.mao_analisada[-1]

    def get_menor_carta_mao(self) -> Carta:
        return self.mao_analisada[0]

    def remover_carta(self, carta: Carta) -> None:
        self.mao.remove(carta)
        self.mao_analisada.remove(carta)

    def escolher_jogada(self, jogadas_rodada: List[Jogada], mesa: Mesa) -> Jogada:

        # o robo sempre tenta vencer, a não ser que o parceiro esteja vencendo...

        if len(jogadas_rodada):
            maior_carta_rodada = max(
                jogadas_rodada, key=lambda jogada: jogada.valor_carta
            )
            if maior_carta_rodada.jogador == self.parceiro:
                # descarte
                carta_jogada = self.get_menor_carta_mao()
                # print(f"Descarte da carta {carta_jogada.num}")
            else:
                maior_carta_mao = self.get_maior_carta_mao()
                if maior_carta_mao.num >= maior_carta_rodada.valor_carta:
                    # Cobrir a maior carta
                    carta_jogada = maior_carta_mao
                    # print(f"Cobre com a carta {carta_jogada.num}")
                else:
                    # Descarte
                    carta_jogada = self.get_menor_carta_mao()
                    # print(f"Descarte da carta {carta_jogada.num}")

        else:
            # jogar a maior na primeira carta da rodada
            carta_jogada = self.get_maior_carta_mao()

        self.remover_carta(carta_jogada)
        jogada = Jogada(self, carta_jogada.num)
        return jogada
