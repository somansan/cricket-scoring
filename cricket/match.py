from .team import Team
from .player import Player
from typing import List, Tuple, Any, Dict


class MatchStats:
    def __init__(self):
        self.score: int = 0
        self.wickets: int = 0
        self.overs: int = 0
        self.curr_rr: float = 0.0
        self.req_rr: float = 0.0
        self.innings: int = 1
        self.on_strike: Player = None
        self.curr_batting: Team = None

    def __call__(self):
        return self.__dict__


class Match:
    def __init__(self, match_no, teams, venue, match_type='', toss=None):
        self.match_no: int = match_no
        self.match_type: str = match_type
        self.teams: Tuple[Team, Team] = teams
        self.toss: Team = toss
        self.venue: str = venue
        self.stats: MatchStats = MatchStats()
        self.result: str = ''

    def get_match_stats(self):
        return self.stats()

    def update_score(self, score):
        self.stats.score += score

    def update_wickets(self, wickets):
        if wickets:
            self.stats.wickets += wickets
        else:
            self.stats.wickets += 1

    def set_match_type(self, match_type):
        self.match_type = match_type

    def set_teams(self, team_a, team_b):
        self.teams = (team_a, team_b)

    def set_venue(self, venue):
        self.venue = venue

    def set_toss(self, toss: Team):
        self.toss = toss
