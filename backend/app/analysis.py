from sqlalchemy import select, update, and_, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, async_object_session as object_session

from app import database
from app.database import engine
from app.interaction import Score, Stage, StageMap, StageMapUser, StageUser, Beatmap

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

def with_primary_key(analysis_dict: dict, **kwargs) -> dict:
    new_dict = {'analysis': analysis_dict}
    for key, item in kwargs.items():
        new_dict[key] = item
    return new_dict


# score: one particular score.
def process_score(score: Score) -> dict:
    beatmap: Beatmap = score.beatmap
    return { 'percentage': score.highest_combo / beatmap.max_combo }


# scores: scores from the same user and the same map.
def process_stage_entry(scores: ScalarResult[Score]) -> dict:
    return { 'play_count': len(scores) }


# scores: scores from different user and the same map.
def process_stage_map(scores: ScalarResult[StageMapUser]) -> dict:
    return { 'play_count': len(scores) }


# scores: scores from the same user and different maps.
def process_stage_user(scores: ScalarResult[StageMapUser]) -> dict:
    return { 'play_count': len(scores) }


# stage: the stage to be processed.
# stage_map: the analysis of each map in the stage.
# stage_user: the analysis of each user in the stage.
def process_stage(stage: Stage, stage_map: dict, stage_user: dict):
    return {}


async def analyze_score(score: Score):
    # score, score_entry: from bottom to top.
    # stage, stage_map, stage_user: from top to bottom.
    score.analysis = await process_score(score)
    await analyze_stage_entry(score.beatmap_md5, score.user_id, score.stage_id)
    await analyze_stage(score.stage)
    
    
async def analyze_stage_entry(session: AsyncSession, beatmap_md5: str, user_id: int, stage_id: int) -> dict:
    condition = and_(Score.beatmap_md5 == beatmap_md5, Score.user_id == user_id, Score.stage_id == stage_id)
    scores = (await session.execute(select(Score).where(condition))).scalars()
    sentence = with_primary_key(await process_stage_entry(scores), stage_id=stage_id, beatmap_md5=beatmap_md5, user_id=user_id)
    await session.execute(update(StageMapUser), sentence)
    
    
async def analyze_stage_map(stage: Stage) -> list[dict]:
    session = object_session(stage)
    sentences = []
    stage_maps = (await session.execute(stage.maps)).scalars()
    for stage_map in stage_maps:
        condition = and_(StageMapUser.stage_id == stage.id, StageMapUser.beatmap_md5 == stage_map.map_md5)
        analysis = (await session.execute(select(StageMapUser).where(condition))).scalars()
        sentences.append(with_primary_key(await process_stage_map(analysis), stage_id=stage.id, map_md5=stage_map.beatmap_md5))
    await session.execute(update(StageMap), sentences)
    return sentences


async def analyze_stage_user(stage: Stage) -> list[dict]:
    session = object_session(stage)
    sentences = []
    for user in stage.team.member:
        condition = and_(StageMapUser.stage_id == stage.id, StageMapUser.user_id == user.id)
        analysis = (await session.execute(select(StageMapUser).where(condition))).scalars()
        sentences.append(with_primary_key(await process_stage_user(analysis), stage_id=stage.id, user_id=user.id))
    await session.execute(update(StageUser), sentences)
    return sentences


async def analyze_stage(stage: Stage):
    stage_map = await analyze_stage_map(stage)
    stage_user = await analyze_stage_user(stage)
    stage.analysis = await process_stage(stage, stage_map, stage_user)


# analyze the scores of a stage from scratch.
async def analyze_scores_scratch(stage: Stage):
    session = object_session(stage)
    scores = await session.scalars(select(Score).where(Score.stage_id == stage.id))  # type: ignore
    stage_maps = (await session.execute(stage.maps)).scalars()
    
    # analyze the scores itself
    sentences = [with_primary_key(await process_score(score), id=score.id) for score in scores]
    await session.execute(update(Score), sentences)
    
    sentences = []
    
    # analyze the scores stage_entry
    for stage_map in stage_maps:
        for user in stage.team.member:
            condition = and_(Score.beatmap_md5 == stage_map.map_md5, Score.user_id == user.id, Score.stage_id == stage_map.stage_id)
            stage_entry_scores = (await session.execute(select(Score).where(condition))).scalars()
            sentences.append(with_primary_key(await process_stage_entry(stage_entry_scores), stage_id=stage.id, beatmap_md5=stage_map.map_md5, user_id=user.id))
    await session.execute(update(StageMapUser), sentences)
    
    
async def analyze_stage_scratch(session: AsyncSession, stage_id: int):
    session = async_session_maker()
    stage = await database.get_model(session, stage_id, Stage)
    # score, score_entry, stage, stage_map, stage_user: from top to bottom.
    await analyze_scores_scratch(session, stage) # revert order in scratch method.
    await analyze_stage_map(stage)
    await analyze_stage_user(stage)
    stage.analysis = await process_stage(stage)