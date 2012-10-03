#!/usr/bin/env python3

from pyglet import clock

from gensokyo.system import System
from gensokyo import component
from gensokyo import locator

from hakurei import game


class FPSSystem(System):

    def __init__(self):
        self.count = 0

    def update(self, dt):
        self.count += dt
        if self.count > 1:
            entity = locator.model.tm['fps_display']
            labels = entity.get((component.Label,))[0]
            for l in labels:
                l.label.text = "{0:.1f}".format(clock.get_fps()) + ' fps'
            self.count = 0


class DataSystem(System):

    """
    Superclass for systems that need to access game data

    """

    fields = set('high_score', 'score', 'lives', 'bombs')

    def get(self, field):
        if field not in self.fields:
            raise TypeError
        entity = locator.model.tm['data']
        for comp in entity.get(game.GameData):
            return getattr(comp, field)

    def set(self, field, value):
        if field not in self.fields:
            raise TypeError
        # set counter
        entity = locator.tm[field]
        entity.set_value(value)
        # set data
        entity = locator.model.tm['data']
        for comp in entity.get(game.GameData):
            setattr(comp, field, value)
