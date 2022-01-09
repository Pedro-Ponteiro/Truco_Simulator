from typing import List, Tuple

from modules.classes.baralho import Carta
from modules.classes.classes_base import Jogada, Jogador, Mesa


class JogadorProbabilistico(Jogador):
    def get_maior_carta_mao(self) -> Carta:
        return self.mao[-1]

    def get_menor_carta_mao(self) -> Carta:
        return self.mao[0]

    def remover_carta_mao(self, carta: Carta) -> None:
        self.mao.remove(carta)

    def definir_estrategia(
        self, turno: int, maior_carta_rodada: Jogada, pontos_time_rival: int
    ) -> Carta:

        v_maior_carta = maior_carta_rodada.valor_carta
        if turno == 4:
            # print("Escolhendo a menor possivel...")
            if pontos_time_rival > 1:
                # tenho que me esforçar pra jogar um pouco maior
                v_maior_carta += 1

            return self.escolher_menor_possivel(v_maior_carta)
        else:
            maior_carta_mao = self.get_maior_carta_mao()
            if maior_carta_rodada.valor_carta <= maior_carta_mao.num:
                # print("vou cobrir essa carta com a minha maior")
                return maior_carta_mao
            # print("Descarto, pois não consigo cobrir")
            return self.get_menor_carta_mao()

    def escolher_menor_possivel(self, maior_carta_rodada: int) -> Carta:
        cartas_maiores: List[bool] = []

        for c in self.mao:
            cartas_maiores.append(c.num >= maior_carta_rodada)

        if any(cartas_maiores):
            # pega a carta suficiente pra ganhar, não necessariamente a maior da mão
            return self.mao[cartas_maiores.index(True)]
        else:
            # nenhuma carta maior ou igual, descarte
            return self.get_menor_carta_mao()

    def escolher_jogada(self, jogadas_rodada: List[Jogada], mesa: Mesa) -> Jogada:

        # o robo sempre tenta vencer, a não ser que o parceiro esteja vencendo...

        turno: int = len(jogadas_rodada) + 1
        if turno == 1:
            if mesa.jogadores[mesa.jogadores.index(self) - 1].time.pontos_mesa > 0:
                # mas a minha maior no segundo
                # print("iniciando com a minha maior")
                carta_jogada = self.get_maior_carta_mao()
            else:
                # print("iniciando com a minha menor")
                # inicia com a menor carta no primeiro round
                carta_jogada = self.get_menor_carta_mao()

        else:
            # mudar para maiores_cart...?

            v_jogadas_rodada = [j.valor_carta for j in jogadas_rodada]
            v_maior_carta_rodada = max(v_jogadas_rodada)
            empate = False
            if v_jogadas_rodada.count(v_maior_carta_rodada) > 1:
                empate = True

            if empate:
                # TODO: se o meu time não fez a primeira rodada, tenho que cobrir!!
                if jogadas_rodada[-1].jogador.time.pontos_mesa > 0:
                    # devo cobrir!
                    # print("Cobrindo o empate")
                    carta_jogada = self.get_maior_carta_mao()
                else:
                    # print(jog;adas_rodada)
                    # print("Deixo o empate acontecer")
                    carta_jogada = self.get_menor_carta_mao()
            else:
                maior_carta_rodada = max(jogadas_rodada, key=lambda x: x.valor_carta)
                if maior_carta_rodada.jogador == self.parceiro:
                    # descarte
                    # print("Meu parceiro esta fazendo, então...")
                    carta_jogada = self.get_menor_carta_mao()
                else:
                    carta_jogada = self.definir_estrategia(
                        turno,
                        maior_carta_rodada,
                        jogadas_rodada[-1].jogador.time.pontos_mesa,
                    )

        self.remover_carta_mao(carta_jogada)
        jogada = Jogada(self, carta_jogada.num)
        # print(f"{self.nome} -> {jogada.valor_carta} {[c.num for c in  self.mao]}")
        # print(jogada)
        return jogada
