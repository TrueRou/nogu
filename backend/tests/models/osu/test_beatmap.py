import pytest
from nogu.app.models.osu.beatmap import BeatmapSrv


@pytest.mark.asyncio
@pytest.mark.skip  # skip this test due to cost of API requests
async def test_beatmap_fetching(db_session):
    beatmap = BeatmapSrv.from_ident(db_session, "4552085")
    assert beatmap is None  # the beatmap is not in the database now.

    beatmap = await BeatmapSrv.request_api(db_session, "4552085")
    assert beatmap is not None  # the beatmap is Rabbit Hole feat. Hatsune Miku

    assert beatmap.artist == "DECO*27"
    assert beatmap.title == "Rabbit Hole feat. Hatsune Miku"
