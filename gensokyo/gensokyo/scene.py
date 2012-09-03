#!/usr/bin/env python3

from gensokyo import globals

class SceneStack:

    def __init__(self):
        self.stack = []

    def push(self, scene):
        self.stack.append(scene)
        self.set()

    def pop(self):
        x = self.stack.pop()
        self.set()
        return x

    def set(self):
        self.stack[-1].set()


class Scene:

    def __init__(self, keys, model, view):
        self.keys = keys
        self.model = model
        self.view = view
        model.register_view(view)

    def set(self):
        globals.KEYS = self.keys
