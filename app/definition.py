import ast
import inspect
from typing import TypeVar, Generic

from app.logging import log

T = TypeVar('T')


# define the object without orm session
# this kind of object can only invoke methods end with "raw"
class Raw(Generic[T]):
    def __init__(self, obj: T):
        self.object: T = obj

    def __getattribute__(self, name):
        attribute = super().__getattribute__(name)
        if inspect.ismethod(attribute):
            if not name.endwith('_raw'):
                log(f'ORM object {type(self.object)} invoke a sql-related function ({name}) without database session. method invoke has been canceled')
                return  # cancel the method invoked
        return attribute

    def __getattr__(self, name):
        return getattr(self.object, name)


class AstChecker:
    def __init__(self, condition: str):
        self.condition = condition

    def check(self, variables):
        try:
            namespace = {}
            namespace.update(variables)
            tree = ast.parse(self.condition, mode='eval')
            return eval(compile(tree, filename='<ast>', mode='eval'), namespace)
        except SyntaxError:
            return False
