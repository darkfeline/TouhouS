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

        self.dispatch_event('on_attach')

    def pop(self):

        scene = self.stack.pop()

        self.remove_handlers(scene.model)
        self.remove_handlers(scene.view)

        self.window.remove_handlers(scene.controller)
        self.window.remove_handlers(scene.view)

        return scene

    def on_push_scene(self, scene):
        self.push(scene)

    def on_pop_scene(self):
        self.pop()

    def update(self, dt):
        self.dispatch_event('on_update', dt)

SceneStack.register_event_type('on_update')
SceneStack.register_event_type('on_key_press')
SceneStack.register_event_type('on_key_release')
SceneStack.register_event_type('on_add_sprite')
SceneStack.register_event_type('on_push_scene')
SceneStack.register_event_type('on_pop_scene')
SceneStack.register_event_type('on_attach')


class Scene:

    def __init__(self, controller, model, view):
        self.controller = controller
        self.model = model
        self.view = view
