from tests.mock import UserFactory, TeamFactory
from nogu.app.models import TeamUserLink, TeamSrv
from nogu.app import database


def test_team_belongings(db_session):
    # create 10 users and a team
    users = UserFactory.batch(10)
    team = TeamFactory.build()
    database.add_model(db_session, *users, team)

    # add 5 users to the team
    database.add_model(db_session, *[TeamUserLink(team_id=team.id, user_id=user.id) for user in users[:5]])

    # check how many users belong to the team
    member_num = 0
    for user in users:
        if TeamSrv._ensure_role(db_session, team, user)[0]:
            member_num += 1

    assert member_num == 5
