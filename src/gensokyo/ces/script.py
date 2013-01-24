"""
Scripting module

Provides stuff for generic scripting.

Scripts
*******

The basic data structure is a ``Script``.

Scripts have the ``run`` method.

``run`` is a method which is called on every tick.

``run`` is passed the entitiy the component belongs to, the
environment which the system belongs to, and the time since the last tick.

ScriptSystem
************

ScriptSystem instances iterate over Script objects every tick.

"""

import abc

from gensokyo import ces


class Script(ces.Component):

    @abc.abstractmethod
    def run(self, entity, world, dt):
        raise NotImplementedError


class ScriptSystem(ces.System):

    def __init__(self, world):
        super().__init__(world)

    def on_update(self, dt):
        for e in ces.intersect(self.world, Script):
            s = self.world.cm[Script]
            s[e].run(e, self.world, dt)
