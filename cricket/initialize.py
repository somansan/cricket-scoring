from typing import List, Tuple
from models import Team, Player

from database import engine, get_db
from models import Base
from enums import PlayerType as pT


def setup_database():
    Base.metadata.create_all(bind=engine)


def fill_sample_data():
    insert_teams(values=sample_teams)
    insert_players(values=sample_players)


def insert_teams(values: List[Tuple]):
    db = get_db()
    rows = list()
    for value in values:
        rows.append(
            Team(
                id=value[0],
                name=value[1],
                match_won=value[2],
                match_lost=value[3],
                match_tied=value[4]
            )
        )
    db.add_all(rows)
    db.commit()


def insert_players(values: List[Tuple]):
    """
    Have auto increment feature.
    Do not provide id in the tuple
    """
    db = get_db()
    rows = list()
    for value in values:
        rows.append(
            Player(
                first_name=value[0],
                last_name=value[1],
                age=value[2],
                match_played=value[3],
                runs=value[4],
                wickets=value[5],
                player_type=value[6],
                team=value[7]
            )
        )
    db.add_all(rows)
    db.commit()


sample_teams = [('IND', 'INDIA', 0, 0, 0), ('AUS', 'AUSTRALIA', 0, 0, 0), ('ENG', 'ENGLAND', 0, 0, 0)]
sample_players = [
    ('Virat', 'Kolhi', 33, 0, 0, 0, pT.BATSMAN, 'IND'),
    ('KL', 'Rahul', 29, 0, 0, 0, pT.BATSMAN, 'IND'),
    ('Mayank', 'Agarwal', 30, 0, 0, 0, pT.BATSMAN, 'IND'),
    ('Cheteswar', 'Pujara', 33, 0, 0, 0, pT.BATSMAN, 'IND'),
    ('Ajinkya', 'Rahane', 33, 0, 0, 0, pT.BATSMAN, 'IND'),
    ('Rishab', 'Pant', 24, 0, 0, 0, pT.KEEPER, 'IND'),
    ('Ravichandar', 'Aswin', 35, 0, 0, 0, pT.ALLROUNDER, 'IND'),
    ('Shardul', 'Thakur', 30, 0, 0, 0, pT.BOWLER, 'IND'),
    ('Mohammad', 'Shami', 31, 0, 0, 0, pT.BOWLER, 'IND'),
    ('Jasprit', 'Bumrah', 28, 0, 0, 0, pT.BOWLER, 'IND'),
    ('Mohammed', 'Siraj', 27, 0, 0, 0, pT.BOWLER, 'IND'),
    ('Marcus', 'Harris', 29, 0, 0, 0, pT.BATSMAN, 'AUS'),
    ('David', 'Warner', 35, 0, 0, 0, pT.BATSMAN, 'AUS'),
    ('Nathan', 'Lyon', 34, 0, 0, 0, pT.BATSMAN, 'AUS'),
    ('Marnus', 'Labuschagne', 27, 0, 0, 0, pT.ALLROUNDER, 'AUS'),
    ('Steve', 'Smith', 32, 0, 0, 0, pT.BATSMAN, 'AUS'),
    ('Travis', 'Head', 27, 0, 0, 0, pT.BATSMAN, 'AUS'),
    ('Cameron', 'Green', 22, 0, 0, 0, pT.ALLROUNDER, 'AUS'),
    ('Alex', 'Carey', 30, 0, 0, 0, pT.KEEPER, 'AUS'),
    ('Pat', 'Cummins', 28, 0, 0, 0, pT.BOWLER, 'AUS'),
    ('Mitchell', 'Starc', 31, 0, 0, 0, pT.BOWLER, 'AUS'),
    ('Scott', 'Boland', 32, 0, 0, 0, pT.BOWLER, 'AUS')
]


if __name__ == "__main__":
    setup_database()
    fill_sample_data()
