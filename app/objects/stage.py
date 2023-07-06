from typing import Optional

from app import database
from app.constants.privileges import MemberPosition
from app.database import db_session
from app.objects.models import Stage, StageMap, User


async def get_stage(oid: int) -> Optional[Stage]:
    async with db_session() as session:
        return await session.get(Stage, oid)


async def get_stage_map(self, beatmap_md5: str) -> Optional[StageMap]:
    async with db_session() as session:
        return await database.query_model(session, self.maps, StageMap.map_md5 == beatmap_md5)


async def position_of(self, user_id: int) -> MemberPosition:
    async with db_session() as session:
        team = await session.scalar(self.team)
        member = await database.query_model(session, team.users, User.id == user_id)
        if member is None:
            return MemberPosition.EMPTY
        return MemberPosition.MEMBER  # TODO: from association
