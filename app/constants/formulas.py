from abc import abstractmethod, ABCMeta


class Formula(metaclass=ABCMeta):
    @abstractmethod
    def calculate(self, **kwargs) -> float: pass

    def __init__(self, formula_id, name, source, description, page):
        self.formula_id = formula_id
        self.name = name
        self.source = source
        self.description = description
        self.page = page


class BanchoFormula(Formula):
    def calculate(self, **kwargs) -> float:
        # TODO: real calculation formula
        return 0.0


bancho_formula = BanchoFormula(formula_id=0, name='Bancho', source='osu!Team', description='vanilla osu experience',
                               page='https://github.com/ppy/osu-performance')
dict_id2obj = {
    0: bancho_formula
}
