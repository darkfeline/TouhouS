#!/usr/bin/env python3

import pyglet

from gensokyo.primitives import Vector, Circle
from gensokyo.object import AbstractContainer
from gensokyo.object import CollisionComponent
from gensokyo.object import PhysicsComponent
from gensokyo.object import GraphicsComponent

from hakurei.globals import GAME_AREA
from hakurei.object.player import PlayerCollisionComponent
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


class BulletCollisionComponent(CollisionComponent):

    def __init__(self, x, y, w, h, hb):
        super().__init__(x, y, w, h, hb)
        self.handlers = {PlayerCollisionComponent:self.die}

    def die(self):
        self.dispatch_event('on_delete')
        self.dispatch_event('on_die')

    def check_bounds(self):
        r = self.rect
        if (r.bottom > GAME_AREA.top or r.top < GAME_AREA.bottom or
                r.left > GAME_AREA.right or r.right < GAME_AREA.left):
            self.die()

    def on_dx(self, dx):
        super().on_dx(dx)
        self.check_bounds()

    def on_dy(self, dy):
        super().on_dy(dy)
        self.check_bounds()

BulletCollisionComponent.register_event_type('on_delete')
BulletCollisionComponent.register_event_type('on_die')


class Bullet(AbstractContainer):

    sprite_img = None
    sprite_group = 'enemy_bullet'

    def __init__(self, x, y, hb=None, speed=500, vector=Vector(0, 1)):
        super().__init__(x, y, hb)

        cls = self.__class__
        p = PhysicsComponent()
        c = BulletCollisionComponent(x, y, cls.sprite_img.width,
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
