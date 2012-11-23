"""
Scripting module

Provides stuff for versatile scripting.

Units
*****

The basic data structure is a *scripting unit*.  Scripting units are tuples
containing ConditionUnits.

ConditionUnits have two main properties and one method.

``satisfied`` returns a Boolean.  ``run`` is a method which is called with the
owning entity as an argument if ``satisfied`` is ``True``.  If ``then`` returns
a scripting unit, it will be added to the Script's list of active units.
Otherwise, ``then`` should return ``None``.  If it returns a list of scripting
units, all of them will be added.  Newly added units will not be run until the
next loop.

If ``expire`` is ``True`` (False by default), the scripting unit will be
expired.  This is immediate; following ConditionUnits will not be processed.

Scripts and ScriptSystem
************************

Script instances have a list of currently active scripting units.

Entities can have multiple Scripts, but there is generally no need, except to
split responsibilities, possibly.

ScriptSystem instances iterate over Script objects and iterate over their
active scripting units every update loop.  Scripting units function like
datafied if/elses.

The conditions in each scripting unit are exclusive, evaluated in order.

"""

import abc

from gensokyo import ces
from gensokyo import locator


class ConditionComponent:

    __meta__ = abc.ABCMeta

    @abc.abstractproperty
    def satisfied(self):
        raise NotImplementedError

    @abc.abstractmethod
    def run(self, entity):
        raise NotImplementedError

    @property
    def expire(self):
        return False


class Script(ces.Component):

    """
    .. attribute:: units

    """

    def __init__(self, units):
        self.units = units


class ScriptSystem(ces.System):

    req_components = (Script,)

    def update(self, dt):
        for entity in locator.em.get_with(self.req_components):
            for script in entity.get(self.req_components[0]):
                for unit in list(script.units):
                    for cond in unit:
                        if hasattr(cond, "update"):
                            cond.update(dt)
                        if cond.satisfied:
                            r = cond.run(entity)
                            if r:
                                try:
                                    script.units.extend(r)
                                except TypeError:
                                    assert isinstance(r, tuple)
                                    script.units.append(r)
                            if cond.expire:
                                script.units.remove(unit)
                                break
