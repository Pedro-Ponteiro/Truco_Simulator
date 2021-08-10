from random import randint
from typing import List, Tuple

from baralho import Carta
from classes_base import Jogada, Jogador, Mesa


class JogadorProbabilistico(Jogador):
    def analisar_cartas_mao(self, mesa: Mesa) -> None:

        pontuacao = int
        self.mao_analisada: List[Tuple[mesa.baralho.tipo_carta, pontuacao]] = []

        cartas_conhecidas = [carta.num for carta in self.mao] + [mesa.vira]
        if self.time.mao_de_onze:
            cartas_conhecidas += [carta.num for carta in self.parceiro.mao]

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

        # print(f"Jogador {self.nome} cartas: {[carta.num for carta in self.mao]}")

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
            # print(f"Inicia com a carta {carta_jogada.num}")

        # DECIDIR SE INICIA UM TRUCO!
        if self.time.pode_trucar and mesa.valor < mesa.truco_maximo:
            if False:
                index_jogador_anterior = mesa.jogadores.index(self) - 1
                jogador_adversario_anterior = mesa.jogadores[index_jogador_anterior]
                if mesa.valor == 1:
                    print(
                        f"Jogador {self.nome} pede Truco ao jogador {jogador_adversario_anterior.nome}!!!"
                    )

                    valor_proposto = mesa.valor + 2
                else:
                    valor_proposto = mesa.valor + 3
                    print(
                        f"Jogador {self.nome} pede {valor_proposto} ao {jogador_adversario_anterior.nome}!!!"
                    )

                resposta = self._trucar(
                    jogador_adversario_anterior, valor_proposto, mesa, jogadas_rodada
                )
                if mesa.vencedor_por_desistencia is not None:
                    return None
                self.time.pode_trucar = False

        # calcular a probabilidade da carta escolhida
        # print(f"\nANALISE DA CARTA: \nVALOR: {carta_jogada.num}\nVIRA: {mesa.vira}\n")
        self.remover_carta(carta_jogada)
        jogada = Jogada(self, carta_jogada.num)
        return jogada

    def decidir_truco(
        self,
        jogador_solicitante: Jogador,
        valor_proposto: int,
        mesa: Mesa,
        jogadas_rodada: List[Jogada],
    ) -> bool:

        # TODO: CALCULAR SE VAI TRUCAR OU NÃO
        # exemplo com 40% de chance de acertar e 10% de chance de pedir mais

        aceitar = randint(1, 10) > 9

        if not aceitar:
            print(f"Proposta recusada por {self.nome}")
            return False

        mesa.valor = valor_proposto

        aumentar = randint(1, 10) > 7

        if aumentar and (mesa.valor < mesa.truco_maximo):
            # pedir pra aumentar

            print(f"Aposta aumentada para {valor_proposto + 3} por {self.nome}!")
            self._trucar(jogador_solicitante, valor_proposto + 3, mesa, jogadas_rodada)
        else:
            print(f"Proposta aceita por {self.nome}!")

        return True


class JogadorAleatorio(Jogador):
    def escolher_jogada(self, jogadas_rodada: List[Jogada], mesa: Mesa) -> Jogada:

        print(f"Jogador {self.nome} cartas: {[c.num for c in self.mao]}")
        carta_num = self.mao.pop().num
        print(f"Escolhe a carta {carta_num}")
        return Jogada(self, carta_num)
