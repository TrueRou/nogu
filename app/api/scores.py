from fastapi import APIRouter, Depends

from .schemas.scores import ScoreBase, ScoreRead
from .users import current_user
from ..interaction import User, Score

router = APIRouter(prefix='/scores')


@router.post('/', response_model=ScoreRead)
async def submit_score(info: ScoreBase, user: User = Depends(current_user)):
    stage = await user.get_active_stage()
    stage_map = await stage.get_stage_map(info.beatmap_md5)
    if stage and stage_map:
        return await Score.web_submit(info.dict(), stage_map.condition_ast, stage)


@router.post('/{score_id}', response_model=ScoreRead)
async def get_score(score_id: int):
    return await Score.get_score(score_id)


# TODO: move to stages api
@router.post('/make', response_model=ScoreRead)
async def make_score(keywords: str, beatmap_md5: str, user: User = Depends(current_user)):
    stage = await user.get_active_stage()
    stage_map = await stage.get_stage_map(beatmap_md5)
    if stage and stage_map:
        fake_score = ScoreBase.from_abs(beatmap_md5, user.id, keywords, stage_map.beatmap.max_combo,
                                        stage_map.condition_represent_mods, stage.mode)
        return await Score.web_submit(fake_score.dict(), stage_map.condition_ast, stage)
