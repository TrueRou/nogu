from typing import Optional

from app.database import db_session
from app.objects.models import User, Team, Stage


async def get_active_team(user: User) -> Optional[Team]:
    async with db_session() as session:
        return await session.scalar(user.active_team)


async def get_active_stage(user: User) -> Optional[Stage]:
    team = await user.get_active_team()
    return await team.get_active_stage() if team else None
