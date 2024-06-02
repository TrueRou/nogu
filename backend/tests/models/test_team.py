from tests.mock import UserFactory, TeamFactory


def test_team_belongings(db_session):
    db_session.add_all(UserFactory.batch(10))
    db_session.add(TeamFactory.build())
    db_session.commit()
