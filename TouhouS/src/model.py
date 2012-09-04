#!/usr/bin/env python3

from pyglet.text import Label
from gensokyo import model
from gensokyo.scene import Scene
from gensokyo.view import View

from reimu import Reimu
from stage import Stage
from ui import UI

class Model(model.Model):

    ui_class = UI
    player_class = Reimu
    stage_class = Stage


class Menu(model.AbstractModel, model.SpriteAdder):

    def __init__(self):
        self.title = Label(x=150, y=150, text="Press any key to start...",
                color=(255, 255, 255, 255))
        self.sprites = set((self.title,))

    def on_update(self, dt):
        if self.sprites:
            self.add_sprite(self.title, 'text')
            self.sprites = set()

    def on_key_press(self, symbol, modifiers):
        scene = Scene(self.master.controller, Model(), View())
        self.master.dispatch_event('on_push_scene', scene)
        self.sprites = set((self.title,))
