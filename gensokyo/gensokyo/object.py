#!/usr/bin/env python3

from pyglet.sprite import Sprite
from pyglet.event import EventDispatcher

from gensokyo import primitives
from gensokyo import constants

class SpriteWrapper(EventDispatcher):

    def __init__(self):
        self.push_handlers(constants.VIEW)

    def add_sprite(self, sprite, group):
        self.dispatch_event('on_add_sprite', sprite, group)

SpriteWrapper.register_event_type('on_add_sprite')


class Object(SpriteWrapper):

    sprite_img = None
    sprite_group = ''

    def __init__(self, x, y, hb=None):
        super().__init__()
        cls = self.__class__
        self.rect = primitives.Rect(0, 0, cls.sprite_img.width,
                cls.sprite_img.height)
        self.hb = hb
        self.sprite = Sprite(cls.sprite_img)
        self.add_sprite(self.sprite, cls.sprite_group)
        self.x, self.y = x, y

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
        self.sprite.x = value

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
        self.sprite.y = value

    @property
    def left(self):
        return self.rect.left

    @left.setter
    def left(self, value):
        self.rect.left = value

    @property
    def right(self):
        return self.rect.right

    @right.setter
    def right(self, value):
        self.rect.right = value

    @property
    def top(self):
        return self.rect.top

    @top.setter
    def top(self, value):
        self.rect.top = value

    @property
    def bottom(self):
        return self.rect.bottom

    @bottom.setter
    def bottom(self, value):
        self.rect.bottom = value

    @property
    def center(self):
        return self.rect.center

    @center.setter
    def center(self, value):
        self.rect.center = value

    def delete(self):
        self.sprite.delete()

    def collide(self, other):
        if isinstance(other, Object):
            return self.hb.collide(other.hb)
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
        object.master = self

    def remove(self, object):
        self.objects.remove(object)
        object.master = None

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
