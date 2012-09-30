#!/usr/bin/env python3
from pyglet.event import EventDispatcher
from pyglet.sprite import Sprite

from gensokyo.primitives import Rect, Circle
from gensokyo import locator

class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y


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

    def on_delete(self):
        self.delete()


class DeathInterface(EventDispatcher):

    """
    Have components subclass this if it needs to kill its container
    """

    def die(self):
        self.dispatch_event('on_delete')
        self.dispatch_event('on_die')

DeathInterface.register_event_type('on_delete')
DeathInterface.register_event_type('on_die')


class LifeComponent(DeathInterface):

    def __init__(self, life):
        self.life = life

    def on_hit(self, dmg):
        self.life -= dmg
        if self.life <= 0:
            self.die()
