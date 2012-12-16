"""
Scripting module

Provides stuff for versatile scripting.

Units
*****

The basic data structure is a ``ScriptingUnit``.

ScriptingUnit has the ``run`` method.

``run`` is a method which is called on every tick.  It returns a ``Result``
``namedtuple`` with two fields.  If the ``expire`` field is true, the
``ScriptingUnit`` will be removed from the ``Script``.  If ``new`` is a
``ScriptingUnit``, it will be added to the ``Script``.

``run`` is passed the entitiy the component belongs to, the
environment which the system belongs to, and the time since the last tick.

Scripts and ScriptSystem
************************

Script instances have a list of currently active ``ScriptingUnit``s.

Entities can have multiple Scripts!  Functionally there is no need, but it is
damn useful.  Use it where it makes sense.

ScriptSystem instances iterate over Script objects and iterate over their
active ``ScriptingUnit``s every tick.  ``ScriptingUnit``s function like
datafied if/elses.

"""

import abc
from collections import namedtuple

from gensokyo import ces

Result = namedtuple('Result', ['expire', 'new'])

class ScriptingUnit(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def run(self, entity, env, dt):
        raise NotImplementedError


class Script(ces.Component):

    """
    .. attribute:: units

    """

    def __init__(self, units):
        """
        :param units: scripting units
        :type units: list

        """
        self.units = units


class ScriptSystem(ces.System):

    req_components = (Script,)

    def __init__(self, env):
        super().__init__(env)
        env.clock.push_handlers(self)

    def on_update(self, dt):
        for entity in self.env.em.get_with(self.req_components):
            for script in entity.get(self.req_components[0]):
                for unit in list(script.units):
                    r = unit.run(entity, self.env, dt)
                    assert isinstance(r, Result)
                    if r.new:
                        script.units.append(r.new)
                    if r.expire:
                        script.units.remove(unit)
