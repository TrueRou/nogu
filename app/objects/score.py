import ast

from sqlalchemy import Column, Integer, Text, Numeric, Boolean, DateTime, text, ForeignKey
from sqlalchemy.orm import relationship

from app import database
from app.constants.formulas import dict_id2obj
from app.constants.servers import Server
from app.database import Base, db_session
from app.objects.beatmap import Beatmap
from app.objects.stage import Stage


class Score(Base):
    __tablename__ = 'scores'

    score_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    beatmap_md5 = Column(Text, ForeignKey('beatmaps.md5'), nullable=False, index=True)
    score = Column(Integer, nullable=False)
    performance_points = Column(Numeric(7, 3), nullable=False)
    accuracy = Column(Numeric(6, 3), nullable=False)
    highest_combo = Column(Integer, nullable=False)
    full_combo = Column(Boolean, nullable=False)
    mods = Column(Integer, nullable=False)
    num_300s = Column(Integer, nullable=False)
    num_100s = Column(Integer, nullable=False)
    num_50s = Column(Integer, nullable=False)
    num_misses = Column(Integer, nullable=False)
    num_gekis = Column(Integer, nullable=False)
    num_katus = Column(Integer, nullable=False)
    grade = Column(Text, nullable=False)
    mode = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    server_id = Column(Integer, nullable=False, default=Server.LOCAL)
    stage_id = Column(Integer, ForeignKey('stages.id'), index=True, nullable=False)

    beatmap = relationship('Beatmap', lazy='dynamic')
    stage = relationship('Stage', lazy='dynamic')

    async def check_condition(self, condition: str) -> bool:
        variables = {
            "acc": self.accuracy,
            "max_combo": self.highest_combo,
            "mods": self.mods,
            "score": self.score
        }
        try:
            namespace = {}
            namespace.update(variables)
            tree = ast.parse(condition, mode='eval')
            return eval(compile(tree, filename='<ast>', mode='eval'), namespace)
        except SyntaxError:
            return False

    @staticmethod
    async def web_submit(info: dict, condition: str, stage: Stage) -> 'Score':
        async with db_session() as session:
            pp = dict_id2obj[stage.formula].calculate(mode=stage.mode)  # TODO: provide correct args to calculate pp
            score = Score(**info, stage_id=stage.id, performance_points=pp)
            if score.check_condition(condition):
                return await database.add_model(session, score)

    @staticmethod
    async def get_score(score_id: int) -> 'Score':
        async with db_session() as session:
            return await database.get_model(session, score_id, Score)
