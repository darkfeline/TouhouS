#!/usr/bin/env python3

import pyglet

from gensokyo.primitives import Vector, Circle
from gensokyo.object import AbstractContainer

from hakurei.globals import GAME_AREA
from hakurei import resources

class BulletGroup(Group):

    @property
    def bullets(self):
        return list(self.objects)

    @bullets.setter
    def bullets(self, value):
        self.objects = set(value)

    def update(self, dt):
        super().update(dt)
        temp = set()
        for b in self.bullets:
            r = b.rect
            if (r.bottom > GAME_AREA.top or r.top < GAME_AREA.bottom or
                    r.left > GAME_AREA.right or r.right < GAME_AREA.left):
                b.delete()
            else:
                temp.add(b)
        self.bullets = temp



class Bullet(AbstractContainer):

    sprite_img = None
    sprite_group = 'enemy_bullet'

    def __init__(self, x, y, hb=None, speed=500, vector=Vector(0, 1)):
        super().__init__(x, y, hb)

        cls = self.__class__
        p = PhysicsComponent()
        c = CollisionComponent(x, y, cls.sprite_img.width,
                cls.sprite_img.height)
        g = GraphicsComponent(cls.sprite_group, img=cls.sprite_img)

        p.v = vector
        p.speed = speed

        p.push_handlers(g)
        p.push_handlers(c)
        c.push_handlers(g)

        self.add(p)
        self.add(c)
        self.add(g)


class RoundBullet(Bullet):

    sprite_img = resources.bullet['round']

    def __init__(self, x, y, vector):
        super().__init__(x, y, speed=300, vector=vector)
        self.hb = Circle(x, y, 10)
