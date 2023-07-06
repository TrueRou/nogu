from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.constants.privileges import MemberPosition
from app.database import Base


class TeamMember(Base):
    __tablename__ = "team_member"
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey('teams.id'), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
    member_position = Column(Integer, nullable=False, default=MemberPosition.MEMBER)

    teams = relationship("Team", back_populates="member")
    member = relationship("User", back_populates="teams")
