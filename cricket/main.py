import random
import sys
from random import choice
import models as m
from cricket.constants import TOTAL_WICKETS, TOTAL_OVERS, TOTAL_INNINGS
from cricket.crud import get_teams, insert_match, insert_live_play, get_last_match_details, fetch_players_by_team
from cricket.enums import Toss, TossDecision
from cricket.manager import GameManager, TeamManager
from database import get_db
from initialize import setup_database, fill_sample_data

"""fetch batsman logic, fetch bowler logic"""

# setup_database()
# fill_sample_data()


def full_name(player: m.Player):
    return m.Player.first_name + " " + m.Player.last_name


print("SELECT TEAMS TO START MATCH: ")
try:
    htm = None
    atm = None
    teams = get_teams(db=get_db())
    for team in teams:
        print(f"{team.id} : {team.name}")

    print("\nEnter Team ID - ")
    home_team = input("TEAM A: ")
    for team in teams:
        if team.id == home_team:
            home_team = team
            htm = TeamManager(team.id, team.name)
            print(team)

    away_team = input("TEAM B: ")
    for team in teams:
        if team.id == away_team:
            away_team = team
            atm = TeamManager(team.id, team.name)
            print(team)

    gm = GameManager()
    home_team_toss = Toss.HEADS
    toss = random.choice([Toss.HEADS, Toss.TAILS])
    toss_result = random.choice([TossDecision.BAT, TossDecision.BOWL])

    if home_team_toss == toss:
        gm.toss(htm)
        if toss_result == TossDecision.BAT:
            gm.batting(htm)
            gm.fielding(atm)
        else:
            gm.fielding(htm)
            gm.batting(atm)
    else:
        gm.toss(atm)
        if toss_result == TossDecision.BAT:
            gm.batting(atm)
            gm.fielding(htm)
        else:
            gm.fielding(atm)
            gm.batting(htm)

    toss_decision = f"{gm.toss.name} chose to {toss_result} first."
    print(f"\n{gm.toss.name} WON THE TOSS")
    print(toss_decision)

    print("\nSTARTING MATCH...")
    match = m.Match(
        home_team=htm.team_id,
        away_team=atm.team_id,
        venue=gm.venue,
        toss=gm.toss.id,
        toss_decision=toss_decision,
        max_overs=TOTAL_OVERS,
        max_wickets=TOTAL_WICKETS
    )
    insert_match(db=get_db(), values=[match])
    match_id = get_last_match_details(get_db()).match_id

    for inning in range(1, TOTAL_INNINGS + 1):
        over = 0
        batting_team_players = fetch_players_by_team(get_db(), gm.batting.id)
        fielding_team_players = fetch_players_by_team(get_db(), gm.fielding.id)
        on_strike = batting_team_players.pop(0) if batting_team_players else None
        non_strike = batting_team_players.pop(0) if batting_team_players else None
        while over < TOTAL_OVERS:
            curr_over = []
            on_bowl = fielding_team_players.pop()
            for ball in range(1, 7):
                run = random.choice([-1, 0, 1, 2, 3, 4, 5, 6])
                if run >= 0 and (run % 2 == 0):
                    curr_over.append(
                        m.LivePlay(
                            match_no=match_id,
                            innings=inning,
                            over=over,
                            ball=ball,
                            on_strike=full_name(on_strike),
                            non_strike=full_name(non_strike),
                            on_bowl=full_name(on_bowl),
                            run=run,
                            wicket=False,
                            batting=gm.batting.id,
                            fielding=gm.fielding.id
                        )
                    )
                elif run >= 0 and (run % 2 != 0):
                    curr_over.append(
                        m.LivePlay(
                            match_no=match_id,
                            innings=inning,
                            over=over,
                            ball=ball,
                            on_strike=full_name(on_strike),
                            non_strike=full_name(non_strike),
                            on_bowl=full_name(on_bowl),
                            run=run,
                            wicket=False,
                            batting=gm.batting.id,
                            fielding=gm.fielding.id
                        )
                    )
                    on_strike, non_strike = non_strike, on_strike
                else:
                    curr_over.append(
                        m.LivePlay(
                            match_no=match_id,
                            innings=inning,
                            over=over,
                            ball=ball,
                            on_strike=full_name(on_strike),
                            non_strike=full_name(non_strike),
                            on_bowl=full_name(on_bowl),
                            run=run,
                            wicket=True,
                            batting=gm.batting.id,
                            fielding=gm.fielding.id
                        )
                    )
                    on_strike = batting_team_players.pop(0) if batting_team_players else None
            insert_live_play(get_db(), curr_over)
            on_strike, non_strike = non_strike, on_strike
            # display score
except Exception as e:
    raise e
