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

You do not need to explicitly add a System to a SystemManager; its ``__init__``
takes its environment as a parameter and will add itself.  Make sure to call
``super().__init__()``.

:class:`System`
    Performs logic by iterating over Entities

:class:`Entity`
    Contains Components

:class:`Component`
    Holds data

:class:`Environment`
    Provides a CES environment, i.e. the four managers

:class:`EntityManager`
    Holds references to Entities

:class:`GroupManager`
    Holds references to groups of Entities

:class:`TagManager`
    Holds references to specific Entities

:class:`SystemManager`
    Holds references to Systems


"""

import abc
from weakref import WeakValueDictionary
from weakref import WeakSet
import logging

from gensokyo.clock import Clock

logger = logging.getLogger(__name__)


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
        :type types: iterable or type
        :rtype: tuple

        """
        try:
            return tuple(tuple(component for component in self if
                         isinstance(component, type)) for type in types)
        except TypeError:
            return tuple(component for component in self if
                         isinstance(component, types))


class System(metaclass=abc.ABCMeta):

    """
    Superclass for Systems

    """

    def __init__(self, env):
        self.env = env
        env.sm.add(self)


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

    def remove(self, entity):
        self.entities.remove(entity)

    def get_with(self, types):
        """
        Find all entities who have at least one component of each type and
        return a set of entities

        :param types: component types to look for
        :type types: iterable
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


class Environment:

    def __init__(self):
        self.em = EntityManager()
        self.sm = SystemManager()
        self.gm = GroupManager()
        self.tm = TagManager()
        self.clock = Clock()


###############################################################################
# Others
###############################################################################
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
