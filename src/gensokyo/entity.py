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
        Find all components of the given types and return a tuple with the
        following format::

            (
                (components where isinstance(component, types[0])),
                (components where isinstance(component, types[1])),
                .
                .
            )

        Some tuples may be empty if the entity does not have those components.

        """
        components = [[] for i in range(len(types))]
        for i, type in enumerate(types):
            for component in self:
                if isinstance(component, type):
                    components[i].append(component)
        return tuple(tuple(a) for a in components)
