#!/usr/bin/env python3

import abc

from pyglet.window import key
from pyglet.event import EventDispatcher
from pyglet.sprite import Sprite

from gensokyo.primitives import Rect, Circle, Vector
from gensokyo import locator

class AbstractComponent:

    __metaclass__ = abc.ABCMeta

    def __init__(self, master):
        self._master = master

    @property
    def master(self):
        return self._master


class CollisionComponent(AbstractComponent):

    def __init__(self, master, x, y, w, h):
        super().__init__(master)
        self.hb = Rect(0, 0, w, h)
        self.x = x
        self.y = y

    @property
    def x(self):
        return self.rect.centerx

    @x.setter
    def x(self, value):
        if isinstance(self.hb, Circle):
            self.hb.x = value
        elif isinstance(self.hb, Rect):
            self.hb.centerx = value

    @property
    def y(self):
        return self.rect.centery

    @y.setter
    def y(self, value):
        if isinstance(self.hb, Circle):
            self.hb.y = value
        elif isinstance(self.hb, Rect):
            self.hb.centery = value

    def collide(self, other):
        return self.hb.collide(other.hb)


class PhysicsComponent(AbstractComponent):

    def __init__(self, master, x, y):
        super().__init__(master)
        self.x = x
        self.y = y
        self.v = Vector(0, 0)
        self.speed = 0

    def update(self, dt):
        self.x += self.v.x * self.speed * dt
        self.y += self.v.y * self.speed * dt


class GraphicsComponent(AbstractComponent):

    def __init__(self, master, group, *args, **kwargs):
        super().__init__(master)
        sprite = Sprite(*args, **kwargs)
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


class InputComponent(AbstractComponent):

    def __init__(self, master):
        super().__init__(master)
        locator.window.push_handlers(self)

    def delete(self):
        locator.window.remove_handlers(self)


class PlayerInputComponent(InputComponent):

    def update(self, dt):
        x = 0
        if locator.key_state[key.LEFT]:
            x = -1
        if locator.key_state[key.RIGHT]:
            x += 1
        y = 0
        if locator.key_state[key.DOWN]:
            y = -1
        if locator.key_state[key.UP]:
            y += 1
        self.v = Vector(x, y).get_unit_vector()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LSHIFT:
            self.focus = 1
        elif symbol == key.Z:
            self.shooting = 1

    def on_key_release(self, symbol, modifiers):
        if symbol == key.LSHIFT:
            self.focus = 0
        elif symbol == key.Z:
            self.shooting = 0


class GameObject:

    sprite_img = None
    sprite_group = ''

    def __init__(self, x, y, hb=None):
        cls = self.__class__
        self.physics = PhysicsComponent(x, y)
        self.collision = CollisionComponent(x, y, cls.sprite_img.width,
                cls.sprite_img.height)
        self.graphics = graphics(self, cls.sprite_group, img=cls.sprite_img)

    def delete(self):
        self.graphics.delete()

    def collide(self, other):
        if isinstance(other, GameObject):
            return self.physics.collide(self, other.physics)
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
        if isinstance(other, GameObject):
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
