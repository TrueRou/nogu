import datetime
import aiohttp
from typing import Any
from sqlmodel import Field, SQLModel, Session, select

from nogu import config
from nogu.app.database import auto_session
from nogu.app.logging import log, Ansi
from nogu.app.constants.osu import Server, Ruleset
from nogu.app.objects import IGNORED_BEATMAP_CHARS, MD5_PATTERN


class Beatmap(SQLModel, table=True):
    __tablename__ = "osu_beatmaps"

    md5: str = Field(primary_key=True)
    id: int | None = Field(index=True)  # null if beatmap is on local server
    set_id: int | None = Field(index=True)  # null if beatmap is on local server
    ranked_status: int
    artist: str
    title: str
    version: str
    creator: str
    filename: str = Field(index=True)
    total_length: int
    max_combo: int
    ruleset: Ruleset
    bpm: float
    cs: float
    ar: float
    od: float
    hp: float
    star_rating: float
    osu_server: int = Field(default=Server.BANCHO)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    checked_at: datetime.datetime  # the time we last checked for updates

    uploaded_by: int | None = Field(default=None, foreign_key="users.id")  # null if beatmap is from remote server


class BeatmapEvent(SQLModel):
    beatmap: Beatmap | None
    message: str | None


class BeatmapSrv:
    @staticmethod
    async def _save_response(session: Session, response_data: list[dict[str, Any]]):
        for entry in response_data:
            filename = "{artist} - {title} ({creator}) [{version}].osu".format(**entry).translate(IGNORED_BEATMAP_CHARS)

            _last_update = entry["last_update"]
            last_update = datetime(
                year=int(_last_update[0:4]),
                month=int(_last_update[5:7]),
                day=int(_last_update[8:10]),
                hour=int(_last_update[11:13]),
                minute=int(_last_update[14:16]),
                second=int(_last_update[17:19]),
            )

            beatmap = Beatmap(
                md5=entry["file_md5"],
                id=entry["beatmap_id"],
                set_id=entry["beatmapset_id"],
                ranked_status=entry["approved"],
                artist=entry["artist"],
                title=entry["title"],
                version=entry["version"],
                creator=entry["creator"],
                filename=filename,
                total_length=int(entry["total_length"]),
                max_combo=int(entry["max_combo"]),
                mode=int(entry["mode"]),
                bpm=float(entry["bpm"] if entry["bpm"] is not None else 0),
                cs=float(entry["diff_size"]),
                od=float(entry["diff_overall"]),
                ar=float(entry["diff_approach"]),
                hp=float(entry["diff_drain"]),
                star_rating=float(entry["difficultyrating"]),
                server_updated_at=last_update,
            )

            session.merge(beatmap)

    def from_ident(session: Session, ident: str):
        if ident.isnumeric():
            sentence = select(Beatmap).where(Beatmap.id == int(ident))
            return session.exec(sentence).first()
        if MD5_PATTERN.match(ident):
            return session.get(Beatmap, ident)

    @staticmethod
    async def request_api(ident: str):
        params = {}

        if MD5_PATTERN.match(ident):
            params["h"] = ident
        elif ident.isnumeric():
            params["b"] = int(ident)
        else:
            return None  # wrong format of ident

        if config.debug:
            log(f"Doing api (getbeatmaps) request {params}", Ansi.LMAGENTA)

        url = "https://old.ppy.sh/api/get_beatmaps"
        params["k"] = str(config.osu_api_v1_key)

        async with aiohttp.ClientSession() as request_session:
            response = await request_session.get(url, params=params)
            response_data = await response.json()
            if response.status == 200 and response_data:
                with auto_session() as session:
                    BeatmapSrv._save_response(session, response_data)
                    a = BeatmapSrv.from_ident(session, ident)
                    return BeatmapSrv.from_ident(session, ident)
