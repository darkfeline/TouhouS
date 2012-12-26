from gensokyo import ces
from gensokyo.ces import script
from gensokyo.ces import rails
from gensokyo.ces.enemy import GenericEnemy
from gensokyo.globals import GAME_AREA


class Stage(ces.Entity):

    def __init__(self, script_):
        super().__init__()
        s = script.Script(script_)
        self.add(s)


# TODO move everything below
class StageOne(Stage):

    def __init__(self):
        super().__init__([LoopSpawnEnemy(GAME_AREA.right + 30, 400)])


# TODO generalize looping
class LoopSpawnEnemy(script.ScriptingUnit):

    def __init__(self, pos, rate):
        self.pos = pos
        self.state = 0
        self.rate = rate

    def run(self, entity, env, dt):
        self.state += dt
        if self.state >= self.rate:
            self.state -= self.rate
            e = GenericEnemy(*self.pos)
            r = rails.Rails((('straight', (GAME_AREA.left - 30, 300), 5),))
            e.add(r)
            s = script.Script([TimedSuicide(6)])
            e.add(s)
            env.em.add(e)
            env.gm.add_to(e, 'enemy')


# TODO generalize this too
class TimedSuicide(script.ScriptingUnit):

    def __init__(self, time):
        self.time = 0
        self.limit = time
        self.expire = True

    def run(self, entity, env, dt):
        self.state += dt
        if self.time > self.limit:
            env.em.delete(entity)
