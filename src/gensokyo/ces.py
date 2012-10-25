"""
This module contains the classes necessary for the Entity/Component/System
design pattern.

In a component/system design, components hold only data.  Systems operate on
entites which own components, and thus all logic are in systems.

"""

import abc

from gensokyo import locator


class Component:

    """
    Abstract Base Class for components

    Please subclass to avoid confusion

    """

    __metaclass__ = abc.ABCMeta


class Entity:

    """
    An entity represents a game object and contains components which
    encapsulate certain data.  It can have any combination of components.
    Generally an entity will only have one component per superclass, e.g., with
    A > C, it will usually have either one A or one C or neither, although in
    certain cases having more of the same component may make sense.  However,
    it may be useful to make Interface superclasses.

    """

    def __init__(self):
        self.components = set()

    def __iter__(self):
        return iter(self.components)

    def add(self, component):
        self.components.add(component)

    def delete(self, component):
        self.components.remove(component)
        if hasattr(component, 'delete'):
            component.delete()

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


class System:

    """
    Superclass for Systems

    """

    __metaclass__ = abc.ABCMeta

    @staticmethod
    def get_with(types):
        """
        :param types: component types to look for
        :type types: tuple
        :rtype: set

        """
        return locator.em.get_with(types)

    @staticmethod
    def get_tag(tag):
        """
        :param tag: tag to look for
        :type tag: str
        :rtype: Entity

        """
        return locator.tm[tag]

    @staticmethod
    def dispatch_event(event, *args):
        """
        :param event: event
        :type event: str

        """
        locator.sm.dispatch_event(event, *args)
