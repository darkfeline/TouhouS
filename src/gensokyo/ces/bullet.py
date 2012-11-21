import numbers

from gensokyo import ces
from gensokyo import primitives
from gensokyo.ces import collision
from gensokyo.ces import physics
from gensokyo.ces import graphics
from gensokyo.ces import gc
from gensokyo import resources


class BulletOrigin(ces.Position):

    def __init__(self, pos):
        """
        :param pos: position
        :type pos: list

        """
        assert isinstance(pos, list)
        self.pos = pos

    @property
    def x(self):
        return self.pos[0]

    @x.setter
    def x(self, value):
        assert isinstance(value, numbers.Real)
        self.pos[0] = value

    @property
    def y(self):
        return self.pos[1]

    @y.setter
    def y(self, value):
        assert isinstance(value, numbers.Real)
        self.pos[1] = value


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


# TODO move these somewhere
class EnemyBullet(Bullet):

    sprite_group = 'enemy_bullet'


class RoundBullet(EnemyBullet):

    sprite_img = resources.bullet['round']

    def __init__(self, x, y, velocity):
        hb = primitives.Circle(x, y, 10)
        super().__init__(x, y, velocity, hb)
