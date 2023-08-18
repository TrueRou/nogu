from fastapi import APIRouter, Depends

from .schemas import APIResponse, docs
from .schemas.score import ScoreBase, ScoreRead
from .users import current_user
from ..database import db_session
from ..interaction import User, Score

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
    stage = user.active_stage
    stage_map = await stage.get_map(info.beatmap_md5)
    if stage and stage_map:
        async with db_session() as session:
            score_raw = Score.from_web(info.dict(), stage)
            return APIResponse(score=await score_raw.submit_raw(score_raw, session, stage_map.condition_ast))


# TODO: move to stages api
@router.post('/make/', responses=docs(ScoreRead))
async def make_score(keywords: str, beatmap_md5: str, user: User = Depends(current_user)):
    stage = user.active_stage
    stage_map = await stage.get_map(beatmap_md5)
    if stage and stage_map:
        fake_score = ScoreBase.from_abs(beatmap_md5, user.id, keywords, stage_map.beatmap.max_combo,
                                        stage_map.condition_represent_mods, stage.mode)
        return APIResponse(score=await submit_score(fake_score, user))
