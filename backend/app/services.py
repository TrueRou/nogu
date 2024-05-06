from datetime import datetime
from typing import Optional, Any

import aiohttp
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, ForeignKey, DateTime, ScalarResult, String, text, Float, Boolean, and_, JSON
from sqlalchemy.ext.asyncio import async_object_session as object_session, AsyncSession
from sqlalchemy.orm import relationship

from app import objects, database, sessions
from app.constants.formulas import bancho_formula, dict_id2obj
from app.constants.privacy import Privacy
from app.constants.privileges import MemberPosition
from app.constants.servers import Server
from app.database import Base, db_session
from app.logging import log, Ansi
import config


class UserAccount(Base):
    __tablename__ = "user_accounts"
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
    server_id = Column(Integer, primary_key=True, nullable=False)
    su_id = Column(Integer, nullable=False)
    su_name = Column(String(64), nullable=False)
    su_flags = Column(Integer, nullable=False)
    su_country = Column(Integer, nullable=False)
    su_playtime = Column(Integer, nullable=False)
    su_major_ruleset = Column(Integer, nullable=False)
    checked_at = Column(DateTime(True), nullable=False, server_default=text("now()"))

    @staticmethod
    async def prepare_avatar(user: 'User', avatar_url: str):
        # TODO... if avatar not exists, prepare avatar for the first time
        pass

    @staticmethod
    async def from_user(session: AsyncSession, server_id: Server, user: 'User') -> Optional['UserAccount']:
        return await database.select_model(session, UserAccount, and_(UserAccount.server_id == server_id.value,
                                                                      UserAccount.user_id == user.id))

    @staticmethod
    async def from_source(session: AsyncSession, server_id: Server, server_user_id: int) -> Optional['UserAccount']:
        return await database.select_model(session, UserAccount, and_(UserAccount.server_id == server_id.value,
                                                                      UserAccount.server_user_id == server_user_id))


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    username = Column(String(64), nullable=False, unique=True)
    privileges = Column(Integer, nullable=False, default=1)
    country = Column(String(64), nullable=False)
    created_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    active_team_id = Column(Integer, ForeignKey('teams.id'), nullable=True)

    accounts = relationship('UserAccount', lazy='selectin', uselist=True)
    active_team = relationship('Team', lazy='selectin', uselist=False)
    teams = relationship('TeamMember', lazy='dynamic', back_populates="member", uselist=True)

    @property
    def active_stage(self) -> Optional['Stage']:
        team: Team = self.active_team
        return team.active_stage if team else None

    @staticmethod
    async def from_id(session: AsyncSession, user_id: int, server=Server.LOCAL) -> Optional['User']:
        if server == Server.LOCAL:
            return await database.get_model(session, user_id, User)
        if server == Server.BANCHO:
            # get relation from cache and then database
            nogu_id = sessions.bancho_nogu_users.get(user_id)
            if nogu_id is None:
                user_account: UserAccount = await database.select_model(session, UserAccount,
                                                                        and_(UserAccount.server_id == server.value,
                                                                             UserAccount.server_user_id == user_id))
                if user_account is not None:
                    nogu_id = user_account.user_id
                    sessions.bancho_nogu_users[user_id] = nogu_id
            if nogu_id is not None:
                return await database.get_model(session, nogu_id, User)


class Beatmap(Base):
    __tablename__ = "beatmaps"
    md5 = Column(String(64), primary_key=True)
    id = Column(Integer, nullable=True, index=True)  # null if beatmap is on local server
    set_id = Column(Integer, nullable=True)  # null if beatmap is on local server
    ranked_status = Column(Integer, nullable=False)
    artist = Column(String(256), nullable=False)
    title = Column(String(256), nullable=False)
    version = Column(String(256), nullable=False)
    creator = Column(String(256), nullable=False)
    filename = Column(String(1024), nullable=False)
    total_length = Column(Integer, nullable=False)
    max_combo = Column(Integer, nullable=False)
    mode = Column(Integer, nullable=False)
    bpm = Column(Float, nullable=False)
    cs = Column(Float, nullable=False)
    ar = Column(Float, nullable=False)
    od = Column(Float, nullable=False)
    hp = Column(Float, nullable=False)
    star_rating = Column(Float, nullable=False)
    updated_at = Column(DateTime(True), nullable=False)
    checked_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    server_id = Column(Integer, nullable=False, default=int(Server.BANCHO))

    @staticmethod
    async def _save_response(session: AsyncSession, response_data: list[dict[str, Any]]):
        for entry in response_data:
            filename = (
                "{artist} - {title} ({creator}) [{version}].osu"
                .format(**entry)
                .translate(objects.IGNORED_BEATMAP_CHARS)
            )

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
                server_updated_at=last_update
            )

            await database.merge_model(session, beatmap)

    @staticmethod
    async def request_api(ident: str) -> Optional['Beatmap']:
        params = {}

        if objects.MD5_PATTERN.match(ident):
            params['h'] = ident
        elif ident.isnumeric():
            params['b'] = int(ident)
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
                async with db_session() as session:
                    await Beatmap._save_response(session, response_data)
                    return await Beatmap.from_ident(session, ident)

    @staticmethod
    async def from_id(session: AsyncSession, beatmap_id: int) -> Optional['Beatmap']:
        return await database.select_model(session, Beatmap, Beatmap.id == beatmap_id)

    @staticmethod
    async def from_md5(session: AsyncSession, md5: str) -> Optional['Beatmap']:
        return await database.get_model(session, md5, Beatmap)

    @staticmethod
    async def from_ident(session: AsyncSession, ident: str) -> Optional['Beatmap']:
        if ident.isnumeric():
            return await Beatmap.from_id(session, int(ident))
        if objects.MD5_PATTERN.match(ident):
            return await Beatmap.from_md5(session, ident)


class Score(Base):
    __tablename__ = 'scores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    beatmap_md5 = Column(String(64), ForeignKey('beatmaps.md5'), nullable=False, index=True)
    score = Column(Integer, nullable=False)
    performance_points = Column(Float, nullable=False)
    accuracy = Column(Float, nullable=False)
    highest_combo = Column(Integer, nullable=False)
    full_combo = Column(Boolean, nullable=False)
    mods = Column(Integer, nullable=False)
    num_300s = Column(Integer, nullable=False)
    num_100s = Column(Integer, nullable=False)
    num_50s = Column(Integer, nullable=False)
    num_misses = Column(Integer, nullable=False)
    num_gekis = Column(Integer, nullable=False)
    num_katus = Column(Integer, nullable=False)
    grade = Column(String(64), nullable=False)
    mode = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    server_id = Column(Integer, nullable=False, default=int(Server.LOCAL))
    stage_id = Column(Integer, ForeignKey('stages.id'), index=True, nullable=False)
    analysis = Column(JSON, nullable=True)

    beatmap = relationship('Beatmap', lazy='selectin')
    stage = relationship('Stage', lazy='selectin', back_populates='scores')

    @staticmethod
    async def from_id(session: AsyncSession, score_id: int) -> Optional['Score']:
        return await database.get_model(session, score_id, Score)

    @staticmethod
    async def conditional_submit(session: AsyncSession, score_info: dict, stage: 'Stage', condition: str) -> Optional['Score']:
        pp = dict_id2obj[stage.formula].calculate(mode=stage.mode)  # TODO: provide correct args to calculate pp
        score = Score(**score_info, stage_id=stage.id, performance_points=pp)
        variables = {
            "acc": score.accuracy,
            "max_combo": score.highest_combo,
            "mods": score.mods,
            "score": score.score
        }
        if objects.AstChecker(condition).check(variables):
            from analysis import analyze_score
            score = await database.add_model(session, score)
            await analyze_score(score)
            return score


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    privacy = Column(Integer, nullable=False, default=int(Privacy.PROTECTED))
    achieved = Column(Boolean, nullable=False, default=False)
    create_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    achieved_at = Column(DateTime(True), nullable=True)
    active_stage_id = Column(Integer, ForeignKey('stages.id'), nullable=True)

    active_stage = relationship('Stage', lazy='selectin', foreign_keys='Team.active_stage_id')
    member = relationship('TeamMember', lazy='immediate', back_populates="teams", uselist=True)
    stages = relationship('Stage', lazy='dynamic', foreign_keys='Stage.team_id')
    
    @staticmethod
    async def fetch_all(session: AsyncSession, limit=20, offset=0, status=-1) -> ScalarResult['Team']:
        if status == -1:
            condition = Team.privacy <= int(Privacy.PROTECTED)
        if status == 0:
            condition = and_(Team.achieved == False, Team.privacy <= int(Privacy.PROTECTED))
        if status == 1:
            condition = and_(Team.achieved == True, Team.privacy <= int(Privacy.PROTECTED))
        return await database.select_models(session=session, obj=Team, condition=condition, offset=offset, limit=limit)
    
    @staticmethod
    async def fetch_me(session: AsyncSession, user: User) -> ScalarResult['TeamMember']:
        return await database.query_models(session=session, sentence=user.teams)

    @staticmethod
    async def from_id(session: AsyncSession, team_id: int) -> Optional['Team']:
        return await database.get_model(session, team_id, Team)

    async def get_stages(self, limit=20, offset=0) -> ScalarResult['Stage']:
        session = object_session(self)
        return await database.query_models(session=session, sentence=self.stages, limit=limit, offset=offset)

    async def set_position(self, user_id: int, position: MemberPosition):
        session = object_session(self)
        member: TeamMember = await database.query_model(session, self.member, TeamMember.user_id == user_id)
        if member is None:
            await database.add_model(session,
                                     TeamMember(team_id=self.id, user_id=user_id, member_position=position.value))
        else:
            member.member_position = position.value
            await session.commit()

    async def position_of(self, user: User) -> MemberPosition:
        session = object_session(self)
        member: TeamMember = await database.query_model(session, self.member, TeamMember.user_id == user.id)
        if member is None:
            return MemberPosition.EMPTY
        return MemberPosition(member.member_position)

    async def member_of(self, user: User) -> bool:
        return await self.position_of(user) != MemberPosition.EMPTY


class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    version = Column(Integer, nullable=False, default=0)
    mode = Column(Integer, nullable=False)
    formula_set = Column(Integer, nullable=False, default=bancho_formula.formula_id)
    created_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    analysis = Column(JSON, nullable=True)
    playlist_id = Column(Integer, ForeignKey('playlists.id'), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)

    playlist = relationship('Playlist', lazy='selectin')  # originated from which playlist
    team = relationship('Team', lazy='selectin', foreign_keys='Stage.team_id',
                        viewonly=True)  # which team owned the stage
    scores = relationship('Score', lazy='dynamic', uselist=True, back_populates='stage')
    maps = relationship('StageMap', lazy='dynamic', uselist=True)

    @staticmethod
    async def from_id(session: AsyncSession, stage_id: int) -> Optional['Stage']:
        return await session.get(Stage, stage_id)

    async def get_beatmap(self, beatmap_md5: str) -> Optional['StageMap']:
        session = object_session(self)
        return await database.query_model(session, self.maps, StageMap.map_md5 == beatmap_md5)

    async def add_beatmap(self, info: dict):
        session = object_session(self)
        return await database.add_model(session, StageMap(**info, stage_id=self.id))

    async def get_beatmaps(self, limit=20, offset=0) -> ScalarResult['StageMap']:
        session = object_session(self)
        return await database.query_models(session=session, sentence=self.maps, limit=limit, offset=offset)

    async def get_scores(self, limit=20, offset=0) -> ScalarResult[Score]:
        session = object_session(self)
        return await database.query_models(session=session, sentence=self.scores, limit=limit, offset=offset)


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    description = Column(String(64), nullable=True)
    version = Column(Integer, nullable=False, default=0)
    mode = Column(Integer, nullable=False)
    formula_set = Column(Integer, nullable=False, default=bancho_formula.formula_id)
    created_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    
    privacy = Column(Integer, nullable=False, default=int(Privacy.PUBLIC))
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    creator = relationship('User', lazy='selectin')
    maps = relationship('PlaylistMap', lazy='dynamic', uselist=True)

class PlaylistUpdate(Base):
    __tablename__ = "playlist_updates"
    
    playlist_id = Column(Integer, ForeignKey('playlists.id'), primary_key=True, nullable=False)
    version = Column(Integer, nullable=False, primary_key=True)
    description = Column(String(64), nullable=False)
    created_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    

class PlaylistMap(Base):
    __tablename__ = "playlist_maps"
    playlist_id = Column(Integer, ForeignKey('playlists.id'), primary_key=True, nullable=False)
    map_md5 = Column(String(64), ForeignKey('beatmaps.md5'), primary_key=True, nullable=False)
    label = Column(String(64), nullable=False) # NM1
    description = Column(String(64), nullable=False) # NoMod Aims
    represent_mods = Column(Integer, nullable=False) # 0(NoMod)
    condition_ast = Column(String(64), nullable=False) # mods == 0
    condition_name = Column(String(64), nullable=False) # NoMod

    beatmap = relationship('Beatmap', lazy='selectin')


class StageMap(Base):
    __tablename__ = "stage_maps"
    stage_id = Column(Integer, ForeignKey('stages.id'), primary_key=True, nullable=False)
    map_md5 = Column(String(64), ForeignKey('beatmaps.md5'), primary_key=True, nullable=False)
    label = Column(String(64), nullable=False) # NM1
    description = Column(String(64), nullable=False) # NoMod Aims
    represent_mods = Column(Integer, nullable=False) # NM(0)
    condition_ast = Column(String(64), nullable=False) # mods == 0
    condition_name = Column(String(64), nullable=False) # NoMod
    analysis = Column(JSON, nullable=True)

    beatmap = relationship('Beatmap', lazy='selectin')


class StageUser(Base):
    __tablename__ = "stage_users"
    stage_id = Column(Integer, ForeignKey('stages.id'), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
    analysis = Column(JSON, nullable=True)


class StageMapUser(Base):
    __tablename__ = "stage_map_user_detail"

    stage_id = Column(Integer, ForeignKey('stages.id'), primary_key=True, nullable=False)
    beatmap_md5 = Column(String(64), ForeignKey('beatmaps.md5'), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
    analysis = Column(JSON, nullable=True)


class TeamMember(Base):
    __tablename__ = "team_member"
    team_id = Column(Integer, ForeignKey('teams.id'), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
    member_position = Column(Integer, nullable=False, default=int(MemberPosition.MEMBER))

    teams = relationship("Team", back_populates="member", lazy='selectin')
    member = relationship("User", back_populates="teams", lazy='selectin')
