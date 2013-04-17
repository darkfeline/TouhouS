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

from gensokyo import ces


class Script(ces.Component):

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

    def run(self, entity, world, root, dt):
        for script in self._subscripts:
            script.run(entity, world, root, dt)


class ScriptSystem(ces.System):

    def __init__(self, world, root):
        super().__init__(world)
        self.root = root

    def on_update(self, dt):
        s = self.world.cm[Script]
        for e in ces.intersect(self.world, Script):
            s[e].run(e, self.world, self.root, dt)
