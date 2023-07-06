from typing import Optional

from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, Text, text
from sqlalchemy.orm import relationship

from app.constants.privacy import Privacy
from app.database import Base, db_session
from app.objects.stage import Stage


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    privacy = Column(Integer, nullable=False, default=Privacy.PROTECTED)
    achieved = Column(Boolean, nullable=False, default=False)
    create_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    finish_at = Column(DateTime(True), nullable=True)
    active_stage_id = Column(Integer, ForeignKey('stages.id'), nullable=True)

    active_stage = relationship('Stage', lazy='dynamic')
    member = relationship('TeamMember', lazy='dynamic', back_populates="teams")
    stages = relationship('Stage', lazy='dynamic')

    async def get_active_stage(self) -> Optional[Stage]:
        async with db_session() as session:
            return await session.scalar(self.active_stage)
