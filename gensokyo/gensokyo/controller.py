#!/usr/bin/env python3

from pyglet.window.key import KeyStateHandler

class Controller(KeyStateHandler):

    def __init__(self):
        super().__init__()
        self.master = None

    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)
        self.master.dispatch_event('on_key_press', symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        super().on_key_release(symbol, modifiers)
        self.master.dispatch_event('on_key_release', symbol, modifiers)
