import ast
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_
from starlette import status

import services
from app import schemas, models
from app.users import current_user, current_stage, get_stage
from services import db_session

scores_router = APIRouter(prefix='/scores', tags=['scores'])


@scores_router.post('/', response_model=schemas.ScoreBase)
async def upload_score(score: schemas.ScoreCreate, user=Depends(current_user), stage=Depends(current_stage)):
    async with db_session() as session:
        condition = and_(models.StageMap.stage_id == stage.id, models.StageMap.map_md5 == score.map_md5)
        stage_maps = await services.select_models(session, models.StageMap, condition)
        variables = {
            "acc": score.accuracy,
            "max_combo": score.max_combo,
            "mods": score.mods,
            "count_300": score.count_300,
            "count_100": score.count_100,
            "count_50": score.count_50,
            "count_miss": score.count_miss,
        }
        for stage_map in stage_maps:
            try:
                namespace = {}
                namespace.update(variables)
                tree = ast.parse(stage_map.condition_ast, mode='eval')
                if eval(compile(tree, filename='<ast>', mode='eval'), namespace):
                    obj = models.Score(**score.dict(), user_id=user.id, stage_id=stage.id)
                    await services.add_model(session, obj)
                    break
            except SyntaxError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Wrong condition ast syntax.',
                )


@scores_router.post('/abstract', response_model=schemas.ScoreBase)
async def upload_score_abstract(beatmap_md5: str, mods: int, description: str, user=Depends(current_user),
                                stage=Depends(get_stage)):
    async with db_session() as session:
        beatmap = await services.get_model(session, beatmap_md5, models.Beatmap)
        data = description.split()
        # 5miss 96.5acc 600c 100w
        for item in data:
            if item.endswith("miss"):
                miss = int(item[:-4])
            elif item.endswith("acc"):
                acc = float(item[:-3])
            elif item.endswith("c"):
                combo = int(item[:-1])
            elif item.endswith("w"):
                score = float(item[:-1]) * 10000.0
        n300 = beatmap.max_combo - miss
        numerator = (acc * 300 * (miss + n300)) - (300 * n300)
        denominator = 100 - acc
        n100 = numerator / denominator
        score = models.Score(stage_id=stage.id, server_id=0, user_id=user.id, map_md5=beatmap_md5, accuracy=acc,
                             max_combo=combo, mode_int=stage.ruleset, mods=mods, score=score, count_miss=miss,
                             count_50=0, count_100=n100, count_300=n300)
        await services.add_model(session, score)


@scores_router.get('', response_model=list[schemas.ScoreFull])
async def get_scores(score_id: Optional[int], stage_id: Optional[int], user=Depends(current_user)):
    async with db_session() as session:
        if not score_id:
            score = await services.get_model(session, score_id, models.Score)
            return [score]
        if not stage_id:
            user_stage = await get_stage(stage_id, user)
            scores = await services.query_models(session, user_stage.scores)
            return scores.all()

