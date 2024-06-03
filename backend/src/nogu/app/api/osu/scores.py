from typing import Any

from fastapi import APIRouter, Depends
from ossapi import MatchResponse, MatchEvent, OssapiAsync
from sqlmodel import select

from nogu import config
from nogu.app.api.users import require_user
from nogu.app.models.osu import *
from nogu.app.models.user import User
from nogu.app.constants.osu import Server
from nogu.app.database import auto_session, manual_session
from nogu.app.constants.exceptions import glob_not_belongings
from nogu.app.objects import AstChecker, Inspector

router = APIRouter(prefix="/scores", tags=["scores"])


@router.post("/", response_model=Score)
def submit_score(score: ScoreBase, user: User = Depends(require_user)):
    with manual_session() as session:
        # try to get the stage map of the user active team.
        sentence = select(StageMap).join(Stage).where(Stage.team_id == user.active_team_id).where(StageMap.map_md5 == score.beatmap_md5)
        stage_map = session.exec(sentence).first()
        if stage_map is not None:
            # check if the score is valid for the stage map condition.
            ast_expression = stage_map.condition.ast_expression
            variables = {
                "acc": score.accuracy,
                "max_combo": score.highest_combo,
                "mods": score.mods,
                "score": score.score,
            }
            if AstChecker(ast_expression).check(variables):
                db_score = Score(**score.model_dump(), full_combo=True, grade="S")  # TODO: full combo and grade calculation
                session.add(db_score)  # TODO: calculate for performance points
                session.commit()
                session.refresh(db_score)
                return db_score


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
                    beatmap = BeatmapSrv.from_ident(session, event.game.beatmap_id)
                    if beatmap is not None:
                        submit_score(ScoreBase.from_ossapi(score, beatmap.md5, user.id), user)


bancho_match_inspector = BanchoMatchInspector(
    interval=config.match_inspection_interval,
    each_interval=config.match_inspection_each_interval,
)


@router.get("/{score_id}", response_model=Score)
async def get_score(score_id: int, user: User = Depends(require_user)):
    with auto_session() as session:
        score = session.get(Score, score_id)
        if ScoreSrv.check_score_visibility(session, score, user):
            raise glob_not_belongings
    return score


@router.post("/partial/", response_model=Score)
async def submit_score_partial(keywords: str, beatmap_md5: str, user: User = Depends(require_user)):
    with auto_session() as session:
        sentence = (
            select(StageMap, Beatmap, Stage)
            .join(Stage)
            .join(Beatmap)
            .where(Stage.team_id == user.active_team_id)
            .where(StageMap.map_md5 == beatmap_md5)
        )
        tuple = session.exec(sentence).first()

        if tuple:
            (stage_map, beatmap, stage) = tuple
            
            data = keywords.split()  # 5miss 96.5acc 600c 100w
            miss = 0
            acc = 100.0
            combo = beatmap.max_combo
            score = 1000000
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
            fake_score = ScoreBase(
                user_id=user.id,
                beatmap_md5=beatmap_md5,
                score=score,
                accuracy=acc,
                highest_combo=combo,
                mods=stage_map.represent_mods,
                num_300s=n300,
                num_100s=n100,
                num_misses=miss,
                num_gekis=0,
                num_katus=0,
                num_50s=0,
                ruleset=stage.ruleset,
                osu_server=Server.LOCAL,
                stage_id=stage.id,
            )

            return submit_score(fake_score, user)


@router.post("/inspect/bancho/{match_id}")
async def inspect_bancho_match(match_id: int):
    bancho_match_inspector.new_target(match_id)
