#!/usr/bin/env python3

from gensokyo.primitives import Circle
from gensokyo.object import CollisionComponent
from gensokyo.object import DeathInterface
from gensokyo.entity import Entity
from gensokyo import component

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


class Bullet(Entity):

    sprite_img = None
    sprite_group = None

    def __init__(self, x, y, velocity, hitbox):

        super().__init__()

        v = velocity
        s = component.Sprite(self.sprite_group, self.sprite_img, x=x, y=y)
        hb = component.Hitbox(hitbox)

        self.add(v)
        self.add(s)
        self.add(hb)


class EnemyBullet(Bullet):

    sprite_group = 'enemy_bullet'

    def __init__(self, x, y, velocity, hitbox):
        super().__init__(x, y, velocity, hitbox)


class RoundBullet(EnemyBullet):

    sprite_img = resources.bullet['round']

    def __init__(self, x, y, velocity):
        hb = Circle(x, y, 10)
        super().__init__(x, y, velocity, hb)
