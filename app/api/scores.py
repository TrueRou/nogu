from fastapi import APIRouter, Depends

from .schemas.scores import ScoreBase, ScoreRead
from .users import current_user
from ..database import db_session
from ..interaction import User, Score

router = APIRouter(prefix='/scores', tags=['scores'])


@router.post('/', response_model=ScoreRead)
async def submit_score(info: ScoreBase, user: User = Depends(current_user)):
    stage = user.active_stage
    stage_map = await stage.get_map(info.beatmap_md5)
    if stage and stage_map:
        async with db_session() as session:
            score_raw = Score.from_web(info.dict(), stage)
            return await score_raw.submit_raw(score_raw, session, stage_map.condition_ast)


@router.get('/{score_id}', response_model=ScoreRead)
async def get_score(score_id: int):
    async with db_session() as session:
        return await Score.from_id(session, score_id)


# TODO: move to stages api
@router.post('/make', response_model=ScoreRead)
async def make_score(keywords: str, beatmap_md5: str, user: User = Depends(current_user)):
    stage = user.active_stage
    stage_map = await stage.get_map(beatmap_md5)
    if stage and stage_map:
        fake_score = ScoreBase.from_abs(beatmap_md5, user.id, keywords, stage_map.beatmap.max_combo,
                                        stage_map.condition_represent_mods, stage.mode)
        return await submit_score(fake_score, user)
