from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, Boolean, func
from sqlalchemy.orm import declarative_base, relationship, backref, Mapped

Base = declarative_base()


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(length=32), index=True, nullable=False)
    privilege = Column(Integer, nullable=False, default=0)
    creation_time = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    accounts = relationship('UserAccount', backref=backref('user', lazy=False), lazy='selectin', uselist=True)


class Team(Base):
    __tablename__ = "team"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    privacy = Column(Integer, nullable=False, default=0)
    achieved = Column(Boolean, nullable=False, default=False)
    availability = Column(Integer, nullable=True)
    creation_time = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    current_stage_id = Column(Integer, ForeignKey('map_stage.id'), nullable=False)
    owner_user_id = Column(Integer, ForeignKey('user.id'), nullable=False)


class Beatmap(Base):
    __tablename__ = "beatmap"
    md5 = Column(String, primary_key=True)
    # beatmap fields
    # use beatmap md5 as primary key, and we don't store beatmapsets


class Pool(Base):
    __tablename__ = "pool"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    privacy = Column(Integer, nullable=False, default=0)
    creation_time = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    last_updated = Column(TIMESTAMP, nullable=False)
    owner_user_id = Column(Integer, ForeignKey('user.id'), nullable=False)


class Stage(Base):
    __tablename__ = "stage"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    creation_time = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    last_updated = Column(TIMESTAMP, nullable=False)
    origin_pool_id = Column(Integer, ForeignKey('pool.id'), nullable=False)
    owner_team_id = Column(Integer, ForeignKey('team.id'), nullable=False)


class Server(Base):
    __tablename__ = "server"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    home_page = Column(String, nullable=False)
    user_page = Column(String, nullable=False)
    default_formula_id = Column(Integer, ForeignKey('formula.id'), nullable=False)


class Formula(Base):
    __tablename__ = "formula"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    origin = Column(String, nullable=False)
    home_page = Column(String, nullable=False)
    supported_ruleset = Column(Integer, nullable=False)


class UserAccount(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), index=True, nullable=False)
    server_id = Column(Integer, ForeignKey('server.id'), index=True, nullable=False)
    server_user_id = Column(Integer, nullable=False)
    server_user_name = Column(String, nullable=False)
    last_check_time = Column(TIMESTAMP, nullable=False)


class PoolMap(Base):
    __tablename__ = "pool_map"
    id = Column(Integer, primary_key=True, autoincrement=True)
    pool_id = Column(Integer, ForeignKey('pool.id'), index=True, nullable=False)
    map_md5 = Column(String, ForeignKey('beatmap.md5'), index=True, nullable=False)
    description = Column(String, nullable=False)
    condition_ast = Column(String, nullable=False)
    condition_name = Column(String, nullable=False)


class StageMap(Base):
    __tablename__ = "stage_map"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stage_id = Column(Integer, ForeignKey('stage.id'), index=True, nullable=False)
    map_md5 = Column(String, ForeignKey('beatmap.md5'), index=True, nullable=False)
    description = Column(String, nullable=False)
    condition_ast = Column(String, nullable=False)
    condition_name = Column(String, nullable=False)


class StageScore(Base):
    __tablename__ = "stage_score"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stage_id = Column(Integer, ForeignKey('stage.id'), index=True, nullable=False)
    server_id = Column(Integer, ForeignKey('server.id'), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), index=True, nullable=False)
    # score fields
