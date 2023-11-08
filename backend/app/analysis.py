from redis.commands.json.path import Path
from redis import Redis
from redis.client import Pipeline
from redis.commands.search.query import Query

from sqlalchemy.ext.asyncio import async_object_session as AsyncSession, async_sessionmaker

from app import database
from app.database import engine, redis
from app.interaction import Score, Stage
from app.api.schemas.score import ScoreAnalysis
from app.api.schemas.beatmap import BeatmapAnalysis

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

def _fetch_scores(condition: str) -> list[int]:
    query = Query(condition).return_field('$.id', as_field='score_id').paging(0, 0)
    documents = redis.ft('scores').search(query).docs
    return [document.score_id for document in documents]

def _fetch_score(score_id: int) -> ScoreAnalysis:
    return redis.json().get(f'score:{score_id}', Path.root_path())

def _renew_stage(pipeline: Redis | Pipeline, stage_id: int):
    pipeline.set(f'stage:{stage_id}', 'active')
    pipeline.expire(f'stage:{stage_id}', 60 * 60 * 24)

def _push_score(pipeline: Redis | Pipeline, score: Score):
    beatmap_dict = BeatmapAnalysis.from_orm(score.beatmap).dict()
    score_dict = ScoreAnalysis.from_orm(score).dict()
    pipeline.json().set(f'score:{score.id}', Path.root_path(), score_dict)
    pipeline.set(f'beatmap:{score.beatmap_md5}', beatmap_dict)

# call this function on every score insert.
async def insert_score(score: Score):
    pipeline = redis.pipeline()
    beatmap_dict = BeatmapAnalysis.from_orm(score.beatmap).dict()
    score_dict = ScoreAnalysis.from_orm(score).dict()
    if (not redis.exists(f'stage:{score.stage_id}')):
        # the stage is recycled by redis (also the scores we need), we need to refresh it.
        # when redis data is lost, we need to refresh the stage.
        await refresh_stage(score.stage_id)
    pipeline.json().set(f'score:{score.id}', Path.root_path(), score_dict) # cache the score (we always have the full scores of the stage)
    pipeline.set(f'beatmap:{score.beatmap_md5}', beatmap_dict) # cache the beatmap (keep every beatmaps of the stage in redis)
    _renew_stage(pipeline, score.stage_id) # renew the stage (keep the stage in redis for 24 hours)
    pipeline.execute()
    analyze_score(score.id) # analyze the score (from bottom to upper)
    await analyze_stage(score.stage_id) # analyze the stage (from upper to bottom)
    
    
async def refresh_stage(stage_id: int):
    session = async_session_maker()
    pipeline = redis.pipeline()
    scores = await database.select_models(session, Score, Score.stage_id == stage_id)
    for score in scores:
        _push_score(pipeline, score)
    pipeline.execute()
    await session.commit()


def process_score(score: ScoreAnalysis, beatmap: BeatmapAnalysis) -> dict:
    return {
        'percentage': score.highest_combo / beatmap.max_combo
    }
    
    
def process_stage(stage: Stage, stage_maps: list[dict], stage_users: list[dict]) -> dict:
    pass
    

# score cache must be existed when we call this mannually.
async def analyze_score(pipeline: Redis | Pipeline, score_id: int):
    score: ScoreAnalysis = _fetch_score(score_id)
    beatmap = BeatmapAnalysis.parse_obj(await redis.get(f'beatmaps:{score.beatmap_md5}'))
    analysis = process_score(score, beatmap)
    pipeline.json().set(f'analysis:score:{score_id}', Path.root_path(), analysis)


# usually, we do not call this method mannually.
async def analyze_scores(stage_id: int):
    pipeline = redis.pipeline()
    for score_id in _fetch_scores(f'@stage_id:[{stage_id} {stage_id}]'):
        analyze_score(pipeline, stage_id, score_id)
    pipeline.execute()

async def analyze_stage(stage_id: int):
    session = async_session_maker()
    stage: Stage = await database.get_model(session, stage_id, Stage)
    stage_maps = []
    stage_users = []
    analysis = process_stage(stage, stage_maps, stage_users)
    redis.json().set(f'analysis:stage:{stage_id}', analysis)
    
    
    