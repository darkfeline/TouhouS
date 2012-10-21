from gensokyo import ces
from gensokyo import primitives

from hakurei.ces import collision
from hakurei.ces import physics
from hakurei.ces import graphics
from hakurei.ces import gc
from hakurei import resources


class Bullet(ces.Entity):

    sprite_img = None
    sprite_group = None
    hitbox = None

    def __init__(self, x, y, velocity):

        """
        :param x: x coordinate
        :type x: int
        :param y: y coordinate
        :type y: int
        :param velocity: physics vectors
        :type velocity: list

        """

        super().__init__()

        hb = collision.Hitbox(self.hitbox)
        hb.x, hb.y = x, y
        self.add(hb)

        s = graphics.Sprite(self.sprite_group, self.sprite_img, x=x, y=y)
        self.add(s)

        v = physics.Physics(velocity)
        self.add(v)

        r = primitives.Rect(0, 0, self.sprite_img.width,
                            self.sprite_img.height)
        r.center = x, y
        p = gc.Presence(r)
        self.add(p)


class EnemyBullet(Bullet):

    sprite_group = 'enemy_bullet'


class RoundBullet(EnemyBullet):

    sprite_img = resources.bullet['round']

    def __init__(self, x, y, velocity):
        hb = primitives.Circle(x, y, 10)
        super().__init__(x, y, velocity, hb)
