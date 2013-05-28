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

from gensokyo import ecs


class Script(ecs.Component):

    """
    Script itself can have sub-Scripts added and removed.  Script.run() then
    delegates its calls.  You can subclass Script and implement run() to do
    whatever.  Remember to call super().run() if you want to delegate further.
    """

    def __init__(self):
        self._subscripts = []

    def add(self, script):
        self._subscripts.append(script)

    def remove(self, script):
        self._subscripts.remove(script)

    def run(self, entity, world, rootenv, dt):
        for script in self._subscripts:
            script.run(entity, world, rootenv, dt)


class ScriptSystem(ecs.System):

    def __init__(self, world, rootenv):
        super().__init__(world)
        self.rootenv = rootenv

    def on_update(self, dt):
        s = self.world.cm[Script]
        for e in ecs.intersect(self.world, Script):
            s[e].run(e, self.world, self.rootenv, dt)
