#!/usr/bin/env python3

from pyglet.event import EventDispatcher

class SceneStack(EventDispatcher):

    def __init__(self, window):
        self.window = window
        self.stack = []

    @property
    def model(self):
        return self.stack[-1].model

    @property
    def view(self):
        return self.stack[-1].view

    @property
    def controller(self):
        return self.stack[-1].controller

    def push(self, scene):

        self.stack.append(scene)

        scene.controller.master = self
        scene.model.master = self
        scene.view.master = self

        self.push_handlers(scene.model)
        self.push_handlers(scene.view)

        self.window.push_handlers(scene.controller)
        self.window.push_handlers(scene.view)

    def pop(self):

        scene = self.stack.pop()

        self.pop_handlers()
        self.pop_handlers()

        self.window.pop_handlers()
        self.window.pop_handlers()

        return scene

    def update(self, dt):
        self.dispatch_event('on_update', dt)

SceneStack.register_event_type('on_update')
SceneStack.register_event_type('on_key_press')
SceneStack.register_event_type('on_key_release')
SceneStack.register_event_type('on_add_sprite')


class Scene:

    def __init__(self, controller, model, view):
        self.controller = controller
        self.model = model
        self.view = view
