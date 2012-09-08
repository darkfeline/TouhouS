#!/usr/bin/env python3

import abc

from pyglet.event import EventDispatcher
from pyglet.sprite import Sprite

from gensokyo import primitives
from gensokyo import locator

class PhysicsComponent:

    def __init__(self, x, y, w, h, hb=None):
        self.hb = hb
        self.rect = primitives.Rect(0, 0, w, h)
        self.x = x
        self.y = y
        self.v = primitives.Vector(0, 0)
        self.speed = 0

    @property
    def x(self):
        return self.rect.centerx

    @x.setter
    def x(self, value):
        self.rect.centerx = value
        if isinstance(self.hb, primitives.Circle):
            self.hb.x = value
        elif isinstance(self.hb, primitives.Rect):
            self.hb.centerx = value

    @property
    def y(self):
        return self.rect.centery

    @y.setter
    def y(self, value):
        self.rect.centery = value
        if isinstance(self.hb, primitives.Circle):
            self.hb.y = value
        elif isinstance(self.hb, primitives.Rect):
            self.hb.centery = value

    def collide(self, other):
        return self.hb.collide(other.hb)


class GraphicsComponent:

    def __init__(self, sprite, group):
        locator.rendering.add_sprite(sprite, group)
        self.sprite = sprite

    @property
    def x(self):
        return self.sprite.x

    @x.setter
    def x(self, value):
        self.sprite.x = value

    @property
    def y(self):
        return self.sprite.y

    @y.setter
    def y(self, value):
        self.sprite.y = value

    def delete(self):
        self.sprite.delete()


class InputComponent:

    def __init__(self):
        locator.window.push_handlers(self)

    def delete(self):
        locator.window.remove_handlers(self)


class GameObject(PhysicsComponent, GraphicsComponent):

    sprite_img = None
    sprite_group = ''

    def __init__(self, x, y, hb=None):
        cls = self.__class__
        PhysicsComponent.__init__(x, y, cls.sprite_img.width,
                cls.sprite_img.height, hb)
        GraphicsComponent.__init__(self, Sprite(cls.sprite_img),
                cls.sprite_group)

    @property
    def x(self):
        return self.physics.x

    @x.setter
    def x(self, value):
        self.physics.x = value
        self.graphics.x = value

    def delete(self):
        GraphicsComponent.delete(self)

    def collide(self, other):
        if isinstance(other, GameObject):
            return PhysicsComponent.collide(self, other)
        elif isinstance(other, Group):
            x = []
            for object in other:
                if self.collide(object):
                    x.append(object)
            return x
        else:
            raise NotImplementedError


class Group:

    def __init__(self):
        super().__init__()
        self.objects = set()

    def __getitem__(self, key):
        return self.objects[key]

    def add(self, object):
        self.objects.add(object)

    def remove(self, object):
        self.objects.remove(object)

    def delete(self, object):
        self.objects.remove(object)
        object.delete()

    def __iter__(self):
        return iter(self.objects)

    def collide(self, other):
        if isinstance(other, Object):
            return other.collide(self)
        elif isinstance(other, Group):
            x = {}
            for a in self:
                y = a.collide(other)
                if y:
                    x[a] = y
            return x
        else:
            raise NotImplementedError

    def update(self, dt):
        for a in self.objects:
            a.update(dt)
