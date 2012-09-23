#!/usr/bin/env python3

from gensokyo.primitives import Vector
from gensokyo.object import Container
from gensokyo.object import CollisionComponent
from gensokyo.object import SpriteComponent
from gensokyo.object import LifeComponent
from gensokyo.physics import LinearAccelPhysicsComp

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

        p = LinearAccelPhysicsComp()
        c = EnemyCollisionComponent(x, y, self.sprite_img.width,
                self.sprite_img.height, self.hb)
        g = SpriteComponent(self.sprite_group, img=self.sprite_img)
        l = LifeComponent(self.init_life)
        a = EnemyAIComponent()

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

        self.dest = Vector(x, y)

    @property
    def accel_dist(self):
        return self.max_speed - self.speed

    @property
    def decel_dist(self):
        return self.speed

    @property
    def dest(self):
        return self._dest

    @dest.setter
    def dest(self, value):
        self._dest = value
        self._vector = value - Vector(self.x, self.y)
        self._vector = self._vector.get_unit_vector()

    @property
    def vector(self):
        return self._vector

    def hit(self, dmg):
        self.life -= dmg
        if self.life < 0:
            self.die()

    def die(self):
        pass

    def fire_at(self, dest):
        dest = Vector(dest[0], dest[1])
        v = dest - Vector(self.x, self.y)
        b = bullet.Bullet(self.x, self.y, vector=v)
        self.bullets.add(b)

    def update(self, dt):
        # movement
        diff = self.dest - Vector(self.x, self.y)
        if diff != Vector(0, 0):
            # acceleration/deceleration
            if diff.length <= self.decel_dist:
                self.speed -= self.accel * dt
            if self.speed < self.max_speed:
                self.speed += self.accel * dt
            # movement
            self.x += self.speed * self.vector.x * dt
            self.y += self.speed * self.vector.y * dt


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
