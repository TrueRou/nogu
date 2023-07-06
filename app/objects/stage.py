from typing import Optional

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, text
from sqlalchemy.orm import relationship

from app import database
from app.constants.formulas import Formulas, bancho_formula
from app.constants.privileges import MemberPosition
from app.database import Base, db_session
from app.objects.team import Team
from app.objects.user import User


class StageMap(Base):
    __tablename__ = "stage_maps"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stage_id = Column(Integer, ForeignKey('stages.id'), index=True, nullable=False)
    map_md5 = Column(Text, ForeignKey('beatmaps.md5'), index=True, nullable=False)
    description = Column(Text, nullable=False)
    condition_ast = Column(Text, nullable=False)
    condition_name = Column(Text, nullable=False)
    condition_represent_mods = Column(Integer, nullable=False)

    beatmap = relationship('Beatmap', lazy='selectin')


class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    mode = Column(Integer, nullable=False, default=0)
    formula = Column(Integer, nullable=False, default=bancho_formula.formula_id)
    created_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    pool_id = Column(Integer, ForeignKey('pools.id'), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)

    pool = relationship('Pool', lazy='dynamic')  # originated from which pool
    team = relationship('Team', lazy='dynamic')  # which team owned the stage
    scores = relationship('Score', lazy='dynamic', uselist=True)
    maps = relationship('StageMap', lazy='dynamic', uselist=True)

    @staticmethod
    async def get_stage(oid: int) -> Optional['Stage']:
        async with db_session() as session:
            return await session.get(Stage, oid)

    async def get_stage_map(self, beatmap_md5: str) -> Optional['StageMap']:
        async with db_session() as session:
            return await database.query_model(self.maps, StageMap.map_md5 == beatmap_md5)

    async def position_of(self, user: User) -> MemberPosition:
        async with db_session() as session:
            team: Team = await session.scalar(self.team)
            member: user = await database.query_model(session, team.users, User.id == user.id)
            if member is None:
                return MemberPosition.EMPTY
            return MemberPosition.MEMBER  # TODO: from association
