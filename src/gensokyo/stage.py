import abc

from gensokyo.ces import script
from gensokyo.ces import rails
from gensokyo.ces import enemy
from gensokyo.globals import GAME_AREA


class Stage(metaclass=abc.ABCMeta):

    def __init__(self, root, world):
        self.root = root
        self.world = world

    @abc.abstractmethod
    def on_update(self, dt):
        raise NotImplementedError


# TODO move everything below
class StageOne(Stage):

    def __init__(self, root, world):
        super().__init__(root, world)
        self.scripts = [LoopSpawnEnemy(GAME_AREA.right + 30, 400)]

    def on_update(self, dt):
        for x in self.scripts:
            x.run(self, dt)


class Script(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def run(self, stage, dt):
        raise NotImplementedError


# TODO generalize looping
class LoopSpawnEnemy:

    def __init__(self, pos, rate):
        self.pos = pos
        self.state = 0
        self.rate = rate

    def run(self, stage, dt):
        self.state += dt
        if self.state >= self.rate:
            self.state -= self.rate
            r = rails.Rails((('straight', (GAME_AREA.left - 30, 300), 5),))
            s = TimedSuicide(6)
            enemy.make_enemy(
                stage.world, stage.root.drawers, enemy.GenericEnemy(),
                self.pos, rails=r, script=s
            )


# TODO generalize this too
class TimedSuicide(script.Script):

    def __init__(self, time):
        self.time = 0
        self.limit = time

    def run(self, entity, env, dt):
        self.state += dt
        if self.time > self.limit:
            env.em.delete(entity)
