from .player import Player
from typing import List, Dict, Any


class TeamStats:
    match_played: int = 0
    match_won: int = 0
    match_lost: int = 0
    match_tied: int = 0

    @staticmethod
    def update_match_win(cls, match_won=1):
        cls.match_won += match_won
        cls.match_played += match_won

    @staticmethod
    def update_match_loss(cls, match_lost=1):
        cls.match_won += match_lost
        cls.match_played += match_lost

    @staticmethod
    def update_match_tie(cls, match_tied=1):
        cls.match_tied += match_tied
        cls.match_played += match_tied


class Team:
    def __init__(self, name, abbr):
        self.name = name
        self.abbr = abbr
        self.players: List[Player] = list()
        self.stats: TeamStats = TeamStats()

    def get_players(self):
        return self.players

    def get_stats(self):
        return self.stats

    def add_player(self, player):
        if self.find_player(player) < 0:
            raise Exception(f"Player {player} already exists!")
        self.players.append(player)

    def remove_player(self, player):
        idx = self.find_player(player)
        if idx < 0:
            return
        self.players.pop(idx)

    def find_player(self, player):
        for idx, player_ in self.players:
            if player == player_:
                return idx
        return -1
