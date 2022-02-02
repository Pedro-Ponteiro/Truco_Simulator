"""Base classes for the game."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple, Union

from modules.classes.deck import Card, Deck


@dataclass
class Play:
    """Player move."""

    player: Player
    card_value: int


class Player:
    """Player abstract class."""

    def __init__(self, nome: str) -> None:
        self.hand: List[Card] = []
        self.name: str = nome
        self.partner: Player = None
        self.team: Team = None

    def _wrap_choose_play(
        self, round_plays: List[Play], table: Table, enemy_team: Team
    ) -> Play:
        """Wrapper that is used by Game object to interact with Player object.

        Args:
            round_plays (List[Play]): list of player moves during the round
            table (Table): list of player moves during the 3 round game
            enemy_team (Team): enemy team object

        Returns:
            Play: chosen card
        """
        return self.choose_play(round_plays, table, enemy_team)

    def choose_play(self, round_plays: List[Play], table: Table) -> Play:
        """Abstract method for children to implement.

        Args:
            round_plays (List[Play]): list of player moves during the round
            table (Table): list of player moves during the 3 round game

        Returns:
            Play: chosen card
        """
        ...

    def __str__(self) -> str:

        return (
            f"Player(hand={[c.value for c in self.hand]},"
            + f"name={self.name},"
            + f"partner={self.partner.name})"
        )

    def __repr__(self) -> str:

        return self.name


class Team:
    """Team of three players."""

    def __init__(self, name: str, player1: Player, player2: Player) -> None:
        self.name: str = name
        self.players: List[Player] = (player1, player2)
        player1.partner = player2
        player2.partner = player1
        player1.team = self
        player2.team = self

        # Manipulated during rounds, tables and games
        self.game_points: int = 0
        self.table_points: int = 0

    def __str__(self) -> str:
        return (
            f"Team(name={self.name},"
            + f"game_pts={self.game_points},"
            + f"table_pts={self.table_points})"
        )

    def __repr__(self) -> str:
        return (
            f"Team(name={self.name},"
            + f"game_pts={self.game_points},"
            + f"table_pts={self.table_points})"
        )


class Round:
    """Round of the game (each game is made of 3 of these)."""

    def __init__(self, team1: Team, team2: Team) -> None:
        self.plays: List[Play] = []
        self.team1 = team1
        self.team2 = team2

    def get_winner(self, players: List[Player], table: Table) -> List[Player]:
        """Iterates through players and decides round winner.

        Args:
            players (List[Player]): players list
            table (Table): game in which the round belongs

        Returns:
            List[Player]: list of winners (more than one if draw)
        """
        player_max_scorer: List[Player] = []
        player_max_score = 0
        for idx_player in range(0, len(players)):

            player = players[idx_player]
            enemy_team = players[idx_player - 1].team
            play = player._wrap_choose_play(self.plays, table, enemy_team)
            self.plays.append(play)
            table.table_plays.append(play)

            score = play.card_value
            if score > player_max_score:
                player_max_scorer = [player]
                player_max_score = score
            elif score == player_max_score and player_max_scorer[0] != player.partner:
                player_max_scorer = player_max_scorer + [player]
        # print("-" * 10)
        return player_max_scorer


class Table:
    """Game made of three rounds."""

    def __init__(self, game: Game, table_value: int = 1) -> None:

        # preparing the deck
        game.deck.collect_cards()
        game.deck.shuffle_cards()

        # extending some game definitions...
        self.deck: Deck = game.deck

        self.game = game

        # determined at "distribute_cards"
        self.manilha: int = 0
        self.vira: int = 0

        # determined at get_winner func
        self.table_value: int = table_value

        # Added along rounds
        self.table_plays: List[Play] = []

        # rows for the attribute table_stats in Game class
        # key is player name, value is his stats
        self.stats: Dict[str, Dict[str, int]] = {
            player.name: {
                "highest_card": 0,
                "middle_card": 0,
                "lowest_card": 0,
                "result": 0,
            }
            for player in game.players
        }

    def distribute_cards(self, players: List[Player]) -> None:
        """Distribute cards among players.

        Args:
            players (List[Player]): players participating
        """
        self.vira = self.deck.cards.pop().value

        # manilha is the next
        if self.vira == self.deck.max_value:
            self.manilha = 1
        else:
            self.manilha = self.vira + 1

        for p in players:
            self.setup_player(p)

    def setup_player(self, player: Player) -> None:
        for _ in range(3):
            card = self.deck.cards.pop()
            if card.value == self.manilha:
                card = Card(card.suit, self.deck.max_value + card.suit)
            player.hand.append(card)
        ordered_cards = sorted(player.hand, key=lambda c: c.value)
        player.hand = ordered_cards

        self.register_player_initial_data(ordered_cards, player.name)

    def register_player_initial_data(
        self, ordered_cards: List[Card], player_name: str
    ) -> None:
        """Register initial data about the players hand.

        Args:
            ordered_cards (List[Card]): list of cards ordered
            player_name (str): player's name
        """
        pĺayer_registry = self.stats[player_name]
        pĺayer_registry["highest_card"] = ordered_cards[2].value
        pĺayer_registry["middle_card"] = ordered_cards[1].value
        pĺayer_registry["lowest_card"] = ordered_cards[0].value

    def setup_player_and_team(self, team1: Team, team2: Team) -> None:
        """Resets the players hands and team points.

        Args:
            team1 (team): team 1
            team2 (team): team 2
        """
        team1.table_points = 0
        team2.table_points = 0

        [player.hand.clear() for player in self.players]

    def register_scores(self, winner_team: Team | None) -> None:
        """Updates the "results" column for each player.

        Args:
            winner_team (Team): winner team
        """
        # Draw case
        if winner_team is None:
            for j in self.game.players:
                self.stats[j.name]["result"] = 0.5
            return

        for player in winner_team.players:
            self.stats[player.name]["result"] = 1

    def reorder_players_after_round(self, round_winners: List[Player]) -> None:
        """Reorder the players according to who won the last round

        Args:
            round_winners (List[Player]): list of players ho won the round
            (more than 1 if draw)
        """
        if len(round_winners) == 1:
            idx = self.players.index(round_winners[0])
            self.players = self.players[idx:] + self.players[:idx]

    def get_winner(
        self,
        players: List[Player],
        team1: Team,
        team2: Team,
        table_value: int = 1,
    ) -> Tuple[Union[Team, None], List[Player]]:
        """Simulate 3 rounds and determines the winners.

        Args:
            players (List[Player]): list of players
            team1 (Team): team 1
            team2 (Team): team 2
            table_value (int, optional): The points that the winners get. Defaults to 1.

        Returns:
            Tuple[Union[Team, None], List[Player]]: winner(s) (None if draw)
        """
        # TODO: test the unlikely cases

        self.players = players
        self.table_value = table_value

        self.distribute_cards(self.players)
        self.next_players = self.players[1:] + [self.players[0]]
        winners: List[List[Player]] = []

        for _ in range(3):

            round_winner = Round(team1, team2).get_winner(self.players, self)
            winners.append(round_winner)

            self.reorder_players_after_round(round_winner)

            for player in round_winner:
                player.team.table_points += 1

            if team1.table_points > 1 or team2.table_points > 1:

                if team1.table_points > team2.table_points:
                    winner = team1
                elif team2.table_points > team1.table_points:
                    winner = team2
                else:
                    # Case win - loss - draw, winner is who won the first round
                    if len(winners[0]) == 1:
                        winner = winners[0][0].team
                    else:
                        # Case draw-draw, one more round should be played
                        if len(winners) == 2:
                            continue
                        # Case draw-draw-draw (no winner lol)
                        winner = None

                break

        self.register_scores(winner)
        self.setup_player_and_team(team1, team2)
        return winner, self.next_players


class Game:
    """Registers scores and simulates Games."""

    def __init__(
        self,
        table_quantity: int,
        players: List[Player],
        team1: Team,
        team2: Team,
    ) -> None:

        self.deck: Deck = Deck()

        self.table_quantity = table_quantity

        self.players = players
        self.team1 = team1
        self.team2 = team2

        self.table_value: int = 1

        # highest_card: [int]
        # middle_card: [int]
        # lowest_card: [int]
        # vitoria: [int] 1 for win, 0 for loss and 0.5 for draw
        self.table_stats: Dict[str, List[int]] = {
            "highest_card": [],
            "middle_card": [],
            "lowest_card": [],
            "result": [],
        }

        for _ in range(self.table_quantity):
            table = Table(self, self.table_value)

            _, self.players = table.get_winner(self.players, self.team1, self.team2)

            self.regsiter_scores(table.stats)

    def regsiter_scores(self, table_stats: Dict[str, Dict[str, int]]) -> None:
        """Register scores coming from Game class.

        Args:
            table_stats (Dict[str, Dict[str, int]]): Game (three rounds) scores.
        """
        for _, stats in table_stats.items():
            for k, v in stats.items():
                self.table_stats[k].append(v)

    def __str__(self) -> str:
        return (
            f"deck={self.deck}\n"
            + f"players={self.players}\nteam1={self.team1}\n"
            + f"team2={self.team2}\n"
        )
