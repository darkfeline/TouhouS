#!/usr/bin/env python3

from gensokyo import manager


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
        self.em = manager.EntityManager()
        self.sm = manager.SystemManager()
