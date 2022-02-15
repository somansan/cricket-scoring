from manager import TeamManager
from typing import List, Optional
import models as m


def full_name(player: m.Player):
    return player.first_name + " " + player.last_name


def find_team_in_list(team_id: str, teams: List[m.Team]) -> Optional[TeamManager]:
    for team in teams:
        if team.id == team_id:
            return TeamManager(team.id, team.name)
    return None
