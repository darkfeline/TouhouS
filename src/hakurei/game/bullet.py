#!/usr/bin/env python3

from gensokyo import ces
from gensokyo import primitives

from hakurei import component
from hakurei import game
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

        hb = component.Hitbox(self.hitbox)
        hb.x, hb.y = x, y
        self.add(hb)

        s = component.Sprite(self.sprite_group, self.sprite_img, x=x, y=y)
        self.add(s)

        v = component.Velocity(velocity)
        self.add(v)

        r = primitives.Rect(0, 0, self.sprite_img.width,
                            self.sprite_img.height)
        r.center = x, y
        p = game.Presence(r)
        self.add(p)


class EnemyBullet(Bullet):

    sprite_group = 'enemy_bullet'


class RoundBullet(EnemyBullet):

    sprite_img = resources.bullet['round']

    def __init__(self, x, y, velocity):
        hb = primitives.Circle(x, y, 10)
        super().__init__(x, y, velocity, hb)
