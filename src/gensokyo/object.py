#!/usr/bin/env python3

import abc

from pyglet.window import key
from pyglet.event import EventDispatcher
from pyglet.sprite import Sprite

from gensokyo.primitives import Rect, Circle, Vector
from gensokyo import locator

class AbstractContainer:

    """
    Abstract Container for Components

    Keeps a reference to components to keep alive.
    Propagates updates to components with update method.

    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.components = set()

    def add(self, c):
        self.components.add(c)

    def update(self, dt):
        for c in self.components:
            if hasattr(c, 'update'):
                c.update(dt)


class AbstractComponent:

    __metaclass__ = abc.ABCMeta


class CollisionComponent(AbstractComponent, EventDispatcher):

    def __init__(self, x, y, w, h, hb):
        self.rect = Rect(0, 0, w, h)
        self.hb = hb
        self.x = x
        self.y = y
        locator.add(self)

    @property
    def x(self):
        return self.rect.centerx

    @x.setter
    def x(self, value):
        self.rect.centerx = value
        if isinstance(self.hb, Circle):
            self.hb.x = value
        elif isinstance(self.hb, Rect):
            self.hb.centerx = value

    @property
    def y(self):
        return self.rect.centery

    @y.setter
    def y(self, value):
        self.rect.centery = value
        if isinstance(self.hb, Circle):
            self.hb.y = value
        elif isinstance(self.hb, Rect):
            self.hb.centery = value

    def on_dx(self, dx):
        self.x += dx

    def on_dy(self, dy):
        self.y += dy


class PhysicsComponent(AbstractComponent, EventDispatcher):

    def __init__(self):
        self.v = Vector(0, 0)
        self.speed = 0

    def update(self, dt):
        self.dispatch_event('on_dx', self.v.x * self.speed * dt)
        self.dispatch_event('on_dy', self.v.y * self.speed * dt)

PhysicsComponent.register_event_type('on_dx')
PhysicsComponent.register_event_type('on_dy')


class GraphicsComponent(AbstractComponent):

    def __init__(self, group, *args, **kwargs):
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

    def on_delete(self):
        self.sprite.delete()

    def on_dx(self, dx):
        self.x += dx

    def on_dy(self, dy):
        self.y += dy

    def on_setx(self x):
        self.x = x

    def on_sety(self y):
        self.y = y


class InputComponent(AbstractComponent):

    def __init__(self):
        locator.window.push_handlers(self)

    def delete(self):
        locator.window.remove_handlers(self)


class GameObject(AbstractContainer):

    """
    Example GameObject implementation

    You'll most likely overwrite __init__

    """

    sprite_img = None
    sprite_group = ''

    def __init__(self, x, y, hb=None):

        super().__init__()

        cls = self.__class__
        p = PhysicsComponent()
        c = CollisionComponent(x, y, cls.sprite_img.width,
                cls.sprite_img.height)
        g = GraphicsComponent(cls.sprite_group, img=cls.sprite_img)

        p.push_handlers(g)
        p.push_handlers(c)
        c.push_handlers(g)

        self.add(p)
        self.add(c)
        self.add(g)


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

    def update(self, dt):
        for a in self.objects:
            a.update(dt)
