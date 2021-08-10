from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple, Union

from baralho import Baralho, Carta


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

    def _trucar(
        self,
        jogador_adversario: Jogador,
        valor_proposto: int,
        mesa: Mesa,
        jogadas_rodada: List[Jogada],
    ) -> None:
        resposta = jogador_adversario.decidir_truco(
            self, valor_proposto, mesa, jogadas_rodada
        )

        if resposta is False:
            mesa.vencedor_por_desistencia = self.time

    def _wrap_escolher_jogada(self, jogadas_rodada: List[Jogada], mesa: Mesa) -> Jogada:

        if mesa.blind_pick is True:
            carta_escolhida = self.mao.pop()
            # print(
            #     f"Jogador {self.nome} escolhe aleatoriamente a carta {carta_escolhida.num}"
            # )
            return Jogada(self, carta_escolhida.num)

        return self.escolher_jogada(jogadas_rodada, mesa)

    def escolher_jogada(self, jogadas_rodada: List[Jogada], mesa: Mesa) -> Jogada:
        ...

    def decidir_truco(
        self,
        jogador_solicitante: Jogador,
        valor_proposto: int,
        mesa: Mesa,
        jogadas_rodada: List[Jogada],
    ) -> bool:
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

        # Setado em trucos, vide classe Jogador
        self.pode_trucar: bool = True

        # Setados ao longo das rodadas, vide classe Rodada
        self.pontos_jogo: int = 0
        self.pontos_mesa: int = 0

        # Setado quando o time atinge 11 pontos sozinho, vide classe Jogo
        self.mao_de_onze: bool = False

    def __str__(self) -> str:
        return f"Time(nome={self.nome},pode_trucar={self.pode_trucar},mao_de_onze={self.mao_de_onze},pts_jogo={self.pontos_jogo},pts_mesa={self.pontos_mesa})"

    def __repr__(self) -> str:
        return f"Time(nome={self.nome},pode_trucar={self.pode_trucar},mao_de_onze={self.mao_de_onze},pts_jogo={self.pontos_jogo},pts_mesa={self.pontos_mesa})"


class Rodada:
    def __init__(self, time1: Time, time2: Time) -> None:
        self.jogadas: List[Jogada] = []
        self.time1 = time1
        self.time2 = time2

    def get_vencedor(self, jogadores: List[Jogador], mesa: Mesa) -> List[Time]:
        max_scorer: List[Time] = []
        max_score = 0
        for jogador in jogadores:
            jogada = jogador._wrap_escolher_jogada(self.jogadas, mesa)

            if mesa.vencedor_por_desistencia is not None:
                return None

            self.jogadas.append(jogada)
            mesa.jogadas_mesa.append(jogada)

            score = jogada.valor_carta
            if score > max_score:
                max_scorer = [jogador.time]
                max_score = score
            elif score == max_score:
                if max_scorer[0] != jogador.parceiro.time:
                    max_scorer = [self.time1, self.time2]

        # vencs = [str(time) for time in max_scorer]
        # if len(vencs) > 1:
        #     # print(
        #     #     "OCORREU UM EMPATE!!!!!!!!! ---------------------------------!!!!!!!!!"
        #     # )
        #     ...
        # else:
        #     print(f"O vencedor da rodada foi {vencs}!")
        return max_scorer


class Mesa:
    def __init__(self, jogo: Jogo, valor: int = 1) -> None:

        # preparando o baralho...
        jogo.baralho.coletar_cartas()
        jogo.baralho.embaralhar_cartas()

        # herdando algumas definições do jogo...
        self.baralho: Baralho = jogo.baralho
        self.truco_maximo = jogo.truco_maximo
        self.blind_pick = jogo.blind_pick
        self.jogo = jogo

        # Setado em "distribuir_cartas"
        self.manilha: int = 0
        self.vira: int = 0

        # setado no método get_vencedor
        self.valor: int = valor

        # Adicionados ao longo das rodadas
        self.jogadas_mesa: List[Jogada] = []

        # setado durante trucos, vide classe Jogador
        self.vencedor_por_desistencia: Time = None

        # linhas para a tabela mesas_stats da classe jogo
        # chave possui nome do jogador, valor é a linha
        self.stats: Dict[str, Dict[str, int]] = {
            jogador.nome: {
                "high_carta": 0,
                "medium_carta": 0,
                "low_carta": 0,
                "resultado": -1,
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
                    # print(
                    #     f"O jogador {jogador.nome} recebeu uma carta com valor {carta.num}!"
                    # )

                jogador.mao.append(carta)

            cartas = sorted(jogador.mao, key=lambda c: c.num)

            registro_jogador = self.stats[jogador.nome]
            registro_jogador["high_carta"] = cartas[2].num
            registro_jogador["medium_carta"] = cartas[1].num
            registro_jogador["low_carta"] = cartas[0].num

            jogador.analisar_cartas_mao(self)

    def setup_jogador_time(self, time1: Time, time2: Time) -> None:
        time1.pontos_mesa = 0
        time1.pode_trucar = True

        time2.pontos_mesa = 0
        time2.pode_trucar = True

        [jogador.mao.clear() for jogador in self.jogadores]

    def register_scores(self, time_vencedor: Time | None) -> None:
        if time_vencedor is None:
            for j in self.jogo.jogadores:
                self.stats[j.nome]["resultado"] = 0
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
        self.valor = valor

        self.distribuir_cartas(self.jogadores)
        vencedores: List[List[Time]] = []

        for _ in range(3):

            rodada_winner = Rodada(time1, time2).get_vencedor(self.jogadores, self)
            vencedores.append(rodada_winner)
            self.jogadores = self.jogadores[1:] + [self.jogadores[0]]

            # TODO: mEeLhorar ISSO PQ TEM ESSE MESMO IF EM TRES LUGARES DIFERENTES
            if self.vencedor_por_desistencia is not None:
                vencedor = self.vencedor_por_desistencia

                break

            for time in rodada_winner:
                time.pontos_mesa += 1

            if time1.pontos_mesa > 1 or time2.pontos_mesa > 1:

                if time1.pontos_mesa > time2.pontos_mesa:
                    vencedor = time1
                elif time2.pontos_mesa > time1.pontos_mesa:
                    vencedor = time2
                else:
                    # Caso vitoria - derrota - empate, vencedor é o que ganhou primeiro
                    if len(vencedores[0]) == 1:
                        vencedor = vencedores[0][0]
                    else:
                        # caso empate-empate, mais uma rodada deve ser jogada
                        if len(vencedores) == 2:
                            continue
                        # caso empate-empate-empate
                        vencedor = None
                        # print(vencedores)
                break
        self.register_scores(vencedor)
        self.setup_jogador_time(time1, time2)
        return vencedor, self.jogadores


class Jogo:
    def __init__(
        self,
        max_points: int,
        truco_maximo: int,
        jogadores: List[Jogador],
        time1: Time,
        time2: Time,
    ) -> None:

        self.baralho: Baralho = Baralho()

        self.max_points = max_points
        self.pts_mesa_especial = max_points - 1
        self.truco_maximo = truco_maximo
        self.jogadores = jogadores
        self.time1 = time1
        self.time2 = time2
        self.blind_pick: bool = False
        self.valor_mesa: int = 1

        # queremos uma tabela com as colunas:
        # high_carta: [int] maior carta
        # medium_carta: [int] carta do meio
        # low_carta: [int] menor carta
        # vitoria: [int] 1 para venceu, -1 para perdeu e 0 para empate

        self.mesas_stats: Dict[str, List[int]] = {
            "high_carta": [],
            "medium_carta": [],
            "low_carta": [],
            "resultado": [],
        }

    def __str__(self) -> str:
        return (
            f"baralho={self.baralho}\npts_mesa_especial={self.pts_mesa_especial}\n"
            + f"truco_maximo={self.truco_maximo}\njogadores={self.jogadores}\ntime1={self.time1}\n"
            + f"time2={self.time2}\nblind_pick={self.blind_pick}\nvalor_mesa={self.valor_mesa}"
        )

    def registrar_scores(self, mesa_stats: Dict[str, Dict[str, int]]) -> None:
        for jogador, stats in mesa_stats.items():
            for k, v in stats.items():
                self.mesas_stats[k].append(v)

    def get_vencedor(self) -> Time:

        # TODO: QUANDO MAO DE ONZE, O JOGADOR PODE DECIDIR SE VAI JOGAR OU NÃO (N JOGANDO, ADVERSARIO GANHA 1)
        # O JOGO AUTOMATICAMENTE PASSA A VALER 3 NESSA SITUAÇÃO

        while True:
            n_mesa = Mesa(self, self.valor_mesa)

            time_vencedor, jogadores = n_mesa.get_vencedor(
                self.jogadores, self.time1, self.time2
            )
            self.jogadores = jogadores

            self.registrar_scores(n_mesa.stats)

            if time_vencedor is None:
                # empate!
                continue
            # else:
            # print(
            #     f"\nO vencedor da mesa foi {time_vencedor}!\nEle ganha {n_mesa.valor} pontos e possui {time_vencedor.pontos_jogo + n_mesa.valor} pontos agora!\n"
            # )
            time_vencedor.pontos_jogo += n_mesa.valor

            if time_vencedor.pontos_jogo >= self.max_points:
                self.time1.pontos_jogo = 0
                self.time2.pontos_jogo = 0
                self.blind_pick = False
                self.time1.mao_de_onze = False
                self.time2.mao_de_onze = False
                return time_vencedor

            if (
                self.time1.pontos_jogo == self.pts_mesa_especial
                and self.time2.pontos_jogo == self.pts_mesa_especial
            ):
                self.blind_pick = True
            elif self.time1.pontos_jogo == self.pts_mesa_especial:
                self.time1.mao_de_onze = True
            elif self.time2.pontos_jogo == self.pts_mesa_especial:
                self.time2.mao_de_onze = True
