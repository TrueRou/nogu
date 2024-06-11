from typing import Generic, Tuple, TypeVar
from nogu.app.models.osu.stage import Stage
from nogu.app.models.team import TeamWithMembers
from sqlmodel import SQLModel

T = TypeVar("T")


def from_tuple(tuple: list[Tuple], type: Generic[T]) -> list[T]:
    results = []
    for item in tuple:
        variables = []
        for i in range(len(item)):
            variables.append(item[i])
        results.append(type(*variables))
    return results


class OsuTeamCombination(SQLModel):
    def __init__(self, *args):
        self.team = args[0]
        self.stage = args[1]

    team: TeamWithMembers
    stage: Stage
