import random
import sys
from random import choice
import models as m
from cricket.crud import get_teams, insert_match, insert_live_play, get_last_match_details, fetch_players_by_team
from cricket.enums import Toss, TossDecision
from database import get_db
from initialize import setup_database, fill_sample_data

"""fetch batsman logic, fetch bowler logic"""

# setup_database()
# fill_sample_data()
max_overs = 10
max_wickets = 10
total_innings = 2


def full_name(player: m.Player):
    return m.Player.first_name + " " + m.Player.last_name


print("SELECT TEAMS TO START MATCH: ")
try:
    teams = get_teams(db=get_db())
    for team in teams:
        print(f"{team.id} : {team.name}")

    print("\nEnter Team ID - ")
    home_team = input("TEAM A: ")
    for team in teams:
        if team.id == home_team:
            home_team = team
            print(team)

    away_team = input("TEAM B: ")
    for team in teams:
        if team.id == away_team:
            away_team = team
            print(team)

    home_team_toss = Toss.HEADS
    toss = random.choice([Toss.HEADS, Toss.TAILS])

    if home_team_toss == toss:
        toss_won = home_team
        toss_failed = away_team
    else:
        toss_won = away_team
        toss_failed = home_team

    toss_result = random.choice([TossDecision.BAT, TossDecision.BOWL])
    toss_decision = f"{toss_won.name} chose to {toss_result} first."
    print(f"\n{toss_won.name} WON THE TOSS")
    print(toss_decision)

    print("\nSTARTING MATCH...")
    match = m.Match(
        home_team=home_team.id,
        away_team=away_team.id,
        venue='XYZ Stadium',
        toss=toss_won.id,
        toss_decision=toss_decision,
        max_overs=max_overs,
        max_wickets=max_wickets
    )
    insert_match(db=get_db(), values=[match])
    match_id = get_last_match_details(get_db()).match_id
    batting, fielding = (toss_won, toss_failed) if toss_result == TossDecision.BAT else (toss_failed, toss_won)

    for inning in range(1, total_innings+1):
        over = 0
        batting_team_players = fetch_players_by_team(get_db(), batting.id)
        fielding_team_players = fetch_players_by_team(get_db(), fielding.id)
        on_strike = batting_team_players.pop(0) if batting_team_players else None
        non_strike = batting_team_players.pop(0) if batting_team_players else None
        while over < max_overs:
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
                            batting=batting,
                            fielding=fielding
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
                            batting=batting,
                            fielding=fielding
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
                            batting=batting,
                            fielding=fielding
                        )
                    )
                    on_strike = batting_team_players.pop(0) if batting_team_players else None
            insert_live_play(get_db(), curr_over)
            on_strike, non_strike = non_strike, on_strike
            # display score
except Exception as e:
    raise e
