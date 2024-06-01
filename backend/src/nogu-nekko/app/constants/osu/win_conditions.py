from enum import IntEnum, auto


class WinCondition(IntEnum):
    SCORE = auto()
    ACCURACY = auto()
    COMBO = auto()
    PP = auto()
