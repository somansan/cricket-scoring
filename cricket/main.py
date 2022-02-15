import random
import time
import models as m

from cricket.utils import full_name, find_team_in_list
from cricket.crud import get_teams, insert_match, insert_live_play, get_last_match_details, \
    fetch_players_by_team, update_team_win, update_team_ties, update_team_loss, update_player_score, \
    update_player_wickets, update_match, man_of_match
from cricket.enums import Toss, TossDecision, Constants as const
from cricket.manager import GameManager, TeamManager, PlayerManager
from database import get_db
from initialize import setup_database, fill_sample_data

# setup_database()
# fill_sample_data()

print("SELECT TEAMS TO START MATCH: ")
try:
    htm = None
    atm = None
    teams = get_teams(db=get_db())
    for team in teams:
        print(f"{team.id} : {team.name}")

    print("\nEnter Team ID - ")
    home_team = input("TEAM A: ").upper()
    htm = find_team_in_list(home_team, teams)
    if not htm:
        raise Exception("Team Not Found!")

    away_team = input("TEAM B: ").upper()
    atm = find_team_in_list(away_team, teams)
    if not atm:
        raise Exception("Team Not Found!")

    gm = GameManager()
    home_team_toss = Toss.HEADS
    toss = random.choice([Toss.HEADS, Toss.TAILS])
    toss_result = random.choice([TossDecision.BAT, TossDecision.BOWL])

    if home_team_toss == toss:
        gm.toss = htm
        if toss_result == TossDecision.BAT:
            gm.batting = htm
            gm.fielding = atm
        else:
            gm.fielding = htm
            gm.batting = atm
    else:
        gm.toss = atm
        if toss_result == TossDecision.BAT:
            gm.batting = atm
            gm.fielding = htm
        else:
            gm.fielding = atm
            gm.batting = htm

    toss_decision = f"{gm.toss.name} chose to {toss_result} first."
    print(f"\n{gm.toss.name} WON THE TOSS")
    print(toss_decision)

    print("\nSTARTING MATCH...")
    match = m.Match(
        home_team=htm.team_id,
        away_team=atm.team_id,
        venue=gm.venue,
        toss=gm.toss.team_id,
        toss_decision=toss_decision
    )
    insert_match(db=get_db(), values=[match])
    match_id = get_last_match_details(get_db()).match_id

    for inning in range(1, const.TOTAL_INNINGS + 1):
        gm.inning = inning
        over = 0
        gm.batting.players = [
            PlayerManager(
                player_id=item.id,
                name=full_name(item)
            ) for item in fetch_players_by_team(get_db(), gm.batting.team_id)
        ]
        gm.fielding.players = [
            PlayerManager(
                player_id=item.id,
                name=full_name(item)
            ) for item in fetch_players_by_team(get_db(), gm.fielding.team_id)
        ]
        gm.on_strike = gm.batting.players.pop(0) if gm.batting.players else None
        gm.non_strike = gm.batting.players.pop(0) if gm.batting.players else None
        inning_complete = False
        while over < const.TOTAL_OVERS and not inning_complete:
            curr_over_objects = []
            gm.this_over = list()
            gm.on_bowl = gm.fielding.players.pop()
            for ball in range(1, 7):
                if inning == 2 and gm.batting.score > gm.batting.target_score:
                    inning_complete = True
                    break
                wicket = False
                run = random.choice([-1, 0, 1, 2, 3, 4, 5, 6])

                if run < 0:
                    wicket = True

                curr_over_objects.append(
                    m.LivePlay(
                        match_no=match_id,
                        innings=inning,
                        over=over,
                        ball=ball,
                        on_strike=gm.on_strike.name,
                        non_strike=gm.non_strike.name,
                        on_bowl=gm.on_bowl.name,
                        run=run,
                        wicket=wicket,
                        batting=gm.batting.team_id,
                        fielding=gm.fielding.team_id
                    )
                )

                if ball != 6:
                    gm.batting.overs = float(f"{over}.{ball}")
                else:
                    gm.batting.overs = over + 1

                if wicket:
                    update_player_score(get_db(), gm.on_strike.player_id, gm.on_strike.score)
                    update_player_wickets(get_db(), gm.on_bowl.player_id, 1)
                    gm.batting.wickets_down += 1
                    gm.this_over.append('W')
                    if gm.batting.wickets_down >= const.TOTAL_WICKETS:
                        inning_complete = True
                        break
                    else:
                        gm.on_strike = gm.batting.players.pop(0)
                else:
                    gm.on_strike.score += run
                    gm.batting.score += run
                    gm.this_over.append(str(run) if run > 0 else '.')
                    if run % 2 != 0:
                        gm.on_strike, gm.non_strike = gm.non_strike, gm.on_strike

            insert_live_play(get_db(), curr_over_objects)
            if inning_complete:
                break
            gm.on_strike, gm.non_strike = gm.non_strike, gm.on_strike
            print(gm)
            time.sleep(1)
            over = gm.batting.overs

        if inning == 1:
            gm.batting, gm.fielding = gm.fielding, gm.batting
            gm.batting.players = []
            gm.fielding.players = []
            gm.batting.target_score = gm.fielding.score + 1
            print(
                f"""{gm.batting.name} NEEDS {gm.batting.target_score} TO WIN IN {const.TOTAL_OVERS} OVERS."""
            )
            time.sleep(2)
            print(f"\nStarting 2nd innings...")
            time.sleep(1)

    if gm.batting.score > gm.batting.target_score:
        update_team_win(get_db(), gm.batting.team_id)
        update_team_loss(get_db(), gm.fielding.team_id)
        match_result = F"{gm.batting.name} won by {const.TOTAL_WICKETS - gm.batting.wickets_down} wickets."
    elif gm.batting.score < gm.batting.target_score:
        update_team_win(get_db(), gm.fielding.team_id)
        update_team_loss(get_db(), gm.batting.team_id)
        match_result = F"{gm.fielding.name} won by {gm.batting.target_score - gm.batting.score} runs."
    else:
        update_team_ties(get_db(), gm.batting.team_id)
        update_team_ties(get_db(), gm.fielding.team_id)
        match_result = "MATCH TIED!"

    print(f"{match_result}")

except Exception as e:
    raise e
