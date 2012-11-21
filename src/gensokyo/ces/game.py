from gensokyo import ces
from gensokyo import locator


class Game(ces.Entity):

    def __init__(self, *args, **kwargs):
        self.add(GameData(*args, **kwargs))


class GameData(ces.Component):

    def __init__(self, high_score=0, score=0, lives=3, bombs=3):
        self.high_score = high_score
        self.score = score
        self.lives = lives
        self.bombs = bombs

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self.score = value
        if value > self.high_score:
            self.high_score = value
