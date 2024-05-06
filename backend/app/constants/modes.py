from enum import IntFlag


class GameMode(IntFlag):
    VN_OSU = 0
    VN_TAIKO = 1
    VN_CATCH = 2
    VN_MANIA = 3
    RX_OSU = 4
    RX_TAIKO = 5
    RX_CATCH = 6
    # RX_MANIA = 7  # doesn't exist
    AP_OSU = 8
    # AP_TAIKO = 9  # doesn't exist
    # AP_CATCH = 10  # doesn't exist
    # AP_MANIA = 11  # doesn't exist


    @staticmethod
    def from_client(vanilla: int, mods: int) -> 'GameMode':
        game_mode = GameMode(vanilla)
        if mods & 128:  # relax
            game_mode += 4
        if mods & 8192:  # autopilot
            game_mode += 8
        return game_mode


    @staticmethod
    def from_v2(ruleset: str) -> 'GameMode':
        if ruleset == "osu":
            return GameMode.VN_OSU
        if ruleset == "taiko":
            return GameMode.VN_TAIKO
        if ruleset == "fruits":
            return GameMode.VN_CATCH
        if ruleset == "mania":
            return GameMode.VN_MANIA
        

    def as_vanilla(self):
        if self == GameMode.AP_OSU:
            return GameMode.VN_OSU
        elif self >= GameMode.RX_OSU:
            return self - GameMode.RX_OSU
        else:
            return self

