import abc

from gensokyo.ecs import script
from gensokyo.ecs import rails
from gensokyo.ecs import enemy
from gensokyo.globals import GAME_AREA


class Stage(metaclass=abc.ABCMeta):

    def __init__(self, world, master):
        self.world = world
        self.master = master

    @abc.abstractmethod
    def on_update(self, dt):
        raise NotImplementedError


# TODO move everything below
class StageOne(Stage):

    def __init__(self, world, master):
        super().__init__(world, master)
        self.scripts = [LoopSpawnEnemy(GAME_AREA.right + 30, 400)]

    def on_update(self, dt):
        for x in self.scripts:
            x.run(self, dt)


class Script(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def run(self, stage, dt):
        raise NotImplementedError


# TODO generalize looping
class LoopSpawnEnemy(Script):

    def __init__(self, pos, rate):
        self.pos = pos
        self.state = 0
        self.rate = rate

    def run(self, stage, dt):
        self.state += dt
        if self.state >= self.rate:
            self.state -= self.rate
            r = rails.Rails((('straight', (GAME_AREA.left - 30, 300), 5),))
            e = enemy.make_enemy(
                stage.world, stage.rootenv.drawers, enemy.GenericEnemy(),
                self.pos, rails=r,
                scriptlets=[TimedSuicide(6), enemy.LoopFireAtPlayer(0.5)]
            )
            stage.world.gm['enemy'].add(e)


class TimedSuicide(script.Script):

    def __init__(self, time):
        self.time = 0
        self.limit = time

    def run(self, entity, env, master, dt):
        self.state += dt
        if self.time > self.limit:
            env.em.delete(entity)
