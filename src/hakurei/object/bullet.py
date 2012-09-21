#!/usr/bin/env python3

import pyglet

from gensokyo.primitives import Vector, Circle
from gensokyo.object import Container
from gensokyo.object import CollisionComponent
from gensokyo.object import SpriteComponent
from gensokyo.object import DeathInterface
from gensokyo.physics import LinearPhysicsComp

from hakurei.globals import GAME_AREA
from hakurei.object.player import PlayerCollisionComponent
from hakurei import resources

class BulletCollisionComponent(CollisionComponent, DeathInterface):

    def __init__(self, x, y, w, h, hb):
        super().__init__(x, y, w, h, hb)
        self.handlers = {PlayerCollisionComponent:self.die}

    def die(self, other):
        super().die()

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


class Bullet(Container):

    sprite_img = None
    sprite_group = 'enemy_bullet'
    hb = None

    def __init__(self, x, y, speed=500, vector=Vector(0, 1)):

        super().__init__()

        p = LinearPhysicsComp()
        c = BulletCollisionComponent(x, y, self.sprite_img.width,
                self.sprite_img.height, self.hb)
        g = SpriteComponent(self.sprite_group, img=self.sprite_img)

        p.vel = vector
        p.speed = speed

        p.push_handlers(g)
        p.push_handlers(c)
        c.push_handlers(g)
        c.push_handlers(self)

        self.add(p)
        self.add(c)
        self.add(g)


class RoundBullet(Bullet):

    sprite_img = resources.bullet['round']

    def __init__(self, x, y, vector):
        super().__init__(x, y, speed=300, vector=vector)
        self.hb = Circle(x, y, 10)
