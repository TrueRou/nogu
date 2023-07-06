from sqlalchemy import Column, Integer, Text, DateTime, text, ForeignKey
from sqlalchemy.orm import relationship

from app.constants.privacy import Privacy
from app.database import Base


class PoolMap(Base):
    __tablename__ = "pool_maps"
    id = Column(Integer, primary_key=True, autoincrement=True)
    pool_id = Column(Integer, ForeignKey('pools.id'), index=True, nullable=False)
    map_md5 = Column(Text, ForeignKey('beatmaps.md5'), index=True, nullable=False)
    description = Column(Text, nullable=False)
    condition_ast = Column(Text, nullable=False)
    condition_name = Column(Text, nullable=False)
    condition_represent_mods = Column(Integer, nullable=False)

    beatmap = relationship('Beatmap', lazy='selectin')


class Pool(Base):
    __tablename__ = "pools"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    mode = Column(Integer, nullable=False)
    privacy = Column(Integer, nullable=False, default=Privacy.PUBLIC)
    created_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    creator_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    creator = relationship('User', lazy='dynamic')
    maps = relationship('PoolMap', lazy='dynamic', uselist=True)
