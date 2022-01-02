import models as m
from sqlalchemy import desc
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


def insert_live_play(db: Session, values: List[Dict] or List[Tuple] or List[m.Match]):
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


if __name__ == "__main__":
    # get_teams(get_db())
    get_last_match_details(get_db())