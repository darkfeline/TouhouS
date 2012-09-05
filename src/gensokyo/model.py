#!/usr/bin/env python3

import abc

class SpriteAdder:

    def add_sprite(self, sprite, group):
        self.master.dispatch_event('on_add_sprite', sprite, group)

    def add_sprites(self, wrapper):
        for item in wrapper.sprites:
            self.add_sprite(*item)
        wrapper.sprites = set()


class AbstractModel(SpriteAdder):
    
    __metaclass__ = abc.ABCMeta

    @property
    def master(self):
        return self._master

    @master.setter
    def master(self, value):
        self._master = value
