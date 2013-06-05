import logging

from gensokyo import primitives
from gensokyo.primitives import Vector
from gensokyo.ecs.enemy import Enemy
from gensokyo.ecs.bullet import make_bullet, RoundBullet
from gensokyo.ecs.script import Scriptlet
from gensokyo.ecs import pos
from gensokyo import resources

logger = logging.getLogger(__name__)

img = resources.enemy['generic']
GenericEnemy = Enemy(
    img=img, hitbox=primitives.Rect(0, 0, img.width, img.height), life=200
)


class LoopFireAtPlayer(Scriptlet):

    def __init__(self, rate, velocity):
        """
        `rate` is seconds per fire.  Smaller rate == faster
        `velocity` is bullet speed, scalar
        """
        self.state = 0
        self.rate = rate
        self.velocity = velocity

    def run(self, entity, world, master, dt):
        self.state += dt
        if self.state >= self.rate:
            player = world.tm['player']
            pos_ = world.cm[pos.Position]
            p = pos_[entity].pos
            v = Vector(*pos_[player].pos) - Vector(*p)
            v = v.get_unit_vector() * self.velocity
            b = make_bullet(world, master.drawer, RoundBullet, p[0], p[1], v)
            world.gm['enemy_bullet'].add(b)
            self.state -= self.rate
