#!/usr/bin/env python3


class SceneStack:

    def __init__(self):
        self.stack = []

    @property
    def top(self):
        return self.stack[-1]

    @property
    def view(self):
        return self.top.view

    @property
    def model(self):
        return self.top.model

    def push(self, scene):
        self.stack.append(scene)

    def pop(self):
        return self.stack.pop()

    def update(self, dt):
        """Calls update on top of stack"""
        self.top.update(dt)

    def on_draw(self):
        self.top.view.draw()


class Scene:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update(self, dt):
        self.model.update(dt)
