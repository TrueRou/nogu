from typing import Sequence

from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app import database
from app.database import engine
from app.interaction import Score, Stage, StageMap, StageMapUser, StageUser, Beatmap

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def with_primary_key(analysis_dict: dict, **kwargs) -> dict:
    new_dict = {'analysis': analysis_dict}
    for key, item in kwargs.items():
        new_dict[key] = item
    return new_dict


# process: score_detail

async def compute_score(score: Score) -> dict:
    # TODO: real formula
    beatmap: Beatmap = score.beatmap
    return {
        'percentage': score.highest_combo / beatmap.max_combo
    }


async def compute_scores(session: AsyncSession, stage: Stage):
    computed_results = []
    scores = await session.scalars(select(Score).where(Score.stage_id == stage.id))  # type: ignore
    for score in scores:
        computed_result = with_primary_key(await compute_score(score), id=score.id)
        computed_results.append(computed_result)
    await session.execute(update(Score), computed_results)


# process: stage_map_user_detail (smu: stage_map_user)

async def compute_smu_scores(particular_scores: Sequence) -> dict:
    # particular_scores: scores from the same user and beatmap.
    # TODO: real formula
    return {
        'play_count': len(particular_scores)
    }


async def compute_smu_users(session: AsyncSession, stage: Stage, stage_map: StageMap) -> list[dict]:
    computed_results = []
    for user in stage.team.member:
        condition = and_(Score.beatmap_md5 == stage_map.map_md5, Score.user_id == user.id,
                         Score.stage_id == stage_map.stage_id)
        current_scores = (await session.execute(select(Score).where(condition))).fetchall()
        computed_result = with_primary_key(await compute_smu_scores(current_scores), stage_id=stage.id,
                                           beatmap_md5=stage_map.map_md5, user_id=user.id)
        computed_results.append(computed_result)
    return computed_results


async def compute_smu(session: AsyncSession, stage: Stage):
    computed_results = []
    stage_maps = (await session.execute(stage.maps)).scalars().fetchall()
    for stage_map in stage_maps:
        computed_result = await compute_smu_users(session, stage, stage_map)
        computed_results.extend(computed_result)
    await session.execute(update(StageMapUser), computed_results)


# process: stage_map_detail

async def compute_stage_map(particular_scores: Sequence) -> dict:
    # particular_scores: scores from the same beatmap and different users.
    # TODO: real formula
    return {
        'play_count': len(particular_scores)
    }


async def compute_stage_maps(session: AsyncSession, stage: Stage) -> list:
    computed_results = []
    stage_maps = (await session.execute(stage.maps)).scalars().fetchall()
    for stage_map in stage_maps:
        condition = and_(StageMapUser.stage_id == stage.id, StageMapUser.beatmap_md5 == stage_map.map_md5)
        current_scores = (await session.execute(select(StageMapUser).where(condition))).fetchall()
        computed_result = with_primary_key(await compute_stage_map(current_scores), stage_id=stage.id,
                                           map_md5=stage_map.beatmap_md5)
        computed_results.append(computed_result)
    await session.execute(update(StageMap), computed_results)
    return computed_results


# process: stage_user_detail

async def compute_stage_user(particular_scores: Sequence) -> dict:
    # particular_scores: scores from the same user and different maps.
    # TODO: real formula
    return {
        'play_count': len(particular_scores)
    }


async def compute_stage_users(session: AsyncSession, stage: Stage) -> list:
    computed_results = []
    for user in stage.team.member:
        condition = and_(StageMapUser.stage_id == stage.id, StageMapUser.user_id == user.id)
        current_scores = (await session.execute(select(StageMapUser).where(condition))).fetchall()
        computed_result = with_primary_key(await compute_stage_user(current_scores), stage_id=stage.id, user_id=user.id)
        computed_results.append(computed_result)
    await session.execute(update(StageUser), computed_results)
    return computed_results


# process: stage_detail
async def compute_stage(stage: Stage, stage_maps: list[dict], stage_users: list[dict]):
    total_play_count = 0
    for stage_map in stage_maps:
        total_play_count += stage_map.get('play_count')
    computed_result = {
        'play_count': total_play_count
    }  # TODO: real formula
    stage.analysis = computed_result


async def process_async(stage_id: int):
    session = async_session_maker()
    stage: Stage = await database.get_model(session, stage_id, Stage)
    await compute_scores(session, stage)  # score_detail
    await compute_smu(session, stage)  # stage_map_user_detail
    cached_maps = await compute_stage_maps(session, stage)  # stage_map_detail
    cached_users = await compute_stage_users(session, stage)  # stage_user_detail
    await compute_stage(stage, cached_maps, cached_users)  # stage_detail
    await session.commit()
