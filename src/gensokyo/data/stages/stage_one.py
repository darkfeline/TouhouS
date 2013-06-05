import logging

from gensokyo.ecs import enemy
from gensokyo import stage
from gensokyo.globals import GAME_AREA
from gensokyo.data.enemies.basic import BasicFairy
from gensokyo.data.enemies import scripts
from gensokyo.data.bullets.basic import BasicRedBullet


logger = logging.getLogger(__name__)


class StageOne(stage.Stage):

    def __init__(self, world, master):
        super().__init__(world, master)
        self.scripts = [LoopSpawnEnemy((GAME_AREA.right + 30, 400), 3)]

    def on_update(self, dt):
        for x in self.scripts:
            x.run(self, dt)


class LoopSpawnEnemy(stage.Script):

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
                stage.world, stage.master.drawer, BasicFairy,
                self.pos[0], self.pos[1], rails=r,
                scriptlets=[
                    scripts.TimedSuicide(6),
                    scripts.LoopFireAtPlayer(0.3, 7, BasicRedBullet)
                ]
            )
            logger.debug('spawned %r', e)
            stage.world.gm['enemy'].add(e)
