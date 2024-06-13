from typing import Generic, Tuple, TypeVar
from nogu.app.models.osu.stage import Stage
from nogu.app.models.team import TeamWithMembers
from sqlmodel import SQLModel

T = TypeVar("T")


def from_tuples(tuple: list[Tuple], type: Generic[T]) -> list[T]:
    results = []
    for item in tuple:
        results.append(from_tuple(item, type))
    return results


def from_tuple(tuple: Tuple, type: Generic[T]) -> T:
    variables = []
    for i in range(len(tuple)):
        variables.append(tuple[i])
    return type(*variables)


class OsuTeamCombination(SQLModel):
    def __init__(self, *args):
        self.team = args[0]
        self.stage = args[1]

    team: TeamWithMembers
    stage: Stage
