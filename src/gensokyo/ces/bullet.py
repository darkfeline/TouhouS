import abc

from gensokyo import ces
from gensokyo import primitives
from gensokyo.ces import collision
from gensokyo.ces import physics
from gensokyo.ces import graphics
from gensokyo.ces import gc
from gensokyo import resources


class Bullet(ces.Entity, metaclass=abc.ABCMeta):

    sprite_img = None
    sprite_group = None
    hitbox = None
    dmg = 0

    def __init__(self, x, y, velocity):

        """
        Does not add bullet to entity manager

        :param x: x coordinate
        :type x: int
        :param y: y coordinate
        :type y: int
        :param velocity: physics vectors
        :type velocity: list

        """

        super().__init__()

        hb = self.hitbox.copy()
        hb = BulletHitbox(hb)
        hb.pos = x, y
        self.add(hb)

        s = BulletSprite(self.sprite_group, self.sprite_img, x=x, y=y)
        self.add(s)

        v = physics.Physics(velocity)
        self.add(v)

        r = primitives.Rect(
            0, 0, self.sprite_img.width, self.sprite_img.height)
        r.center = x, y
        p = BulletPresence(r)
        self.add(p)


class BulletHitbox(collision.Hitbox, physics.PhysicsPosition):
    pass


class BulletSprite(graphics.Sprite, physics.PhysicsPosition):
    pass


class BulletPresence(gc.Presence, physics.PhysicsPosition):
    pass


# TODO probably move this too
class EnemyBullet(Bullet, metaclass=abc.ABCMeta):

    sprite_group = 'enemy_bullet'


# TODO move this somewhere
class RoundBullet(EnemyBullet):

    sprite_img = resources.bullet['round']

    def __init__(self, x, y, velocity):
        hb = primitives.Circle(x, y, 10)
        super().__init__(x, y, velocity, hb)
