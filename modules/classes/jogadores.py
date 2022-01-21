from typing import List, Optional

from modules.classes.baralho import Carta
from modules.classes.classes_base import Jogada, Jogador, Mesa, Time


class Estrategia:
    """Strategy used by NormalPlayer"""

    def __init__(
        self,
        turno: int,
        maior_carta_rodada: Optional[Jogada],
        pontos_time_rival: int,
        jogador: "JogadorProbabilistico",
        jogadas_rodada: List[Jogada],
    ) -> None:
        self.turno = turno
        self.maior_carta_rodada = maior_carta_rodada
        self.pontos_time_rival = pontos_time_rival
        self.jogador = jogador
        self.jogadas_rodada = jogadas_rodada

        self.turno_estrategia = {
            1: self.primeiro_turno,
            2: self.segundo_terceiro_turno,
            3: self.segundo_terceiro_turno,
            4: self.quarto_turno,
        }

    def escolher_melhor_carta(self) -> Carta:
        """Uses turn strategy to choose best card.

        Returns:
            Carta: chosen card
        """
        if len(self.jogador.mao) == 1:
            return self.jogador.get_menor_carta_mao()

        return self.turno_estrategia[self.turno]()

    def primeiro_turno(self) -> Carta:
        """Strategy for the first turn

        Returns:
            Carta: chosen card
        """
        if self.pontos_time_rival > 0:
            # print("iniciando com a minha maior")
            return self.jogador.get_maior_carta_mao()
        else:
            # print("iniciando com a minha menor")
            return self.jogador.get_menor_carta_mao()

    def segundo_terceiro_turno(self) -> Carta:
        """Strategy for the second and third turn.

        Returns:
            Carta: chosen card
        """
        maior_carta_mao = self.jogador.get_maior_carta_mao()
        menor_carta_mao = self.jogador.get_menor_carta_mao()

        if self.pontos_time_rival == 1 and self.jogador.time.pontos_mesa == 1:
            return maior_carta_mao

        if self.is_empate():
            if self.pontos_time_rival > 0:
                # devo cobrir!
                # print("Cobrindo o empate")
                carta_jogada = maior_carta_mao
                if carta_jogada.num <= self.maior_carta_rodada.valor_carta:
                    carta_jogada = menor_carta_mao
            else:
                # print(jogadas_rodada)
                # print("Deixo o empate acontecer")
                carta_jogada = menor_carta_mao
        else:
            if self.maior_carta_rodada.jogador == self.jogador.parceiro:
                # descarte
                # print("Meu parceiro esta fazendo, então...")
                carta_jogada = menor_carta_mao
            else:
                if self.maior_carta_rodada.valor_carta <= maior_carta_mao.num:
                    # print("vou cobrir ou empatar essa carta com a minha maior")
                    carta_jogada = maior_carta_mao
                else:
                    # print("Descarto, pois não consigo cobrir")
                    carta_jogada = menor_carta_mao

        return carta_jogada

    def quarto_turno(self) -> Carta:
        """Strategy for the forth turn.

        Returns:
            Carta: chosen card
        """
        if self.is_empate():
            if self.pontos_time_rival > 0:
                return self.jogador.get_maior_carta_mao()
            else:
                return self.jogador.get_menor_carta_mao()

        menor_carta_mao = self.jogador.get_menor_carta_mao()

        if self.maior_carta_rodada.jogador == self.jogador.parceiro:
            # descarte
            return menor_carta_mao

        valor_a_ser_alcancado = self.maior_carta_rodada.valor_carta
        if self.pontos_time_rival == 1 and self.jogador.time.pontos_mesa != 1:
            # tenho que me esforçar pra jogar um pouco maior
            valor_a_ser_alcancado += 1

        return self.jogador.escolher_menor_possivel(valor_a_ser_alcancado)

    def is_empate(self) -> bool:
        """Check if it is currently a draw.

        Returns:
            bool: True if draw, False otherwise.
        """
        maior_carta_entre_jogadas = [
            j.jogador
            for j in self.jogadas_rodada
            if j.valor_carta == self.maior_carta_rodada.valor_carta
        ]
        if len(maior_carta_entre_jogadas) > 1:
            if self.jogador.parceiro in maior_carta_entre_jogadas:
                return True

        return False


class JogadorProbabilistico(Jogador):
    """Player responsible for choosing the card.

    Args:
        Jogador: Abstract super class. Has methods wrapping these ones.
    """

    # TODO: transfer generic methos to abstract class

    def get_maior_carta_mao(self) -> Carta:
        """Returns highest available card.

        Returns:
            Carta: highest card
        """
        return self.mao[-1]

    def get_menor_carta_mao(self) -> Carta:
        """Returns lowest card.

        Returns:
            Carta: lowest card
        """
        return self.mao[0]

    def remover_carta_mao(self, carta: Carta) -> None:
        """Remove the card from the player hand.

        Args:
            carta (Carta): card to be removed
        """
        self.mao.remove(carta)

    def escolher_menor_possivel(self, maior_carta_rodada: int) -> Carta:
        """Finds the next higher/equal card value from player hand.

        Args:
            maior_carta_rodada (int): games current highest card.

        Returns:
            Carta: best card possible.
        """
        cartas_maiores_ou_iguais: List[bool] = [
            c.num >= maior_carta_rodada for c in self.mao
        ]

        if any(cartas_maiores_ou_iguais):
            # pega a carta suficiente pra ganhar, não necessariamente a maior da mão
            return self.mao[cartas_maiores_ou_iguais.index(True)]
        else:
            # nenhuma carta maior ou igual, descarte
            return self.get_menor_carta_mao()

    def escolher_jogada(
        self, jogadas_rodada: List[Jogada], mesa: Mesa, time_inimigo: Time
    ) -> Jogada:
        """Chooses the card based on game status and strategy.

        Args:
            jogadas_rodada (List[Jogada]): player moves that have been made already.
            mesa (Mesa): three round data
            time_inimigo (Time): enemy team object

        Returns:
            Jogada: player move
        """
        turno: int = len(jogadas_rodada) + 1

        maior_carta_rodada = (
            max(jogadas_rodada, key=lambda x: x.valor_carta)
            if len(jogadas_rodada) > 0
            else None
        )

        carta_jogada = Estrategia(
            turno,
            maior_carta_rodada,
            time_inimigo.pontos_mesa,
            self,
            jogadas_rodada,
        ).escolher_melhor_carta()

        self.remover_carta_mao(carta_jogada)
        jogada = Jogada(self, carta_jogada.num)
        # print(f"{self.nome} -> {jogada.valor_carta} {[c.num for c in  self.mao]}")
        # print(jogada)
        return jogada
