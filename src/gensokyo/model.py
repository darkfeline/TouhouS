#!/usr/bin/env python3

import abc

from pyglet.event import EVENT_HANDLED

class SpriteAdder:

    def add_sprite(self, sprite, group):
        self.master.dispatch_event('on_add_sprite', sprite, group)

    def add_sprites(self, wrapper):
        for item in wrapper.sprites:
            self.add_sprite(*item)
        wrapper.sprites = set()


class AbstractModel:
    
    __metaclass__ = abc.ABCMeta

    @property
    def master(self):
        return self._master

    @master.setter
    def master(self, value):
        self._master = value

    @abc.abstractmethod
    def on_key_press(self, symbol, modifiers):
        raise NotImplementedError

    @abc.abstractmethod
    def on_key_release(self, symbol, modifiers):
        raise NotImplementedError

    @abc.abstractmethod
    def on_update(self, dt):
        raise NotImplementedError

class Model(AbstractModel, SpriteAdder):

    def on_key_press(self, symbol, modifiers):
        return EVENT_HANDLED

    def on_key_release(self, symbol, modifiers):
        return EVENT_HANDLED

    def on_update(self, dt):
        return EVENT_HANDLED
