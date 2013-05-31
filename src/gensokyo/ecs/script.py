"""
Scripting module

Provides stuff for generic scripting.

Scripts
*******

The basic data structure is a ``Script``.

Scripts have the ``run`` method, which is called on every tick.  See code for
signature.

ScriptSystem
************

ScriptSystem instances iterate over Script objects every tick.
"""

import abc

from gensokyo import ecs


class Script(ecs.Component):

    """
    Due to how ECS is implemented, you need to add a Script to an Entity and
    then add Scriptlets to it.  Allows Entities to run arbitrary code.
    """

    def __init__(self):
        self._subscripts = []

    def add(self, script):
        assert isinstance(script, Scriptlet)
        self._subscripts.append(script)

    def remove(self, script):
        self._subscripts.remove(script)

    def run(self, entity, world, rootenv, dt):
        for script in self._subscripts:
            script.run(entity, world, rootenv, dt)


class Scriptlet(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def run(self, entity, world, rootenv, dt):
        raise NotImplementedError


class ScriptSystem(ecs.System):

    def __init__(self, world, rootenv):
        super().__init__(world)
        self.rootenv = rootenv

    def on_update(self, dt):
        s = self.world.cm[Script]
        for e in ecs.intersect(self.world, Script):
            s[e].run(e, self.world, self.rootenv, dt)
