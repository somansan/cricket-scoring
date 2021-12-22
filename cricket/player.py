from .enums import PlayerType


class Player:
    def __init__(self, name, player_no):
        self.name = name
        self.player_no = player_no
        self.match_played = 0
        self.runs = 0
        self.wickets = 0
        self.player_type = PlayerType.BATSMAN

    def update_runs(self, runs=1):
        self.runs += runs

    def update_wickets(self, wickets=1):
        self.wickets += wickets

    def update_matches_played(self, matches=1):
        self.match_played += matches
