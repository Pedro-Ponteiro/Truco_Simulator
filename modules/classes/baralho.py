from dataclasses import dataclass
from itertools import product
from random import shuffle
from typing import Dict, List, Tuple


@dataclass
class Carta:
    type: int
    num: int


class Baralho:
    def __init__(self) -> None:

        self.tipo_carta: Carta = Carta

        self.card_types, self.card_nums = self._get_card_infos()
        self.cartas: List[Carta] = [
            Carta(c_type, c_num)
            for c_type, c_num in product(self.card_types, self.card_nums)
        ]

        self.bkp_cartas: List[Carta] = self.cartas.copy()

        # dados estatisticos
        self.qtd_total_cartas: int = len(self.cartas)
        self.valor_maximo: int = max(self.cartas, key=lambda carta: carta.num).num
        self.card_amount: Dict[int, int] = self._get_card_amounts()

    def coletar_cartas(self):
        self.cartas = self.bkp_cartas.copy()

    def embaralhar_cartas(self):
        shuffle(self.cartas)

    def _get_card_infos(self) -> Tuple[List[int], List[int]]:
        card_types = {
            "ouros": 1,
            "espada": 2,
            "coracao": 3,
            "paus": 4,
        }
        card_nums = {
            "4": 1,
            "5": 2,
            "6": 3,
            "7": 4,
            "Q": 5,
            "J": 6,
            "K": 7,
            "A": 8,
            "2": 9,
            "3": 10,
        }

        return (list(card_types.values()), list(card_nums.values()))

    def _get_card_amounts(self) -> Dict[int, int]:

        fim_range = self.valor_maximo + 1

        c_am = {c: 4 for c in range(1, fim_range)}
        # inserindo manilhas
        c_am.update({c: 1 for c in range(fim_range, fim_range + 4)})

        return c_am

    def calc_qtd_cartas_abaixo(
        self, card_num: int, cards_conhecidas: List[int], num_manilha: int
    ) -> int:
        """calcula a quantidade de cartas que estão acima de card_num

        Args:
            card_num (int): Numero da carta já convertido
            cards_conhecidas (List[int]): lista de numero de cartas conhecidas e convertidas, como as outras cartas na mão do jogador,
            a vira , e as cartas do parceiro caso seja mao de onze
            num_manilha (int): numero da manilha, sem conversão (abaixo de self.valor_maximo)

        Returns:
            int: quantidade de cartas acima de card_num
        """

        # retirar de todas as cards as conhecidas
        c_amounts = self.card_amount.copy()
        c_amounts[num_manilha] = 0

        for c_conhecida in cards_conhecidas:
            c_amounts[c_conhecida] -= 1

        # somar as que estão abaixo ou igual
        qtd_abaixo = sum([qtd for num, qtd in c_amounts.items() if num <= card_num])

        return qtd_abaixo

    def __str__(self) -> str:
        return f"{self.bkp_cartas}"
