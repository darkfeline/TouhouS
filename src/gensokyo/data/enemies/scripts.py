from gensokyo.ecs.script import Scriptlet
from gensokyo.primitives import Vector
from gensokyo.ecs import pos
from gensokyo.ecs.bullet import make_bullet


class LoopFireAtPlayer(Scriptlet):

    def __init__(self, rate, velocity, bullet):
        """
        `rate` is seconds per fire.  Smaller rate == faster
        `velocity` is bullet speed, scalar
        `bullet` is bullet seed
        """
        self.state = 0
        self.rate = rate
        self.velocity = velocity
        self.bullet = bullet

    def run(self, entity, world, master, dt):
        self.state += dt
        if self.state >= self.rate:
            player = world.tm['player']
            pos_ = world.cm[pos.Position]
            p = pos_[entity].pos
            v = Vector(*pos_[player].pos) - Vector(*p)
            v = v.get_unit_vector() * self.velocity
            b = make_bullet(world, master.drawer, self.bullet, p[0], p[1], v)
            world.gm['enemy_bullet'].add(b)
            self.state -= self.rate
