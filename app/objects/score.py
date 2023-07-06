import ast
from app import database
from app.constants.formulas import dict_id2obj
from app.database import db_session
from app.objects.models import Score, Stage


async def check_condition(score: Score, condition: str) -> bool:
    variables = {
        "acc": score.accuracy,
        "max_combo": score.highest_combo,
        "mods": score.mods,
        "score": score.score
    }
    try:
        namespace = {}
        namespace.update(variables)
        tree = ast.parse(condition, mode='eval')
        return eval(compile(tree, filename='<ast>', mode='eval'), namespace)
    except SyntaxError:
        return False


async def web_submit(info: dict, condition: str, stage: Stage) -> Score:
    async with db_session() as session:
        pp = dict_id2obj[stage.formula].calculate(mode=stage.mode)  # TODO: provide correct args to calculate pp
        score = Score(**info, stage_id=stage.id, performance_points=pp)
        if score.check_condition(condition):
            return await database.add_model(session, score)


async def get_score(score_id: int) -> Score:
    async with db_session() as session:
        return await database.get_model(session, score_id, Score)
