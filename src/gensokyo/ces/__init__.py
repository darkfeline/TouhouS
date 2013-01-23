"""
This package contains the classes necessary for the Entity/Component/System
design pattern.

In a component/system design, components hold only data.  Systems operate on
entites which own components, and thus all logic are in systems.

The rationale is to properly separate functionality that may be shared in
different ways between different entities.  An entity/component pattern
addresses this problem.  However, different logic may need to access different
components and data, so keeping logic separate in Systems removes the need for
hard dependencies/events.

:class:`System`
    Performs logic by iterating over Entities

:class:`Component`
    Holds data

:class:`World`
    Provides a CES world


"""

import abc
from weakref import WeakValueDictionary
import weakref
import logging
from collections import defaultdict

from gensokyo.clock import Clock

__all__ = ['Component', 'System', 'World', 'intersect']
logger = logging.getLogger(__name__)


class Component(metaclass=abc.ABCMeta):
    pass


class System(metaclass=abc.ABCMeta):

    """
    Superclass for Systems

    """

    def __init__(self, world):
        self.world = weakref.ref(world)
        world.add_system(self)


class World:

    def __init__(self):
        self.em = dict()
        self.cm = defaultdict(WeakValueDictionary)
        self.sm = set()
        self.clock = Clock()
        self._idgen = IdGen()

    def make_entity(self):
        e = self._idgen.next()
        self.em[e] = set()
        return e

    def add_component(self, entity, component):
        self.em[entity].add(component)
        self.cm[type(component)][entity] = component

    def remove_entity(self, entity):
        del self.em[entity]
        self._idgen.free(entity)

    def add_system(self, system):
        self.sm.add(system)


class IdGen:

    def __init__(self):
        self._next = 1
        self._free = []

    def next(self):
        if self._free:
            return self._free.pop(0)
        else:
            a = self._next
            self._next += 1
            return a

    def free(self, value):
        self._free.append(value)


def intersect(world, *args):
    entities = set(x for x in world.cm[args.pop()])
    while args:
        entities &= set(x for x in world.cm[args.pop()])
    return entities
