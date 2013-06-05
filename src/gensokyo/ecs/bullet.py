from collections import namedtuple
from functools import partial

from gensokyo import primitives
from gensokyo import ecs
from gensokyo.ecs import collision
from gensokyo.ecs import physics
from gensokyo.ecs import sprite
from gensokyo.ecs import gc
from gensokyo.ecs import pos
from gensokyo.ecs.script import Script

__all__ = ["Bullet", "EnemyBullet", "Damage", "make_bullet"]
Bullet = namedtuple("Bullet", ['img', 'group', 'hitbox', 'dmg'])
EnemyBullet = partial(Bullet, group='enemy_bullet', dmg=1)


def make_bullet(world, drawer, bullet, x, y, v, *, scriptlets=None):

    e = world.make_entity()
    add = partial(world.add_component, e)
    pos_ = pos.Position((x, y))
    add(pos_)
    hb = collision.Hitbox(pos_, bullet.hitbox.copy())
    add(hb)
    sprite_ = sprite.Sprite(pos_, drawer, bullet.group, bullet.img)
    add(sprite_)
    vel = physics.Velocity(v)
    add(vel)
    dmg = Damage(bullet.dmg)
    add(dmg)

    r = primitives.Rect(0, 0, bullet.img.width, bullet.img.height)
    p = gc.Presence(pos_, r)
    add(p)

    if scriptlets:
        s = Script()
        for x in scriptlets:
            s.add(x)
        add(s)

    return e


class Damage(ecs.Component):

    def __init__(self, dmg):
        self.dmg = dmg
