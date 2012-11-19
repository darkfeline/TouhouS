from gensokyo.primitives import Vector
from gensokyo.ces.enemy import GenericEnemy
from gensokyo.globals import GAME_AREA


# TODO fix everything
class Stage:

    def __init__(self):
        super().__init__()
        self.player = None  # reference only

    def update(self, dt):
        self.enemies.update(dt)
        self.bullets.update(dt)


class Enemy(GenericEnemy):

    def __init__(self, x, y, player):
        super().__init__(x, y)
        self.state = 0
        self.player = player

    def update(self, dt):
        super().update(dt)
        self.state += dt
        while self.state > .5:
            self.fire_at(self.player.center)
            self.state -= .5


class StageOne(Stage):

    def __init__(self):
        super().__init__()
        self.state = 0
        self.rate = 1

    def update(self, dt):
        super().update(dt)
        self.state += dt
        while self.state > self.rate:
            e = Enemy(GAME_AREA.right + 30, 400, self.player)
            e.dest = Vector(GAME_AREA.left - 30, 300)
            self.enemies.add(e)
            self.state -= self.rate
        temp = []
        for e in self.enemies:
            if e.right < GAME_AREA.left:
                e.delete()
            else:
                temp.append(e)
        self.enemies.enemies = temp