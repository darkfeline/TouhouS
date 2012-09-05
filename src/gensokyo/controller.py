#!/usr/bin/env python3

import abc

from pyglet.window.key import KeyStateHandler

class AbstractController:

    __metaclass__ = abc.ABCMeta

    @property
    def master(self):
        return self._master

    @master.setter
    def master(self, value):
        self._master = value

    @abc.abstractmethod
    def __getitem__(self, key):
        raise NotImplementedError


class Controller(KeyStateHandler, AbstractController):

    def __init__(self):
        super().__init__()
        self.master = None

    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)
        self.master.dispatch_event('on_key_press', symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        super().on_key_release(symbol, modifiers)
        self.master.dispatch_event('on_key_release', symbol, modifiers)
