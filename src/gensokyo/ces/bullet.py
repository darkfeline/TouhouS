from collections import namedtuple
from functools import partial

from gensokyo import primitives
from gensokyo.ces import collision
from gensokyo.ces import physics
from gensokyo.ces import graphics
from gensokyo.ces import gc
from gensokyo import resources

Bullet = namedtuple("Bullet", ['img', 'group', 'hitbox', 'dmg'])
EnemyBullet = partial(Bullet, group='enemy_bullet')
RoundBullet = partial(
    EnemyBullet, img=resources.bullet['round'],
    hitbox=primitives.Circle(0, 0, 10))


def make_bullet(world, bullet, x, y, v):

    e = world.make_entity()

    hb = BulletHitbox(bullet.hitbox.copy())
    hb.setpos((x, y))
    world.add_component(e, hb)

    sprite = graphics.Sprite(bullet.group, bullet.img, x=x, y=y)
    world.add_component(e, sprite)

    vel = physics.Velocity(v)
    world.add_component(e, vel)

    r = primitives.Rect(0, 0, bullet.img.width, bullet.img.height)
    r.center = x, y
    p = gc.Presence(r)
    world.add_component(e, p)

    return e


class BulletHitbox(collision.Hitbox):
    pass
