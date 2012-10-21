#!/usr/bin/env python3

from pyglet import clock

from gensokyo import ces

from hakurei import component


class FPSSystem(ces.System):

    def __init__(self):
        self.count = 0

    def update(self, dt):
        self.count += dt
        if self.count > 1:
            entity = self.get_tag('fps_display')
            for l in entity.get(component.Label):
                l.label.text = "{0:.1f}".format(clock.get_fps()) + ' fps'
            self.count = 0


class DataSystem(ces.System):

    """
    Superclass for systems that need to access game data

    """

    fields = set('high_score', 'score', 'lives', 'bombs')

    def get(self, field):
        if field not in self.fields:
            raise TypeError
        entity = self.get_tag('data')
        for comp in entity.get(component.GameData):
            return getattr(comp, field)

    def set(self, field, value):
        if field not in self.fields:
            raise TypeError
        # set counter
        entity = self.get_tag('data')
        entity.set_value(value)
        # set data
        entity = self.get_tag(field)
        for comp in entity.get(component.GameData):
            setattr(comp, field, value)


class EnemyAISystem(ces.System):

    req_components = (component.EnemyAI,)

    def goto(self, entity, ai, step=0):

        """
        :param entity: entity passed to call
        :type entity: Entity
        :param ai: AI component passed to call
        :type entity: EnemyAI
        :param step: index in script to jump to
        :type step: int

        """

        ai.step = step

    def sleep(self, entity, ai, time):

        """
        :param entity: entity passed to call
        :type entity: Entity
        :param ai: AI component passed to call
        :type entity: EnemyAI
        :param time: time to sleep in seconds
        :type time: int

        """

        ai.sleep = time

    def call(self, entity, ai, method_name, *args, **kwargs):

        """
        Call method with given name and pass it the given entity

        Valid methods for such calling have the type signature::

            method_name(self, entity, ai, *args, **kwargs)

        `*args` and `**kwargs` are optional depending on method.

        :param entity: entity passed to call
        :type entity: Entity
        :param ai: AI component passed to call
        :type entity: EnemyAI
        :param method_name: name of method
        :type method_name: str

        """

        return getattr(self, method_name)(self, entity, ai, *args, **kwargs)

    # TODO implement this
    def move_to(self, entity, ai, dest):
        pass

    def update(self, dt):
        entities = self.get_with(self.req_components)
        for e in entities:
            for ai in e.get(component.EnemyAI):
                if ai.sleep > 0:
                    ai.sleep -= dt
                else:
                    if ai.step < len(ai.script):
                        self.call(e, ai, *ai.script[ai.step])
                        ai.step += 1
