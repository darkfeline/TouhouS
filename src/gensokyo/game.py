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
        """Calls update on top of stack"""
        self.top.update(dt)


class Scene:

    """
    Abstract Scene

    """

    def __init__(self):
        self.objects = set()

    def add(self, obj):
        self.objects.add(obj)

    def on_remove(self, obj):
        self.objects.remove(obj)

    def update(self, dt):
        """Calls update on all objects with update attribute"""
        for obj in self.objects:
            if hasattr(obj, 'update'):
                obj.update(dt)
