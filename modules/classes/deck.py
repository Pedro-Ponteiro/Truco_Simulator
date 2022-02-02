"""Classes related exclusively to the deck."""

from dataclasses import dataclass
from itertools import product
from random import shuffle
from typing import List, Tuple


@dataclass
class Card:
    """Card with type and value (num)."""

    suit: int
    value: int


class Deck:
    """Deck of cards."""

    def __init__(self) -> None:

        self.card_type: Card = Card

        self.card_suits, self.card_values = self._get_card_infos()
        self.cards: List[Card] = [
            Card(c_type, c_value)
            for c_type, c_value in product(self.card_suits, self.card_values)
        ]

        self.bkp_cards: List[Card] = self.cards.copy()

        self.max_value: int = max(self.cards, key=lambda card: card.value).value

    def collect_cards(self) -> None:
        """Reset the deck."""
        self.cards = self.bkp_cards.copy()

    def shuffle_cards(self) -> None:
        """Shuffle the deck."""
        shuffle(self.cards)

    def _get_card_infos(self) -> Tuple[List[int], List[int]]:
        """Define the cards available and their values.

        Returns:
            Tuple[List[int], List[int]]: list of card values and card types values
        """
        card_suits = {
            "diamonds": 1,
            "spades": 2,
            "hearts": 3,
            "clubs": 4,
        }
        card_values = {
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

        return (list(card_suits.values()), list(card_values.values()))

    def __str__(self) -> str:
        return f"{self.bkp_cards}"
