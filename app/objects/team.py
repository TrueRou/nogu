from typing import Optional

from app.database import db_session
from app.objects.models import Team, Stage


async def get_active_stage(team: Team) -> Optional[Stage]:
    async with db_session() as session:
        return await session.scalar(team.active_stage)
