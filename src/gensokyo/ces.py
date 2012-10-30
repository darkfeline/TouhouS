"""
This module contains the classes necessary for the Entity/Component/System
design pattern.

In a component/system design, components hold only data.  Systems operate on
entites which own components, and thus all logic are in systems.

"""

import abc


class Component:

    """
    Abstract Base Class for components

    Please subclass to avoid confusion

    """

    __metaclass__ = abc.ABCMeta


class ExclusiveComponent(Component):

    """
    ABC for exclusive components

    .. attribute: exclusive_key
        key used for exclusion

    """

    __metaclass__ = abc.ABCMeta


class Entity:

    """
    An entity represents a game object and contains components which
    encapsulate certain data.  It can have only one exclusive components with a
    given key, but otherwise can have any combination of components.

    Generally an entity will only have one component per superclass, e.g., with
    A > C, it will usually have either one A or one C or neither, although in
    certain cases having more of the same component may make sense.  However,
    it may be useful to make Interface superclasses.

    """

    def __init__(self):
        self.components = set()
        self.ex_keys = set()

    def __iter__(self):
        return iter(self.components)

    def add(self, component):
        if isinstance(component, ExclusiveComponent):
            if component.exclusive_key in self.ex_keys:
                raise TypeError(component.__class__ + " already exists in " +
                                self)
            else:
                self.ex_keys.add(component.exclusive_key)
        self.components.add(component)

    def delete(self, component):
        self.components.remove(component)
        if isinstance(component, ExclusiveComponent):
            self.ex_keys.remove(component.exclusive_key)
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
