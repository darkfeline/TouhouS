from gensokyo import ces
from gensokyo import locator


class GameData(ces.Component):

    def __init__(self, high_score=0, score=0, lives=3, bombs=3):
        self.high_score = high_score
        self.score = score
        self.lives = lives
        self.bombs = bombs


class DataSystem(ces.System):

    """
    Superclass for systems that need to access game data

    """

    fields = set(['high_score', 'score', 'lives', 'bombs'])

    def get(self, field):
        if field not in self.fields:
            raise TypeError
        entity = locator.tm.get_tag('data')
        for comp in entity.get(GameData):
            return getattr(comp, field)

    def set(self, field, value):
        if field not in self.fields:
            raise TypeError
        # set counter
        entity = locator.tm.get_tag('data')
        entity.set_value(value)
        # set data
        entity = locator.tm.get_tag(field)
        for comp in entity.get(GameData):
            setattr(comp, field, value)
