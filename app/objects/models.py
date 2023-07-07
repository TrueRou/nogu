from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, text, Float, Boolean
from sqlalchemy.orm import relationship

from app.constants.formulas import bancho_formula
from app.constants.privacy import Privacy
from app.constants.privileges import MemberPosition
from app.constants.servers import Server
from app.database import Base


class UserAccount(Base):
    __tablename__ = "user_accounts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
    server_id = Column(Integer, nullable=False)
    server_user_id = Column(Integer, nullable=False)
    server_user_name = Column(String(64), nullable=False)
    checked_at = Column(DateTime(True), nullable=False, server_default=text("now()"))


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


class Beatmap(Base):
    __tablename__ = "beatmaps"
    md5 = Column(String(64), primary_key=True)
    id = Column(Integer, nullable=True)  # null if beatmap is on local server
    set_id = Column(Integer, nullable=True)  # null if beatmap is on local server
    ranked_status = Column(Integer, nullable=False)
    artist = Column(String(64), nullable=False)
    title = Column(String(64), nullable=False)
    version = Column(String(64), nullable=False)
    creator = Column(String(64), nullable=False)
    filename = Column(String(64), nullable=False)
    total_length = Column(Integer, nullable=False)
    max_combo = Column(Integer, nullable=False)
    mode = Column(Integer, nullable=False)
    bpm = Column(Float, nullable=False)
    cs = Column(Float, nullable=False)
    ar = Column(Float, nullable=False)
    od = Column(Float, nullable=False)
    hp = Column(Float, nullable=False)
    star_rating = Column(Float, nullable=False)
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    server_updated_at = Column(DateTime(True), nullable=False)
    server_id = Column(Integer, nullable=False, default=Server.BANCHO)


class Score(Base):
    __tablename__ = 'scores'

    score_id = Column(Integer, primary_key=True, autoincrement=True)
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
    server_id = Column(Integer, nullable=False, default=Server.LOCAL)
    stage_id = Column(Integer, ForeignKey('stages.id'), index=True, nullable=False)

    beatmap = relationship('Beatmap', lazy='selectin')
    stage = relationship('Stage', lazy='selectin', back_populates='scores')


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    privacy = Column(Integer, nullable=False, default=Privacy.PROTECTED)
    achieved = Column(Boolean, nullable=False, default=False)
    create_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    finish_at = Column(DateTime(True), nullable=True)
    active_stage_id = Column(Integer, ForeignKey('stages.id'), nullable=True)

    active_stage = relationship('Stage', lazy='selectin', foreign_keys='Team.active_stage_id')
    member = relationship('TeamMember', lazy='dynamic', back_populates="teams")
    stages = relationship('Stage', lazy='dynamic', foreign_keys='Stage.team_id')


class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    mode = Column(Integer, nullable=False, default=0)
    formula = Column(Integer, nullable=False, default=bancho_formula.formula_id)
    created_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    pool_id = Column(Integer, ForeignKey('pools.id'), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)

    pool = relationship('Pool', lazy='selectin')  # originated from which pool
    team = relationship('Team', lazy='selectin', foreign_keys='Stage.team_id', viewonly=True)  # which team owned the stage
    scores = relationship('Score', lazy='dynamic', uselist=True, back_populates='stage')
    maps = relationship('StageMap', lazy='dynamic', uselist=True)


class Pool(Base):
    __tablename__ = "pools"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    description = Column(String(64), nullable=True)
    mode = Column(Integer, nullable=False)
    privacy = Column(Integer, nullable=False, default=Privacy.PUBLIC)
    created_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    creator = relationship('User', lazy='selectin')
    maps = relationship('PoolMap', lazy='dynamic', uselist=True)


class PoolMap(Base):
    __tablename__ = "pool_maps"
    id = Column(Integer, primary_key=True, autoincrement=True)
    pool_id = Column(Integer, ForeignKey('pools.id'), index=True, nullable=False)
    map_md5 = Column(String(64), ForeignKey('beatmaps.md5'), index=True, nullable=False)
    description = Column(String(64), nullable=False)
    condition_ast = Column(String(64), nullable=False)
    condition_name = Column(String(64), nullable=False)
    condition_represent_mods = Column(Integer, nullable=False)

    beatmap = relationship('Beatmap', lazy='selectin')


class StageMap(Base):
    __tablename__ = "stage_maps"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stage_id = Column(Integer, ForeignKey('stages.id'), index=True, nullable=False)
    map_md5 = Column(String(64), ForeignKey('beatmaps.md5'), index=True, nullable=False)
    description = Column(String(64), nullable=False)
    condition_ast = Column(String(64), nullable=False)
    condition_name = Column(String(64), nullable=False)
    condition_represent_mods = Column(Integer, nullable=False)

    beatmap = relationship('Beatmap', lazy='selectin')


class TeamMember(Base):
    __tablename__ = "team_member"
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey('teams.id'), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
    member_position = Column(Integer, nullable=False, default=MemberPosition.MEMBER)

    teams = relationship("Team", back_populates="member")
    member = relationship("User", back_populates="teams")