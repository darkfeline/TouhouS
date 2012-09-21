#!/usr/bin/env python3

from pyglet.window import key
from pyglet.event import EventDispatcher
from pyglet.sprite import Sprite

from gensokyo.primitives import Rect, Circle, Vector
from gensokyo import locator

class Container(EventDispatcher):

    """
    Container for Components

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


class CollisionComponent(EventDispatcher):

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


class PhysicsComponent(EventDispatcher):

    """
    Physics Component

    .. attribute:: vel

        velocity vector

    .. attribute:: acc

        acceleration vector

    """

    def __init__(self):
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)

    @property
    def speed(self):
        return self.vel.length

    @speed.setter
    def speed(self, value):
        self.vel = self.vel.get_unit_vector() * value

    @property
    def accel(self):
        return self.acc.length

    @accel.setter
    def accel(self, value):
        self.acc = self.acc.get_unit_vector() * value

    def update(self, dt):
        self.dispatch_event('on_dx', self.vel.x * dt)
        self.dispatch_event('on_dy', self.vel.y * dt)
        self.vel += self.acc * dt

PhysicsComponent.register_event_type('on_dx')
PhysicsComponent.register_event_type('on_dy')


class SpriteComponent:

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


class InputComponent:

    def __init__(self):
        locator.window.push_handlers(self)

    def delete(self):
        locator.window.remove_handlers(self)


class AIComponent(EventDispatcher):

    """
    Abstract AI Component

    There's not much to put here...
    Most likely you'll have this handle and dispatch events.
    You'll have to implement that yourself.

    """

    pass


class DeathInterface(EventDispatcher):

    """
    Have components subclass this if it needs to kill its container
    """

    def die(self):
        self.dispatch_event('on_delete')
        self.dispatch_event('on_die')

DeathInterface.register_event_type('on_delete')
DeathInterface.register_event_type('on_die')
