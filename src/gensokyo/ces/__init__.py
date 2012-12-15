"""
This module contains the classes necessary for the Entity/Component/System
design pattern.

In a component/system design, components hold only data.  Systems operate on
entites which own components, and thus all logic are in systems.

The rationale is to properly separate functionality that may be shared in
different ways between different entities.  An entity/component pattern
addresses this problem.  However, different logic may need to access different
components and data, so keeping logic separate in Systems removes the need for
hard dependencies/events.

"""

import abc
from weakref import WeakValueDictionary
from weakref import WeakSet
import logging


###############################################################################
# Component, Entity, System
###############################################################################
class Component(metaclass=abc.ABCMeta):

    """
    Abstract Base Class for components

    Please subclass to avoid confusion

    """

    pass


class Entity:

    """
    An entity represents a game object and contains components which
    encapsulate certain data.

    An entity can have any combination of components.  Generally speaking, you
    will only have one of most components of in a given entity, but this not
    enforced in any way.  Feel free to::

        entity.get(Component)[0]

    or::

        for component in entity.get(Component)

    but you should use asserts in the former just in case.

    At times, "Interface" Component superclasses (e.g., Position) may be
    useful.

    """

    def __init__(self):
        self.components = set()

    def __iter__(self):
        return iter(self.components)

    def add(self, component):
        self.components.add(component)

    def delete(self, component):
        self.components.remove(component)
        try:
            component.delete()
        except AttributeError:
            pass

    def get(self, types):
        """
        If types is a single type, return a tuple of components who are an
        instance of type or a subclass of type.  If types is a list of types,
        return a tuple of all components of the given types with the following
        format::

            (
                (components where isinstance(component, types[0])),
                (components where isinstance(component, types[1])),
                .
                .
            )

        Some tuples may be empty if the entity does not have those components.

        When using the returned tuple, favor iterating over it with a `for`
        loop instead of doing `entity.get(type)[0]`.  An entity may have more
        than one of that component, in which case order is not guaranteed as
        components are stored interally in sets.

        :param types: component types to look for
        :type types: tuple or type
        :rtype: tuple

        """
        try:
            return tuple(tuple(component for component in self if
                         isinstance(component, type)) for type in types)
        except TypeError:
            return tuple(component for component in self if
                         isinstance(component, types))


class Position(Component, metaclass=abc.ABCMeta):

    """
    Overwrite ``pos`` property if needed.  ``pos`` should be the position, a
    tuple with the right dimensions.

    """

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value


class System(metaclass=abc.ABCMeta):

    """
    Superclass for Systems

    """

    def __init__(self, scene):
        self.scene = scene


###############################################################################
# Managers and Environment
###############################################################################
class EntityManager:

    def __init__(self):
        self.entities = set()

    def add(self, entity):
        logger.debug("Add entity %s", entity)
        self.entities.add(entity)

    def __iter__(self):
        return iter(self.entities)

    def delete(self, entity=None):
        if entity:
            self.entities.remove(entity)
            for a in entity.get(Component):
                entity.delete(a)
        else:
            for entity in list(self.entities):
                self.delete(entity)

    def get_with(self, types):
        """
        Find all entities who have at least one component of each type and
        return a set of entities

        :param types: component types to look for
        :type types: tuple
        :rtype: set

        """
        good = set()
        for entity in self.entities:
            components = entity.get(types)
            # Check if all slots in components are filled
            if len([a for a in components if len(a) == 0]) == 0:
                good.add(entity)
        return good


class GroupManager:

    def __init__(self):
        self.groups = {}

    def __getitem__(self, key):
        return self.groups[key]

    def make_group(self, key):
        if not key in self.groups.keys():
            self.groups[key] = WeakSet()

    def add_to(self, key, entity):
        self.groups[key].add(entity)


class TagManager:

    def __init__(self):
        self.items = WeakValueDictionary()

    def __getitem__(self, key):
        return self.items[key]

    def tag(self, key, entity):
        self.items[key] = entity


class SystemManager:

    def __init__(self):
        self.systems = set()

    def add(self, system):
        logger.debug("Add system %s", system)
        self.systems.add(system)

    def __iter__(self):
        return iter(self.systems)

    def delete(self):
        for a in self.systems:
            if hasattr(a, 'delete'):
                a.delete()


class Environment:

    def __init__(self):
        self.em = EntityManager()
        self.sm = SystemManager()
        self.gm = GroupManager()
        self.tm = TagManager()

    def delete(self):
        self.em.delete()
        self.sm.delete()
