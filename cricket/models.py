from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from database import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    match_played = Column(Integer)
    runs = Column(Integer)
    wickets = Column(Integer)
    player_type = Column(String)
    team = Column(String, ForeignKey("teams.id"))


class Team(Base):
    __tablename__ = "teams"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    match_won = Column(Integer)
    match_lost = Column(Integer)
    match_tied = Column(Integer)

    def __str__(self):
        return f"""
        Team        : {self.name}
        Code        : {self.id}
        Match won   : {self.match_won}
        Match lost  : {self.match_lost}
        Match tied  : {self.match_tied}
        """


class Match(Base):
    __tablename__ = "match"

    match_id = Column(Integer, primary_key=True, index=True)
    home_team = Column(String, ForeignKey("teams.id"))
    away_team = Column(String, ForeignKey("teams.id"))
    venue = Column(String)
    toss = Column(String, ForeignKey("teams.id"))
    toss_decision = Column(String)
    max_overs = Column(Integer)
    max_wickets = Column(Integer)
    match_result = Column(String)
    man_of_match = Column(Integer, ForeignKey("players.id"))
    home_team_score = Column(Integer)
    away_team_score = Column(Integer)
    home_team_wickets_fallen = Column(Integer)
    away_team_wickets_fallen = Column(Integer)
    home_team_overs_faced = Column(Float)
    away_team_overs_faced = Column(Float)


class LivePlay(Base):
    __tablename__ = "live_play"

    sno = Column(Integer, primary_key=True)
    match_no = Column(Integer, ForeignKey("match.match_id"))
    innings = Column(Integer)
    over = Column(Integer)
    ball = Column(Integer)
    on_strike = Column(String)
    non_strike = Column(String)
    on_bowl = Column(String)
    run = Column(Integer)
    wicket = Column(Boolean)
    batting = Column(String, ForeignKey("teams.id"))
    fielding = Column(String, ForeignKey("teams.id"))
