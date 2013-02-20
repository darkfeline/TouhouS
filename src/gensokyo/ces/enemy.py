from collections import namedtuple
from functools import partial

from gensokyo import ces
from gensokyo import primitives
from gensokyo.ces import collision
from gensokyo.ces import graphics
from gensokyo.primitives import Vector
from gensokyo.ces.bullet import make_bullet, RoundBullet
from gensokyo.ces import rails
from gensokyo.ces import script
from gensokyo.ces.pos import Position
from gensokyo import resources

__all__ = ['Enemy', 'make_enemy', 'GenericEnemy', 'GrimReaper',
           'LoopFireAtPlayer']
Enemy = namedtuple("Enemy", ['img', 'group', 'hitbox', 'life'])
Enemy = partial(Enemy, group='enemy')

img = resources.enemy['generic']
GenericEnemy = partial(
    Enemy, img=img, hitbox=primitives.Rect(0, 0, img.width, img.height),
    life=200)


def make_enemy(world, enemy, x, y, *, rails, script):

    e = world.make_entity()

    hb = collision.Hitbox(enemy.hb.copy())
    hb.setpos((x, y))
    world.add_component(e, hb)

    sprite = graphics.Sprite(enemy.group, enemy.img, x=x, y=y)
    world.add_component(e, sprite)

    l = Life(enemy.life)
    world.add_component(e, l)

    r = rails.Rails(rails, (x, y))
    world.add_component(e, r)

    world.add_component(e, script)

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


class LoopFireAtPlayer(script.Script):

    def __init__(self, rate):
        """rate is seconds per fire.  Smaller rate == faster"""
        self.state = 0
        self.rate = rate

    def run(self, entity, world, dt):
        self.state += dt
        if self.state >= self.rate:
            pos = world.cm[Position]
            player = world.tm['player']
            p = pos[entity].pos
            v = Vector(*pos[player].pos) - Vector(*p)
            b = make_bullet(RoundBullet(), p[0], p[1], v)
            world.gm['enemy_bullet'].add(b)
