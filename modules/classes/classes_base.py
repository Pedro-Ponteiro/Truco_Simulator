"""Base classes for the game."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple, Union

from modules.classes.baralho import Baralho, Carta


@dataclass
class Jogada:
    """Player move."""

    jogador: Jogador
    valor_carta: int


class Jogador:
    """Player abstract class."""

    def __init__(self, nome: str) -> None:
        self.mao: List[Carta] = []
        self.nome: str = nome
        self.parceiro: Jogador = None
        self.time: Time = None

    def _wrap_escolher_jogada(
        self, jogadas_rodada: List[Jogada], mesa: Mesa, time_inimigo: Time
    ) -> Jogada:
        """Wrapper that is used by Game object to interact with Player object

        Args:
            jogadas_rodada (List[Jogada]): list of player moves during the round
            mesa (Mesa): list of player moves during the 3 round game
            time_inimigo (Time): enemy team object

        Returns:
            Jogada: chosen card
        """

        return self.escolher_jogada(jogadas_rodada, mesa, time_inimigo)

    def escolher_jogada(self, jogadas_rodada: List[Jogada], mesa: Mesa) -> Jogada:
        """Abstract method for children to implement.

        Args:
            jogadas_rodada (List[Jogada]): list of player moves during the round
            mesa (Mesa): list of player moves during the 3 round game

        Returns:
            Jogada: chosen card
        """
        ...

    def __str__(self) -> str:

        return (
            f"Jogador(mao={[c.num for c in self.mao]},"
            + "nome={self.nome},"
            + "parceiro={self.parceiro.nome})"
        )

    def __repr__(self) -> str:

        return self.nome


class Time:
    """Team of three players."""

    def __init__(self, nome: str, jogador1: Jogador, jogador2: Jogador) -> None:
        self.nome: str = nome
        self.jogadores: List[Jogador] = (jogador1, jogador2)
        jogador1.parceiro = jogador2
        jogador2.parceiro = jogador1
        jogador1.time = self
        jogador2.time = self

        # Setados ao longo das rodadas, vide classe Rodada
        self.pontos_jogo: int = 0
        self.pontos_mesa: int = 0

    def __str__(self) -> str:
        return (
            f"Time(nome={self.nome},"
            + "pts_jogo={self.pontos_jogo},"
            + "pts_mesa={self.pontos_mesa})"
        )

    def __repr__(self) -> str:
        return (
            f"Time(nome={self.nome},"
            + "pts_jogo={self.pontos_jogo},"
            + "pts_mesa={self.pontos_mesa})"
        )


class Rodada:
    """Round of the game (each game is made of 3 of these)."""

    def __init__(self, time1: Time, time2: Time) -> None:
        self.jogadas: List[Jogada] = []
        self.time1 = time1
        self.time2 = time2

    def get_vencedor(self, jogadores: List[Jogador], mesa: Mesa) -> List[Jogador]:
        """Iterates through players and decides round winner.

        Args:
            jogadores (List[Jogador]): players list
            mesa (Mesa): game in which the round belongs

        Returns:
            List[Jogador]: list of winners (more than one if draw)
        """
        player_max_scorer: List[Jogador] = []
        player_max_score = 0
        for idx_jogador in range(0, len(jogadores)):

            jogador = jogadores[idx_jogador]
            time_inimigo = jogadores[idx_jogador - 1].time
            jogada = jogador._wrap_escolher_jogada(self.jogadas, mesa, time_inimigo)
            # print(jogada)
            self.jogadas.append(jogada)
            # print(self.jogadas)
            mesa.jogadas_mesa.append(jogada)

            score = jogada.valor_carta
            if score > player_max_score:
                player_max_scorer = [jogador]
                player_max_score = score
            elif score == player_max_score and player_max_scorer[0] != jogador.parceiro:
                player_max_scorer = player_max_scorer + [jogador]
        # print("-" * 10)
        return player_max_scorer


class Mesa:
    """Game made of three rounds."""

    def __init__(self, jogo: Jogo, valor: int = 1) -> None:

        # preparando o baralho...
        jogo.baralho.coletar_cartas()
        jogo.baralho.embaralhar_cartas()

        # herdando algumas definições do jogo...
        self.baralho: Baralho = jogo.baralho

        self.jogo = jogo

        # Setado em "distribuir_cartas"
        self.manilha: int = 0
        self.vira: int = 0

        # setado no método get_vencedor
        self.valor: int = valor

        # Adicionados ao longo das rodadas
        self.jogadas_mesa: List[Jogada] = []

        # linhas para a tabela mesas_stats da classe jogo
        # chave possui nome do jogador, valor é a linha
        self.stats: Dict[str, Dict[str, int]] = {
            jogador.nome: {
                "high_carta": 0,
                "medium_carta": 0,
                "low_carta": 0,
                "resultado": 0,
            }
            for jogador in jogo.jogadores
        }

    def distribuir_cartas(self, jogadores: List[Jogador]) -> None:
        """Distribute cards among players.

        Args:
            jogadores (List[Jogador]): players participating
        """
        self.vira = self.baralho.cartas.pop().num

        # manilha é a proxima!
        if self.vira == self.baralho.valor_maximo:
            self.manilha = 1
        else:
            self.manilha = self.vira + 1

        for jogador in jogadores:
            for _ in range(3):
                carta = self.baralho.cartas.pop()
                if carta.num == self.manilha:
                    carta = Carta(carta.suit, self.baralho.valor_maximo + carta.suit)
                jogador.mao.append(carta)
            cartas_ord = sorted(jogador.mao, key=lambda c: c.num)
            jogador.mao = cartas_ord
            registro_jogador = self.stats[jogador.nome]
            registro_jogador["high_carta"] = cartas_ord[2].num
            registro_jogador["medium_carta"] = cartas_ord[1].num
            registro_jogador["low_carta"] = cartas_ord[0].num

        # TODO: TESTES AQUI PRA BAIXO
        # cartas_time1 = sorted(jogadores[0].mao + jogadores[2].mao,
        # key=lambda x: x.num)
        # cartas_time2 = sorted(jogadores[1].mao + jogadores[3].mao,
        # key=lambda x: x.num)
        # pts_time1 = sum([c.num for c in cartas_time1[-2:]])
        # pts_time2 = sum([c.num for c in cartas_time2[-2:]])

        # if pts_time1 == pts_time2:
        #     pts_time1 = sum([c.num for c in cartas_time1[-3:]])
        #     pts_time2 = sum([c.num for c in cartas_time2[-3:]])

        # print("-------------------")
        # if pts_time1 > pts_time2:
        #     print(f"{jogadores[0].time} deveria vencer com {pts_time1}")
        #     self.deveria_vencer: Time = jogadores[0].time
        # elif pts_time2 > pts_time1:
        #     print(f"{jogadores[1].time} deveria vencer com {pts_time2}")
        #     self.deveria_vencer: Time = jogadores[1].time
        # else:
        #     print("Ninguem deveria vencer!")
        #     self.deveria_vencer: Time = None
        # print("------------------")

    def setup_jogador_time(self, time1: Time, time2: Time) -> None:
        """Resets the players hands and team points.

        Args:
            time1 (Time): team 1
            time2 (Time): team 2
        """
        time1.pontos_mesa = 0
        time2.pontos_mesa = 0

        [jogador.mao.clear() for jogador in self.jogadores]

    def register_scores(self, time_vencedor: Time | None) -> None:
        """Updates the "results" column for each player.

        Args:
            time_vencedor (Time): winner team
        """
        # caso empate
        if time_vencedor is None:
            for j in self.jogo.jogadores:
                self.stats[j.nome]["resultado"] = 0.5
            return

        for jogador in time_vencedor.jogadores:
            self.stats[jogador.nome]["resultado"] = 1

    def get_vencedor(
        self,
        jogadores: List[Jogador],
        time1: Time,
        time2: Time,
        valor: int = 1,
    ) -> Tuple[Union[Time, None], List[Jogador]]:
        """Simulate 3 rounds and determines the winners.

        Args:
            jogadores (List[Jogador]): list of players
            time1 (Time): team 1
            time2 (Time): team 2
            valor (int, optional): The points that the winners get. Defaults to 1.

        Returns:
            Tuple[Union[Time, None], List[Jogador]]: winner(s) (None if draw)
        """
        # TODO: test the unlikely cases

        self.jogadores = jogadores
        self.next_jogadores = self.jogadores[1:] + [self.jogadores[0]]
        self.valor = valor

        self.distribuir_cartas(self.jogadores)
        vencedores: List[List[Jogador]] = []

        for _ in range(3):

            rodada_winner = Rodada(time1, time2).get_vencedor(self.jogadores, self)
            vencedores.append(rodada_winner)

            if len(rodada_winner) == 1:
                idx = jogadores.index(rodada_winner[0])
                self.jogadores = jogadores[idx:] + jogadores[:idx]

            for jogador in rodada_winner:
                jogador.time.pontos_mesa += 1

            if time1.pontos_mesa > 1 or time2.pontos_mesa > 1:

                if time1.pontos_mesa > time2.pontos_mesa:
                    vencedor = time1
                elif time2.pontos_mesa > time1.pontos_mesa:
                    vencedor = time2
                else:
                    # Caso vitoria - derrota - empate, vencedor é o que ganhou primeiro
                    if len(vencedores[0]) == 1:
                        vencedor = vencedores[0][0].time
                    else:
                        # caso empate-empate, mais uma rodada deve ser jogada
                        if len(vencedores) == 2:
                            continue
                        # caso empate-empate-empate
                        vencedor = None

                break

        # TODO: TESTE
        # print("-" * 10)
        # print("-" * 10)
        # print(f"{vencedor} é o vencedor!")
        # if (not self.deveria_vencer is None) and (vencedor != self.deveria_vencer):
        #     input("Ele não deveria vencer! Oh no....")

        # print("-" * 10)
        # print("-" * 10)

        self.register_scores(vencedor)
        self.setup_jogador_time(time1, time2)
        return vencedor, self.next_jogadores


class Jogo:
    """Registers scores and simulates Games."""

    def __init__(
        self,
        nr_mesas: int,
        jogadores: List[Jogador],
        time1: Time,
        time2: Time,
    ) -> None:

        self.baralho: Baralho = Baralho()

        self.nr_mesas = nr_mesas

        self.jogadores = jogadores
        self.time1 = time1
        self.time2 = time2

        self.valor_mesa: int = 1

        # queremos uma tabela com as colunas:
        # high_carta: [int] maior carta
        # medium_carta: [int] carta do meio
        # low_carta: [int] menor carta
        # vitoria: [int] 1 para venceu, 0 para perdeu e 0.5 para empate
        self.mesas_stats: Dict[str, List[int]] = {
            "high_carta": [],
            "medium_carta": [],
            "low_carta": [],
            "resultado": [],
        }

        for _ in range(self.nr_mesas):
            n_mesa = Mesa(self, self.valor_mesa)

            _, self.jogadores = n_mesa.get_vencedor(
                self.jogadores, self.time1, self.time2
            )

            self.registrar_scores(n_mesa.stats)

    def registrar_scores(self, mesa_stats: Dict[str, Dict[str, int]]) -> None:
        """Register scores coming from Game class.

        Args:
            mesa_stats (Dict[str, Dict[str, int]]): Game (three rounds) scores.
        """
        for _, stats in mesa_stats.items():
            for k, v in stats.items():
                self.mesas_stats[k].append(v)

    def __str__(self) -> str:
        return (
            f"baralho={self.baralho}\n"
            + f"jogadores={self.jogadores}\ntime1={self.time1}\n"
            + f"time2={self.time2}\n"
        )
