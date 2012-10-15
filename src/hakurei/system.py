#!/usr/bin/env python3

from pyglet import clock

from gensokyo import system
from gensokyo import component
from gensokyo import locator

from hakurei import game
from hakurei.globals import GAME_AREA


class FPSSystem(system.System):

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


class DataSystem(system.System):

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


class GameCollisionSystem(system.CollisionSystem):

    @staticmethod
    def check_types(entities, types):
        """Return True if one entity is one type, and the other is the other"""
        e1, e2 = entities
        t1, t2 = types
        if isinstance(e1, t1) and isinstance(e2, t2) or \
                isinstance(e1, t2) and isinstance(e2, t1):
            return True
        else:
            return False

    def on_collide(self, entities):
        e1, e2 = entities
        # TODO player + enemy bullet
        # TODO enemy + player bullet


class GarbageCollectSystem(system.System):

    req_components = (game.Presence,)

    @staticmethod
    def check_bounds(entity):
        """Return True if entity is outside bounds"""
        c = entity.get(game.Presence)
        if len(c) < 1:
            raise NotImplementedError
        r = c[0].hb
        if (r.bottom > GAME_AREA.top or r.top < GAME_AREA.bottom or
                r.left > GAME_AREA.right or r.right < GAME_AREA.left):
            return True
        else:
            return False

    def update(self, dt):
        entities = locator.em.get_with(self.req_components)
        for e1 in enumerate(entities):
            if self.check_bounds(e1):
                locator.em.delete(e1)
