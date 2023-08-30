from typing import Any

from fastapi import APIRouter, Depends
from ossapi import MatchResponse, MatchEvent
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import APIResponse, docs
from app.api.schemas.score import ScoreBase, ScoreRead
from app.api.users import current_user
from app.constants.servers import Server
from app.database import db_session, async_session_maker
from app.definition import Inspector
from app.interaction import User, Score, Beatmap
from app.sessions import api_client


async def _submit_score(info: ScoreBase, user: User = Depends(current_user)):
    stage = user.active_stage
    stage_map = await stage.get_map(info.beatmap_md5)
    if stage and stage_map:
        async with db_session() as session:
            score_raw = Score.from_web(info.dict(), stage)
            return APIResponse(score=await score_raw.submit_raw(score_raw, session, stage_map.condition_ast))


class BanchoMatchInspector(Inspector):
    db_session: AsyncSession = async_session_maker()

    async def consume(self, target: Any) -> int:
        match: MatchResponse = await api_client.match(target)
        if match.match.end_time is not None:
            self.remove_target(target)
        for event in match.events:
            await self.resulting(target, event.id, event)
        return match.latest_event_id

    async def process_result(self, target: Any, event: MatchEvent):
        for score in event.game.scores:
            user = await User.from_id(self.db_session, score.user_id, Server.BANCHO)
            if user is not None:
                beatmap = await Beatmap.from_id(self.db_session, event.game.beatmap_id)
                if beatmap is not None:
                    await _submit_score(ScoreBase.from_ossapi(score, beatmap.md5, user.id), user)
        await self.db_session.commit()


router = APIRouter(prefix='/scores', tags=['scores'])


@router.get('/{score_id}', responses=docs(ScoreRead))
async def get_score(score_id: int):
    async with db_session() as session:
        score = await Score.from_id(session, score_id)
        if score is None:
            return APIResponse(success=False, info="Score not found.")
        return APIResponse(beatmap=ScoreRead.from_orm(score))


@router.post('/', responses=docs(ScoreRead))
async def submit_score(info: ScoreBase, user: User = Depends(current_user)):
    await _submit_score(info, user)


# TODO: move to stages api
@router.post('/make/', responses=docs(ScoreRead))
async def make_score(keywords: str, beatmap_md5: str, user: User = Depends(current_user)):
    stage = user.active_stage
    stage_map = await stage.get_map(beatmap_md5)
    if stage and stage_map:
        fake_score = ScoreBase.from_abs(beatmap_md5, user.id, keywords, stage_map.beatmap.max_combo,
                                        stage_map.condition_represent_mods, stage.mode)
        return APIResponse(score=await submit_score(fake_score, user))
