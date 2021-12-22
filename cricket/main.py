import sys
from random import choice
from db import create_connection
from pathlib import Path


def initialize():
    print("""SELECT TEAMS TO BEGIN MATCH""")
    teams = dict()  # fetch teams from database key: name, value: Team ; Display teams.keys()
    team_a = teams[input("Team A: ")]
    team_b = teams[input("Team B: ")]


if __name__ == "__main__":
    conn = create_connection(str(Path(__file__).parent.parent) + r"\resources\cricket.db")
    if conn:
        conn.close()
