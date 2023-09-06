from multiprocessing import Pool, Queue
from typing import Sequence

from sqlalchemy import select, create_engine, update, and_
from sqlalchemy.orm import sessionmaker, Session

import config
from app.interaction import Score, Stage, StageMap, StageMapUser, StageUser

pool = Pool(4)
analyze_task_queue: Queue[int] = Queue()
analyze_response_queue: Queue[int] = Queue()

engine = create_engine(config.mysql_url, echo=False, future=True)
session_maker = sessionmaker(engine, expire_on_commit=False)


def with_primary_key(analysis_dict: dict, **kwargs) -> dict:
    new_dict = {'analysis': analysis_dict}
    for key, item in kwargs:
        new_dict[key] = item
    return new_dict


# process: score_detail

def compute_score(score: Score) -> dict:
    # TODO: real formula
    return {}


def compute_scores(session: Session, stage: Stage):
    computed_results = []
    scores = session.scalars(select(Score).where(Score.stage_id == stage.id))  # type: ignore
    for score in scores:
        computed_result = with_primary_key(compute_score(score), id=score.id)
        computed_results.append(computed_result)
    session.execute(update(Score), computed_results)


# process: stage_map_user_detail (smu: stage_map_user)

def compute_smu_scores(particular_scores: Sequence) -> dict:
    # particular_scores: scores from the same user and beatmap.
    # TODO: real formula
    return {}


def compute_smu_users(session: Session, stage: Stage, stage_map: StageMap) -> list[dict]:
    computed_results = []
    for user in stage.team.member:
        condition = and_(Score.beatmap_md5 == stage_map.map_md5, Score.user_id == user.id,
                         Score.stage_id == stage_map.stage_id)
        current_scores = session.execute(select(Score).where(condition)).fetchall()
        computed_result = with_primary_key(compute_smu_scores(current_scores), stage_id=stage.id,
                                           beatmap_md5=stage_map.map_md5, user_id=user.id)
        computed_results.append(computed_result)
    return computed_results


def compute_smu(session: Session, stage: Stage):
    computed_results = []
    stage_maps = session.execute(stage.maps).scalars().fetchall()
    for stage_map in stage_maps:
        computed_result = compute_smu_users(session, stage, stage_map)
        computed_results.extend(computed_result)
    session.execute(update(StageMapUser), computed_results)


# process: stage_map_detail

def compute_stage_map(particular_scores: Sequence) -> dict:
    # particular_scores: scores from the same beatmap and different users.
    # TODO: real formula
    return {}


def compute_stage_maps(session: Session, stage: Stage) -> list:
    computed_results = []
    stage_maps = session.execute(stage.maps).scalars().fetchall()
    for stage_map in stage_maps:
        condition = and_(StageMapUser.stage_id == stage.id, StageMapUser.beatmap_md5 == stage_map.map_md5)
        current_scores = session.execute(select(StageMapUser).where(condition)).fetchall()
        computed_result = with_primary_key(compute_stage_map(current_scores), stage_id=stage.id,
                                           map_md5=stage_map.beatmap_md5)
        computed_results.append(computed_result)
    session.execute(update(StageMap), computed_results)
    return computed_results


# process: stage_user_detail

def compute_stage_user(particular_scores: Sequence) -> dict:
    # particular_scores: scores from the same user and different maps.
    # TODO: real formula
    return {}


def compute_stage_users(session: Session, stage: Stage) -> list:
    computed_results = []
    for user in stage.team.member:
        condition = and_(StageMapUser.stage_id == stage.id, StageMapUser.user_id == user.id)
        current_scores = session.execute(select(StageMapUser).where(condition)).fetchall()
        computed_result = with_primary_key(compute_stage_user(current_scores), stage_id=stage.id, user_id=user.id)
        computed_results.append(computed_result)
    session.execute(update(StageUser), computed_results)
    return computed_results


# process: stage_detail
def compute_stage(session: Session, stage: Stage, stage_maps: list[dict], stage_users: list[dict]):
    # particular_scores: scores from the same user and different maps.
    computed_result = {}  # TODO: real formula
    stage.analysis = computed_result
    session.commit()


def analyze_task(analysis_requests: Queue[int]):
    while True:
        stage_id = analysis_requests.get()
        with session_maker() as session:
            stage = session.get(Stage, stage_id)
            compute_scores(session, stage)  # score_detail
            compute_smu(session, stage)  # stage_map_user_detail
            cached_maps = compute_stage_maps(session, stage)  # stage_map_detail
            cached_users = compute_stage_users(session, stage)  # stage_user_detail
            compute_stage(session, stage, cached_maps, cached_users)  # stage_detail
            analyze_response_queue.put(stage_id)


def begin_analyze():
    for i in range(5):
        pool.apply_async(analyze_task, args=(analyze_task_queue,))
    pool.close()
    pool.join()
