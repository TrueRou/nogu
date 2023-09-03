from typing import Any

from fastapi import APIRouter, Depends
from ossapi import MatchResponse, MatchEvent
from sqlalchemy.ext.asyncio import AsyncSession

import config
from app.api.schemas import APIResponse, docs, APIException
from app.api.schemas.score import ScoreBase, ScoreRead
from app.api.users import current_user
from app.constants.servers import Server
from app.database import db_session as database_session
from app.definition import Inspector
from app.interaction import User, Score, Beatmap
from app.sessions import api_client

router = APIRouter(prefix='/scores', tags=['scores'])


async def require_score(score_id: int, session: AsyncSession = Depends(database_session), user: User = Depends(current_user)):
    score = await Score.from_id(session, score_id)
    if score is None:
        raise APIException(info="Score not found.")
    if score.user_id != user.id:
        raise APIException(info="No permission.")
    return score


@router.post('/', responses=docs(ScoreRead))
async def submit_score(info: ScoreBase, user: User = Depends(current_user),
                       session: AsyncSession = Depends(database_session)):
    stage = user.active_stage
    stage_map = await stage.get_map(info.beatmap_md5)
    if stage and stage_map:
        score = await Score.conditional_submit(session, info.dict(), stage, stage_map.condition_ast)
        return APIResponse(score=score)


class BanchoMatchInspector(Inspector):
    async def consume(self, target: Any) -> int:
        match: MatchResponse = await api_client.match(target)
        if match.match.end_time is not None:
            self.remove_target(target)
        for event in match.events:
            await self.resulting(target, event.id, event)
        return match.latest_event_id

    async def process_result(self, target: Any, event: MatchEvent):
        async with database_session() as db_session:
            for score in event.game.scores:
                user = await User.from_id(db_session, score.user_id, Server.BANCHO)
                if user is not None:
                    beatmap = await Beatmap.from_id(db_session, event.game.beatmap_id)
                    if beatmap is not None:
                        await submit_score(ScoreBase.from_ossapi(score, beatmap.md5, user.id), user)
            await db_session.commit()


bancho_match_inspector = BanchoMatchInspector(interval=config.match_inspection_interval,
                                              each_interval=config.match_inspection_each_interval)


@router.get('/{score_id}', responses=docs(ScoreRead))
async def get_score(score: Score = Depends(require_score)):
    return APIResponse(beatmap=ScoreRead.from_orm(score))


@router.post('/make/', responses=docs(ScoreRead))
async def make_score(keywords: str, beatmap_md5: str, user: User = Depends(current_user)):
    stage = user.active_stage
    stage_map = await stage.get_map(beatmap_md5)
    if stage and stage_map:
        fake_score = ScoreBase.from_abs(beatmap_md5, user.id, keywords, stage_map.beatmap.max_combo,
                                        stage_map.condition_represent_mods, stage.mode)
        return APIResponse(score=await submit_score(fake_score, user))


@router.post('/inspect/bancho/{match_id}')
async def inspect_bancho_match(match_id: int):
    bancho_match_inspector.new_target(match_id)
