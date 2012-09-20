#!/usr/bin/env python3

class Game:

    """
    Game stack.

    """

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


class Scene:

    """
    Abstract Scene

    """

    def __init__(self):
        self.objects = set()

    def on_remove(self, obj):
        self.objects.remove(obj)
