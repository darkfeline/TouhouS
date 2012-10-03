#!/usr/bin/env python3


class Entity:

    """
    An entity represents a game object and contains components which
    encapsulate certain data.  An entity should only have one component per
    superclass, e.g., it should have either an A component or an
    ASubclass component, not both.  However, it may be useful to make Interface
    superclasses.

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

        """
        try:
            return tuple([tuple([
                component for component in self if isinstance(component, type)
                ]) for type in types])
        except TypeError:
            return tuple([
                component for component in self if isinstance(component, types)
                ])
