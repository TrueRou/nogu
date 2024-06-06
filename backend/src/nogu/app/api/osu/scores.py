from typing import Any

from fastapi import APIRouter, Depends
from ossapi import MatchResponse, MatchEvent, OssapiAsync
from sqlmodel import select

from nogu import config
from nogu.app.api.users import require_user
from nogu.app.models.osu import *
from nogu.app.models.user import User
from nogu.app.constants.osu import Server
from nogu.app.database import auto_session
from nogu.app.constants.exceptions import glob_not_belongings
from nogu.app.objects import Inspector

router = APIRouter(prefix="/scores", tags=["scores"])


@router.get("/{score_id}", response_model=Score)
async def get_score(score_id: int, user: User = Depends(require_user)):
    with auto_session() as session:
        score = session.get(Score, score_id)
        if ScoreSrv.check_score_visibility(session, score, user):
            raise glob_not_belongings
    return score


@router.post("/", response_model=Score)
async def submit_score(score: ScoreBase, user: User = Depends(require_user)):
    with auto_session() as session:
        score = ScoreSrv.submit_score(session, score, user)
    return score


@router.post("/partial/", response_model=Score)
async def submit_score_partial(keywords: str, beatmap_md5: str, user: User = Depends(require_user)):
    with auto_session() as session:
        score = ScoreSrv.submit_partial(session, keywords, beatmap_md5, user)
    return score


class BanchoMatchInspector(Inspector):
    def __init__(self, interval: float, each_interval: float):
        super().__init__(interval, each_interval)
        self.api_client = OssapiAsync(config.osu_api_v2_id, config.osu_api_v2_secret)

    async def consume(self, target: Any) -> int:
        match: MatchResponse = await self.api_client.match(target)
        if match.match.end_time is not None:
            self.remove_target(target)
        for event in match.events:
            await self.resulting(target, event.id, event)
        return match.latest_event_id

    async def process_result(self, target: Any, event: MatchEvent):
        with auto_session() as session:
            if event.game is None or event.game.scores is None:
                return
            for score in event.game.scores:
                # find the user if he created user_accounts in our database.
                sentence = select(User).join(UserAccount).where(UserAccount.su_id == score.user_id, UserAccount.osu_server == Server.BANCHO)
                user = session.exec(sentence).first()
                if user is not None:
                    ScoreSrv.submit_inspected(session, score, user)


bancho_match_inspector = BanchoMatchInspector(
    interval=config.match_inspection_interval,
    each_interval=config.match_inspection_each_interval,
)


@router.post("/inspect/bancho/{match_id}")
async def inspect_bancho_match(match_id: int):
    bancho_match_inspector.new_target(match_id)
