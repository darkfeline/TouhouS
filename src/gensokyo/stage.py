import abc
import logging

from gensokyo.ecs import script
from gensokyo.ecs import enemy
from gensokyo.globals import GAME_AREA

logger = logging.getLogger(__name__)


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
        self.scripts = [LoopSpawnEnemy((GAME_AREA.right + 30, 400), 3)]

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
        logger.debug('LoopSpawnEnemy(%r, %r)', pos, rate)
        self.pos = pos
        self.state = 0
        self.rate = rate

    def run(self, stage, dt):
        self.state += dt
        if self.state >= self.rate:
            logger.debug('LoopSpawnEnemy: spawning')
            self.state -= self.rate
            r = (('straight', (GAME_AREA.left - 30, 300), 5),)
            e = enemy.make_enemy(
                stage.world, stage.master.drawer, enemy.GenericEnemy,
                self.pos[0], self.pos[1], rails=r,
                scriptlets=[TimedSuicide(6), enemy.LoopFireAtPlayer(0.3, 7)]
            )
            logger.debug('spawned %r', e)
            stage.world.gm['enemy'].add(e)


class TimedSuicide(script.Scriptlet):

    def __init__(self, time):
        self.state = 0
        self.limit = time

    def run(self, entity, world, master, dt):
        self.state += dt
        if self.state > self.limit:
            logger.debug('TimedSuicide killed %r', entity)
            world.remove_entity(entity)
