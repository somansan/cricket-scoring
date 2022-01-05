import models as m
from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from database import get_db
from typing import List, Tuple, Dict


def get_teams(db: Session) -> List[m.Team]:
    return db.query(m.Team).all()


def get_team_by_id(db: Session, team_id: str) -> List[m.Team]:
    return db.query(m.Team).where(m.Team.id == team_id).all()


def get_team_by_name(db: Session, team_name: str) -> List[m.Team]:
    return db.query(m.Team).where(m.Team.name == team_name).all()


def insert_match(db: Session, values: List[Dict] or List[Tuple]):
    rows = list()
    for value in values:
        if isinstance(value, tuple):
            rows.append(m.Match(*value))
        elif isinstance(value, dict):
            rows.append(m.Match(**value))
        elif isinstance(value, m.Match):
            rows.append(value)
        else:
            raise Exception("Invalid type given for insert")
    db.add_all(rows)
    db.commit()


def insert_live_play(db: Session, values: List[Dict] or List[Tuple] or List[m.LivePlay]):
    rows = list()
    for value in values:
        if isinstance(value, tuple):
            rows.append(m.LivePlay(*value))
        elif isinstance(value, dict):
            rows.append(m.LivePlay(**value))
        elif isinstance(value, m.LivePlay):
            rows.append(value)
        else:
            raise Exception("Invalid type given for insert")
    db.add_all(rows)
    db.commit()


def get_last_match_details(db: Session) -> m.Match:
    return db.query(m.Match).order_by(desc(m.Match.match_id)).limit(1).all()[0]


def fetch_players_by_team(db: Session, team: str) -> List[m.Player]:
    return db.query(m.Player).where(m.Player.team == team).all()


def update_team_win(db: Session, team: str):
    db.query(m.Team).filter(m.Team.id == team).update({'match_won': m.Team.match_won + 1})
    db.commit()


def update_team_loss(db: Session, team: str):
    db.query(m.Team).filter(m.Team.id == team).update({'match_lost': m.Team.match_lost + 1})
    db.commit()


def update_team_ties(db: Session, team: str):
    db.query(m.Team).filter(m.Team.id == team).update({'match_tied': m.Team.match_lost + 1})
    db.commit()


def update_player_score(db: Session, player: int, runs: int):
    db.query(m.Player).filter(m.Player.id == player).update({'runs': m.Player.runs + runs})
    db.commit()


def update_player_wickets(db: Session, player: int, wickets: int):
    db.query(m.Player).filter(m.Player.id == player).update({'wickets': m.Player.wickets + wickets})
    db.commit()


def update_player_matches(db: Session, player: int):
    db.query(m.Player).filter(m.Player.id == player).update({'match_played': m.Player.match_played + 1})
    db.commit()


def update_match(db: Session, match: int, values: dict):
    db.query(m.Match).filter(m.Match.match_id == match).update(values)
    db.commit()


def man_of_match(db: Session, match: int):
    return db.query(m.LivePlay.on_strike, func.sum(m.LivePlay.run).label('total_runs')).filter(
        m.LivePlay.match_no == match).group_by(m.LivePlay.on_strike).order_by(desc('total_runs')).limit(1).all()[0]


if __name__ == "__main__":
    # get_teams(get_db())
    # get_last_match_details(get_db())
    # print(get_db().query(m.Team.match_won).where(m.Team.id == 'IND').all())
    # update_team_win(get_db(), team='IND')
    # print(get_db().query(m.Match.match_id, m.Match.venue).all())
    print(man_of_match(get_db(), 11))
