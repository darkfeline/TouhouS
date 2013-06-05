from collections import namedtuple
from functools import partial
import logging

from gensokyo import ecs
from gensokyo.sprite import SpriteDrawer
from gensokyo.ecs import collision
from gensokyo.ecs import sprite
from gensokyo.ecs.rails import Rails
from gensokyo.ecs.script import Script
from gensokyo.ecs import pos

__all__ = ['Enemy', 'make_enemy', 'Life', 'GrimReaper']
logger = logging.getLogger(__name__)

Enemy = namedtuple("Enemy", ['img', 'group', 'hitbox', 'life'])
Enemy = partial(Enemy, group='enemy')


def make_enemy(world, drawer, enemy, x, y, *, rails, scriptlets):

    logger.debug(
        'make_enemy(%r, %r, %r, %r, %r, rails=%r, scriptlets=%r)', world,
        drawer, enemy, x, y, rails, scriptlets)
    assert isinstance(world, ecs.World)
    assert isinstance(drawer, SpriteDrawer)

    e = world.make_entity()
    add = partial(world.add_component, e)

    pos_ = pos.Position((x, y))
    add(pos_)
    hb = collision.Hitbox(pos_, enemy.hitbox.copy())
    add(hb)
    sprite_ = sprite.Sprite(pos_, drawer, enemy.group, enemy.img)
    add(sprite_)
    l = Life(enemy.life)
    add(l)
    r = Rails(rails, (x, y))
    add(r)

    if scriptlets:
        s = Script()
        for x in scriptlets:
            s.add(x)
        add(s)

    return e


class Life(ecs.Component):

    def __init__(self, life):
        self.life = life


class GrimReaper(ecs.System):

    def on_update(self, dt):
        entities = ecs.intersect(self.world, Life)
        l = self.world.cm[Life]
        for e in entities:
            if l[e].life <= 0:
                self.world.remove_entity(e)
