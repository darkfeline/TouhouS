#!/usr/bin/env python3

import abc

from pyglet.window import key
from pyglet.event import EventDispatcher
from pyglet.sprite import Sprite

from gensokyo.primitives import Rect, Circle, Vector
from gensokyo import locator

class AbstractContainer(EventDispatcher):

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

    def on_die(self):
        self.dispatch_event('on_remove', self)

AbstractContainer.register_event_type('on_remove')


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


class SpriteComponent(AbstractComponent):

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

    def on_setx(self, x):
        self.x = x

    def on_sety(self, y):
        self.y = y


class InputComponent(AbstractComponent):

    def __init__(self):
        locator.window.push_handlers(self)

    def delete(self):
        locator.window.remove_handlers(self)


class AIComponent(AbstractComponent, EventDispatcher):

    """
    Abstract AI Component

    There's not much to put here...
    Most likely you'll have this handle and dispatch events.
    You'll have to implement that yourself.

    """

    pass
