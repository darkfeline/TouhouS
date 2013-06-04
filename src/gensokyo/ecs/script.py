"""
Scripting module

Provides stuff for generic scripting.

Scripts and Scriplets
---------------------

Script components are added to entities and Scriptlets are added to the Script.
Scriptlets can implement arbitrary run() methods, which are called every tick.

ScriptSystem
------------

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

    def run(self, entity, world, master, dt):
        for script in self._subscripts:
            script.run(entity, world, master, dt)


class Scriptlet(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def run(self, entity, world, master, dt):
        raise NotImplementedError


class ScriptSystem(ecs.System):

    def __init__(self, world, master):
        """
        `world` is an ECS World, self-explanatory.  `master` is the master
        object, which owns the `world` and generally is running the show.  In
        this case, it'd probably be a State (like GameScene).
        """
        super().__init__(world)
        self.master = master

    def on_update(self, dt):
        s = self.world.cm[Script]
        for e in ecs.intersect(self.world, Script):
            s[e].run(e, self.world, self.master, dt)
