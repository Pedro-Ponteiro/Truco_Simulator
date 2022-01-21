from dataclasses import dataclass
from itertools import product
from random import shuffle
from typing import List, Tuple


@dataclass
class Carta:
    """Card with type and value (num)"""

    type: int
    num: int


class Baralho:
    """Deck of cards."""

    def __init__(self) -> None:

        self.tipo_carta: Carta = Carta

        self.card_types, self.card_nums = self._get_card_infos()
        self.cartas: List[Carta] = [
            Carta(c_type, c_num)
            for c_type, c_num in product(self.card_types, self.card_nums)
        ]

        self.bkp_cartas: List[Carta] = self.cartas.copy()

        self.valor_maximo: int = max(self.cartas, key=lambda carta: carta.num).num

    def coletar_cartas(self):
        """Reset the deck."""
        self.cartas = self.bkp_cartas.copy()

    def embaralhar_cartas(self):
        """Shuffle the deck."""
        shuffle(self.cartas)

    def _get_card_infos(self) -> Tuple[List[int], List[int]]:
        """Define the cards available and their values.

        Returns:
            Tuple[List[int], List[int]]: list of card values and card types values
        """
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

    def __str__(self) -> str:
        return f"{self.bkp_cartas}"
