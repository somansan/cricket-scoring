from typing import List, Optional
from math import floor
from cricket.enums import Constants as consts


class PlayerManager:

    def __init__(self, player_id, name):
        self.player_id: int = player_id
        self.name: str = name
        self.score: int = 0
        self.wickets: int = 0
        self.balls_faced: int = 0

    def strike_rate(self):
        return self.score / self.balls_faced


class TeamManager:

    def __init__(self, team_id: str, name: str):
        self.team_id: str = team_id
        self.name: str = name
        self.score: int = 0
        self.overs: float = 0.0
        self.wickets_down: int = 0
        self.target_score: int = 0
        self.players = Optional[List[PlayerManager]]

    def curr_rr(self):
        over, balls = floor(self.overs), int((self.overs - int(self.overs)) * 10)
        return round(self.score / (over + balls / 6), 2)

    def req_rr(self):
        try:
            over, balls = floor(self.overs), int((self.overs - int(self.overs)) * 10)
            return round((self.target_score - self.score) / (consts.TOTAL_OVERS - (over + balls / 6)), 2)
        except ZeroDivisionError:
            return 0


class GameManager:

    def __init__(self, venue: str = 'Melbourne'):
        self.venue = venue
        self.inning = 1
        self.this_over = list()
        self.batting = Optional[TeamManager]
        self.fielding = Optional[TeamManager]
        self.toss = Optional[TeamManager]
        self.on_strike = Optional[PlayerManager]
        self.non_strike = Optional[PlayerManager]
        self.on_bowl = Optional[PlayerManager]

    def __str__(self):
        return f"""
    {self.batting.team_id}: {self.batting.score}/{self.batting.wickets_down}    OVERS: {self.batting.overs}     THIS OVER: {' '.join(self.this_over)}
    {self.on_strike.name.upper()}*  : {self.on_strike.score}                    
    {self.non_strike.name.upper()}  : {self.non_strike.score}
    CURR_RR : {self.batting.curr_rr()}                            
    REQ_RR  : {'-' if self.inning == 1 or not self.batting.req_rr() else self.batting.req_rr()}
    ==================================
"""
