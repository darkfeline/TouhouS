"""
Scripting module

Provides stuff for generic scripting.

Scripts
*******

The basic data structure is a ``Script``.

Scripts have the ``run`` method, which is called on every tick.

``run`` is passed the entitiy the component belongs to, the
world which the system belongs to, and the time since the last tick.

ScriptSystem
************

ScriptSystem instances iterate over Script objects every tick.

"""

import abc

from gensokyo import ces


class Script(ces.Component, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def run(self, entity, world, dt):
        raise NotImplementedError


class ScriptSystem(ces.System):

    def on_update(self, dt):
        for e in ces.intersect(self.world, Script):
            s = self.world.cm[Script]
            s[e].run(e, self.world, dt)
