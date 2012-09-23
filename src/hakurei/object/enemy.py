#!/usr/bin/env python3

from gensokyo.primitives import Vector
from gensokyo.object import Container
from gensokyo.object import CollisionComponent
from gensokyo.object import SpriteComponent
from gensokyo.object import LifeComponent
from gensokyo.physics import SmoothDestComp

from hakurei.object import bullet
from hakurei.object.player import PlayerBulletCollisionComponent
from hakurei import resources

class EnemyCollisionComponent(CollisionComponent):

    def __init__(self, x, y, w, h, hb):
        super().__init__(x, y, w, h, hb)
        self.handlers = {PlayerBulletCollisionComponent:self.hit}

    def hit(self, other):
        self.dispatch_event('on_hit', other.dmg)

EnemyCollisionComponent.register_event_type('on_hit')


class Enemy(Container):

    sprite_img = None
    sprite_group = 'enemy'
    hb = None
    init_life = 200

    def __init__(self, x, y):

        super().__init__()

        p = SmoothDestComp()
        c = EnemyCollisionComponent(x, y, self.sprite_img.width,
                self.sprite_img.height, self.hb)
        g = SpriteComponent(self.sprite_group, img=self.sprite_img)
        l = LifeComponent(self.init_life)

        p.speed = 0
        p.accel = 100
        p.max_speed = 300

        p.push_handlers(g)
        p.push_handlers(c)
        c.push_handlers(l)
        l.push_handlers(g)
        l.push_handlers(self)

        self.add(p)
        self.add(c)
        self.add(g)
        self.add(l)

        self.physics = p


class GenericEnemy(Enemy):

    sprite_img = resources.enemy['generic']

    def __init__(self, x, y):
        super().__init__(x, y)
        self.hb = self.rect
        self.max_speed = 300
        self.accel = 100
        self.life = 200

    def fire_at(self, dest):
        dest = Vector(dest[0], dest[1])
        v = dest - Vector(self.x, self.y)
        b = bullet.RoundBullet(self.x, self.y, vector=v)
        self.bullets.add(b)
