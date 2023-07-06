from typing import Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, text
from sqlalchemy.orm import relationship

from app.database import Base, db_session
from app.objects.stage import Stage, StageMap
from app.objects.team import Team


class UserAccount(Base):
    __tablename__ = "user_accounts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), index=True, nullable=False)
    server_id = Column(Integer, nullable=False)
    server_user_id = Column(Integer, nullable=False)
    server_user_name = Column(Text, nullable=False)
    checked_at = Column(DateTime(True), nullable=False, server_default=text("now()"))


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    username = Column(Text, nullable=False, unique=True)
    privileges = Column(Integer, nullable=False)
    country = Column(Text, nullable=False)
    created_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    active_team_id = Column(Integer, ForeignKey('teams.id'), nullable=True)

    accounts = relationship('UserAccount', lazy='selectin', uselist=True)
    active_team = relationship('Team', lazy='dynamic')
    teams = relationship('TeamMember', lazy='dynamic', back_populates="member")

    async def get_active_team(self) -> Optional[Team]:
        async with db_session() as session:
            return await session.scalar(self.active_team)

    async def get_active_stage(self) -> Optional[Stage]:
        team = await self.get_active_team()
        return await team.get_active_stage() if team else None

