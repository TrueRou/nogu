from multiprocessing import Pool, Queue
from sqlalchemy import select
from interaction import Score, ScoreDetail, StageMapUserDetail, StageMapDetail, StageUserDetail, StageDetail
from app.database import db_session as database_session

pool = Pool(4)
queue: Queue[int] = Queue()


def analyze_task(analysis_requests: Queue[int]):
    while True:
        stage_id = analysis_requests.get()
        with database_session() as session:
            # get scores from stage_id
            scores = session.execute(select(Score).where(Score.stage_id == stage_id)).scalars()
            # process every score
            score_detail_list = []
            stage_map_user_detail_list = []
            stage_map_detail_list = []
            stage_user_detail_list = []
            stage_detail_list = []
            for score in scores:
                # analyze to Score_detail
                score_detail = ScoreDetail()
                # TODO score_detail analyze
                score_detail_list.append(score_detail)

                stage_map_user_detail = StageMapUserDetail()
                # TODO stage_map_user_detail  analyze
                stage_map_user_detail_list.append(stage_map_user_detail)

                stage_map_detail = StageMapDetail()
                # TODO stage_map_detail  analyze
                stage_map_detail_list.append(stage_map_detail)

                stage_user_detail = StageUserDetail()
                # TODO stage_user_detail  analyze
                stage_user_detail_list.append(stage_user_detail)

                stage_detail = StageDetail()
                # TODO stage_detail  analyze
                stage_detail_list.append(stage_detail)
            session.bulk_save_objects(score_detail_list)
            session.bulk_save_objects(stage_map_user_detail_list)
            session.bulk_save_objects(stage_map_detail_list)
            session.bulk_save_objects(stage_user_detail_list)
            session.bulk_save_objects(stage_detail_list)
            session.commit()
            # TODO sleeep?


def begin_analyze():
    for i in range(5):
        pool.apply_async(analyze_task, args=(queue,))
    pool.close()
    pool.join()
