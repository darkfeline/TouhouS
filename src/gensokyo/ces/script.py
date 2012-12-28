"""
Scripting module

Provides stuff for versatile scripting.

Scripts
*******

The basic data structure is a ``Script``.

Scripts have the ``run`` method.

``run`` is a method which is called on every tick.  It should return a Boolen;
if it is true, the Script is removed from the entity.

``run`` is passed the entitiy the component belongs to, the
environment which the system belongs to, and the time since the last tick.

ScriptSystem
************

ScriptSystem instances iterate over Script objects every tick.

"""

import abc

from gensokyo import ces


class Script(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def run(self, entity, env, dt):
        raise NotImplementedError


class ScriptSystem(ces.System):

    req_components = (Script,)

    def __init__(self, env):
        super().__init__(env)
        env.clock.push_handlers(self)

    def on_update(self, dt):
        for entity in self.env.em.get_with(self.req_components):
            for script in entity.get(self.req_components[0]):
                    r = script.run(entity, self.env, dt)
                    if r:
                        entity.delete(script)
