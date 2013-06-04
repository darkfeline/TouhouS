"""
ecs package
===========

This package contains the classes necessary for the Entity/Component/System
design pattern.

In a component/system design, components hold only data.  Systems operate on
entites which own components, and thus all logic are in systems.

The rationale is to properly separate functionality that may be shared in
different ways between different entities.  An entity/component pattern
addresses this problem.  However, different logic may need to access different
components and data, so keeping logic separate in Systems removes the need for
hard dependencies/events.

Entity
------

An empy class that is instantiated and used as a key for interacting with
stuff.  Conceptually, an entity is an object that has components that have
data, but in implementation is just a key to reference component instances.

System
------

Performs logic by iterating over Entities.  Usually has an on_update() method
which gets registered with Clocks, but can also trigger on other events.
Systems are added into a list in a World for simple bookkeeping.

A typical on_update() loop looks like::

    def on_update(self, dt):
        entities = intersect(self.world, ComponentA, ComponentB)
        a, b = self.world.cm[ComponentA], self.world.cm[ComponentB]
        for e in entities:
            component_a = a[e]
            component_b = b[e]
            # do stuff

Component
---------

Holds data.  Avoid temptation of cramming logic into them.  Each Entity can
only hold one Component per Component class, but you can implement
subcomponents into your Component/System if you wish.

World
-----

Provides a ECS world.  Keeps track of entities, systems, and components.
"""

import abc
import weakref
from weakref import WeakKeyDictionary, WeakValueDictionary, WeakSet
import logging
from collections import defaultdict

__all__ = ['Component', 'System', 'World', 'intersect']
logger = logging.getLogger(__name__)


class Component(metaclass=abc.ABCMeta):
    pass


class System(metaclass=abc.ABCMeta):

    """
    Superclass for Systems

    Provides a useful default __init__() that you should probably call
    with super().
    """

    def __init__(self, world):
        """Create a weak reference to `world` and add self to `world"""
        self.get_world = weakref.ref(world)
        world.add_system(self)

    @property
    def world(self):
        return self.get_world()


class World:

    """
    You can use ``tm`` and ``gm`` directly, but use World's exposed methods for
    making/removing entities, components and systems>

    Attributes:

    em
        ``em[entity] = set([component])``
    tm
        Tag manager. Use ``tm['tag'] = entity``
    cm
        Component manager.  ``cm[class][entity] = component``
    gm
        Group manager.  ``gm['group'].add(entity)``
    """

    def __init__(self):
        self.em = dict()
        self.cm = defaultdict(WeakKeyDictionary)
        self.tm = WeakValueDictionary()
        self.gm = defaultdict(WeakSet)
        self.sm = set()

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


class Entity:
    pass


def intersect(world, *args):
    """Return all entities with given components."""
    assert len(args) > 0
    assert isinstance(world, World)
    args = iter(args)
    entities = set(x for x in world.cm[next(args)])
    for a in args:
        entities &= set(x for x in world.cm[a])
    return entities
