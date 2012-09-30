#!/usr/bin/env python3


class SceneStack:

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

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update(self, dt):
        self.model.update(dt)
        self.view.update(dt)
