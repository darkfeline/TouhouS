#!/usr/bin/env python3

from pyglet.event import EventDispatcher

class Game:

    def __init__(self):
        self.stack = []

    @property
    def top(self):
        return self.stack[-1]

    def push(self, model):
        self.stack.append(model)

    def pop(self):
        return self.stack.pop()

    def update(self, dt):
        self.top.update(dt)


class Model(EventDispatcher):

    def update(self, dt):
        self.dispatch_event('on_update', dt)
