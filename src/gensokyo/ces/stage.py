from gensokyo import ces
from gensokyo.ces import script
from gensokyo.ces import rails
from gensokyo.ces import observer
from gensokyo.ces.enemy import GenericEnemy
from gensokyo.globals import GAME_AREA
from gensokyo import locator


class Stage(ces.Entity):

    def __init__(self, script_):
        super().__init__()
        s = script.Script(script_)
        self.add(s)


# TODO move everything below
class StageOne(Stage):

    def __init__(self):
        super().__init__([(LoopSpawnEnemy(GAME_AREA.right + 30, 400),)])


# TODO generalize looping
class LoopSpawnEnemy(script.ConditionUnit, observer.Updating):

    def __init__(self, pos, rate):
        self.pos = pos
        self.state = 0
        self.rate = rate

    @property
    def satisfied(self):
        if self.state > self.rate:
            return True
        else:
            return False

    def run(self, entity):
        self.state -= self.rate
        e = GenericEnemy(*self.pos)
        r = rails.Rails((('straight', (GAME_AREA.left - 30, 300), 5),))
        e.add(r)
        s = script.Script([TimedSuicide(6)])
        e.add(s)
        locator.em.add(e)
        locator.gm.add_to(e, 'enemy')

    def on_update(self, dt):
        self.state += dt


# TODO generalize this too
class TimedSuicide(script.ConditionUnit, observer.Updating):

    def __init__(self, time):
        self.time = 0
        self.limit = time
        self.expire = True

    @property
    def satisfied(self):
        if self.time > self.limit:
            return True
        else:
            return False

    def run(self, entity):
        locator.em.delete(entity)

    def on_update(self, dt):
        self.state += dt
