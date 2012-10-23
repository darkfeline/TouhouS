from gensokyo import ces
from gensokyo import primitives

from hakurei.ces import collision
from hakurei.ces import graphics
from hakurei.ces import rails
from hakurei.ces import bullet
from hakurei import resources


class Life(ces.Component):

    def __init__(self, life):
        self.life = life


class Enemy(ces.Entity):

    sprite_img = None
    sprite_group = 'enemy'
    hb = None
    init_life = 200

    def __init__(self, x, y, script):

        """
        :param x: x coordinate
        :type x: int
        :param y: y coordinate
        :type y: int

        """

        super().__init__()

        hb = collision.Hitbox(self.hitbox)
        hb.x, hb.y = x, y
        self.add(hb)

        s = graphics.Sprite(self.sprite_group, self.sprite_img, x=x, y=y)
        self.add(s)

        r = rails.Rails(script)
        self.add(r)

        l = Life(self.init_life)
        self.add(l)


class GenericEnemy(Enemy):

    sprite_img = resources.enemy['generic']
    hb = primitives.Circle(0, 0, sprite_img.width)
    init_life = 200

    # TODO move to rails
    def fire_at(self, dest):
        dest = primitives.Vector(dest[0], dest[1])
        v = dest - primitives.Vector(self.x, self.y)
        b = bullet.RoundBullet(self.x, self.y, vector=v)
        self.bullets.add(b)
