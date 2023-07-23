from typing import Optional

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app import definition
from app.api.schemas.beatmaps import BeatmapRead
from app.database import db_session
from app.interaction import Beatmap

router = APIRouter(prefix='/beatmaps')


async def _fetch_single_beatmap(session: AsyncSession, ident: str) -> Optional[Beatmap]:
    if ident.isnumeric():
        return await Beatmap.from_id(session, int(ident))
    if definition.MD5_PATTERN.match(ident):
        return await Beatmap.from_md5(session, ident)


@router.post('/{ident}', response_model=BeatmapRead)
async def get_beatmap(ident: str):
    async with db_session() as session:
        return _fetch_single_beatmap(session, ident)
