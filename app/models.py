from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, Boolean, func, Float
from sqlalchemy.orm import declarative_base, relationship, backref

Base = declarative_base()


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(64), index=True, nullable=False)
    privilege = Column(Integer, nullable=False, default=0)
    creation_time = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    active_team_id = Column(Integer, ForeignKey('team.id'), nullable=True)
    active_team = relationship('Team', lazy='selectin')
    accounts = relationship('UserAccount', lazy='selectin', uselist=True)
    teams = relationship('Team', lazy='dynamic', secondary='team_member', back_populates="users")


class Team(Base):
    __tablename__ = "team"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    privacy = Column(Integer, nullable=False, default=0)
    achieved = Column(Boolean, nullable=False, default=False)
    availability = Column(Integer, nullable=True)
    creation_time = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    # active_stage = relationship('Stage', lazy='selectin')
    users = relationship('User', lazy='dynamic', secondary='team_member', back_populates="teams")


class Beatmap(Base):
    __tablename__ = "beatmap"
    md5 = Column(String(64), primary_key=True)
    # beatmap fields
    set_id = Column(Integer, nullable=False)
    difficulty_rating = Column(Float, nullable=False)
    id = Column(Integer, nullable=False)
    mode = Column(String(64), nullable=False)
    status = Column(String(64), nullable=False)
    total_length = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)  # Refer to the creator id
    version = Column(String(64), nullable=False)
    accuracy = Column(Float, nullable=False)
    ar = Column(Float, nullable=False)
    bpm = Column(Float, nullable=False)
    convert = Column(Boolean, nullable=False)
    count_circles = Column(Integer, nullable=False)
    count_sliders = Column(Integer, nullable=False)
    count_spinners = Column(Integer, nullable=False)
    cs = Column(Integer, nullable=False)
    deleted_at = Column(TIMESTAMP)
    drain = Column(Integer, nullable=False)
    hit_length = Column(Integer, nullable=False)
    is_scoreable = Column(Boolean, nullable=False)
    last_updated = Column(TIMESTAMP, nullable=False)
    mode_int = Column(Integer, nullable=False)
    ranked = Column(Boolean, nullable=False)
    url = Column(String(64), nullable=False)
    max_combo = Column(Integer, nullable=False)


class Pool(Base):
    __tablename__ = "pool"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    ruleset = Column(Integer, nullable=False, default=0)
    description = Column(String(64), nullable=True)
    privacy = Column(Integer, nullable=False, default=0)
    creation_time = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    last_updated = Column(TIMESTAMP, nullable=False)
    owner_id = Column(Integer, ForeignKey('user.id'), nullable=False)


class Stage(Base):
    __tablename__ = "stage"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    ruleset = Column(Integer, nullable=False, default=0)
    creation_time = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    last_updated = Column(TIMESTAMP, nullable=False)
    pool_id = Column(Integer, ForeignKey('pool.id'), nullable=False)  # originated from which pool
    team_id = Column(Integer, ForeignKey('team.id'), nullable=False)  # which team owned the stage


class Server(Base):
    __tablename__ = "server"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    domain = Column(String(64), nullable=False)
    home_page = Column(String(64), nullable=False)
    user_page = Column(String(64), nullable=False)


class Formula(Base):
    __tablename__ = "formula"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    author = Column(String(64), nullable=False)
    origin = Column(String(64), nullable=False)
    home_page = Column(String(64), nullable=False)
    supported_ruleset = Column(Integer, nullable=False)


class Score(Base):
    __tablename__ = "score"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stage_id = Column(Integer, ForeignKey('stage.id'), index=True, nullable=False)
    server_id = Column(Integer, ForeignKey('server.id'), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), index=True, nullable=False)
    map_md5 = Column(String(64), ForeignKey('beatmap.md5'), index=True, nullable=False)
    # score fields
    accuracy = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    max_combo = Column(Integer, nullable=False)
    mode_int = Column(Integer, nullable=False)
    mods = Column(Integer, nullable=False)
    rank = Column(String(64), nullable=False)
    score = Column(Integer, nullable=False)
    count_300 = Column(Integer, nullable=False)
    count_100 = Column(Integer, nullable=False)
    count_50 = Column(Integer, nullable=False)
    count_miss = Column(Integer, nullable=False)
    stage = relationship('Stage', backref=backref('scores', lazy='dynamic'), lazy='selectin')
    beatmap = relationship('Beatmap', lazy='selectin')


class UserAccount(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), index=True, nullable=False)
    server_id = Column(Integer, ForeignKey('server.id'), index=True, nullable=False)
    server_user_id = Column(Integer, nullable=False)
    server_user_name = Column(String(64), nullable=False)
    last_check_time = Column(TIMESTAMP, nullable=False)


class PoolMap(Base):
    __tablename__ = "pool_map"
    id = Column(Integer, primary_key=True, autoincrement=True)
    pool_id = Column(Integer, ForeignKey('pool.id'), index=True, nullable=False)
    map_md5 = Column(String(64), ForeignKey('beatmap.md5'), index=True, nullable=False)
    description = Column(String(64), nullable=False)
    condition_ast = Column(String(64), nullable=False)
    condition_name = Column(String(64), nullable=False)


class StageMap(Base):
    __tablename__ = "stage_map"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stage_id = Column(Integer, ForeignKey('stage.id'), index=True, nullable=False)
    map_md5 = Column(String(64), ForeignKey('beatmap.md5'), index=True, nullable=False)
    description = Column(String(64), nullable=False)
    condition_ast = Column(String(64), nullable=False)
    condition_name = Column(String(64), nullable=False)


class TeamMember(Base):
    __tablename__ = "team_member"
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey('team.id'), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), index=True, nullable=False)
