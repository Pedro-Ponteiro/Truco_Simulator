from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple, Union

from modules.classes.baralho import Baralho, Carta


@dataclass
class Jogada:
    def __init__(self, jogador: Jogador, valor_carta: int) -> None:
        self.jogador = jogador
        self.valor_carta = valor_carta


class Jogador:
    def __init__(self, nome: str) -> None:
        self.mao: List[Carta] = []
        self.nome: str = nome
        self.parceiro: Jogador = None
        self.time: Time = None

    def _wrap_escolher_jogada(self, jogadas_rodada: List[Jogada], mesa: Mesa) -> Jogada:

        return self.escolher_jogada(jogadas_rodada, mesa)

    def escolher_jogada(self, jogadas_rodada: List[Jogada], mesa: Mesa) -> Jogada:
        ...

    def analisar_cartas_mao(self, mesa: Mesa) -> None:
        ...

    def __str__(self) -> str:

        return f"Jogador(mao={self.mao},nome={self.nome},parceiro={self.parceiro.nome}"

    def __repr__(self) -> str:

        return f"Jogador(mao={self.mao},nome={self.nome},parceiro={self.parceiro.nome}"


class Time:
    def __init__(self, nome, jogador1: Jogador, jogador2: Jogador) -> None:
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
        return f"Time(nome={self.nome},pode_trucar={self.pode_trucar},mao_de_onze={self.mao_de_onze},pts_jogo={self.pontos_jogo},pts_mesa={self.pontos_mesa})"

    def __repr__(self) -> str:
        return f"Time(nome={self.nome},pode_trucar={self.pode_trucar},mao_de_onze={self.mao_de_onze},pts_jogo={self.pontos_jogo},pts_mesa={self.pontos_mesa})"


class Rodada:
    def __init__(self, time1: Time, time2: Time) -> None:
        self.jogadas: List[Jogada] = []
        self.time1 = time1
        self.time2 = time2

    def get_vencedor(self, jogadores: List[Jogador], mesa: Mesa) -> List[Jogador]:
        max_scorer: List[Time] = []
        max_score = 0
        for jogador in jogadores:
            jogada = jogador._wrap_escolher_jogada(self.jogadas, mesa)

            self.jogadas.append(jogada)
            mesa.jogadas_mesa.append(jogada)

            score = jogada.valor_carta
            if score > max_score:
                max_scorer = [jogador]
                max_score = score
            elif score == max_score:
                if max_scorer[0] != jogador.parceiro.time:
                    max_scorer = max_scorer + [jogador]

        return max_scorer


class Mesa:
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

    def distribuir_cartas(self, jogadores: List[Jogador]):

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
                    carta = Carta(carta.type, self.baralho.valor_maximo + carta.type)
                jogador.mao.append(carta)

            cartas = sorted(jogador.mao, key=lambda c: c.num)

            registro_jogador = self.stats[jogador.nome]
            registro_jogador["high_carta"] = cartas[2].num
            registro_jogador["medium_carta"] = cartas[1].num
            registro_jogador["low_carta"] = cartas[0].num

            jogador.analisar_cartas_mao(self)

    def setup_jogador_time(self, time1: Time, time2: Time) -> None:
        time1.pontos_mesa = 0
        time2.pontos_mesa = 0

        [jogador.mao.clear() for jogador in self.jogadores]

    def register_scores(self, time_vencedor: Time | None) -> None:
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

        self.jogadores = jogadores
        self.next_jogadores = self.jogadores[1:] + [self.jogadores[0]]
        self.valor = valor

        self.distribuir_cartas(self.jogadores)
        vencedores: List[List[Jogador]] = []

        for _ in range(3):

            rodada_winner = Rodada(time1, time2).get_vencedor(self.jogadores, self)
            vencedores.append(rodada_winner)

            if len(rodada_winner) == 1:
                # TODO: player whon wins starts the next round
                ...

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
        self.register_scores(vencedor)
        self.setup_jogador_time(time1, time2)
        return vencedor, self.next_jogadores


class Jogo:
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

    def __str__(self) -> str:
        return (
            f"baralho={self.baralho}\n"
            + f"jogadores={self.jogadores}\ntime1={self.time1}\n"
            + f"time2={self.time2}\n"
        )

    def registrar_scores(self, mesa_stats: Dict[str, Dict[str, int]]) -> None:
        for jogador, stats in mesa_stats.items():
            for k, v in stats.items():
                self.mesas_stats[k].append(v)
