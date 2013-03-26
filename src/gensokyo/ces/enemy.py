from collections import namedtuple
from functools import partial

from gensokyo import ces
from gensokyo import primitives
from gensokyo.ces import collision
from gensokyo.ces import sprite
from gensokyo.primitives import Vector
from gensokyo.ces.bullet import make_bullet, RoundBullet
from gensokyo.ces.rails import Rails
from gensokyo.ces.script import Script
from gensokyo.ces import pos
from gensokyo import resources

__all__ = ['Enemy', 'make_enemy', 'GenericEnemy', 'GrimReaper',
           'LoopFireAtPlayer']
Enemy = namedtuple("Enemy", ['img', 'group', 'hitbox', 'life'])
Enemy = partial(Enemy, group='enemy')

img = resources.enemy['generic']
GenericEnemy = partial(
    Enemy, img=img, hitbox=primitives.Rect(0, 0, img.width, img.height),
    life=200)


def make_enemy(world, drawer, enemy, x, y, *, rails, script):

    e = world.make_entity()
    add = partial(world.add_component, e)

    pos_ = pos.Position(x, y)
    add(pos_)

    hb = collision.Hitbox(pos_, enemy.hb.copy())
    add(hb)

    sprite_ = sprite.Sprite(pos_, drawer, enemy.group, enemy.img)
    add(sprite_)

    l = Life(enemy.life)
    add(l)

    r = Rails(rails, (x, y))
    add(r)

    assert isinstance(script, Script)
    add(script)

    return e


class Life(ces.Component):

    def __init__(self, life):
        self.life = life


class GrimReaper(ces.System):

    def on_update(self, dt):
        entities = ces.intersect(self.world, Life)
        l = self.world.cm[Life]
        for e in entities:
            if l[e].life <= 0:
                self.world.remove_entity(e)


#class GenericEnemy(Enemy):
#
#    sprite_img = resources.enemy['generic']
#    hb = primitives.Rect(0, 0, sprite_img.width, sprite_img.height)
#    init_life = 200
#
#    def __init__(self, x, y):
#
#        super().__init__(x, y)
#
#        s = LoopFireAtPlayer((x, y), 0.5)
#        self.add(s)


class LoopFireAtPlayer(Script):

    def __init__(self, rate):
        """rate is seconds per fire.  Smaller rate == faster"""
        self.state = 0
        self.rate = rate

    def run(self, entity, world, root, dt):
        self.state += dt
        if self.state >= self.rate:
            player = world.tm['player']
            pos_ = world.cm[pos.Position]
            p = pos_[entity].pos
            v = Vector(*pos_[player].pos) - Vector(*p)
            b = make_bullet(RoundBullet(), p[0], p[1], v)
            world.gm['enemy_bullet'].add(b)
            self.state -= self.rate
