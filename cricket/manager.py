from typing import List
from math import floor
from constants import TOTAL_OVERS


class PlayerManager:
    id: int = 0
    name: str = ''
    score: int = 0
    wickets: int = 0
    balls_faced: int = 0

    def strike_rate(self):
        return self.score / self.balls_faced


class TeamManager:

    def __init__(self, team_id: str, name: str):
        self.team_id: str = ''
        self.name: str = ''
        self.score: int = ''
        self.overs: float = 0.0
        self.wickets_down: int = 0
        self.target_score: int = 0
        self.players: List[PlayerManager]

    def curr_rr(self):
        over, balls = floor(self.overs), int((self.overs - int(self.overs)) * 10)
        return round(self.score / (over + balls / 6), 2)

    def req_rr(self):
        over, balls = floor(self.overs), int((self.overs - int(self.overs)) * 10)
        return round((self.target_score - self.score) / (TOTAL_OVERS - (over + balls / 6)), 2)


class GameManager:

    def __init__(self, venue: str = 'Melbourne'):
        self.venue = venue
        self._batting = None
        self._fielding = None
        self._toss = None
        self.inning = 1
        self._on_strike = None
        self._non_strike = None
        self._on_bowl = None

    @property
    def toss(self):
        return self._toss

    @toss.setter
    def toss(self, value: TeamManager):
        self._toss = value

    @property
    def batting(self):
        return self._batting

    @batting.setter
    def batting(self, value: TeamManager):
        self._batting = value

    @property
    def fielding(self):
        return self._fielding

    @fielding.setter
    def fielding(self, value: TeamManager):
        self._fielding = value

    @property
    def on_strike(self):
        return self._on_strike

    @on_strike.setter
    def on_strike(self, value: PlayerManager):
        self._on_strike = value

    @property
    def non_strike(self):
        return self._non_strike

    @non_strike.setter
    def non_strike(self, value: PlayerManager):
        self._non_strike = value

    @property
    def on_bowl(self):
        return self._on_bowl

    @on_bowl.setter
    def on_bowl(self, value: PlayerManager):
        self._on_bowl = value
