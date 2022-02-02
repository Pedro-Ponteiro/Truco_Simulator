"""Player classes that uses strategy to choose best cards."""

from typing import List, Optional

from modules.classes.base_classes import Play, Player, Table, Team
from modules.classes.deck import Card


class Strategy:
    """Strategy used by NormalPlayer."""

    def __init__(
        self,
        turn: int,
        highest_round_card: Optional[Play],
        rival_team_points: int,
        player: "PlayerImplementation1",
        round_plays: List[Play],
    ) -> None:
        self.turn = turn
        self.highest_round_card = highest_round_card
        self.rival_team_points = rival_team_points
        self.player = player
        self.round_plays = round_plays

        self.strategy_turn = {
            1: self.first_turn,
            2: self.second_third_turn,
            3: self.second_third_turn,
            4: self.fourth_turn,
        }

    def choose_best_card(self) -> Card:
        """Uses turn strategy to choose best card.

        Returns:
            Card: chosen card
        """
        if len(self.player.hand) == 1:
            return self.player.get_lowest_hand_card()

        return self.strategy_turn[self.turn]()

    def first_turn(self) -> Card:
        """Strategy for the first turn.

        Returns:
            Carta: chosen card
        """
        if self.rival_team_points > 0:
            # print("starting with highest card")
            return self.player.get_highest_hand_card()
        else:
            # print("starting with lowest card")
            return self.player.get_lowest_hand_card()

    def second_third_turn(self) -> Card:
        """Strategy for the second and third turn.

        Returns:
            Card: chosen card
        """
        highest_hand_card = self.player.get_highest_hand_card()
        lowest_hand_card = self.player.get_lowest_hand_card()

        if self.rival_team_points == 1 and self.player.team.table_points == 1:
            return highest_hand_card

        if self.is_draw():
            if self.rival_team_points > 0:
                # devo cobrir!
                # print("Covering")
                plays_card = highest_hand_card
                if plays_card.value <= self.highest_round_card.card_value:
                    plays_card = lowest_hand_card
            else:
                # print(jogadas_rodada)
                # print("Let draw happen")
                plays_card = lowest_hand_card
        else:
            if self.highest_round_card.player == self.player.partner:
                # descarte
                # print("My partner is already winning, discarding")
                plays_card = lowest_hand_card
            else:
                if self.highest_round_card.card_value <= highest_hand_card.value:
                    # print("cover")
                    plays_card = highest_hand_card
                else:
                    # print("discarding")
                    plays_card = lowest_hand_card

        return plays_card

    def fourth_turn(self) -> Card:
        """Strategy for the forth turn.

        Returns:
            Card: chosen card
        """
        if self.is_draw():
            if self.rival_team_points > 0:
                return self.player.get_highest_hand_card()
            else:
                return self.player.get_lowest_hand_card()

        lowest_card_hand = self.player.get_lowest_hand_card()

        if self.highest_round_card.player == self.player.partner:
            # discarding
            return lowest_card_hand

        value_to_be_reached = self.highest_round_card.card_value
        if self.rival_team_points == 1 and self.player.team.table_points != 1:
            # tenho que me esforçar pra jogar um pouco maior
            value_to_be_reached += 1

        return self.player.choose_lowest_possible(value_to_be_reached)

    def is_draw(self) -> bool:
        """Check if it is currently a draw.

        Returns:
            bool: True if draw, False otherwise.
        """
        highest_cards_among_plays = [
            j.player
            for j in self.round_plays
            if j.card_value == self.highest_round_card.card_value
        ]
        if (
            len(highest_cards_among_plays) > 1
            and self.player.partner in highest_cards_among_plays
        ):
            return True

        return False


class PlayerImplementation1(Player):
    """Player responsible for choosing the card.

    Args:
        Player: Abstract super class. Has methods wrapping these ones.
    """

    # TODO: transfer generic methods to abstract class

    def get_highest_hand_card(self) -> Card:
        """Returns highest available card.

        Returns:
            Card: highest card
        """
        return self.hand[-1]

    def get_lowest_hand_card(self) -> Card:
        """Returns lowest card.

        Returns:
            Card: lowest card
        """
        return self.hand[0]

    def remove_card_from_hand(self, card: Card) -> None:
        """Remove the card from the player hand.

        Args:
            card (Card): card to be removed
        """
        self.hand.remove(card)

    def choose_lowest_possible(self, value_to_be_reached: int) -> Card:
        """Finds the next higher/equal card value from player hand.

        Args:
            value_to_be_reached (int): games current highest card.

        Returns:
            Carta: best card possible.
        """
        higher_or_equal_cards: List[bool] = [
            c.value >= value_to_be_reached for c in self.hand
        ]

        if any(higher_or_equal_cards):
            # get card high enough to win
            return self.hand[higher_or_equal_cards.index(True)]
        else:
            # discarding
            return self.get_lowest_hand_card()

    def choose_play(
        self, round_plays: List[Play], table: Table, enemy_team: Team
    ) -> Play:
        """Chooses the card based on game status and strategy.

        Args:
            round_plays (List[Play]): player moves that have been made already.
            table (Table): three round data
            enemy_team (Team): enemy team object

        Returns:
            Play: player move
        """
        turn: int = len(round_plays) + 1

        highest_round_card = (
            max(round_plays, key=lambda x: x.card_value)
            if len(round_plays) > 0
            else None
        )

        card_played = Strategy(
            turn,
            highest_round_card,
            enemy_team.table_points,
            self,
            round_plays,
        ).choose_best_card()

        self.remove_card_from_hand(card_played)
        play = Play(self, card_played.value)
        return play
