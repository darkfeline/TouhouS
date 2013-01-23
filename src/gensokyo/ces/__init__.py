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

:class:`Entity`
    Contains Components

:class:`Component`
    Holds data

:class:`Environment`
    Provides a CES environment


"""

import abc
from weakref import WeakKeyDictionary
import logging
from collections import defaultdict

from gensokyo.clock import Clock

logger = logging.getLogger(__name__)


class Component(metaclass=abc.ABCMeta):
    pass


class Entity:
    pass


class System(metaclass=abc.ABCMeta):

    """
    Superclass for Systems

    """

    def __init__(self, env):
        self.env = env
        env.add_system(self)


class Environment:

    def __init__(self):
        self.em = dict()
        self.cm = defaultdict(WeakKeyDictionary)
        self.sm = set()
        self.clock = Clock()

    def make_entity(self):
        e = Entity()
        self.em[e] = set()
        return e

    def add_component(self, entity, component):
        self.em[entity].add(component)
        self.cm[type(component)][entity] = component

    def remove_entity(self, entity):
        del self.em[entity]

    def add_system(self, system):
        self.sm.add(system)


def intersect(env, *args):
    entities = set(x for x in env.cm[args.pop()])
    while args:
        entities &= set(x for x in env.cm[args.pop()])
    return entities
