from enum import IntEnum, unique


@unique
class Ruleset(IntEnum):
    OSU = 0
    TAIKO = 1
    CATCH = 2
    MANIA = 3
    OSU_RX = 4
    TAIKO_RX = 5
    CATCH_RX = 6
    # RX_MANIA = 7  # doesn't exist
    OSU_AP = 8
    # AP_TAIKO = 9  # doesn't exist
    # AP_CATCH = 10  # doesn't exist
    # AP_MANIA = 11  # doesn't exist

    @staticmethod
    def from_client(vanilla: int, mods: int) -> "Ruleset":
        game_mode = Ruleset(vanilla)
        if mods & 128:  # relax
            game_mode += 4
        if mods & 8192:  # autopilot
            game_mode += 8
        return game_mode

    @staticmethod
    def from_v2(ruleset: str) -> "Ruleset":
        if ruleset == "osu":
            return Ruleset.OSU
        if ruleset == "taiko":
            return Ruleset.TAIKO
        if ruleset == "fruits":
            return Ruleset.CATCH
        if ruleset == "mania":
            return Ruleset.MANIA

    def as_vanilla(self):
        if self == Ruleset.OSU_AP:
            return Ruleset.OSU
        elif self >= Ruleset.OSU_RX:
            return self - Ruleset.OSU_RX
        else:
            return self
