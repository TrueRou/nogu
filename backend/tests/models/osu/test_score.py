from nogu.app.analysis.osu import analyze_score
from nogu.app.models.osu.score import Score, ScoreSrv
from nogu.app.models.team import TeamVisibility
import pytest
from tests.mock import AstConditionFactory, BeatmapFactory, ScoreBaseFactory, ScoreFactory, StageFactory, StageMapFactory, UserFactory, TeamFactory
from nogu.app.models import TeamUserLink
from nogu.app import database


def test_score_visibility(db_session):
    # create 2 users, 2 beatmaps and a team
    users = UserFactory.batch(2)
    team = TeamFactory.build(visibility=TeamVisibility.PRIVATE.value)
    beatmap = BeatmapFactory.batch(2)

    database.add_model(db_session, *users, *beatmap, team)

    # add one user and one stage to the team
    database.add_model(db_session, TeamUserLink(team_id=team.id, user_id=users[0].id))
    stage = StageFactory.build(team_id=team.id)
    database.add_model(db_session, stage)

    # add one stage beatmap to the stage
    ast_condition = AstConditionFactory.build(user_id=users[0].id)
    database.add_model(db_session, ast_condition)
    stage_map = StageMapFactory.build(stage_id=stage.id, map_md5=beatmap[0].md5, condition_id=ast_condition.id)
    database.add_model(db_session, stage_map)

    # upload a score for user 0
    score = ScoreFactory.build(user_id=users[0].id, stage_id=stage.id, beatmap_md5=beatmap[0].md5)
    database.add_model(db_session, score)

    # can the user (user 0) see the score now? yes!
    assert ScoreSrv._ensure_visibility(db_session, score, users[0])[0] == True

    # can the other user (user 1) see the score now? no!
    assert ScoreSrv._ensure_visibility(db_session, score, users[1])[0] == False

    # add user 1 to the team, can he see the score now? yes!
    database.add_model(db_session, TeamUserLink(team_id=team.id, user_id=users[1].id))
    assert ScoreSrv._ensure_visibility(db_session, score, users[1])[0] == True

    # add user 0 to another team, and set a score there
    team1 = TeamFactory.build(visibility=TeamVisibility.PRIVATE.value)
    database.add_model(db_session, team1)
    stage1 = StageFactory.build(team_id=team1.id)
    database.add_model(db_session, stage1, TeamUserLink(team_id=team1.id, user_id=users[0].id))
    stage_map1 = StageMapFactory.build(stage_id=stage1.id, map_md5=beatmap[1].md5, condition_id=ast_condition.id)
    score1 = ScoreFactory.build(user_id=users[0].id, stage_id=stage1.id, beatmap_md5=beatmap[1].md5)
    database.add_model(db_session, stage_map1, score1)

    # what if user 0 set a score in another team, can user 1 access it? no!
    assert ScoreSrv._ensure_visibility(db_session, score1, users[1])[0] == False

    # make the team public, can all the users see all the scores now? yes!
    team.visibility = TeamVisibility.PUBLIC
    team1.visibility = TeamVisibility.PUBLIC
    db_session.commit()

    users = [*users, *UserFactory.batch(10)]
    database.add_model(db_session, *users)

    for user in users:
        assert ScoreSrv._ensure_visibility(db_session, score, user)[0] == True
        assert ScoreSrv._ensure_visibility(db_session, score1, user)[0] == True


@pytest.mark.asyncio
async def test_score_submit(db_session):
    user = UserFactory.build()
    user2 = UserFactory.build()
    beatmap = BeatmapFactory.build()
    beatmap2 = BeatmapFactory.build()
    team = TeamFactory.build(active=True)
    database.add_model(db_session, beatmap, beatmap2, team, user, user2)

    ast = AstConditionFactory().build(ast_expression="acc > 90", user_id=user.id)
    database.add_model(db_session, ast)
    stage = StageFactory.build(team_id=team.id)
    database.add_model(db_session, stage)
    stage_map = StageMapFactory.build(stage_id=stage.id, map_md5=beatmap.md5, condition_id=ast.id)
    database.add_model(db_session, stage_map)
    user_team = TeamUserLink(team_id=team.id, user_id=user.id)
    database.add_model(db_session, user_team)

    score1 = ScoreBaseFactory.build(user_id=user.id, beatmap_md5=beatmap.md5, accuracy=80.0)
    score2 = ScoreBaseFactory.build(user_id=user.id, beatmap_md5=beatmap.md5, accuracy=95.0)
    score3 = ScoreBaseFactory.build(user_id=user.id, beatmap_md5=beatmap2.md5, accuracy=100.0)
    score4 = ScoreBaseFactory.build(user_id=user2.id, beatmap_md5=beatmap.md5, accuracy=95.0)
    score5 = ScoreBaseFactory.build(user_id=user.id, beatmap_md5=beatmap.md5, accuracy=95.0)

    score1: Score = ScoreSrv.submit_score(db_session, score1, user)
    score2: Score = ScoreSrv.submit_score(db_session, score2, user)
    score3: Score = ScoreSrv.submit_score(db_session, score3, user)
    score4: Score = ScoreSrv.submit_score(db_session, score4, user2)
    score5: Score = ScoreSrv.submit_score(db_session, score5, user)

    assert score3.stage_id == None  # stage map ×
    assert score1.stage_id == None  # stage map √ condition ×
    assert score4.stage_id == None  # stage map √ condition √ user ×
    assert score2.stage_id == stage.id  # stage map √ condition √ user √

    analyze_score(score2.id)
