from nogu.app.database import session_ctx
from nogu.app.models.osu.beatmap import Beatmap
from nogu.app.models.osu.score import Score
from nogu.app.models.osu.stage import Stage, StageMap, StageMapUser, StageUser
from nogu.app.models.team import TeamUserLink
from sqlalchemy import ScalarResult, event, update
from sqlalchemy.orm import object_session
from sqlmodel import Session, select, and_


def _with_PK(analysis_dict: dict, **kwargs) -> dict:
    new_dict = {"analysis": analysis_dict}
    for key, item in kwargs.items():
        new_dict[key] = item
    return new_dict


# score: one particular score.
def _process_score(score: Score, beatmap: Beatmap) -> dict:
    return {"percentage": score.highest_combo / beatmap.max_combo}


# scores: scores from the same user and the same map.
def _process_stage_map_user(scores: ScalarResult[Score]) -> dict:
    return {"play_count": len(list(scores))}


# scores: scores from different user and the same map.
def _process_stage_map(scores: ScalarResult[StageMapUser]) -> dict:
    return {"play_count": len(list(scores))}


# scores: scores from the same user and different maps.
def _process_stage_user(scores: ScalarResult[StageMapUser]) -> dict:
    return {"play_count": len(list(scores))}


# stage: the stage to be processed.
# stage_map: the analysis of each map in the stage.
# stage_user: the analysis of each user in the stage.
def _process_stage(stage: Stage, stage_map: dict, stage_user: dict):
    return {}


def _analyze_stage_map_user(session: Session, beatmap_md5: str, user_id: int, stage_id: int) -> dict:
    condition = and_(Score.beatmap_md5 == beatmap_md5, Score.user_id == user_id, Score.stage_id == stage_id)
    scores = session.scalars(select(Score).where(condition))
    sentence = _with_PK(_process_stage_map_user(scores), stage_id=stage_id, map_md5=beatmap_md5, user_id=user_id)
    session.bulk_update_mappings(StageMapUser, [sentence])


def _analyze_stage_map(session: Session, stage: Stage) -> list[dict]:
    sentences = []
    stage_maps = session.scalars(select(StageMap).where(StageMap.stage_id == stage.id))
    for stage_map in stage_maps:
        condition = and_(StageMapUser.stage_id == stage.id, StageMapUser.map_md5 == stage_map.map_md5)
        analysis = session.scalars(select(StageMapUser).where(condition))
        sentences.append(_with_PK(_process_stage_map(analysis), stage_id=stage.id, map_md5=stage_map.map_md5))
    session.bulk_update_mappings(StageMap, sentences)
    return sentences


def _analyze_stage_user(session: Session, stage: Stage) -> list[dict]:
    sentences = []
    team_member = session.scalars(select(TeamUserLink).where(TeamUserLink.team_id == stage.team_id))
    for relation in team_member:
        condition = and_(StageMapUser.stage_id == stage.id, StageMapUser.user_id == relation.user_id)
        analysis = session.scalars(select(StageMapUser).where(condition))
        sentences.append(_with_PK(_process_stage_user(analysis), stage_id=stage.id, user_id=relation.user_id))
    for sentence in sentences:
        sentence = select(StageUser).where(and_(StageUser.stage_id == sentence["stage_id"], StageUser.user_id == sentence["user_id"]))
    session.bulk_update_mappings(StageUser, sentences)
    return sentences


def _analyze_stage(session: Session, stage: Stage):
    stage_map = _analyze_stage_map(session, stage)
    stage_user = _analyze_stage_user(session, stage)
    stage.analysis = _process_stage(stage, stage_map, stage_user)


# analyze the scores of a stage from scratch.
def _analyze_scores_scratch(session: Session, stage: Stage):
    sentences = []
    stage_maps = session.scalars(select(StageMap).where(StageMap.stage_id == stage.id))
    team_member = session.scalars(select(TeamUserLink).where(TeamUserLink.team_id == stage.team_id))

    # analyze the stage map user.
    for stage_map in stage_maps:
        scores: list[Score] = session.scalars(select(Score).where(and_(Score.stage_id == stage.id, Score.beatmap_md5 == stage_map.map_md5)))
        beatmap = session.get(Beatmap, stage_map.map_md5)
        for score in scores:
            score.analysis = _process_score(score, beatmap)
        session.commit()  # merge the results for the calculation of stage map user.
        for relation in team_member:
            condition = and_(Score.beatmap_md5 == stage_map.map_md5, Score.user_id == relation.user_id, Score.stage_id == stage_map.stage_id)
            scores = session.scalars(select(Score).where(condition))
            sentence = _with_PK(_process_stage_map_user(scores), stage_id=stage.id, map_md5=stage_map.map_md5, user_id=relation.user_id)
            sentences.append(sentence)
    session.exec(update(StageMapUser), sentences)
    session.commit()  # merge the results for the calculation of stage map.


def analyze_score(score_id: int):
    # step1: score, stage_map_user -> from bottom to top.
    # step2: stage_map, stage_user, stage -> from top to bottom.
    with session_ctx() as session:
        score = session.get(Score, score_id)
        beatmap = session.get(Beatmap, score.beatmap_md5)
        stage = session.get(Stage, score.stage_id)
        score.analysis = _process_score(score, beatmap)
        _analyze_stage_map_user(session, score.beatmap_md5, score.user_id, score.stage_id)
        session.commit()  # merge the results of step1 for the calculation of step2.
        _analyze_stage(session, stage)
        session.commit()  # merge the results of step2.


def analyze_stage_scratch(stage_id: int):
    # step1: score, stage_map_user -> from top to bottom.
    # step2: stage_map, stage_user, stage -> from top to bottom.
    with session_ctx() as session:
        stage = session.get(Stage, stage_id)
        _analyze_scores_scratch(session, stage)  # revert order in scratch method.
        stage_maps = _analyze_stage_map(session, stage)
        stage_users = _analyze_stage_user(session, stage)
        stage.analysis = _process_stage(stage, stage_maps, stage_users)
        session.commit()  # merge the results of step2.
